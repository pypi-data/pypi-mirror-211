from .fixtures import serializer_json_proxy  # noqa: F401


def simple_function(a: int, b: int = 5):
    return (a + b) * a


def wrapper(func):
    def inner(*args, **kwargs):
        print("Done")
        return func(*args, **kwargs)

    return inner


def generator(_range: int = 5):
    for i in range(_range):
        yield i


def recursive_function(n: int):
    if n == 0 or n == 1:
        return n
    return n + recursive_function(n - 1) + recursive_function(n - 2)


class Iterator:
    lst = [1, 2, 3, 4, "Hello"]
    iterator = iter(lst)

    def __iter__(self):
        return self

    def __next__(self):
        return next(self.iterator)


def wrapper_for_closure(a: int = 5, c: float = 2.1):
    local_scope_variable = a + c

    def closure(b: int):
        return local_scope_variable + b

    return closure


import re  # noqa: E402


def func_that_uses_external_package(s: str = "Hello World"):
    word_count = re.split(r" ", s)
    return word_count


def test_simple_function(serializer_json_proxy):
    res = serializer_json_proxy.dumps(simple_function)
    des = serializer_json_proxy.loads(res)
    assert des(1, 2) == simple_function(1, 2)


def test_wrapper(serializer_json_proxy):
    res = serializer_json_proxy.dumps(wrapper)
    des = serializer_json_proxy.loads(res)
    assert des(simple_function)(1, 2) == simple_function(1, 2)


def test_generator(serializer_json_proxy):
    res = serializer_json_proxy.dumps(generator())
    des = serializer_json_proxy.loads(res)
    assert next(des) == next(generator())


def test_iterator(serializer_json_proxy):
    res = serializer_json_proxy.dumps(iter(Iterator()))
    des = serializer_json_proxy.loads(res)

    assert next(des) == Iterator().lst[0]


def test_recursive_function(serializer_json_proxy):
    res = serializer_json_proxy.dumps(recursive_function)
    des = serializer_json_proxy.loads(res)
    assert des(3) == recursive_function(3)


def test_lambda_function(serializer_json_proxy):
    res = serializer_json_proxy.dumps(lambda m: m.lower())
    des = serializer_json_proxy.loads(res)
    assert des("I LOVE BSUIR") == "i love bsuir"


def test_closure_function(serializer_json_proxy):
    res = serializer_json_proxy.dumps(wrapper_for_closure(5))
    des = serializer_json_proxy.loads(res)
    assert wrapper_for_closure(5)(2) == des(2)


def test_func_with_package(serializer_json_proxy):
    res = serializer_json_proxy.dumps(func_that_uses_external_package)
    des = serializer_json_proxy.loads(res)

    assert func_that_uses_external_package() == des()
