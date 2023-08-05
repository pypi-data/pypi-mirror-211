import os
import sys

import yaml

from rcplus_alloy_common.airflow.observability import slack_alert_on_retry, slack_alert_on_failure


def load_project_config(depth=1):
    """Load Alloy project configuration.

    The convention is to put the project.yml in the same directory as the dag script.
    """
    back = sys._getframe(depth)  # pylint: disable=protected-access
    fileloc = back.f_code.co_filename if back else ""
    config_filepath = os.path.join(os.path.dirname(fileloc), "project.yml")

    with open(config_filepath) as f:
        project = yaml.safe_load(f)
    return project


def set_default_callbacks(default_args):
    """Set default callbacks for tasks

    TODO: does the order matters?
    """
    if "on_retry_callback" not in default_args:
        default_args["on_retry_callback"] = slack_alert_on_retry
    elif isinstance(default_args["on_retry_callback"], list):
        default_args["on_retry_callback"] = (
            [x for x in default_args["on_retry_callback"] if x is not slack_alert_on_retry]
        )
        default_args["on_retry_callback"] = default_args["on_retry_callback"] + [slack_alert_on_retry]
    else:
        if default_args["on_retry_callback"] is not slack_alert_on_retry:
            default_args["on_retry_callback"] = [default_args["on_retry_callback"], slack_alert_on_retry]

    if "on_failure_callback" not in default_args:
        default_args["on_failure_callback"] = slack_alert_on_failure
    elif isinstance(default_args["on_failure_callback"], list):
        default_args["on_failure_callback"] = (
            [x for x in default_args["on_failure_callback"] if x is not slack_alert_on_failure]
        )
        default_args["on_failure_callback"] = default_args["on_failure_callback"] + [slack_alert_on_failure]
    else:
        if default_args["on_failure_callback"] is not slack_alert_on_failure:
            default_args["on_failure_callback"] = [default_args["on_failure_callback"], slack_alert_on_failure]
    return default_args
