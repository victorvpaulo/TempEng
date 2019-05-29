class Parser:
    VARIABLE_START_MARK = "{{"
    VARIABLE_END_MARK = "}}"
    CONTROL_START_MARK = "{%"
    CONTROL_END_MARK = "%}"

    def __init__(self):
        self.indent_level = 0

    def starts_with_control_expression(self, text):
        if text[0:2] == self.CONTROL_START_MARK \
                and self.CONTROL_END_MARK in text:
            return True
        return False

    def starts_with_variable_expression(self, text):
        if text[0:2] == self.VARIABLE_START_MARK \
                and self.VARIABLE_END_MARK in text:
            return True
        return False

    def contains_dynamic_expression(self, text):
        # If no dynamic expression (control,variable) is present then
        # the text is just a single static expression.
        if (self.VARIABLE_START_MARK in text
            and self.VARIABLE_END_MARK in text) \
                or (self.CONTROL_START_MARK in text
                    and self.CONTROL_END_MARK in text):
            return True
        return False

    def extract_static_expression(self, text,
                                  dynamic_expression_start_mark):
        static_expression_end = text.find(dynamic_expression_start_mark)
        static_expression = text[0:static_expression_end]
        return static_expression

    def extract_dynamic_expression(self, text, end_mark):
        expression_end = text.find(end_mark) + len(end_mark)
        expression = text[0:expression_end]
        return expression

    def remove_markers(self, expression, start_mark, end_mark):
        expression_starting_index = expression.find(start_mark) + 2
        expression_ending_index = expression.find(end_mark)
        expression_content = expression[
                             expression_starting_index:expression_ending_index]
        return expression_content

    def get_remaining_text(self, raw_expression, text):
        raw_expression = raw_expression
        text = text[len(raw_expression):]
        return text

    def find_next_dynamic_expression_start(self, text):
        next_control_expression_mark = text.find(self.CONTROL_START_MARK)
        next_variable_mark = text.find(self.VARIABLE_START_MARK)

        if next_control_expression_mark == -1:
            return self.VARIABLE_START_MARK
        elif next_variable_mark == -1:
            return self.CONTROL_START_MARK
        elif next_control_expression_mark < next_variable_mark:
            return self.CONTROL_START_MARK
        else:
            return self.VARIABLE_START_MARK

    def is_just_an_indent_level_marker(self, expression_type):
        # {%endif%} and {%endfor%} statements exist just to sign that
        # the block of code inside the if/for is finished, and the next
        # statement has the same indent level than the
        # for/if statement. As such, there is no need to include this
        # kind of block in the expressions to be compiled.

        return expression_type == "end"

    def compute_next_indent_level(self, expression_type):
        if expression_type == "if" or expression_type == "for":
            self.indent_level += 1
        elif expression_type == "end":
            self.indent_level -= 1

    def find_control_expression_type(self, expression_content):
        if expression_content[0:2] == "if":
            return "if"
        elif expression_content[0:3] == "for":
            return "for"
        else:
            return "end"

    def build_expression(self, content, expression_type):
        expression = {"type": expression_type,
                      "level": self.indent_level,
                      "content": content}

        return expression

    def add_expression(self, content, expression_type, expressions):
        expression = self.build_expression(content, expression_type)
        expressions.append(expression)

    def parse(self, text: str):
        expressions = []
        while text != "":
            if self.starts_with_control_expression(text):
                raw_expression = self.extract_dynamic_expression(
                    text, self.CONTROL_END_MARK)
                content = self.remove_markers(
                    raw_expression, self.CONTROL_START_MARK,
                    self.CONTROL_END_MARK).strip()
                expression_type = self.find_control_expression_type(content)
            elif self.starts_with_variable_expression(text):
                raw_expression = self.extract_dynamic_expression(
                    text, self.VARIABLE_END_MARK)
                content = self.remove_markers(
                    raw_expression, self.VARIABLE_START_MARK,
                    self.VARIABLE_END_MARK).strip()
                expression_type = "variable"
            else:
                raw_expression = text
                content = text
                if self.contains_dynamic_expression(text):
                    static_expression_end_mark = \
                        self.find_next_dynamic_expression_start(text)
                    raw_expression = self.extract_static_expression(
                        text, static_expression_end_mark)
                    content = raw_expression
                expression_type = "static_string"

            if not self.is_just_an_indent_level_marker(expression_type):
                self.add_expression(content, expression_type, expressions)
            text = self.get_remaining_text(raw_expression, text)
            self.compute_next_indent_level(expression_type)
        return expressions


