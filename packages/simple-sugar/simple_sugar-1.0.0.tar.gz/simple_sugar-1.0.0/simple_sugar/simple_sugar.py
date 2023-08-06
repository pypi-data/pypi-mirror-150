import json
import math
import random
import re


class dictionary(dict):
    """
    This class controls the syntactic sugar for the dictionary by overriding the dict class

    Example: d = dictionary()
             d.first = "Hello"
             d.second = "World!

    """

    def __getattr__(self, key):
        """
        Returns the value of the item at the key
        :param key: The key for which value to find
        :return: The value with the key
        """
        return dict.__getitem__(self, key)

    def __setattr__(self, key, value):
        """
        Sets the value of the dictionary with a key and value
        :param key: The new key
        :param value: The new value
        :return: The new key/value pair
        """
        return dict.__setitem__(self, key, value)

    def get_keys(self):
        """
        Loops through all of the keys in the dictionary.
        :return: A new list of dictionary keys
        """
        keys = []

        for key in self:
            keys.append(key)

        return keys

    def get_values(self):
        """
        Loops through all of the values and returns as a list
        :return: A new list of dictionary values
        """
        values = []

        for key in self:
            values.append(self[key])

        return values

    def remove(self, key=None):
        """
        Sugar for removing an item from the dictionary, or clearing the entire dictionary
        :param key: Optional key if removing only one pair
        :return:
        """
        if key is None:
            self.clear()
        else:
            self.pop(key)

    def __str__(self):
        """
        Override string to support empty dictionaries
        :return:
        """
        if not self:
            return "Dictionary is empty."
        else:
            dict_str = ""
            for item in self.items():
                dict_str += item.__str__()

            return dict_str

    def update(self, value, keys=None):
        """
        Sets the value of all keys given to the value, removing the need
        for the user writing a loop
        :param value: The value to update the keys to
        :param keys: Optional keys to update
        :return:
        """
        if keys is None:
            for key in self:
                self[key] = value
        else:
            for key in keys:
                self[key] = value


def raise_invalid_index_error(index):
    """
    Raises an invalid index error
    :param index: The index that is invalid
    :return:
    """
    error_string = "Index {0} is out of range. Please provide valid indexes only.".format(index)
    raise IndexError(error_string)


def raise_size_of_list_error(index, list_size):
    """
    Raises an invalid index error if the index exceeds size of list
    :param index: The index that is invalid
    :param list_size: The target list size
    :return:
    """
    error_string = "Index {0} is out of range. Size of list is {1}".format(index, list_size)
    raise IndexError(error_string)


def printer(item=None, from_index=None, to_index=None):
    """
    Sugar for printing values, lists and dictionaries for a more user friendly output
    :param item: The item to print to the console
    :param from_index: If the item is a list, the index to print from
    :param to_index: If the item is a list, the index to print to
    :return:
    """
    if item is None:
        raise ValueError("Argument 'item' not provided. Please provide a value to print")
    else:
        if isinstance(item, list):
            to_print = []

            # List index error handling
            if from_index is not None or to_index is not None:
                if from_index is not None:
                    if from_index < 1:
                        raise_invalid_index_error(from_index)
                    else:
                        from_index = from_index - 1
                if to_index is not None:
                    if to_index > len(item):
                        raise_size_of_list_error(to_index, len(item))

            if from_index is not None and to_index is not None:
                to_print = item[from_index:to_index]

            elif from_index is not None and to_index is None:
                to_print = item[from_index:]

            elif from_index is None and to_index is not None:
                to_print = item[:to_index]
            else:
                to_print = item

            print(to_print)
        else:
            print(item)


def get_random(from_n=None, to_n=None):
    """
    Gets a random number, optionally including from and to numbers
    :param from_n: The lowest the number can be
    :param to_n: The highest the number can be
    :return: The random number
    """
    if from_n is None and to_n is None:
        return random.random()
    if from_n is None:
        return math.floor(random.randrange(0, to_n))
    if to_n is None:
        return math.floor(random.randrange(from_n, 100))

    if from_n > to_n:
        error_string = "Lower limit is larger than Upper Limit. Ensure the first value is smaller than the second " \
                       "value. "
        raise ValueError(error_string)

    return math.floor(random.randrange(from_n, to_n))


def even(val):
    """
    Returns if a value is even
    :param val: The value to test
    :return: True if even, False if not
    """
    if not (isinstance(val, int) or isinstance(val, float)):
        raise ValueError("Input value must be a number")

    return val % 2 == 0


def odd(val):
    """
    Returns if a value is odd
    :param val: The value to test
    :return: True if odd, False if not
    """
    if not (isinstance(val, int) or isinstance(val, float)):
        raise ValueError("Input value must be a number")

    return not val % 2 == 0


def average(first, second=None):
    """
    Finds the average of two numbers, or a list
    :param first: The input, either a number or a list
    :param second: The second input, optional in case finding the average of a list
    :return: The average value
    """

    if isinstance(first, list):
        if second is not None:
            raise ValueError("Do not provide a second argument if evaluating a list")
        else:
            total = 0
            for item in first:
                total += item

            return total / len(first)

    if second is None:
        return first
    else:
        return (first + second) / 2


def prime(value):
    """
    Finds if a number is prime or not
    :param value: The value to see if it is prime or not
    :return: True if prime, False if not prime
    """
    prime_flag = True

    if value > 1:
        for x in range(2, value):
            if value % x == 0:
                prime_flag = False
                break

        return prime_flag
    else:
        return not prime_flag


def get_file(filepath, split=True, whitespace=False, punctuation=True):
    """
    Reads a file and returns as a list
    :param split:
    :param punctuation:
    :param filepath: The path of the file to read
    :param whitespace: Optional parameter if whitespace characters are to be counted, False by default
    :return: A list containing each line of the file
    """
    formatted_file = ""
    with open(filepath) as file:
        # Handle if whitespace characters should be included
        if not whitespace:
            formatted_file = [line.rstrip() for line in file]
        else:
            formatted_file = file.readlines()

        # Handle punctuation being removed
        if not punctuation:
            formatted_file = [re.sub(r'[^\w\s]', '', formatted_line) for formatted_line in formatted_file]

        # Handle if the file should be split by line
        if not split:
            formatted_file = '\n'.join(formatted_file)

        return formatted_file


def to_file(filepath, data, append=False):
    """
    Writes a string, list or dictionary to a file, optionally appending to an existing file
    :param filepath: The path of the file to write to
    :param text: The text to write to the file
    :param append: Optional flag for appending to existing file
    :return:
    """
    if append:
        write_method = 'a'
    else:
        write_method = 'w'

    with open(filepath, write_method) as file:
        if write_method == 'a':
            file.write('\n')

        if isinstance(data, list):
            file.writelines(data)
        elif isinstance(data, dict):
            for key, value in data.items():
                file.write("{0}:{1}\n".format(key, value))
        else:
            file.write(data)
