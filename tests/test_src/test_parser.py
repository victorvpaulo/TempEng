import sys
from pathlib import Path

current_path = Path(__file__).resolve()
test_path = current_path.parent.parent
project_path = test_path.parent
sys.path.append(str(test_path))
sys.path.append(str(project_path))

from unittest import TestCase

from src.compiler import Parser


class ParserUnitTest(TestCase):
    def setUp(self):
        self.p = Parser()

    def test_parse(self):
        self.assertEqual(self.p.parse("abc"), [
            {"type": "static_string", "level": 0, "content": "abc"}])
        self.assertEqual(self.p.parse("{{a.b.c}}"), [
            {"type": "variable", "level": 0, "content": "a.b.c"}])
        self.assertEqual(self.p.parse("{%if x == y%}"), [
            {"type": "if", "level": 0, "content": "if x == y"}])
        self.p.indent_level = 0

        self.assertEqual(self.p.parse("{%for x in y%}"), [
            {"type": "for", "level": 0, "content": "for x in y"}])
        self.p.indent_level = 0

        self.assertEqual(self.p.parse("{%for x in y%}"), [
            {"type": "for", "level": 0, "content": "for x in y"}])
        self.assertEqual(self.p.parse("{%for z in w%}"), [
            {"type": "for", "level": 1, "content": "for z in w"}])
        self.p.indent_level = 0

        self.assertEqual(self.p.parse("{%for x in y%}{{x.z}}abc{%endfor%}fgh"),
                         [{"type": "for", "level": 0, "content": "for x in y"},
                          {"type": "variable", "level": 1,
                           "content": "x.z"},
                          {"type": "static_string", "level": 1,
                           "content": "abc"},
                          {"type": "static_string", "level": 0,
                           "content": "fgh"}])
        self.p.indent_level = 0

        self.assertEqual(self.p.parse("{%if x == y%}{{x.z}}abc{%endif%}fgh"),
                         [{"type": "if", "level": 0, "content": "if x == y"},
                          {"type": "variable", "level": 1,
                           "content": "x.z"},
                          {"type": "static_string", "level": 1,
                           "content": "abc"},
                          {"type": "static_string", "level": 0,
                           "content": "fgh"}])
        self.p.indent_level = 0

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

    def test_compute_next_indent_level(self):
        self.p.compute_next_indent_level("for")
        self.assertEqual(self.p.indent_level, 1)
        self.p.compute_next_indent_level("if")
        self.assertEqual(self.p.indent_level, 2)
        self.p.compute_next_indent_level("end")
        self.assertEqual(self.p.indent_level, 1)
        self.p.compute_next_indent_level("end")
        self.assertEqual(self.p.indent_level, 0)

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
