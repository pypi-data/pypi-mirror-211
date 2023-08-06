import re
from io import BytesIO
from urllib.parse import urlparse

import botocore
import boto3

from airflow.models import Variable, BaseOperator
from airflow.exceptions import AirflowException
from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.amazon.aws.operators.ecs import EcsRunTaskOperator
from airflow.providers.amazon.aws.operators.glue import GlueJobOperator
from airflow.providers.amazon.aws.operators.athena import AthenaOperator

from rcplus_alloy_common.airflow.decorators import alloyize


@alloyize
class AlloyBashOperator(BashOperator):
    """Alloy BashOperator"""


@alloyize
class AlloyPythonOperator(PythonOperator):
    """Alloy PythonOperator"""


@alloyize
class AlloyGlueJobOperator(GlueJobOperator):
    """Alloy GlueJobOperator class with dag_run_id injected."""
    dest_s3_path = None

    def prepare_log4j2(self, dag_id, dag_run_id):
        # retrieve the log4j2.properties S3 url and extract the bucket name and object key
        boto3_session = boto3.Session()
        ssm = boto3_session.client("ssm")
        conf_s3_path = ssm.get_parameter(Name="/alloy/airflow/glue/logzio_appender_conf_s3_path")["Parameter"]["Value"]
        parsed_s3_url = urlparse(conf_s3_path, allow_fragments=False)
        s3_bucket_name = parsed_s3_url.netloc
        s3_key_src = parsed_s3_url.path.lstrip("/")
        #
        # read the log4j2.properties file from S3 as a template
        s3 = boto3_session.client("s3")
        templ = BytesIO()
        s3.download_fileobj(s3_bucket_name, s3_key_src, templ)
        #
        # inject the extra attributes into the template and upload the result back to S3
        extra_attrs = (
            f"env={self.project.get('env', 'dev')};"
            f"version={self.project.get('project_version', 'undefined')};"
            f"repository={self.project.get('git_repo_name', 'undefined')};"
            f"software_component={self.project.get('software_component', 'undefined')};"
            f"dag_id={dag_id or 'undefined'};"
            f"dag_run_id={dag_run_id or 'undefined'};"
            f"task_id={self.task_id or 'undefined'}"
        )
        conf_str_desc = re.sub(
            r"^appender\.logzio\.additionalFields\s*=\s*.*$",
            f"appender.logzio.additionalFields = {extra_attrs}",
            templ.getvalue().decode("utf-8"),
            flags=re.MULTILINE,
        )
        s3_key_dest = f"config/{dag_id}/{dag_run_id}/log4j2.properties"
        self.dest_s3_path = f"s3://{s3_bucket_name}/{s3_key_dest}"
        s3.upload_fileobj(BytesIO(conf_str_desc.encode("utf-8")), s3_bucket_name, s3_key_dest)

    def execute(self, context):
        # NOTE-zw: here we instruct the GlueJobOperator to use log4j2.properties from S3. This is a hack because there
        #         is no other way to pass the context attributes to log4j before it got initialized. The workaround we
        #         apply here is based on a BIG assumption: for each Glue Job run task there is a new Spark node
        #         initialized. This assumption is true for the current implementation of the GlueJobOperator as of
        #         2021-05-03 (Airflow 2.6.1).
        dag_id = context["dag"].dag_id
        dag_run_id = context["dag_run"].run_id
        self.prepare_log4j2(dag_id, dag_run_id)
        if self.script_args is None:
            self.script_args = {}

        self.script_args["--extra-files"] = (
            f"{self.script_args['--extra-files']},{self.dest_s3_path}"
            if "--extra-files" in self.script_args and len(self.script_args["--extra-files"]) > 0
            else self.dest_s3_path
        )

        return super().execute(context)


