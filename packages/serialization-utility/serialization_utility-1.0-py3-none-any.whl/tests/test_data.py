import math

primitive_int: int = -12
primitive_float: float = 123.123
primitive_str: str = 'Hello:Andrey'
primitive_bool: bool = True
primitive_none = None

example_bytes_hex: str = '7c017c005f007c027c005f0164005300'
example_bytes = bytes.fromhex(example_bytes_hex)

example_list: list = [1, 2, 3, 4, 5]
example_dict: dict = {
    'id': 1234567890,
    'login': 'admin',
    'password': 'root'
}
example_tuple: tuple = 0, 9, 8, 7, 6

global_int: int = 42


def example_function(x: int):
    return math.sin(x * global_int / math.pi)


class TestSimpleClass:
    id: int = 0
    login: str = 'user'
    password: str = 'qwerty'
    is_admin: bool = False


class TestClass:
    complex_dict: dict = {
        'dict': {
            'types': [1, 1.0, True, None]
        },
        'tupel': (1, '1', None)
    }

    def __init__(self, data):
        self.data = data

    def inner_func(self, n: int):
        return [self.data]*n
