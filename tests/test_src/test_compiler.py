import sys
from pathlib import Path

current_path = Path(__file__).resolve()
test_path = current_path.parent.parent
project_path = test_path.parent
sys.path.append(str(test_path))
sys.path.append(str(project_path))

import unittest
from src.compiler import Compiler


class CompilerUnitTest(unittest.TestCase):
    def setUp(self):
        self.c = Compiler("str_list", 1)

    def test_compile_expression(self):
        self.assertEqual(self.c.compile_expression("if", "if x == y", 0),
                         "\n    if context['x'] == context['y']:")
        self.assertEqual(self.c.compile_expression("variable", "a.b", 0),
                         "\n    str_0 = context['a']['b']"
                         "\n    str_list.append(str_0)")
        self.assertEqual(self.c.compile_expression("static_string", "xyz", 0),
                         "\n    str_1 = 'xyz'\n    str_list.append(str_1)")
        self.assertEqual(self.c.compile_expression("for", "for x in y", 0),
                         "\n    for x in context['y']:")
        self.c.add_variable_to_scope("z", 1)
        self.assertEqual(self.c.compile_expression("for", "for x in z", 2),
                         "\n            for x in z:")
        self.assertEqual(self.c.compile_expression("for", "for x in z", 1),
                         "\n        for x in context['z']:")

    def test_compile_if(self):
        self.assertEqual(self.c.compile_if("if x == y", 0),
                         "\n    if context['x'] == context['y']:")
        self.assertEqual(self.c.compile_if("if x.k == y", 0),
                         "\n    if context['x']['k'] == context['y']:")
        self.assertEqual(self.c.compile_if("if x == y", 1),
                         "\n        if context['x'] == context['y']:")
        self.assertEqual(self.c.compile_if("if x != y", 0),
                         "\n    if context['x'] != context['y']:")
        self.assertEqual(self.c.compile_if("if x > y", 0),
                         "\n    if context['x'] > context['y']:")
        self.assertEqual(self.c.compile_if("if x >= y", 0),
                         "\n    if context['x'] >= context['y']:")
        self.assertEqual(self.c.compile_if("if x < y", 0),
                         "\n    if context['x'] < context['y']:")
        self.assertEqual(self.c.compile_if("if x <= y", 0),
                         "\n    if context['x'] <= context['y']:")
        self.c.add_variable_to_scope("z", 0)
        self.assertEqual(self.c.compile_if("if x == z", 1),
                         "\n        if context['x'] == z:")
        self.assertEqual(self.c.compile_if("if 'abc' == y", 1),
                         "\n        if 'abc' == context['y']:")
        self.assertEqual(self.c.compile_if("if 123.4 == y", 1),
                         "\n        if 123.4 == context['y']:")
        self.assertEqual(self.c.compile_if("if x == True", 1),
                         "\n        if context['x'] == True:")
        self.assertEqual(self.c.compile_if("if x == False", 1),
                         "\n        if context['x'] == False:")

    def test_if_value_is_static_string(self):
        self.assertEqual(self.c.if_value_is_static_string("'abc'"), True)
        self.assertEqual(self.c.if_value_is_static_string("abc"), False)
        self.assertEqual(self.c.if_value_is_static_string("'abc"), False)
        self.assertEqual(self.c.if_value_is_static_string("abc'"), False)
        self.assertEqual(self.c.if_value_is_static_string('"abc"'), True)
        self.assertEqual(self.c.if_value_is_static_string('abc'), False)
        self.assertEqual(self.c.if_value_is_static_string('"abc'), False)
        self.assertEqual(self.c.if_value_is_static_string('abc"'), False)

    def test_if_value_is_numeric(self):
        self.assertEqual(self.c.if_value_is_numeric("123"), True)
        self.assertEqual(self.c.if_value_is_numeric("123.0"), True)
        self.assertEqual(self.c.if_value_is_numeric("123."), True)
        self.assertEqual(self.c.if_value_is_numeric("123.2.3"), False)
        self.assertEqual(self.c.if_value_is_numeric("abc"), False)
        self.assertEqual(self.c.if_value_is_numeric("True"), False)
        self.assertEqual(self.c.if_value_is_numeric("False"), False)

    def test_if_value_is_boolean(self):
        self.assertEqual(self.c.if_value_is_boolean("True"), True)
        self.assertEqual(self.c.if_value_is_boolean("False"), True)
        self.assertEqual(self.c.if_value_is_boolean("123"), False)
        self.assertEqual(self.c.if_value_is_boolean("x.y"), False)

    def test_get_comparison_operator(self):
        self.assertEqual(self.c.get_comparison_operator("if x > 10"), ">")
        self.assertEqual(self.c.get_comparison_operator("if x >= 10"), ">=")
        self.assertEqual(self.c.get_comparison_operator("if x < 10"), "<")
        self.assertEqual(self.c.get_comparison_operator("if x <= 10"), "<=")
        self.assertEqual(self.c.get_comparison_operator("if x == 10"), "==")
        self.assertEqual(self.c.get_comparison_operator("if x != 10"), "!=")
        self.assertEqual(self.c.get_comparison_operator("if x == True"), "==")
        self.assertEqual(self.c.get_comparison_operator("if x is True"), None)
        self.assertEqual(self.c.get_comparison_operator("if x != True"), "!=")
        self.assertEqual(self.c.get_comparison_operator("if x is not True"),
                         None)

    def test_compile_for(self):
        self.assertEqual(self.c.compile_for("for x in y", 0),
                         "\n    for x in context['y']:")
        self.assertEqual(self.c.compile_for("for x in y", 1),
                         "\n        for x in context['y']:")
        self.c.add_variable_to_scope("z", 0)
        self.assertEqual(self.c.compile_for("for x in z", 0),
                         "\n    for x in z:")

    def test_get_element_of_sequence(self):
        self.assertEqual(self.c.get_element_of_sequence("for x in y"), "x")
        self.assertEqual(self.c.get_element_of_sequence("for  x  in y"), "x")

    def test_get_sequence(self):
        self.assertEqual(self.c.get_sequence("for x in y"), "y")
        self.assertEqual(self.c.get_sequence("for x in y "), "y")
        self.assertEqual(self.c.get_sequence("for x in y.z"), "y.z")

    def test_compile_variable(self):
        self.assertEqual(self.c.compile_variable("a", 0),
                         "\n    str_0 = context['a']"
                         "\n    str_list.append(str_0)")
        self.assertEqual(self.c.compile_variable("a.b.c", 0),
                         "\n    str_1 = context['a']['b']['c']"
                         "\n    str_list.append(str_1)")
        self.c.add_variable_to_scope("z", 0)
        self.assertEqual(self.c.compile_variable("z", 1),
                         "\n        str_2 = z"
                         "\n        str_list.append(str_2)")
        self.assertEqual(self.c.compile_variable("z.a", 1),
                         "\n        str_3 = z['a']"
                         "\n        str_list.append(str_3)")
        self.assertEqual(self.c.compile_variable("z.a", 0, True),
                         "z['a']")

    def test_compile_static_string(self):
        self.assertEqual(self.c.compile_static_string("abc", 0),
                         "\n    str_0 = 'abc'\n    str_list.append(str_0)")
        self.assertEqual(self.c.compile_static_string('abc', 0),
                         "\n    str_1 = 'abc'\n    str_list.append(str_1)")

    def test_compile_string(self):
        self.assertEqual(self.c.compile_static_string("abc def", 0),
                         "\n    str_0 = 'abc def'\n    str_list.append(str_0)")
        self.assertEqual(self.c.compile_static_string('hij', 0),
                         "\n    str_1 = 'hij'\n    str_list.append(str_1)")

    def test_get_append_string_to_list_statement(self):
        self.assertEqual(
            self.c.get_append_string_to_list_statement("str_0", 0),
            "\n    str_list.append(str_0)")
        self.c.string_list_identifier = "lst"
        self.assertEqual(
            self.c.get_append_string_to_list_statement("str_0", 0),
            "\n    lst.append(str_0)")

    def test_indent(self):
        self.assertEqual(self.c.indent("for x in y:", 0),
                         "\n    for x in y:")
        self.assertEqual(self.c.indent("if x == y:", 1),
                         "\n        if x == y:")
        self.c.indentation = self.c.TAB
        self.assertEqual(self.c.indent("str_1 = 'abc'", 1),
                         "\n\t\tstr_1 = 'abc'")
        self.c.initial_indent_level = 3
        self.assertEqual(self.c.indent("str_1 = 'abc'", 2),
                         "\n\t\t\t\t\tstr_1 = 'abc'")

    def test_get_scope_variable(self):
        self.assertEqual(self.c.get_scope_variable("context"), "context")
        self.c.scope_variables = [("context", -1), ("x", 1)]
        self.assertEqual(self.c.get_scope_variable("x"), "x")
        self.assertEqual(self.c.get_scope_variable("y"), "context")
        self.c.scope_variables = [("context", -1), ("x", 1), ("y", 2)]
        self.assertEqual(self.c.get_scope_variable("x"), "x")

    def test_add_variable_to_scope(self):
        self.c.add_variable_to_scope("x", 0)
        self.assertEqual(self.c.scope_variables, [("context", -1), ("x", 1)])
        self.c.add_variable_to_scope("z", 1)
        self.assertEqual(self.c.scope_variables,
                         [("context", -1), ("x", 1), ("z", 2)])

    def test_remove_out_of_scope_variables(self):
        self.c.scope_variables = [("context", -1), ("abc", 1), ("def", 2)]
        self.c.remove_out_of_scope_variables(2)
        self.assertSequenceEqual(self.c.scope_variables,
                                 [("context", -1), ("abc", 1)])

        self.c.scope_variables = [("context", -1), ("abc", 1), ("def", 2)]
        self.c.remove_out_of_scope_variables(1)
        self.assertSequenceEqual(self.c.scope_variables, [("context", -1)])


if __name__ == '__main__':
    unittest.main()