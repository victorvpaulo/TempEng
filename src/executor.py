import json
from importlib import import_module, invalidate_caches
from sys import path as syspath
from utils import get_timestamp


def build_file_from_template(context, output_path, template):
    if "$file_name$" in context:
        file_name = context["$file_name$"]
    else:
        file_name = get_timestamp()
    output_path_with_filename = output_path / file_name
    template.build_text_file(context, output_path_with_filename)
    return output_path_with_filename


def import_compiled_template(template_path, module_name):
    syspath.append(str(template_path))
    invalidate_caches()
    return import_module(module_name)


def is_free_of_reserved_keywords(context):
    if "context" in context:
        return False
    return True


def is_valid_context(context):
    if isinstance(context, dict) and is_free_of_reserved_keywords(context):
        return True
    return False


def load_data_contexts_from_file(contexts_file_path):
    with open(contexts_file_path, 'r') as file:
        return json.loads(file.read())


def get_data_contexts(contexts_file_path):
    contexts = load_data_contexts_from_file(contexts_file_path)
    if not isinstance(contexts, list):
        contexts = [contexts]
    return contexts


def execute_compiled_template(template_path, template_module_name,
                              context_file_path, output_path):
    template = import_compiled_template(template_path, template_module_name)
    contexts = get_data_contexts(context_file_path)
    for context in contexts:
        if is_valid_context(context):
            file_path = build_file_from_template(context, output_path, template)
            print("a")
            print("File generated. Sent to:\n\t" + str(file_path))
        else:
            # TODO: add a better error handling.
            print("ERROR - Invalid Context")