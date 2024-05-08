def add_two_numbers(number_one: float, number_two: float) -> float:
    # return a + b
    try:
        return number_one + number_two
    except TypeError:
        raise TypeError("Both number_one and and number_two should be numbers")


def throw_error_function():
    raise ValueError("This is a value error")
