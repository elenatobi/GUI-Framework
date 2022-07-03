from abc import ABC, abstractmethod

TYPE_ERROR_MESSAGE = "Expected type {}, but got {}"

class DimentionBase(ABC):
    @abstractmethod
    def __init__(self):
        pass

    @abstractmethod
    def explicit(self, other):
        pass

    @abstractmethod
    def __repr__(self, other):
        pass

class DimentionValueBase(DimentionBase):
    def __init__(self, value):
        self.value = value

    def __add__(self, other):
        Types.check(other, type(self))
        return type(self)(self.value + other.value)

    def __sub__(self, other):
        Types.check(other, type(self))
        return type(self)(self.value - other.value)

class Pixel(DimentionValueBase):
    def explicit(self, other):
        Types.check(other, Pixel)
        return other + self if self.value < 0 else self

    def __repr__(self):
        return f"{self.value}px"

class Percentage(DimentionValueBase):
    def explicit(self, other):
        Types.check(other, Pixel)
        delta_length = Pixel(self.value / 100 * other.value)
        return other + delta_length if self.value < 0 else delta_length

    def __repr__(self):
        return f"{self.value}%"

class Vector(DimentionBase):
    def __init__(self, x, y):
        self.x = Converter.convert(x)
        self.y = Converter.convert(y)

    def __add__(self, other):
        Types.check(other, Vector)
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        Types.check(other, Vector)
        return Vector(self.x - other.x, self.y - other.y)

    def explicit(self, other):
        Types.check(other, Vector)
        return Vector(self.x.explicit(other.x), self.y.explicit(other.y))

    def __repr__(self):
        return f"Vector({self.x}, {self.y})"

class RectDimention(DimentionBase):
    def __init__(self, x, y, width, height):
        self.position = Vector(x, y)
        self.size = Vector(width, height)

    def explicit(self, other):
        Types.check(other, RectDimention)
        new_position = self.position.explicit(other.size) + other.position
        new_size = self.size.explicit(other.size)
        return RectDimention(new_position.x, new_position.y, new_size.x, new_size.y)

    def block_width(self, other):
        Types.check(other, RectDimention)
        return self.position.x.explicit(other.size.x) + self.size.x.explicit(other.size.x)

    def block_height(self, other):
        Types.check(other, RectDimention)
        return self.position.y.explicit(other.size.y) + self.size.y.explicit(other.size.y)

    def __repr__(self):
        return f"RectDimention({self.position.x}, {self.position.y}, {self.size.x}, {self.size.y})"

class Converter:
    def is_number(value):
        result = value.count(".") == 0 or value.count(".") == 1
        if value[0] == "-":
            value = value[1:]
        for char in value:
            result = result and char in "0123456789."
        return result

    def convert(value):
        if type(value) in [Pixel, Percentage]:
            return value
        if type(value) in [int, float]:
            return Pixel(value)
        if type(value) != str:
            raise TypeError(f"Expected type Pixel, Percentage, int, float, str, but got {type(value)}")
        if Converter.is_number(value):
            return Pixel(float(value))
        if value[-2:] == "px" and Converter.is_number(value[:-2]):
            return Pixel(float(value[:-2]))
        if value[-1:] == "%" and Converter.is_number(value[:-1]):
            return Percentage(float(value[:-1]))
        raise Exception("Wrong string format")

class Types:
    def check(value, expected_type):
        if type(value) != expected_type:
            raise TypeError(TYPE_ERROR_MESSAGE.format(expected_type.__name__, type(value).__name__))

print(RectDimention("-2%", "3%", 20, "17%").block_height(RectDimention(3, 2, 76, 87)))