class Compiler:
    FOUR_SPACES = "    "
    TWO_SPACES = "  "
    TAB = "\t"

    def __init__(self, string_list_identifier, initial_indent_level,
                 indentation=FOUR_SPACES):
        self.string_list_identifier = string_list_identifier
        self.initial_indent_level = initial_indent_level
        self.indentation = indentation
        self.string_variable_counter = 0
        # A for loop variable will have scope level 1
        # (Like product in 'for product in products').
        # If the for loop is nested inside another for loop
        # the variable will have scope level 2, and so on.
        # In the compiled template context is the identifier of
        # the dictionary containing dynamic data to be se inserted.
        # As such, it has a kind of global scope in the template module,
        # represented by a -1 scope level in the code below.
        self.scope_variables = [("context", -1)]

    def compile_expression(self, expression_type, expression_content,
                           indent_level):
        if expression_type == "if":
            return self.compile_if(expression_content, indent_level)
        elif expression_type == "for":
            return self.compile_for(expression_content, indent_level)
        elif expression_type == "variable":
            return self.compile_variable(expression_content,
                                         indent_level)
        else:
            return self.compile_static_string(expression_content,
                                              indent_level)

    def compile_if(self, if_expression, indent_level):
        comparison_expression = if_expression.replace("if", "")
        comparison_operator = self.get_comparison_operator(
            comparison_expression)
        values_to_be_compared = comparison_expression.split(
            comparison_operator)
        for index in range(0, len(values_to_be_compared)):
            value = values_to_be_compared[index].strip()
            if self.if_value_is_static_string(value):
                values_to_be_compared[index] = value
            else:
                values_to_be_compared[index] = self.compile_variable(
                    value, indent_level, True)
        compiled_if_expression = "if " + values_to_be_compared[0] + " " \
                                 + comparison_operator + " " + \
                                 values_to_be_compared[1] \
                                 + ":"

        compiled_if_expression = self.indent(compiled_if_expression,
                                             indent_level)
        return compiled_if_expression

    def if_value_is_static_string(self, if_value):
        starting_character = if_value[0]
        ending_character = if_value[-1]
        if (starting_character == '"' and ending_character == '"') or (
                starting_character == "'" and ending_character == "'"):
            return True
        return False

    def get_comparison_operator(self, if_expression):
        operators = ("==", "!=", ">", ">=", "<", "<=")
        for operator in operators:
            if operator in if_expression:
                return operator
        return None

    def compile_for(self, for_expression, indent_level):
        self.add_variable_to_scope(for_expression, indent_level)

        sequence_variable = self.get_sequence_variable(for_expression)
        compiled_sequence_variable = self.compile_variable(sequence_variable,
                                                           indent_level,
                                                           True)
        compiled_for_expression = for_expression.replace(
            sequence_variable, " " + compiled_sequence_variable) + ":"
        compiled_for_expression = self.indent(compiled_for_expression,
                                              indent_level)
        return compiled_for_expression

    def get_element_of_sequence(self, for_expression):
        return for_expression[3:for_expression.index("in")].strip()

    def get_sequence_variable(self, for_expression):
        return for_expression[for_expression.index("in") + 2:]

    def compile_variable(self, raw_variable, indent_level,
                         control_expression_variable=False):
        keys = raw_variable.split(".")
        scope_variable = self.get_scope_variable(keys[0])
        compiled_expression = scope_variable

        for index in range(0, len(keys)):
            key = keys[index].strip()
            if index == 0 and key == scope_variable:
                continue
            compiled_expression += "['" + key + "']"
        if not control_expression_variable:
            compiled_expression = self.compile_string(
                compiled_expression, indent_level)

        return compiled_expression

    def compile_static_string(self, raw_string, indent_level):
        string = repr(raw_string)
        return self.compile_string(string, indent_level)

    def compile_string(self, string, indent_level):
        string_variable_identifier = "str_" + str(self.string_variable_counter)
        self.string_variable_counter += 1
        header = string_variable_identifier + " = "
        header = self.indent(header, indent_level)
        append_statement = self.get_append_string_to_list_statement(
            string_variable_identifier, indent_level)
        compiled_expression = header + string + append_statement
        return compiled_expression

    def get_append_string_to_list_statement(self, string_variable_identifier,
                                            indent_level):
        append_statement = self.string_list_identifier \
                           + ".append(" + string_variable_identifier + ")"
        append_statement = self.indent(append_statement, indent_level)
        return append_statement

    def indent(self, compiled_expression, indent_level):
        indented_expression = "\n"
        for level in range(0, indent_level + self.initial_indent_level):
            indented_expression += self.indentation
        indented_expression += compiled_expression
        return indented_expression

    def method_name(self, idented_expression):
        return idented_expression

    def get_scope_variable(self, variable):
        for scope_variable in self.scope_variables[::-1]:
            if scope_variable[0] == variable:
                return scope_variable[0]
            return self.scope_variables[0][0]

    def add_variable_to_scope(self, for_expression, indent_level):
        variable = self.get_element_of_sequence(for_expression)
        self.scope_variables.append((variable, indent_level))

    def remove_out_of_scope_variables(self, indent_level):
        for variable in self.scope_variables[::-1]:
            variable_level = variable[1]
            if variable_level <= indent_level:
                self.scope_variables.remove(variable)
            else:
                return


def compile_template(static_template_path, output_path):
    static_template_file = open(static_template_path, "r")
    compilation_output_file = open(output_path, "w")

    parser = Parser()
    compiler = Compiler("str_list", 1)

    add_output_file_header(compilation_output_file, compiler.indentation,
                           compiler.string_list_identifier)

    for line in static_template_file:
        expressions = parser.parse(line)
        for expression in expressions:
            compiled_expression = compiler.compile_expression(
                expression["type"],
                expression["content"],
                expression["level"])
            compilation_output_file.write(compiled_expression)

    add_output_file_footer(compilation_output_file, compiler.indentation,
                           compiler.string_list_identifier)

    print("Template compiled. Sent to:\n\t" + str(output_path))


def add_output_file_header(compiled_output_file, indentation,
                           string_list_identifier):
    output_file_header = "def build_text_file(context, output_path):\n" \
                         + indentation + string_list_identifier + " = []\n"
    compiled_output_file.write(output_file_header)


def add_output_file_footer(compiled_output_file, indentation,
                           string_list_identifier):
    output_file_footer = "\n\n" + indentation \
                         + "output_file = open(output_path, 'w')\n" \
                         + indentation \
                         + "for string in " + string_list_identifier + ":\n" \
                         + indentation + indentation \
                         + "output_file.write(str(string))\n"
    compiled_output_file.write(output_file_footer)
