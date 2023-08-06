import pytest
from char_counter import CharCounter, InvalidInputType


@pytest.fixture()
def char_counter():
    return CharCounter()


@pytest.mark.parametrize("text, expected_result", [
    ("hello", 3),
    ("world", 5),
    ("hello world", 6),
    ("", 0)
])
def test_count_unique_characters(char_counter, text, expected_result):
    assert char_counter.count_chars(text) == expected_result


@pytest.mark.parametrize("type_input", [
    123,
    3.14,
    True,
    [1, 2, 3],
    {"a": 1, "b": 2},
    None
])
def test_count_unique_characters_invalid_input(char_counter, type_input):
    with pytest.raises(InvalidInputType):
        char_counter.count_chars(type_input)


def test_count_unique_characters_with_cache_write(char_counter):
    text, expected_result = "hello world", 6

    assert char_counter.cache == {}

    result = char_counter.count_chars(text)
    assert result == expected_result

    assert char_counter.cache == {text: expected_result}


def test_count_unique_characters_with_cache_read(char_counter):
    text, expected_result = "hello world", 6

    assert char_counter.cache == {}

    char_counter.cache[text] = expected_result

    result_from_cache = char_counter.count_chars(text)
    assert result_from_cache == expected_result
