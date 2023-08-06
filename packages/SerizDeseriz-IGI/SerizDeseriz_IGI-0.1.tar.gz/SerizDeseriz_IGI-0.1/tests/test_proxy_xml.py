"""
the work of 'pre_serializer' tool was confirmed in test_proxy_json testing modules,
so this one is created to prove pre_serializer compatibility with xml_serializer
"""
from .fixtures import serializer_xml_proxy  # noqa: F401
from .test_proxy_json_functions import generator, simple_function


def test_generator(serializer_xml_proxy):
    res = serializer_xml_proxy.dumps(generator())
    des = serializer_xml_proxy.loads(res)

    assert next(des) == next(generator())


def test_simple_function(serializer_xml_proxy):
    res = serializer_xml_proxy.dumps(simple_function)
    des = serializer_xml_proxy.loads(res)

    assert simple_function(1, 2) == des(1, 2)
