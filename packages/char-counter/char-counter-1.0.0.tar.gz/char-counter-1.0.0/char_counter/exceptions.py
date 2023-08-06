class InvalidInputType(Exception):
    """
    Raised when an input is of the wrong type.
    """

    def __init__(self, expected_type, actual_type):
        super().__init__(f"Invalid input type. Expected {expected_type}, but got {actual_type}.")
        self.expected_type = expected_type
        self.actual_type = actual_type
