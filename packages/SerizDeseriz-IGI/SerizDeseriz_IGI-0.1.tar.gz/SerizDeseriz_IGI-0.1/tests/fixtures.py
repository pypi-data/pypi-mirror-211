import pytest
from SerizDeseriz_IGI import SerializerFactory
from SerizDeseriz_IGI.built_in_serializers import (JSONSerializer,
                                                   XMLSerializer)


@pytest.fixture
def serializer_json_proxy():
    return SerializerFactory.create_serializer("JSON")


@pytest.fixture
def serializer_xml_proxy():
    return SerializerFactory.create_serializer("XML")


@pytest.fixture
def json_serializer():
    return JSONSerializer()


@pytest.fixture
def xml_serializer():
    return XMLSerializer()
