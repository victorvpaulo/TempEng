from unittest import TestCase
from src.compiler import Parser


class ParserDrivingCarUnitTest(TestCase):
    def setUp(self):
        self.parser = Parser()

    def test_starts_with_control_expression(self):
        self.assertEqual(
            self.parser.starts_with_control_expression("{{abc}}"), False)
        self.assertEqual(
            self.parser.starts_with_control_expression(" {%abc%}"), False)
        self.assertEqual(
            self.parser.starts_with_control_expression("{%abc"), False)
        self.assertEqual(
            self.parser.starts_with_control_expression("{%abc%}"), True)

    def test_starts_with_variable_expression(self):
        self.assertEqual(
            self.parser.starts_with_control_expression("{%abc%}"), False)
        self.assertEqual(
            self.parser.starts_with_control_expression(" {{abc}}"), False)
        self.assertEqual(
            self.parser.starts_with_control_expression("{{abc"), False)
        self.assertEqual(
            self.parser.starts_with_control_expression("{{abc}}"), True)

    def test_contains_dynamic_expression(self):
        self.assertEqual(
            self.parser.contains_dynamic_expression("ABC"), False)
        self.assertEqual(
            self.parser.contains_dynamic_expression("{{abc"), False)
        self.assertEqual(
            self.parser.contains_dynamic_expression("{%abc"), False)
        self.assertEqual(
            self.parser.contains_dynamic_expression("{{abc%}"), False)
        self.assertEqual(
            self.parser.contains_dynamic_expression("{%abc}}"), False)
        self.assertEqual(
            self.parser.contains_dynamic_expression("{%abc%}"), True)
        self.assertEqual(
            self.parser.contains_dynamic_expression("{{abc}}"), True)
        self.assertEqual(
            self.parser.contains_dynamic_expression("ABC {%abc%}"), True)
        self.assertEqual(
            self.parser.contains_dynamic_expression("ABC {{abc}}"), True)
        self.assertEqual(
            self.parser.contains_dynamic_expression("{{abc%}  {%abc%}"), True)
        self.assertEqual(
            self.parser.contains_dynamic_expression("{%abc}} {{abc}}"), True)

    def test_extract_static_expression(self):
        self.assertEqual(self.parser.extract_static_expression(
            "aabc {{abc}}", self.parser.VARIABLE_START_MARK), "aabc ")
        self.assertEqual(self.parser.extract_static_expression(
            "aabc {{abc}} a",self.parser.VARIABLE_START_MARK), "aabc ")
        self.assertEqual(self.parser.extract_static_expression(
            "{{abc}} a", self.parser.VARIABLE_START_MARK), "")



