from .fixtures import serializer_json_proxy  # noqa: F401


class Point:
    first_coordinate: int
    second_coordinate: int

    def __init__(self, first_coordinate, second_coordinate):
        self.first_coordinate = first_coordinate
        self.second_coordinate = second_coordinate

    def vector(self):
        return self.first_coordinate**2 + self.second_coordinate**2


class MetricUnit:
    first_coordinate = 0
    second_coordinate = 0

    def calculate_metric(self):
        return self.first_coordinate + self.second_coordinate


class MultipleParentPoint(MetricUnit, Point):
    pass


class PolitePoint(Point):
    @staticmethod
    def greeting(name: str):
        return f"Hello, {name}"


class WideFunctionalityPoint(Point):
    @classmethod
    def init_attributes(cls):
        cls.first_coordinate = 0
        cls.second_coordinate = 0


def test_point_class(serializer_json_proxy):
    res = serializer_json_proxy.dumps(Point)  # class
    des = serializer_json_proxy.loads(res)
    a = des(1, 2)  # constructor

    assert a.vector() == Point(1, 2).vector()  # method


def test_mro(serializer_json_proxy):
    res = serializer_json_proxy.dumps(MultipleParentPoint)
    des = serializer_json_proxy.loads(res)
    # strings are absolutely identical, but tuples contain classes which can't be compared by == operator
    assert str(MultipleParentPoint.__mro__) == str(des.__mro__)
    assert des(1, 2).vector() == MultipleParentPoint(1, 2).vector()  # make sure everything works


def test_staticmethod(serializer_json_proxy):
    res = serializer_json_proxy.dumps(PolitePoint)
    des = serializer_json_proxy.loads(res)

    assert des.greeting("pavel") == PolitePoint.greeting("pavel")  # calling static methods


def test_classmethod(serializer_json_proxy):
    res = serializer_json_proxy.dumps(WideFunctionalityPoint)
    des = serializer_json_proxy.loads(res)

    des.init_attributes()  # class method that sets coordinates to 0
    assert des.first_coordinate == des.second_coordinate == 0