@alloyize
class AlloyEcsRunTaskOperator(EcsRunTaskOperator):
    """Alloy ECSRunTaskOperator"""

    def __init__(self, *args, cluster: str = "", overrides: dict | None = None, **kwargs):
        if overrides is None:
            overrides = {}
        super().__init__(*args, cluster=cluster, overrides=overrides, **kwargs)

    def set_cluster(self):
        if not self.cluster:
            self.cluster = Variable.get("global_SHARED_ECS_CLUSTER")

    def network_configuration_factory(self):
        self.network_configuration = {
            "awsvpcConfiguration": {
                "subnets": Variable.get("global_VPC_PRIVATE_SUBNETS").split(","),
                "securityGroups": [Variable.get("global_VPC_DEFAULT_SECURITY_GROUP")],
                "assignPublicIp": "DISABLED",
            },
        }

    def overrides_factory(self, dag_id, dag_run_id):
        # NOTE-zw:
        # We have to be very careful to handle the edge cases here, because:
        #   1. as an Alloy common practice, one ECS task normally contains two containers, one for the
        #      actual task and a sidecar for logging;
        #   2. `containerOverrides` might not exist
        #   3. the logger sidecar normally has no override in the definition (but it could have)
        #   4. `environment` might not exist
        if "containerOverrides" not in self.overrides:
            self.overrides["containerOverrides"] = []
        primary_container = None
        logging_sidecar = None
        for c in self.overrides["containerOverrides"]:
            # NOTE: the convention is that the primary container is named after the task definition
            if c["name"] == self.task_definition:
                # NOTE-zw: so far we do not have a reason to inject the logging context into the primary app container!
                primary_container = c
            elif c["name"] == "logzio-logs-router":
                # NOTE-zw: we need to inject the logging context into the logger sidecar because this is where the
                # fluent-bit runs.
                logging_sidecar = c
        if primary_container is None:
            if len(self.overrides["containerOverrides"]) > int(logging_sidecar is not None):
                additional_container_names = [
                    c["name"]
                    for c in self.overrides["containerOverrides"]
                    if c["name"] not in ["logzio-logs-router", self.task_definition]
                ]
                self.log.warning(
                    "containerOverrides contains containers other than "
                    f"['logzio-logs-router', '{self.task_definition}']: {additional_container_names}"
                )
            primary_container = {
                "name": self.task_definition,
                "environment": [],
            }
            self.overrides["containerOverrides"].append(primary_container)
        if logging_sidecar is None:
            if len(self.overrides["containerOverrides"]) > 1:
                additional_container_names = [
                    c["name"]
                    for c in self.overrides["containerOverrides"]
                    if c["name"] not in ["logzio-logs-router", self.task_definition]
                ]
                self.log.warning(
                    "containerOverrides contains containers other than "
                    f"['logzio-logs-router', '{self.task_definition}']: {additional_container_names}"
                )
            logging_sidecar = {
                "name": "logzio-logs-router",
                "environment": [],
            }
            self.overrides["containerOverrides"].append(logging_sidecar)
        if "environment" not in logging_sidecar:
            logging_sidecar["environment"] = []
        logging_sidecar["environment"].extend(
            [
                {"name": "DAG_RUN_ID", "value": dag_run_id},
                {"name": "DAG_ID", "value": dag_id},
                {"name": "TASK_ID", "value": self.task_id or "undefined"},
            ]
        )

    def execute(self, context, session=None):
        """
        Inject environment variables DAG_TASK_ID, DAG_RUN_ID, DAG_ID as logging context into both containers
        of the ECS task.
        The logging context helps to filter and locate log messages irrelevant from the original producer.
        """
        self.set_cluster()
        self.network_configuration_factory()
        self.overrides_factory(context["dag"].dag_id or "undefined", context["dag_run"].run_id or "undefined")

        return super().execute(context, session)


class S3ReleaseLockOperator(BaseOperator):
    """
    Custom class to handle S3-based locks release. The lock can be release only if a DAG "owns" the lock.
    The ownership is detected by lock's file content (lock_id).
    """

    def __init__(
        self,
        *,
        bucket: str,
        lock_key: str,
        lock_id: str,
        aws_conn_id: str = "aws_default",
        **kwargs,
    ):
        if any([bucket is None, lock_key is None, lock_id is None]):
            raise AirflowException("Bucket, lock_key and lock_id should not be None")

        super().__init__(**kwargs)
        self.bucket = bucket
        self.lock_key = lock_key
        self.lock_id = lock_id
        self.aws_conn_id = aws_conn_id

    def execute(self, context):
        s3_hook = S3Hook(aws_conn_id=self.aws_conn_id)
        try:
            lock_id = s3_hook.read_key(self.lock_key, self.bucket)
        except botocore.exceptions.ClientError as e:
            if e.response["Error"]["Code"] == "404":
                self.log.info(f"The lock `{self.lock_key}` does not exist")
                return
            raise e
        if lock_id == self.lock_id:
            self.log.info(f"Release the lock `{self.lock_key}`")
            s3_hook.delete_objects(bucket=self.bucket, keys=self.lock_key)
            return

        self.log.warning(
            f"The lock `{self.lock_key}` not released because its lock id is `{lock_id}` but expected `{self.lock_id}`"
        )


@alloyize
class AlloyS3ReleaseLockOperator(S3ReleaseLockOperator):
    """Alloy S3ReleaseLockOperator"""


@alloyize
class AlloyAthenaOperator(AthenaOperator):
    """Alloy AthenaOperator"""
    template_fields = tuple(AthenaOperator.template_fields) + ("workgroup", )
