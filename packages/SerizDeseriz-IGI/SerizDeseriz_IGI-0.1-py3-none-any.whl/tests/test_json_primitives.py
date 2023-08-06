from .fixtures import json_serializer  # noqa: F401


def test_int(json_serializer):
    int_val = 123456567678789
    res = json_serializer.dumps(int_val)

    assert str(int_val) == res
    assert int_val == json_serializer.loads(res)


def test_float(json_serializer):
    float_val = 123234.3452345
    res = json_serializer.dumps(float_val)

    assert str(float_val) == res
    assert float_val == json_serializer.loads(res)


def test_none(json_serializer):
    res = json_serializer.dumps(None)

    assert "null" == res
    assert json_serializer.loads(res) is None


def test_str(json_serializer):
    string = "I love BSUIR"
    res = json_serializer.dumps(string)

    assert f'"{string}"' == res
    assert string == json_serializer.loads(res)


def test_true(json_serializer):
    res = json_serializer.dumps(True)

    assert "true" == res
    assert json_serializer.loads(res)


def test_false(json_serializer):
    res = json_serializer.dumps(False)

    assert "false" == res
    assert not json_serializer.loads(res)
