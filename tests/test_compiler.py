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
        self.assertEqual(self.c.compile_if("if x is True", 0),
                         "\n    if context['x'] is True:")
        self.assertEqual(self.c.compile_if("if x is not True", 0),
                         "\n    if context['x'] is not True:")
        self.assertEqual(self.c.compile_if("if x", 0),
                         "\n    if context['x']:")
        self.assertEqual(self.c.compile_if("if x and y", 0),
                         "\n    if context['x'] and context['y']:")
        self.assertEqual(self.c.compile_if("if x or y", 0),
                         "\n    if context['x'] or context['y']:")
        self.assertEqual(self.c.compile_if("if x is y", 0),
                         "\n    if context['x'] is context['y']:")
        self.assertEqual(self.c.compile_if("if x is None", 0),
                         "\n    if context['x'] is None:")
        self.assertEqual(self.c.compile_if("if x is not None", 0),
                         "\n    if context['x'] is not None:")
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
        self.assertEqual(self.c.compile_if("if x > 1 and x < 3", 1),
                         "\n        if context['x'] > 1 and context['x'] < 3:")
        self.assertEqual(self.c.compile_if("if x < 1 or x > 3", 1),
                         "\n        if context['x'] < 1 or context['x'] > 3:")
        self.assertEqual(
            self.c.compile_if("if x < 1 or x > 3 and y is True", 1),
            "\n        if context['x'] < 1 or context['x'] > 3 "
            "and context['y'] is True:")

    def test_if_value_is_static_string(self):
        self.assertEqual(self.c.is_static_string("'abc'"), True)
        self.assertEqual(self.c.is_static_string("abc"), False)
        self.assertEqual(self.c.is_static_string("'abc"), False)
        self.assertEqual(self.c.is_static_string("abc'"), False)
        self.assertEqual(self.c.is_static_string('"abc"'), True)
        self.assertEqual(self.c.is_static_string('abc'), False)
        self.assertEqual(self.c.is_static_string('"abc'), False)
        self.assertEqual(self.c.is_static_string('abc"'), False)

    def test_if_value_is_numeric(self):
        self.assertEqual(self.c.is_numeric("123"), True)
        self.assertEqual(self.c.is_numeric("123.0"), True)
        self.assertEqual(self.c.is_numeric("123."), True)
        self.assertEqual(self.c.is_numeric("123.2.3"), False)
        self.assertEqual(self.c.is_numeric("abc"), False)
        self.assertEqual(self.c.is_numeric("True"), False)
        self.assertEqual(self.c.is_numeric("False"), False)

    def test_if_value_is_boolean(self):
        self.assertEqual(self.c.is_boolean("True"), True)
        self.assertEqual(self.c.is_boolean("False"), True)
        self.assertEqual(self.c.is_boolean("123"), False)
        self.assertEqual(self.c.is_boolean("x.y"), False)

    def test_is_comparison_operator(self):
        self.assertEqual(self.c.is_operator("=="), True)
        self.assertEqual(self.c.is_operator("!="), True)
        self.assertEqual(self.c.is_operator(">="), True)
        self.assertEqual(self.c.is_operator(">"), True)
        self.assertEqual(self.c.is_operator("<="), True)
        self.assertEqual(self.c.is_operator("<"), True)
        self.assertEqual(self.c.is_operator("or"), True)
        self.assertEqual(self.c.is_operator("and"), True)
        self.assertEqual(self.c.is_operator("is"), True)
        self.assertEqual(self.c.is_operator("not"), True)
        self.assertEqual(self.c.is_operator("abc"), False)

    def test_element_of_if_expression_is_variable(self):
        self.assertEqual(self.c.element_of_if_expression_is_variable("abc"),
                         True)
        self.assertEqual(self.c.element_of_if_expression_is_variable("'abc'"),
                         False)
        self.assertEqual(self.c.element_of_if_expression_is_variable('"abc"'),
                         False)
        self.assertEqual(self.c.element_of_if_expression_is_variable("True"),
                         False)
        self.assertEqual(self.c.element_of_if_expression_is_variable("False"),
                         False)
        self.assertEqual(self.c.element_of_if_expression_is_variable("None"),
                         False)
        self.assertEqual(self.c.element_of_if_expression_is_variable("123"),
                         False)
        self.assertEqual(self.c.element_of_if_expression_is_variable("=="),
                         False)
        self.assertEqual(self.c.element_of_if_expression_is_variable("!="),
                         False)
        self.assertEqual(self.c.element_of_if_expression_is_variable(">="),
                         False)
        self.assertEqual(self.c.element_of_if_expression_is_variable(">"),
                         False)
        self.assertEqual(self.c.element_of_if_expression_is_variable("<="),
                         False)
        self.assertEqual(self.c.element_of_if_expression_is_variable("<"),
                         False)
        self.assertEqual(self.c.element_of_if_expression_is_variable("or"),
                         False)
        self.assertEqual(self.c.element_of_if_expression_is_variable("and"),
                         False)
        self.assertEqual(self.c.element_of_if_expression_is_variable("is"),
                         False)
        self.assertEqual(self.c.element_of_if_expression_is_variable("not"),
                         False)

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
