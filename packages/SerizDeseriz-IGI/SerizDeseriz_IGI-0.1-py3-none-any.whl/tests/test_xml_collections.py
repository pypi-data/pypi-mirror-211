from .fixtures import xml_serializer  # noqa: F401


def test_list(xml_serializer):
    lst = [1, 2, 3]
    res = xml_serializer.dumps(lst)

    assert "<list><int>1</int><int>2</int><int>3</int></list>" == res
    assert lst == xml_serializer.loads(res)


def test_tuple(xml_serializer):
    lst = (
        1,
        2,
        3,
    )
    res = xml_serializer.dumps(lst)

    assert "<list><int>1</int><int>2</int><int>3</int></list>" == res
    assert list(lst) == xml_serializer.loads(res)


def test_empty_collection(xml_serializer):
    res = xml_serializer.dumps([])

    assert "<list></list>" == res
    assert [] == xml_serializer.loads(res)


def test_cmplx_collection(xml_serializer):
    lst = [1, 2, "hello", [1, 2, 3]]
    res = xml_serializer.dumps(lst)

    assert (
        "<list><int>1</int><int>2</int><str>hello</str><list><int>1</int><int>2</int><int>3</int></list></list>" == res
    )
    assert lst == xml_serializer.loads(res)


def test_dict(xml_serializer):
    dct = {"hello": "world"}
    res = xml_serializer.dumps(dct)

    assert "<dict><hello><str>world</str></hello></dict>" == res
    assert dct == xml_serializer.loads(res)


def test_cmplx_dict(xml_serializer):
    dct = {"hello": "world", "dictionary": {"first": [1, 2, "hello"]}}
    res = xml_serializer.dumps(dct)

    assert (
        "<dict><hello><str>world</str></hello><dictionary><dict><first><list><int>1</int><int>2</int><str>"
        "hello</str></list></first></dict></dictionary></dict>"
    ) == res
    assert dct == xml_serializer.loads(res)
