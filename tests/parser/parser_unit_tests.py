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
            "aabc {%abc%} a", self.parser.CONTROL_START_MARK), "aabc ")
        self.assertEqual(self.parser.extract_static_expression(
            "{{abc}} a", self.parser.VARIABLE_START_MARK), "")

    def test_extract_dynamic_expression(self):
        self.assertEqual(self.parser.extract_dynamic_expression(
            "{{abc}}aabc", self.parser.VARIABLE_END_MARK), "{{abc}}")
        self.assertEqual(self.parser.extract_dynamic_expression(
            "{%abc%} aabc a", self.parser.CONTROL_END_MARK), "{%abc%}")
        self.assertEqual(self.parser.extract_dynamic_expression(
            "{{abc}} a {%abc%}", self.parser.VARIABLE_END_MARK), "{{abc}}")

    def test_remove_markers(self):
        self.assertEqual(
            self.parser.remove_markers("{{abc}}",
                                       self.parser.VARIABLE_START_MARK,
                                       self.parser.VARIABLE_END_MARK), "abc")
        self.assertEqual(
            self.parser.remove_markers("{%def%}",
                                       self.parser.CONTROL_START_MARK,
                                       self.parser.CONTROL_END_MARK), "def")
        self.assertEqual(
            self.parser.remove_markers("{{ abc }}",
                                       self.parser.VARIABLE_START_MARK,
                                       self.parser.VARIABLE_END_MARK), " abc ")
        self.assertEqual(
            self.parser.remove_markers("{% def %}",
                                       self.parser.CONTROL_START_MARK,
                                       self.parser.CONTROL_END_MARK), " def ")

    def test_get_remaining_text(self):
        self.assertEqual(
            self.parser.get_remaining_text("{{abc}}", "{{abc}} {%def%}"),
            " {%def%}")
        self.assertEqual(
            self.parser.get_remaining_text("{%abc%}", "{%abc%}xyx"),
            "xyx")
