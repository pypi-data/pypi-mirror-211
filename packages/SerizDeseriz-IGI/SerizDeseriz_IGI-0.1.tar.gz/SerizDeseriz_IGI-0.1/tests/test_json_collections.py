import pytest  # noqa: F401

from .fixtures import json_serializer  # noqa: F401


def test_list(json_serializer):
    lst = [1, 2, 3, 4, 5, 6]
    res = json_serializer.dumps(lst)

    assert "[1,2,3,4,5,6]" == res
    assert lst == json_serializer.loads(res)


def test_tuple(json_serializer):
    lst = (1, 2, 3, 4, 5, 6)
    res = json_serializer.dumps(lst)

    assert "[1,2,3,4,5,6]" == res
    assert list(lst) == json_serializer.loads(res)


def test_empty_collection(json_serializer):
    res = json_serializer.dumps([])

    assert "[]" == res
    assert [] == json_serializer.loads(res)


def test_cmplx_collection(json_serializer):
    lst = [1, 2, "hello", [1, 2, 3]]
    res = json_serializer.dumps(lst)

    assert '[1,2,"hello",[1,2,3]]' == res
    assert lst == json_serializer.loads(res)


def test_dict(json_serializer):
    dct = {"hello": "world"}
    res = json_serializer.dumps(dct)

    assert '{"hello": "world"}' == res
    assert dct == json_serializer.loads(res)


def test_cmplx_dict(json_serializer):
    dct = {"hello": "world", "dictionary": {"first": [1, 2, "hello"]}}
    res = json_serializer.dumps(dct)

    assert '{"hello": "world","dictionary": {"first": [1,2,"hello"]}}' == res
    assert dct == json_serializer.loads(res)
