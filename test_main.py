from unittest import TestCase

import main
from pathlib import Path
import json

class Test(TestCase):
    def setUp(self):
        self.test_html = Path('./fixtures/test.txt').read_text()
        self.expected_json = json.loads(Path('fixtures/test_expectation.json').read_text(), strict=False)

    def test_parse_html_no_result(self):
        assert main.parse_html("") == {}

    def test_parse_html_success(self):
        parsed_html = main.parse_html(self.test_html)
        assert parsed_html.items() == self.expected_json.items()
