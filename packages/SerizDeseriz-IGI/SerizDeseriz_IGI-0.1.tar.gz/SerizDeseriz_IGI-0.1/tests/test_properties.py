import pytest

from .fixtures import serializer_xml_proxy  # noqa: F401


class _C:
    _value = 9

    @property
    def value(self):
        return self._value

    @value.setter
    def val_set(self, val):
        if val < 3:
            raise Exception()
        self._value = val


class ManyProps:
    _f_value = "Hello"
    _s_value = 12.2

    @property
    def value1(self):
        return self._f_value

    @value1.setter
    def value1_set(self, val):
        if val < 3:
            raise Exception()
        self._f_value = val

    @property
    def value2(self):
        return self._s_value

    @value2.setter
    def value2_set(self, val):
        if val < 3:
            raise Exception()
        self._s_value = val

    @value2.deleter
    def value2_del(self):
        self._s_value = "another string"


def test_simple_property(serializer_xml_proxy):
    serialized = serializer_xml_proxy.dumps(_C)
    deserialized = serializer_xml_proxy.loads(serialized)

    instance = deserialized()
    assert instance.value == _C().value
    instance.value = 5
    assert instance.value == 5
    with pytest.raises(
        Exception,
    ):
        instance.value = 1


def test_complex_property(serializer_xml_proxy):
    serialized = serializer_xml_proxy.dumps(ManyProps)
    deserialized = serializer_xml_proxy.loads(serialized)

    instance = deserialized()
    assert instance.value1 == ManyProps()._f_value
    instance.value1 = 5
    assert instance.value1 == 5
    del instance.value2
    assert instance._s_value == "another string"
