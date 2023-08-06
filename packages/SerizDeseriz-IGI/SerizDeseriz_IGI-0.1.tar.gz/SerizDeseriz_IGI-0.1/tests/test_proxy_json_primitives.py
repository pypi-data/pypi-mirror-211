from .fixtures import serializer_json_proxy  # noqa: F401


def test_proxy_primitives(serializer_json_proxy):
    int_val = 123456567678789
    res = serializer_json_proxy.dumps(int_val)

    assert str(int_val) == res
    assert int_val == serializer_json_proxy.loads(res)


def test_proxy_float(serializer_json_proxy):
    float_val = 123234.3452345
    res = serializer_json_proxy.dumps(float_val)

    assert str(float_val) == res
    assert float_val == serializer_json_proxy.loads(res)


def test_proxy_none(serializer_json_proxy):
    res = serializer_json_proxy.dumps(None)

    assert "null" == res
    assert serializer_json_proxy.loads(res) is None


def test_proxy_str(serializer_json_proxy):
    string = "I love BSUIR"
    res = serializer_json_proxy.dumps(string)

    assert f'"{string}"' == res
    assert string == serializer_json_proxy.loads(res)


def test_proxy_true(serializer_json_proxy):
    res = serializer_json_proxy.dumps(True)

    assert "true" == res
    assert serializer_json_proxy.loads(res)


def test__proxy_false(serializer_json_proxy):
    res = serializer_json_proxy.dumps(False)

    assert "false" == res
    assert not serializer_json_proxy.loads(res)


def test_proxy_bytes(serializer_json_proxy):
    byte_var = b"hello world"
    res = serializer_json_proxy.dumps(byte_var)
    des = serializer_json_proxy.loads(res)

    assert des == byte_var
