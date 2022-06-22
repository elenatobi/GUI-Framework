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

COLOR_TRANSPARENCY = "TRANSPARENT"
COLOR_DEFAULT = "BLACK"

def get_color(color_keyword):
    if not color_keyword.upper() in CONST_COLORS.keys():
        raise Exception("Invalid color keyword '" + color_keyword + "'")
    return CONST_COLORS[color_keyword.upper()]

class Vector:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        else:
            raise Exception("Invalid index written, index must be 0 or 1")

    def __len__(self):
        return 2

class DrawConsole:
    def __init__(self):
        pass

    def drawWidgetBase(self, positions, color):
        print("WidgetBase: Positions:", positions, "Color:", color)

    def drawLine(self, positions, color):
        print("Line: Positions:", positions, "Color:", color)

    def drawRect(self, positions, color):
        print("Rect: Positions:", positions, "Color:", color)

    def drawCircle(self, positions, color):
        print("Circle: Positions:", positions, "Color:", color)

    def drawEllipse(self, positions, color):
        print("Ellipse: Positions:", positions, "Color:", color)

    def drawImage(self, positions, image, source):
        print("Image: Positions:", positions, "Source:", source)
        return image

    def drawLayoutBase(self, positions, color):
        print("LayoutBase: Positions:", positions, "Color:", color)

class WidgetBase:
    def __init__(self, positions, color_keyword):
        if not self.check_valid_position_length(len(positions)):
            raise Exception("Invalid position length of " + type(self).__name__)
        self.positions = positions
        self.color = get_color(color_keyword)
        self.dimensions = 2

    def check_valid_position_length(self, position_length):
        return position_length == 2

    def check_dimentions(self, delta_positions_length):
        if self.dimensions != delta_positions_length:
            raise Exception("Invalid dimentions, current canvas is " + str(self.dimensions) + "D")

    def move_delta(self, delta_positions):
        self.check_dimentions(len(delta_positions))
        for index in range(len(delta_positions)):
            self.positions[index] = self.positions[index] + delta_positions[index]
    
    def __repr__(self):
        return type(self).__name__ + str(self.__dict__)

    def draw(self, draw_object):
        if self.color != CONST_COLORS[COLOR_TRANSPARENCY]:
            getattr(draw_object, "draw" + type(self).__name__)(self.positions, self.color)

class Line(WidgetBase):
    def check_valid_position_length(self, position_length):
        return position_length >= 4 and position_length % 2 == 0

    def move_delta(self, delta_positions):
        self.check_dimentions(len(delta_positions))
        for index in range(len(self.positions)):
            self.positions[index] = self.positions[index] + delta_positions[index%len(delta_positions)]

class Rect(WidgetBase):
    def check_valid_position_length(self, position_length):
        return position_length == 4

class Circle(WidgetBase):
    def check_valid_position_length(self, position_length):
        return position_length == 3

class Ellipse(Rect):
    pass

class Image(Rect):
    def __init__(self, positions, source):
        super().__init__(positions, COLOR_DEFAULT)
        self.source = source
        self.image = None

    def draw(self, draw_object):
        self.image = getattr(draw_object, "draw" + type(self).__name__)(self.positions, self.image, self.source)

class LayoutBase(Rect):
    def __init__(self, positions, color_keyword):
        super().__init__(positions, color_keyword)
        self.widgets = []

    def append(self, widget):
        widget.move_delta(Vector(self.positions[0], self.positions[1]))
        self.widgets.append(widget)

    def move_delta(self, delta_positions):
        super().move_delta(delta_positions)
        for widget in self.widgets:
            widget.move_delta(delta_positions)

    def draw(self, draw_object):
       super().draw(draw_object)
       for widget in self.widgets:
           widget.draw(draw_object)

d = DrawConsole()

l = LayoutBase([5, 8, 100, 100], "green")
l.append(Line([3, 4, 8, 19], "red"))
l.append(Rect([4, 5, 2, 3], "lime"))
l.move_delta([3, 7])
print(l)
l.draw(d)