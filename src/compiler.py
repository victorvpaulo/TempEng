class Parser:
    VARIABLE_START_MARK = "{{"
    VARIABLE_END_MARK = "}}"
    CONTROL_START_MARK = "{%"
    CONTROL_END_MARK = "%}"

    def __init__(self):
        self.hierarchical_level = 0

    def starts_with_control_expression(self, text):
        if text[0:2] == "{%" and "%}" in text:
            return True
        return False

    def starts_with_variable_expression(self, text):
        if text[0:2] == "{{" and "}}" in text:
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

    def remove_markers(self, expression, end_mark,
                       start_mark=None, strip=False):
        expression_ending_index = expression.find(end_mark)
        expression_starting_index = 0
        if start_mark is not None:
            expression_starting_index = expression.find(start_mark) + 2

        expression_content = expression[
                             expression_starting_index:expression_ending_index]
        if strip:
            expression_content = expression_content.strip()
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

    def is_just_a_hierarchical_level_marker(self, expression_type):
        # {%endif%} and {%endfor%} statements exist just to sign that
        # the block of code inside the if/for is finished, and the next
        # statement has the same indent (hierarchical) level than the
        # for/if statement. As such, there is no need to include this
        # kind of block in the expressions to be compiled.

        return expression_type == "end"

    def compute_next_hierarchical_level(self, expression_type):
        if expression_type == "if" or expression_type == "for":
            self.hierarchical_level += 1
        elif expression_type == "end":
            self.hierarchical_level -= 1

    def find_control_expression_type(self, expression_content):
        if expression_content[0:2] == "if":
            return "if"
        elif expression_content[0:3] == "for":
            return "for"
        else:
            return "end"

    def build_expression(self, content, expression_type):
        expression = {"type": expression_type,
                      "level": self.hierarchical_level,
                      "content": content}

        return expression

    def add_expression(self, content, expression_type, expressions):
        expression = self.build_expression(content, expression_type)
        expressions.append(expression)

    def parse(self, text: str):
        expressions = []
        while text != "":
            if self.starts_with_control_expression(text):
                raw_expression = \
                    self.extract_dynamic_expression(text,
                                                    self.CONTROL_END_MARK)
                content = self.remove_markers(
                    raw_expression, self.CONTROL_END_MARK,
                    self.CONTROL_START_MARK, True)
                expression_type = self.find_control_expression_type(content)
            elif self.starts_with_variable_expression(text):
                raw_expression = \
                    self.extract_dynamic_expression(text,
                                                    self.VARIABLE_END_MARK)
                content = self.remove_markers(
                    raw_expression, self.VARIABLE_END_MARK,
                    self.VARIABLE_START_MARK, True)
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

            if not self.is_just_a_hierarchical_level_marker(expression_type):
                self.add_expression(content, expression_type, expressions)
            text = self.get_remaining_text(raw_expression, text)
            self.compute_next_hierarchical_level(expression_type)
        return expressions


def write_to_output(output, content):
    output.write(content)


def compilator_placeholder(expressions):
    for expression in expressions:
        print(str(expression))


def compile_template(static_template_path, output_path):
    with open(static_template_path, "r") as staticf:
        parser = Parser()
        for line in staticf:
            expressions = parser.parse(line)
            compilator_placeholder(expressions)
