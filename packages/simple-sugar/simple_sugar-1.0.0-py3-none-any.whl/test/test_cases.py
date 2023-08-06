import unittest
from os.path import exists

from simple_sugar.simple_sugar import *
from unittest.mock import *


class TestSimpleSugarDictionary(unittest.TestCase):
    def test_creation(self):
        test_dict = dictionary()
        self.assertTrue(isinstance(test_dict, dict))

    def test_set_and_get(self):
        test_dict = dictionary()
        test_dict.test_key = "test value"

        self.assertEqual("test_key", test_dict.get_keys()[0])
        self.assertEqual("test value", test_dict.get_values()[0])

    def test_remove(self):
        test_dict = dictionary()
        test_dict.test_key = "test value"
        empty_dict = {}

        test_dict.remove()
        self.assertDictEqual(test_dict, empty_dict)

    def test_empty_dictionary_print(self):
        test_dict = dictionary()

        self.assertEqual("Dictionary is empty.", test_dict.__str__())

    def test_update(self):
        test_dict = dictionary()
        test_dict.test_key = "test value"

        test_dict.update(True)

        self.assertEqual(test_dict.test_key, True)

    def test_dictionary_can_use_core_methods(self):
        test_dict = dictionary()
        test_dict.test_key = "test value"

        copied_dict = test_dict.copy()

        self.assertEqual(copied_dict, test_dict)


class TestSimpleSugarPrinter(unittest.TestCase):
    def test_no_argument_error(self):
        try:
            printer()
        except ValueError:
            pass

    @patch('builtins.print')
    def test_print_string(self, test_print):
        test_string = "test string"

        printer(test_string)
        test_print.assert_called_with('test string')

    @patch('builtins.print')
    def test_print_list(self, test_print):
        test_list = ['test', 'list']

        printer(test_list)
        test_print.assert_called_with(test_list)

    @patch('builtins.print')
    def test_print_dictionary(self, test_print):
        test_dict = {"first_key": "first_value",
                     "second_key": "second_value"}

        printer(test_dict)
        test_print.assert_called_with(test_dict)

    def test_illegal_upper_list_bound(self):
        test_list = [1, 2, 3, 4, 5]

        try:
            printer(test_list, to_index=6)
        except IndexError:
            pass

    def test_illegal_lower_bound(self):
        test_list = [1, 2, 3, 4, 5]

        try:
            printer(test_list, from_index=-1)
        except IndexError:
            pass

    @patch('builtins.print')
    def test_lower_bound(self, test_print):
        test_list = [1, 2, 3, 4, 5]

        printer(test_list, from_index=3)

        test_print.assert_called_with([3, 4, 5])

    @patch('builtins.print')
    def test_upper_bound(self, test_print):
        test_list = [1, 2, 3, 4, 5]

        printer(test_list, to_index=3)

        test_print.assert_called_with([1, 2, 3])

    @patch('builtins.print')
    def test_print_list_no_bounds(self, test_print):
        test_list = [1, 2, 3, 4, 5]

        printer(test_list)

        test_print.assert_called_with(test_list)


class TestSimpleSugarMathematicalOperations(unittest.TestCase):
    def test_average(self):
        av = average(1, 3)

        self.assertEqual(2, av)

    def test_average_of_list(self):
        test_list = [1, 2, 3, 4]

        av = average(test_list)

        self.assertEqual(2.5, av)

    def test_average_throws_error(self):
        test_list = [1, 2, 3, 4]

        try:
            av = average(test_list, 4)
        except ValueError:
            pass

    def test_average_no_second_input(self):
        av = average(4)

        self.assertEqual(4, av)

    def test_prime(self):
        value = 7

        self.assertTrue(prime(value))

    def test_not_prime(self):
        value = 12

        self.assertFalse(prime(value))

    def test_odd_and_even(self):
        self.assertTrue(even(2))
        self.assertFalse(even(7))
        self.assertTrue(odd(3))
        self.assertFalse(odd(2))

    def test_get_random_no_arguments(self):
        self.assertTrue(0.0 <= get_random() <= 1.0)

    def test_get_random_with_lower_bound(self):
        self.assertTrue(get_random(from_n=5) >= 5)

    def test_get_random_with_upper_bound(self):
        self.assertTrue(get_random(to_n=10) <= 10)

    def test_get_random_with_limits(self):
        self.assertTrue(10 <= get_random(10, 20) <= 20)


class TestSimpleSugarFileOperations(unittest.TestCase):
    def test_get_file_as_string(self):
        file = get_file('unit_test_file.txt', split=False)
        test_string = "Test line 1,\nTest line 2."

        self.assertEqual(file, test_string)

    def test_get_file_as_list(self):
        file = get_file('unit_test_file.txt')
        test_list = ["Test line 1,", "Test line 2."]

        self.assertEqual(file, test_list)

    def test_get_file_with_whitespace(self):
        file = get_file('unit_test_file.txt', whitespace=True)
        test_list = ["Test line 1,\n", "Test line 2."]

        self.assertEqual(file, test_list)

    def test_get_file_without_punctuation(self):
        file = get_file('unit_test_file.txt', punctuation=False)
        test_list = ["Test line 1", "Test line 2"]

        self.assertEqual(file, test_list)

    def test_get_file_without_punctuation_as_string(self):
        file = get_file('unit_test_file.txt', punctuation=False, split=False)
        test_string = "Test line 1\nTest line 2"

        self.assertEqual(file, test_string)

    def test_writing_to_file(self):
        text = ["Test text."]
        path = "test_write_file.txt"

        to_file(path, text)

        self.assertTrue(exists(path))

        test_file = open(path)
        self.assertEqual(text, test_file.readlines())

    def test_writing_dict_to_file(self):
        text_dict = {"test_key": "test_value"}
        path = "test_dict_write_file.txt"

        to_file(path, text_dict)

        self.assertTrue(exists(path))

        test_file = open(path)
        self.assertEqual(["test_key:test_value\n"], test_file.readlines())


if __name__ == '__main__':
    unittest.main()
