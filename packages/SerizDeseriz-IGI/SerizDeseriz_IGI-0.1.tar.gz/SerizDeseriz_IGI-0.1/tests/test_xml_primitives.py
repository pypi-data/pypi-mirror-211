from .fixtures import xml_serializer  # noqa: F401


def test_int(xml_serializer):
    int_val = 123456567678789
    res = xml_serializer.dumps(int_val)

    assert f"<int>{str(int_val)}</int>" == res
    assert int_val == xml_serializer.loads(res)


def test_float(xml_serializer):
    float_val = 123234.3452345
    res = xml_serializer.dumps(float_val)

    assert f"<float>{str(float_val)}</float>" == res
    assert float_val == xml_serializer.loads(res)


def test_none(xml_serializer):
    res = xml_serializer.dumps(None)

    assert "<none>None</none>" == res
    assert xml_serializer.loads(res) is None


def test_str(xml_serializer):
    string = "I love BSUIR"
    res = xml_serializer.dumps(string)

    assert f"<str>{string}</str>" == res
    assert string == xml_serializer.loads(res)


def test_true(xml_serializer):
    res = xml_serializer.dumps(True)

    assert "<bool>True</bool>" == res
    assert xml_serializer.loads(res)


def test_false(xml_serializer):
    res = xml_serializer.dumps(False)

    assert "<bool>False</bool>" == res
    assert not xml_serializer.loads(res)
