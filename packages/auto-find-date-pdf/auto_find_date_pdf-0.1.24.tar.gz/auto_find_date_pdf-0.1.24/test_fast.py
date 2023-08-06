import re

from text_search import replace_multiple_strings, init_replace, supported_images


def test_supported_images():
    assert supported_images('jlksjfd.JPG') == True
    assert supported_images('jlksjfd.BMP') == True


def test_replace_multiple_strings():
    # Test case 1: basic input
    input_string = "I like apples, bananas, and oranges"
    replacements_dict = {"apples": "pears", "bananas": "kiwis", "oranges": "plums"}
    expected_output = "I like pears, kiwis, and plums"
    init_replace(replacements_dict)
    assert replace_multiple_strings(input_string, replacements_dict) == expected_output

    # Test case 2: empty input string
    input_string = ""
    replacements_dict = {"foo": "bar", "baz": "qux"}
    expected_output = ""
    assert replace_multiple_strings(input_string, replacements_dict) == expected_output

    # Test case 3: empty replacements_dict
    input_string = "hello world"
    replacements_dict = {}
    expected_output = "hello world"
    assert replace_multiple_strings(input_string, replacements_dict) == expected_output

    # Test case 4: replace with empty string
    input_string = "hello world"
    replacements_dict = {"hello": "", "world": ""}
    expected_output = " "
    assert replace_multiple_strings(input_string, replacements_dict) == expected_output

    # Test case 5: replace with longer string
    input_string = "the cat in the hat"
    replacements_dict = {"cat": "big cat", "hat": "big hat"}
    expected_output = "the big cat in the big hat"
    assert replace_multiple_strings(input_string, replacements_dict) == expected_output

    # Test case 6: replace with special characters
    input_string = "hello world"
    replacements_dict = {"hello": "h€llø", "world": "wørld"}
    expected_output = "h€llø wørld"
    assert replace_multiple_strings(input_string, replacements_dict) == expected_output

    # Test case 7: case-sensitive replacement
    input_string = "Hello WORLD"
    replacements_dict = {"Hello": "Hi", "world": "Earth"}
    expected_output = "Hi WORLD"
    assert replace_multiple_strings(input_string, replacements_dict) == expected_output

    print("All test cases pass")
