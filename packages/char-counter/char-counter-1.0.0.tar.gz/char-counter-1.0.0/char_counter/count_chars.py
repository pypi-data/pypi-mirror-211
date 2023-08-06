from collections import Counter
from char_counter.input_validator import validate_input_type


class CharCounter:
    def __init__(self):
        self.cache = {}

    def count_chars(self, text) -> int:
        validate_input_type(text, str)

        if text in self.cache:
            return self.cache[text]

        counter = Counter(text)
        unique_chars_count = sum(map(lambda x: x == 1, counter.values()))
        self.cache[text] = unique_chars_count
        return unique_chars_count
