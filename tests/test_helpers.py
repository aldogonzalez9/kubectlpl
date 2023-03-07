import os
import unittest
import sys

from kubectl_prettylogs_wrapper.helpers import load_json_from_raw_log


class TestHelpers(unittest.TestCase):
    @staticmethod
    def get_test_sample(sample_name):
        with open(os.path.join(sys.path[0], f"files/{sample_name}"), "r") as f:
            file_content = f.read()
        return file_content

    def test_nested_log_with_escaped_quotes(self):
        test_sample = self.get_test_sample("nested_log.json")
        result = load_json_from_raw_log(test_sample)
        assert type(result) is dict
        assert type(result["payload"]) is dict
