from char_counter.exceptions import InvalidInputType


def validate_input_type(text, expected_type) -> None:
    if not isinstance(text, expected_type):
        input_type = type(text).__name__
        raise InvalidInputType(expected_type=expected_type.__name__, actual_type=input_type)
