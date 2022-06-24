import pygame

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

    def drawWidgetBase(self, positions, color, border_width):
        print("WidgetBase: Positions:", positions, "Color:", color, "Border width:", border_width)

    def drawLine(self, positions, color, border_width):
        print("Line: Positions:", positions, "Color:", color, "Border width:", border_width)

    def drawRect(self, positions, color, border_width):
        print("Rect: Positions:", positions, "Color:", color, "Border width:", border_width)

    def drawCircle(self, positions, color, border_width):
        print("Circle: Positions:", positions, "Color:", color, "Border width:", border_width)

    def drawEllipse(self, positions, color, border_width):
        print("Ellipse: Positions:", positions, "Color:", color, "Border width:", border_width)

    def drawImage(self, positions, image, source):
        print("Image: Positions:", positions, "Source:", source)
        return image

    def drawText(self, positions, text_string, text_surface, color):
        print("Image: Positions:", positions, "Text:", text_string, "Color:", color)
        return text_surface

    def drawLayoutBase(self, positions, color, border_width):
        print("LayoutBase: Positions:", positions, "Color:", color, "Border width:", border_width)

class DrawPygame:
    def __init__(self, widget):
        self.widget = widget
        self.color = get_color("gray")
        self.running = True
        self.refresh = True
        pygame.init()
        self.screen = pygame.display.set_mode([500, 500])

    def drawRect(self, positions, color, border_width):
        pygame.draw.rect(self.screen, color, positions, border_width)

    def _handle_sensor(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def _draw_screen(self):
        self.screen.fill(self.color)
        self.widget.draw(self)
        pygame.display.flip()

    def run(self):
        while self.running:
            self._handle_sensor()
            if self.refresh:
                print("PYGAME CONSOLE LOG: REFRESHING CANVAS")
                self._draw_screen()
                self.refresh = False
        pygame.quit()

class WidgetBase:
    def __init__(self, positions, color_keyword, border_width = 0):
        if not self.check_valid_position_length(len(positions)):
            raise Exception("Invalid position length of " + type(self).__name__)
        self.positions = positions
        self.color = get_color(color_keyword)
        self.border_width = border_width
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
            getattr(draw_object, "draw" + type(self).__name__)(self.positions, self.color, self.border_width)

    def is_inside(self, x, y):
        return False

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

    def is_inside(self, x, y):
        return self.positions[0] < x < self.positions[0] + self.positions[2] and self.positions[1] < y < self.positions[1] + self.positions[3]

class Circle(WidgetBase):
    def check_valid_position_length(self, position_length):
        return position_length == 3

    def is_inside(self, x, y):
        return (x-self.positions[0])**2 + (y-self.positions[1])**2 < self.positions[2]**2

class Ellipse(Rect):
    def is_inside(self, x, y):
        return (x-self.positions[0])**2 / self.positions[2]**2 + (y-self.positions[1])**2 / self.positions[3]**2 < 1

class Image(Rect):
    def __init__(self, positions, source):
        super().__init__(positions, COLOR_DEFAULT)
        self.source = source
        self.image = None

    def draw(self, draw_object):
        self.image = getattr(draw_object, "draw" + type(self).__name__)(self.positions, self.image, self.source)

class Text(Rect):
    def __init__(self, positions, text_string, color_keyword):
        super().__init__(positions, color_keyword)
        self.text_string = text_string
        self.font = None
        self.text_surface = None

    def check_valid_position_length(self, position_length):
        return position_length == 3

    def draw(self, draw_object):
        self.text_surface = getattr(draw_object, "draw" + type(self).__name__)(self.positions, self.text_string, self.text_surface, self.color)

class LayoutBase(Rect):
    def __init__(self, positions, color_keyword, widgets = [], border_width = 0):
        super().__init__(positions, color_keyword, border_width)
        self.widgets = []
        if widgets != []:
            self.append_multiple(widgets)

    def append(self, widget):
        widget.move_delta(Vector(self.positions[0], self.positions[1]))
        self.widgets.append(widget)

    def append_multiple(self, widgets):
        for widget in widgets:
            self.append(widget)

    def __getitem__(self, index):
        return self.widgets[index]

    def move_delta(self, delta_positions):
        super().move_delta(delta_positions)
        for widget in self.widgets:
            widget.move_delta(delta_positions)

    def draw(self, draw_object):
       super().draw(draw_object)
       for widget in self.widgets:
           widget.draw(draw_object)

d = DrawConsole()

"""
l = LayoutBase([5, 8, 100, 100], "green", [
    Line([3, 4, 8, 19], "red"),
    Rect([4, 5, 2, 3], "lime"),
    Circle([3, 2, 5], "blue"),
    LayoutBase([3, 20, 97, 80], "cyan", [
        Ellipse([2, 5, 4, 3], "navy"),
        Text([12, 3, 5], "Hello world", "black")
    ]),
    Rect([23, 2, 10, 5], "red", 3),
])
l.move_delta([3, 7])
l.draw(d)
"""

#e = Ellipse([3, 6, 2, 3], "blue")
"""
e.is_inside(5, 3)
"""

p = DrawPygame(Rect([10, 10, 50, 50], "green"))
p.run()
