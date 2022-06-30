class ConsoleDraw:
    def __init__(self, widget):
        self.widget = widget

    def draw(self):
        self.widget.draw(self)

    def drawWidgetBase(self, positions, color, border_width):
        print("WidgetBase", positions.position.x.value, positions.position.y.value, color, border_width)

class ValueBase:
    def __init__(self):
        pass

    def check_type(self, other):
        if type(other) != type(self):
            raise TypeError(f"The type must be {type(self).__name__}, not {type(other).__name__}")

    def check_explicit_other(other):
        pass

    def explicit(self, other):
        pass

    def __add__(self, other):
        pass

    def __sub__(self, other):
        pass

    def __repr__(self):
        pass

class ScalarBase(ValueBase):
    def __init__(self, value):
        self.value = value

    def check_explicit_other(other):
        if type(other) != Pixel:
            raise TypeError(f"The type must be Pixel, not {type(other).__name__}")

    def __add__(self, other):
        self.check_type(other)
        return type(self)(self.value + other.value)

    def __sub__(self, other):
        self.check_type(other)
        return type(self)(self.value - other.value)

    def __repr__(self):
        return f"{type(self).__name__}({self.value})"

class Pixel(ScalarBase):
    def explicit(self, other):
        type(self).check_explicit_other(other)
        if self.value < 0:
            return other + self
        return self

class Percentage(Pixel):
    def explicit(self, other):
        type(self).check_explicit_other(other)
        pixel_length = Pixel(self.value / 100 * other.value)
        if self.value < 0:
            return other + pixel_length
        return pixel_length

class Vector(ValueBase):
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def check_explicit_other(other):
        if type(other) != Vector:
            raise TypeError(f"The type must be Vector, not {type(other).__name__}")
        Pixel.check_explicit_other(other.x)
        Pixel.check_explicit_other(other.y)

    def explicit(self, other):
        type(self).check_explicit_other(other)
        return Vector(self.x.explicit(other.x), self.y.explicit(other.y))

    def __add__(self, other):
        self.check_type(other)
        return type(self)(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        self.check_type(other)
        return type(self)(self.x - other.x, self.y - other.y)

    def __repr__(self):
        return f"{type(self).__name__}({self.x}, {self.y})"

class Base(ValueBase):
    def __init__(self, position, size):
        self.position = position
        self.size = size

    def check_explicit_other(other):
        if type(other) != Base:
            raise TypeError(f"The type must be Base, not {type(other).__name__}")
        Vector.check_explicit_other(other.position)
        Vector.check_explicit_other(other.size)

    def explicit(self, other):
        type(self).check_explicit_other(other)
        return Base(self.position.explicit(other.size) + other.position, self.size.explicit(other.size))

    def __repr__(self):
        return f"{type(self).__name__}({self.position}, {self.size})"

class Positions(ValueBase):
    def __init__(self, positions):
        self.positions = positions

    def check_explicit_other(other):
        if type(other) != Base:
            raise TypeError(f"The type must be Base, not {type(other).__name__}")
        Vector.check_explicit_other(other.position)
        Vector.check_explicit_other(other.size)

    def explicit(self, other):
        type(self).check_explicit_other(other)
        new_positions = []
        for position in self.positions:
            new_positions.append(position.explicit(other.size) + other.position)
        return Positions(new_positions)

    def __repr__(self):
        return f"{type(self).__name__}({self.positions})"

def string_is_number(value):
    result = len(value) != 0 and (value.count(".") == 0 or value.count(".") == 1)
    if value[0] == "-":
        value = value[1:]
    for char in value:
        result = result and char in "0123456789."
    return result

def convert(value):
    if type(value) in [Pixel, Percentage]:
        return value
    if type(value) == int or type(value) == float:
        return Pixel(value)
    if type(value) != str:
        raise TypeError(f"Invalid value type, expected Pixel, Percentage, int, str but got {type(value)}")
    if string_is_number(value):
        return Pixel(float(value))
    if value[-2:] == "px" and string_is_number(value[:-2]):
        return Pixel(float(value[:-2]))
    if value[-1:] == "%" and string_is_number(value[:-1]):
        return Percentage(float(value[:-1]))
    raise TypeError("Wrong string format")


VALUE_ZERO = Pixel(0)
VECTOR_ZERO = Vector(VALUE_ZERO, VALUE_ZERO)
BASE_ZERO = Base(VECTOR_ZERO, VECTOR_ZERO)

class WidgetBase:
    def __init__(self, x, y, color, border_width = 0):
        self.position = Vector(convert(x), convert(y))
        self.color = color
        self.border_width = border_width

    def explicit(self, base):
        return Base(self.position, VECTOR_ZERO).explicit(base)

    def get_block_width(self):
        pass

    def get_block_height(self):
        pass

    def draw(self, draw_obj, base = BASE_ZERO):
        getattr(draw_obj, "draw" + type(self).__name__)(self.explicit(base), self.color, self.border_width)

w = WidgetBase("2%", "-5%", "green")
d = ConsoleDraw(w)
#ex = w.explicit(Base(Vector(Pixel(12), Pixel(23)), Vector(Pixel(71), Pixel(63))))
w.draw(d, Base(Vector(Pixel(12), Pixel(23)), Vector(Pixel(71), Pixel(63))))