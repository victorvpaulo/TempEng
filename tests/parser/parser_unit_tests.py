from unittest import TestCase
from src.compiler import Parser


class ParserDrivingCarUnitTest(TestCase):
    def setUp(self):
        self.p = Parser()

    def test_starts_with_control_expression(self):
        self.assertEqual(
            self.p.starts_with_control_expression("{{abc}}"), False)
        self.assertEqual(
            self.p.starts_with_control_expression(" {%abc%}"), False)
        self.assertEqual(
            self.p.starts_with_control_expression("{%abc"), False)
        self.assertEqual(
            self.p.starts_with_control_expression("{%abc%}"), True)

    def test_starts_with_variable_expression(self):
        self.assertEqual(
            self.p.starts_with_variable_expression("{%abc%}"), False)
        self.assertEqual(
            self.p.starts_with_variable_expression(" {{abc}}"), False)
        self.assertEqual(
            self.p.starts_with_variable_expression("{{abc"), False)
        self.assertEqual(
            self.p.starts_with_variable_expression("{{abc}}"), True)

    def test_contains_dynamic_expression(self):
        self.assertEqual(
            self.p.contains_dynamic_expression("ABC"), False)
        self.assertEqual(
            self.p.contains_dynamic_expression("{{abc"), False)
        self.assertEqual(
            self.p.contains_dynamic_expression("{%abc"), False)
        self.assertEqual(
            self.p.contains_dynamic_expression("{{abc%}"), False)
        self.assertEqual(
            self.p.contains_dynamic_expression("{%abc}}"), False)
        self.assertEqual(
            self.p.contains_dynamic_expression("{%abc%}"), True)
        self.assertEqual(
            self.p.contains_dynamic_expression("{{abc}}"), True)
        self.assertEqual(
            self.p.contains_dynamic_expression("ABC {%abc%}"), True)
        self.assertEqual(
            self.p.contains_dynamic_expression("ABC {{abc}}"), True)
        self.assertEqual(
            self.p.contains_dynamic_expression("{{abc%}  {%abc%}"), True)
        self.assertEqual(
            self.p.contains_dynamic_expression("{%abc}} {{abc}}"), True)

    def test_extract_static_expression(self):
        self.assertEqual(self.p.extract_static_expression(
            "aabc {{abc}}", self.p.VARIABLE_START_MARK), "aabc ")
        self.assertEqual(self.p.extract_static_expression(
            "aabc {%abc%} a", self.p.CONTROL_START_MARK), "aabc ")
        self.assertEqual(self.p.extract_static_expression(
            "{{abc}} a", self.p.VARIABLE_START_MARK), "")

    def test_extract_dynamic_expression(self):
        self.assertEqual(self.p.extract_dynamic_expression(
            "{{abc}}aabc", self.p.VARIABLE_END_MARK), "{{abc}}")
        self.assertEqual(self.p.extract_dynamic_expression(
            "{%abc%} aabc a", self.p.CONTROL_END_MARK), "{%abc%}")
        self.assertEqual(self.p.extract_dynamic_expression(
            "{{abc}} a {%abc%}", self.p.VARIABLE_END_MARK), "{{abc}}")

    def test_remove_markers(self):
        self.assertEqual(
            self.p.remove_markers("{{abc}}",
                                  self.p.VARIABLE_START_MARK,
                                  self.p.VARIABLE_END_MARK), "abc")
        self.assertEqual(
            self.p.remove_markers("{%def%}",
                                  self.p.CONTROL_START_MARK,
                                  self.p.CONTROL_END_MARK), "def")
        self.assertEqual(
            self.p.remove_markers("{{ abc }}",
                                  self.p.VARIABLE_START_MARK,
                                  self.p.VARIABLE_END_MARK), " abc ")
        self.assertEqual(
            self.p.remove_markers("{% def %}",
                                  self.p.CONTROL_START_MARK,
                                  self.p.CONTROL_END_MARK), " def ")

    def test_get_remaining_text(self):
        self.assertEqual(
            self.p.get_remaining_text("{{ab}}", "{{ab}} {%de%}"), " {%de%}")
        self.assertEqual(
            self.p.get_remaining_text("{%ab%}", "{%ab%}xy"), "xy")

    def test_is_just_an_indent_level_marker(self):
        self.assertEqual(
            self.p.is_just_an_indent_level_marker("end"), True)
        self.assertEqual(
            self.p.is_just_an_indent_level_marker("if"), False)
        self.assertEqual(
            self.p.is_just_an_indent_level_marker("for"), False)
        self.assertEqual(
            self.p.is_just_an_indent_level_marker("variable"), False)
        self.assertEqual(
            self.p.is_just_an_indent_level_marker("static_string"), False)

    def(self):
        self.assertEqual(self.p.compute_next_indent_level("for"), 1)
        self.assertEqual(self.p.compute_next_indent_level("if"), 2)
        self.assertEqual(self.p.compute_next_indent_level("end"), 1)
        self.assertEqual(self.p.compute_next_indent_level("end"), 0)

    def test_find_control_expression_type(self):
        self.assertEqual(
            self.p.find_control_expression_type("for x in y"), "for")
        self.assertEqual(
            self.p.find_control_expression_type("if x == y"), "if")
        self.assertEqual(
            self.p.find_control_expression_type("endfor"), "end")
        self.assertEqual(
            self.p.find_control_expression_type("endif"), "end")

    def test_build_expression(self):
        self.assertEqual(self.p.build_expression("for x in y", "for"),
                         {"type": "for", "level": 0, "content": "for x in y"})
        self.p.indent_level = 1
        self.assertEqual(self.p.build_expression("ab.xy", "variable"),
                         {"type": "variable", "level": 1, "content": "ab.xy"})
