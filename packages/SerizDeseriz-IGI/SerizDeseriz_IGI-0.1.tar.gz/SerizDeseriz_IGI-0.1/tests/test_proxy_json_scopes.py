from .fixtures import serializer_json_proxy  # noqa: F401


def wrapper():
    a = 10

    def inner():
        return a + 1

    return inner


a = 5


def wrapper_2():
    a = 10

    def inner():
        global a
        return a + 1

    return inner


def test_nonlocal(serializer_json_proxy):
    res = serializer_json_proxy.dumps(wrapper())
    des = serializer_json_proxy.loads(res)

    assert des() == 11


def test_global(serializer_json_proxy):
    res = serializer_json_proxy.dumps(wrapper_2())
    des = serializer_json_proxy.loads(res)

    assert des() == 6
