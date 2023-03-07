import json
import os
import re
import uuid

from kubectl_prettylogs_wrapper.constants import COLOR_SEQUENCE_PREFIX


def color_text(text: str, color: int):
    return "{0}{1}m{2}{0}0m".format(COLOR_SEQUENCE_PREFIX, color, text)


def parse_trace_item(trace_item: str) -> str:
    """
    Format error trace item to make it more readable
    :param trace_item:
    :return: Formatted trace
    """
    trace_item = trace_item.strip()
    # use this match to check if this is a trace path or the "code source" of the exception
    # e.g. File \"/path/to/file/where/exception/occurred.py\", line <number>, in <method_name>
    # or this_code(caused, the, exception)
    error_path_match = re.match('File (.*), line (\d+), in (.+)', trace_item)
    if error_path_match:
        groups = error_path_match.groups()
        path = groups[0]
        path = path.replace(os.getcwd(), '')
        error_line_number = groups[1]
        error_method = groups[2]
        colorized_trace_element = "\t{0} ({1}): {2}".format(
            color_text(path, 36),
            color_text(error_line_number, 33),
            color_text(error_method, 32)
        )
        return colorized_trace_element
    else:
        return f"\t\t{trace_item}"


def pretty_stacktrace(stacktrace_message: str) -> str:
    """
    Indent, format and colorize a stacktrace log to make it human-readable
    :param stacktrace_message: Complete stacktrace in log
    :return: 
    """
    pretty_trace_items = []
    stacktrace_items = [stacktrace_item for stacktrace_item in stacktrace_message.split("\n") if stacktrace_item]
    trace_exception = stacktrace_items.pop()
    trace_exception = f'\t{color_text("Error ", 33)} {color_text(trace_exception, 31)}'
    trace_initial_message = stacktrace_items.pop(0)
    pretty_trace_items.append(trace_initial_message)
    for stacktrace_item in stacktrace_items:
        parsed_message = parse_trace_item(stacktrace_item)
        pretty_trace_items.append(parsed_message)
    pretty_trace_items.append(trace_exception)
    return '\n'.join(pretty_trace_items)


def load_json_from_raw_log(raw_json: str):
    # For nested json value as string
    nested_json = re.search('"{(.*)}"', raw_json)
    nested_json_parsed = {}
    replacement_marker = None
    if nested_json:
        nested_json = nested_json.group(0).strip('"')
        replacement_marker = str(uuid.uuid4())
        raw_json = raw_json.replace(nested_json, replacement_marker)
        # found escaped quotation marks in a few nested jsons which caused loads() to fail
        nested_json = nested_json.replace('\\"', '"')
        nested_json_parsed = load_json_from_raw_log(nested_json)
    json_log_loaded = json.loads(raw_json, strict=False)

    if replacement_marker:
        # replacement_key = None
        for k, v in json_log_loaded.items():
            if v == replacement_marker:
                # It might not be safe to change the structure of the container in a loop (e.g. add, remove) but
                # assigning a different value at a given existing index does not incur any problem.
                json_log_loaded[k] = nested_json_parsed
                break
    return json_log_loaded
