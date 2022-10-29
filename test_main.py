from unittest import TestCase

import main
from pathlib import Path
import json

class Test(TestCase):
    def setUp(self):
        self.test_html = Path('./fixtures/test.txt').read_text()
        self.expected_json = json.loads(Path('fixtures/test_expectation.json').read_text(), strict=False)
        # self.test_html1 = Path('fixtures/test_1.html').read_text()
        # self.expected_json1 = json.loads(Path('fixtures/test_1_expectation.json').read_text(), strict=False)

    def test_parse_html_no_result(self):
        assert main.parse_html("<html><body><div></div></body></html>", "div") == {}

    def test_parse_html_success(self):
        parsed_data = main.parse_html(self.test_html, "div", "div-col columns column-width")
        assert parsed_data.items() == self.expected_json.items()

    def test_parse_robots(self):
        default_delay = 0.2
        can_crawl, delay = main.parse_robots("https://www.dnes.bg/", default_delay)
        assert can_crawl
        assert delay == default_delay