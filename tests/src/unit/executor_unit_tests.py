import src.executor as ex
import json
from pathlib import Path
from unittest import TestCase


# TODO: The remaining functions need mock files to be tested.
class ExecutorUnitTest(TestCase):

    # def test_generate_file(self):

    # def test_import_compiled_template(self):

    def test_is_free_of_reserved_keywords(self):
        self.assertEqual(
            ex.is_free_of_reserved_keywords({"context": "", "abc": ""}), False)
        self.assertEqual(
            ex.is_free_of_reserved_keywords({"$file_name$": "", "abc": ""}),
            True)
        self.assertEqual(
            ex.is_free_of_reserved_keywords({"abc": {"context": ""}}), True)

    def test_is_valid_context(self):
        self.assertEqual(ex.is_valid_context({"abc": ""}), True)
        self.assertEqual(ex.is_valid_context(["abc"]), False)
        self.assertEqual(ex.is_valid_context({"context": ""}), False)

    # Todo: Load test data path from file.


    def test_load_data_contexts_from_file(self):
        file_path_1 = Path(
            '../data/executorunittests/context_1.json')
        file_1 = open(file_path_1, 'r')
        self.assertEqual(ex.load_data_contexts_from_file(file_path_1),
                         json.loads(file_1.read()))
        file_1.close()

    def test_get_data_contexts(self):
        file_path_1 = Path(
            '../data/executorunittests/context_1.json')
        file_1 = open(file_path_1, 'r')
        self.assertEqual(ex.get_data_contexts(file_path_1),
                         json.loads(file_1.read()))
        file_1.close()

        # If the json is not a json array
        # (and therefore a python list after loading and conversion)
        # this method should put the loaded json data into a list.
        file_path_2 = Path(
            '../data/executorunittests/context_2.json')
        file_2 = open(file_path_2, 'r')
        self.assertEqual(ex.get_data_contexts(file_path_2),
                         [json.loads(file_2.read())])
        file_2.close()

    # def test_execute_compiled_template():
