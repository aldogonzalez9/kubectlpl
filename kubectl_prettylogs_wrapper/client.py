import subprocess
import json


from kubectl_prettylogs_wrapper.helpers import pretty_stacktrace, color_text, load_json_from_raw_log
from kubectl_prettylogs_wrapper.constants import (
    LOG_LEVELS,
    LOG_LEVEL_ERROR,
    LOG_LEVEL_INFO,
    LOG_LEVEL_INFO_KEY,
    DEFAULT_SINCE_TIME,
    STACK_TRACE_MARKER,
    STACK_TRACE_KEY
)


class KubectlPrettyLogsWrapperClient:
    def __init__(
        self,
        pod: str,
        name_space: str,
        container: str,
        since: str = DEFAULT_SINCE_TIME,
        selected_logging_level: str = LOG_LEVEL_INFO_KEY
    ):
        self.pod = pod
        self.name_space = name_space
        self.since = since
        self.selected_logging_level = selected_logging_level
        self.container = container

    def _kubectl_command_args_builder(self) -> str:
        """
        :return: string representation of kubectl command args
        """
        name_space_arg = f"-n {self.name_space}" if self.name_space else None
        since_arg = f"--since={self.since}" if self.since else None
        container = f"-c {self.container}" if self.container else None
        command_args = " ".join([cmd_arg for cmd_arg in [name_space_arg, since_arg, self.pod, container] if cmd_arg])
        return command_args

    @staticmethod
    def _kubectl_command_runner(command_args: str):
        try:
            kubectl_command = f"kubectl logs {command_args}"
            print(f"Kubectl command to run: {kubectl_command}")
            output = subprocess.check_output(kubectl_command, shell=True)
            return output.decode("utf-8").split("\n")
        except Exception as ex:
            print(ex)

    def get_pod_logs(self):
        command_logging_level_value = LOG_LEVELS.get(self.selected_logging_level)
        command_output = self._kubectl_command_runner(self._kubectl_command_args_builder())
        if not command_output:
            print("Unable to find logs")
            return
        for raw_log in command_output:
            try:
                # todo: regex
                if raw_log.startswith("{") and raw_log.endswith("}"):
                    parsed_log = load_json_from_raw_log(raw_log)
                    # We will assign INFO logging level if not log level field is found
                    parsed_log_logging_level = parsed_log.get("logLevel") or parsed_log.get("level", LOG_LEVEL_INFO_KEY)
                    parsed_log_logging_level_value = LOG_LEVELS.get(parsed_log_logging_level)
                    # Check if logging level of current log is same or below of requested logging value in command
                    if parsed_log_logging_level_value <= command_logging_level_value:
                        pretty_trace = None
                        if parsed_log_logging_level_value == LOG_LEVEL_ERROR and parsed_log.get(STACK_TRACE_KEY):
                            log_trace = parsed_log.get(STACK_TRACE_KEY)
                            pretty_trace = pretty_stacktrace(log_trace)
                            parsed_log[STACK_TRACE_KEY] = STACK_TRACE_MARKER
                        formatted_log = json.dumps(parsed_log, indent=2)
                        if pretty_trace:
                            formatted_log = formatted_log.replace(STACK_TRACE_MARKER, pretty_trace)
                        print(formatted_log)
                else:
                    if command_logging_level_value == LOG_LEVEL_INFO:
                        print(color_text(raw_log, 37))
            except Exception as e:
                error = color_text(f"There was an error parsing below log: '{e}'", 36)
                print(error)
                print(raw_log)


