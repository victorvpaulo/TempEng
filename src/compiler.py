class Parser():
    def __init__(self, hierarchical_level: int = 0):
        self.hierarchical_level = hierarchical_level

    def parse(self, text: str):
        expressions = []

        while text != "":
            if ("{%" not in text or "%}" not in text) \
                    and ("{{" not in text or "}}" not in text):
                expression = {"type": "string",
                              "level": self.hierarchical_level,
                              "content": text}
                expressions.append(expression)
                text = ""
            elif text[0:2] == "{%":
                type = ""
                hierarchical_level_change = 0
                close_bracket_index = text.find("%}")
                text_segment_content = text[2:close_bracket_index].strip()
                if text_segment_content[0:3] == "end":
                    hierarchical_level_change = -1
                    type = text_segment_content
                else:
                    hierarchical_level_change = 1
                    if text_segment_content[0:2] == "if":
                        type = "if"
                    else:
                        type = "for"

                expression = {"type": type,
                              "level": self.hierarchical_level,
                              "content": text_segment_content}

                expressions.append(expression)
                text = text[close_bracket_index+2:]
                self.hierarchical_level += hierarchical_level_change
            elif text[0:2] == "{{":
                close_bracket_index = text.find("}}")
                text_segment_content = text[2:close_bracket_index].strip()
                expression = {"type": "substituion",
                              "level": self.hierarchical_level,
                              "content": text_segment_content}

                expressions.append(expression)
                text = text[close_bracket_index+2:]
            else:
                next_if_for_mark = text.find("{%")
                next_substitution_mark = text.find("{{")
                next_expression_starting_index = 0
                if next_if_for_mark != -1 \
                        and next_if_for_mark < next_substitution_mark:
                    next_expression_starting_index = next_if_for_mark
                else:
                    next_expression_starting_index = next_substitution_mark
                text_segment = text[0:next_expression_starting_index]
                expression = {"type": "string",
                              "level": self.hierarchical_level,
                              "content": text_segment}
                expressions.append(expression)
                text = text[next_expression_starting_index:]

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
