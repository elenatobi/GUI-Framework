from abc import ABC, abstractmethod

CONST_COLORS = {
    "BLACK"      : (  0,   0,   0),
    "WHITE"      : (255, 255, 255),
    "RED"        : (255,   0,   0),
    "LIME"       : (  0, 255,   0),
    "BLUE"       : (  0,   0, 255),
    "YELLOW"     : (255, 255,   0),
    "CYAN"       : (  0, 255, 255),
    "MAGNETA"    : (255,   0, 255),
    "SILVER"     : (192, 192, 192),
    "GRAY"       : (128, 128, 128),
    "MARRON"     : (128,   0,   0),
    "OLIVE"      : (128, 128,   0),
    "GREEN"      : (  0, 128,   0),
    "PURPLE"     : (128,   0, 128),
    "TEAL"       : (  0, 128, 128),
    "NAVY"       : (  0,   0, 128),
    "TRANSPARENT": ( -1,  -1,  -1)
}

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

class DimentionValueBase(ABC):
    def __init__(self, value):
        self.value = value

    def __add__(self, other):
        if type(other) == type(self):
            return type(self)(self.value + other.value)
        raise TypeError(f"{type(self).__name__} cannot add with {type(other).__name__}")
    
    def __sub__(self, other):
        if type(other) == type(self):
            return type(self)(self.value - other.value)
        raise TypeError(f"{type(self).__name__} cannot sub with {type(other).__name__}")

    @abstractmethod
    def pixelfy(self, other):
        return ""

    @abstractmethod
    def __repr__(self):
        return ""

class Pixel(DimentionValueBase):
    def pixelfy(self, other):
        if type(other) == Pixel:
            return self + other if self.value < 0 else self
        raise TypeError(f".pixelfy parameter must be Pixel")

    def __repr__(self):
        return f"{self.value}px"

class Percentage(DimentionValueBase):
    def pixelfy(self, other):
        if type(other) == Pixel:
            offset = Pixel(self.value / 100 * other.value)
            return other + offset if self.value < 0 else offset
        raise TypeError(f".pixelfy parameter must be Pixel")

    def __repr__(self):
        return f"{self.value}%"

class DimentionRect:
    def __init__(self, x, y, width, height):
        self.x      = Converter.convert(x)
        self.y      = Converter.convert(y)
        self.width  = Converter.convert(width)
        self.height = Converter.convert(height)

    def __add__(self, other):
        if type(other) == DimentionRect:
            return DimentionRect(self.x + other.x.pixelfy(self.width),
                                 self.y + other.y.pixelfy(self.height),
                                 other.width.pixelfy(self.width),
                                 other.height.pixelfy(self.height))
        if type(other) == DimentionLine:
            new_points = []
            for (x, y) in other.points:
                new_points.append((self.x + x.pixelfy(self.width), self.y + y.pixelfy(self.height)))
            return DimentionLine(new_points)
        raise TypeError(f"DimentionRect cannot add {type(other).__name__}")

    def block_width(self, other):
        return self.x.pixelfy(other.width) + self.width.pixelfy(other.width)

    def __repr__(self):
        return f"DimentionRect({self.x}, {self.y}, {self.width}, {self.height})"

    def to_list(self):
        return [self.x.value, self.y.value, self.width.value, self.height.value]

class DimentionLine:
    def __init__(self, points):
        self.points = []
        self.multiple_append(points)

    def check_points(points):
        if not type(points) in [list, tuple]:
            raise TypeError(f"Expected points type list or tuple, but got {type(points).__name__}")
        for pair in points:
            if not type(pair) in [list, tuple]:
                raise TypeError(f"Expected points pair type list or tuple, but got {type(points).__name__}")
            if len(pair) != 2:
                raise TypeError(f"Expected points pair length 2, but got {len(pair)}")
        return True

    def append(self, x, y):
        self.points.append((Converter.convert(x), Converter.convert(y)))

    def multiple_append(self, points):
        DimentionLine.check_points(points)
        for (x, y) in points:
            self.append(x, y)

    def __repr__(self):
        return f"DimentionLine{self.points}"

    def to_list(self):
        result = []
        for (x, y) in self.points:
            result.append((x.value, y.value))
        return result

class Color:
    def __init__(self, color_keyword):
        self.color = Color.get_color(color_keyword)

    def get_color(color_keyword):
        if color_keyword.upper() in CONST_COLORS.keys():
            return CONST_COLORS[color_keyword.upper()]
        raise Exception(f"Invalid color keyword {color_keyword}")

    def to_tuple(self):
        return self.color

    def __repr__(self):
        return f"Color {self.color}"

print(DimentionRect("2%", 3, "-40%", 2).block_width(DimentionRect(10, 15, 140, 200)))
