from .fixtures import serializer_json_proxy  # noqa: F401
from .test_proxy_json_classes import Point


def test_object(serializer_json_proxy):
    res = serializer_json_proxy.dumps(Point(1, 2))
    des = serializer_json_proxy.loads(res)
    assert des.vector() == 5


def test_dynamic_attribute(serializer_json_proxy):
    obj = Point(1, 2)
    obj.first = 1
    res = serializer_json_proxy.dumps(obj)
    des = serializer_json_proxy.loads(res)

    assert des.first == obj.first
