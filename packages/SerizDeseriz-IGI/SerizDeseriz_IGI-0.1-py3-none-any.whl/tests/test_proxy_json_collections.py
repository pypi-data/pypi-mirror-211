from .fixtures import serializer_json_proxy  # noqa: F401


def test_list(serializer_json_proxy):
    lst = [1, 2, 3, 4, 5, 6]
    res = serializer_json_proxy.dumps(lst)

    assert "[1,2,3,4,5,6]" == res
    assert lst == serializer_json_proxy.loads(res)


def test_tuple(serializer_json_proxy):
    lst = (1, 2, 3, 4, 5, 6)
    res = serializer_json_proxy.dumps(lst)

    assert '{"__type": "tuple","data": [1,2,3,4,5,6]}' == res
    assert lst == serializer_json_proxy.loads(res)


def test_empty_collection(serializer_json_proxy):
    res = serializer_json_proxy.dumps([])

    assert "[]" == res
    assert [] == serializer_json_proxy.loads(res)


def test_set(serializer_json_proxy):
    st = {1, 2, "hello"}
    res = serializer_json_proxy.dumps(st)

    assert '{"__type": "set","data": [1,2,"hello"]}' == res
    assert st == serializer_json_proxy.loads(res)


def test_cmplx_collection(serializer_json_proxy):
    lst = [1, 2, "hello", [1, 2, 3]]
    res = serializer_json_proxy.dumps(lst)

    assert '[1,2,"hello",[1,2,3]]' == res
    assert lst == serializer_json_proxy.loads(res)


def test_dict(serializer_json_proxy):
    dct = {"hello": "world"}
    res = serializer_json_proxy.dumps(dct)

    assert '{"hello": "world"}' == res
    assert dct == serializer_json_proxy.loads(res)


def test_cmplx_dict(serializer_json_proxy):
    dct = {"hello": "world", "dictionary": {"first": [1, 2, "hello"]}}
    res = serializer_json_proxy.dumps(dct)

    assert '{"hello": "world","dictionary": {"first": [1,2,"hello"]}}' == res
    assert dct == serializer_json_proxy.loads(res)
