import os
from pathlib import Path

from .config_reader import get_path_from_config
from src.compiler import compile_template
from src.executor import execute_compiled_template


def load_file_content(path):
    with open(path, 'r') as f:
        file_content = f.read()
    return file_content


def clear_temp_files(path):
    for file_path in path.iterdir():
        if file_path.is_file() and file_path.name[0:4] == "TEMP":
            os.remove(file_path)
        if file_path.is_dir() and file_path.name == "results":
            for fp in file_path.iterdir():
                if fp.is_file() and fp.name[0:4] == "TEMP":
                    os.remove(fp)


def compare_expected_and_actual_results_from_execution(execution_path):
    for result_file in execution_path:
        path = Path(result_file)
        name = Path(result_file).name

        print("\t\t\tExecution: Testing result files: " + name)

        temp_file = result_file.replace(path.name, "TEMP_" + name)
        with open(result_file, 'r') as rf:
            result = rf.read()
        with open(temp_file, 'r') as tf:
            temp = tf.read()

        assert result == temp


def test_template_execution(test_compiled_template_path, data_context_path,
                            results_path):
    test_compiled_template_path = Path(test_compiled_template_path)
    test_compiled_template_name = test_compiled_template_path.name.replace(
        ".py", "")
    test_compiled_template_folder_path = Path(
        test_compiled_template_path).parent
    try:
        execute_compiled_template(test_compiled_template_folder_path,
                                  test_compiled_template_name,
                                  data_context_path,
                                  Path(results_path[0]).parent, silent=True)

        compare_expected_and_actual_results_from_execution(results_path)

        print("\t\tExecution: test succeeded.")
    except (AssertionError, FileNotFoundError) as e:
        print("\t\tExecution: test failed.")
        raise e


def test_template_compilation(static_template_path, compiled_template_path):
    try:
        compilation_output_path = str(compiled_template_path).replace(
            "compiled_template", "TEMP_template_compilation_test")
        compile_template(static_template_path, compilation_output_path,
                         silent=True)
        expected = load_file_content(compiled_template_path)
        actual = load_file_content(compilation_output_path)
        if expected == actual:
            print("\t\tCompilation: test succeeded.")
        else:
            raise AssertionError("The files are not equal:\n\tExpected: "
                                 + compiled_template_path + "\n\tActual: "
                                 + compilation_output_path)
    except (AssertionError, ValueError, SyntaxError) as e:
        print("\t\tCompilation: test failed.")
        raise e


def issue_test_starting_message(has_compilation_test, has_execution_test,
                                case_identifier):
    test_message = "\tRunning "
    test_types = []
    if has_compilation_test:
        test_types.append("COMPILATION")
    if has_execution_test:
        test_types.append("EXECUTION")
    tests = ' and '.join(test_types)
    test_message += tests + " tests for test case: " + case_identifier + "."
    print(test_message)


def has_compilation_test(test_case):
    return 'static_template' in test_case and 'compiled_template' in test_case


def has_execution_test(test_case):
    return 'compiled_template' in test_case and 'results' in test_case


def run_test(test_case):
    compilation_test = has_compilation_test(test_case)
    execution_test = has_execution_test(test_case)
    if not compilation_test and not execution_test:
        return
    else:
        issue_test_starting_message(compilation_test, execution_test,
                                    test_case['case_identifier'])
        if compilation_test:
            test_template_compilation(test_case['static_template'],
                                      test_case['compiled_template'])
        if execution_test:
            test_template_execution(test_case['compiled_template'],
                                    test_case['data_context'],
                                    test_case['results'])

        # If the test failed it's helpful to have te temporary test file
        # at hands for debugging. So the temporary test files are deleted
        # only when the test succeeds.
        clear_temp_files(Path(test_case['test_case_path']))


def is_test_file(file_path, file_name):
    test_file_names = ["compiled_template.py", "data_context.json",
                       "static_template", "result_"]
    return file_path.is_file() and file_name in test_file_names


def format_key_from_file_name(file_name):
    if "." in file_name:
        file_name = file_name[0:file_name.rfind('.')]
    return file_name


def build_test(test_case_path):
    test_case = {'case_identifier': test_case_path.name,
                 'test_case_path': str(test_case_path)}
    for file_path in test_case_path.iterdir():
        file_name = file_path.name
        if is_test_file(file_path, file_name):
            test_case[format_key_from_file_name(file_name)] = str(file_path)
        elif file_path.is_dir() and file_path.name == 'results':
            for fp in file_path.iterdir():
                if is_test_file(fp, fp.name[0:fp.name.rfind("_") + 1]):
                    if 'results' not in test_case:
                        test_case['results'] = []
                    test_case['results'].append(str(fp))
    return test_case


def run_integration_test(test_case_path):
    test_case = build_test(test_case_path)
    run_test(test_case)


def run_all_integration_tests():
    tests_data_path = get_path_from_config('integration_tests_data')
    for test_case_path in tests_data_path.iterdir():
        if test_case_path.is_dir():
            run_integration_test(test_case_path)
            print("__________________________________________________________")
