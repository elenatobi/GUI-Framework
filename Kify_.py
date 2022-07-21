CONST_FLOAT_LEFT = "left"
CONST_FLOAT_RIGHT = "right"

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

class Dimention:
    def __init__(self, value, float_pos = CONST_FLOAT_LEFT):
        if not float_pos in [CONST_FLOAT_LEFT, CONST_FLOAT_RIGHT]:
            raise Exception("Wrong float pos")
        self.value = value
        self.float_pos = float_pos

class Pixel(Dimention):
    def explicit(self, other):
        if self.float_pos == CONST_FLOAT_LEFT:
            return self.value
        elif self.float_pos == CONST_FLOAT_RIGHT:
            return other - self.value

    def __repr__(self):
        return f"{self.float_pos} {self.value}px"

class Percentage(Dimention):
    def explicit(self, other):
        if self.float_pos == CONST_FLOAT_LEFT:
            return self.value / 100 * other
        elif self.float_pos == CONST_FLOAT_RIGHT:
            return other - other * self.value / 100

    def __repr__(self):
        return f"{self.float_pos} {self.value}%"

class Convert:
    def convert(value, float_pos = CONST_FLOAT_LEFT):
        if type(value) in [int, float]:
            return Pixel(value, float_pos)
        elif value[-1] == "%":
            return Percentage(float(value[:-1]), float_pos)
        return Pixel(float(value), float_pos)

    def convert_float(value):
        if type(value) in [int, float]:
            return Pixel(value)
        value = value.split(" ")
        if len(value) == 1:
            return Convert.convert(value[0])
        else:
            return Convert.convert(value[1], value[0])

class RectPosition:
    def __init__(self, x, y, width, height):
        self.x = Convert.convert_float(x)
        self.y = Convert.convert_float(y)
        self.width = Convert.convert_float(width)
        self.height = Convert.convert_float(height)

    def explicit(self, translation = [0, 0, 0, 0]):
        return [self.x.explicit(translation[2]) + translation[0],
                self.y.explicit(translation[3]) + translation[1],
                self.width.explicit(translation[2]),
                self.height.explicit(translation[3])]

    def __repr__(self):
        return f"RectPos({self.x}, {self.y}, {self.width}, {self.height})"

class PointPosition:
    def __init__(self, points):
        self.points = []
        for point in points:
            self.points.append(Convert.convert_float(point))

    def explicit(self, translation = [0, 0, 0, 0]):
        explicit_points = []
        for i in range(len(self.points)):
            if i % 2 == 0:
                explicit_points.append(self.points[i].explicit(translation[2]) + translation[0])
            else:
                explicit_points.append(self.points[i].explicit(translation[3]) + translation[1])
        return explicit_points

    def __repr__(self):
        result = "PointPos("
        for point in self.points:
            result = result + f"{point}, "
        return result[:-2] + ")"

class Color:
    def __init__(self, color_keyword):
        if not color_keyword.upper() in CONST_COLORS:
            raise Exception("Wrong color keyword")
        self.color = CONST_COLORS[color_keyword.upper()]

class Widget:
    def __init__(self, color):
        self.positions = None
        self.color = Color(color)

    def traverse(self, traverse_obj, translation = [0, 0, 0, 0]):
        getattr(traverse_obj, traverse_obj.traverse_name + type(self).__name__)(self.positions.explicit(translation), self.color.color)

class Rect(Widget):
    def __init__(self, x, y, width, height, color):
        super().__init__(color)
        self.positions = RectPosition(x, y, width, height)

class Line(Widget):
    def __init__(self, points, color):
        super().__init__(color)
        self.positions = PointPosition(points)

class Ellipse(Rect):
    pass

class ConsoleDraw:
    def __init__(self):
        self.traverse_name = "draw"

    def drawRect(self, positions, color):
        print("Rect", positions, color)

    def drawLine(self, positions, color):
        print("Line", positions, color)

    def drawEllipse(self, positions, color):
        print("Ellipse", positions, color)

d = ConsoleDraw()
e = Ellipse(10, "right 20%", "30%", 40, "green")
e.traverse(d, [18, 27, 83, 97])
print([10+18, 97-97*.2+27, .3*83, 40])