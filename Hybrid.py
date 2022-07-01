from abc import ABC, abstractmethod
import pygame

class ConsoleDraw:
    def __init__(self, widget):
        self.widget = widget

    def draw(self):
        self.widget.draw(self)

    def drawWidgetBase(self, positions, color, border_width):
        print("WidgetBase", positions.position.x, positions.position.y, color, border_width)

    def drawRect(self, position, color, border_width):
        print("WidgetBase", position.position.x, position.position.y, position.size.x, position.size.y, color, border_width)

class CanvasDraw:
    def __init__(self, widget):
        self.widget = widget
        self.running = True
        pygame.init()
        self.screen = pygame.display.set_mode((500, 500))
        pygame.display.set_caption("LAROI")

    def draw(self):
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
            self.screen.fill((128, 128, 128))
            self.widget.draw(self)
            pygame.draw.circle(self.screen, (255, 0, 0), (30, 20), 10)
            pygame.display.flip()
        pygame.display.quit()
        pygame.quit()

    def drawWidgetBase(self, positions, color, border_width):
        print("WidgetBase", positions.position.x, positions.position.y, color, border_width)

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

class Vector(ValueBase):
    def __init__(self, x, y):
        self.x = convert(x)
        self.y = convert(y)

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


VALUE_ZERO = Pixel(0)
VECTOR_ZERO = Vector(VALUE_ZERO, VALUE_ZERO)
BASE_ZERO = Base(VECTOR_ZERO, VECTOR_ZERO)

class WidgetBase(ABC):
    def __init__(self, position, color, border_width = 0):
        self.position = position
        self.color = color
        self.border_width = border_width
        self.sensor_handlers = {"click": None, "release": None, "key": None}

    def explicit(self, base):
        return self.position.explicit(base)

    @abstractmethod
    def get_block_width(self, base = BASE_ZERO):
        return 0

    @abstractmethod
    def get_block_height(self, base = BASE_ZERO):
        return 0

    def on(self, sensor_handler_name, sensor_handler):
        if not callable(sensor_handler):
            raise TypeError(f"sensor_handler is not a function, got instead {type(sensor_handler)}")
        self.sensor_handlers[sensor_handler_name] = sensor_handler

    def run_sensor_handle(self, sensor_handler_name, cargo):
        if self.sensor_handlers[sensor_handler_name]:
            self.sensor_handlers[sensor_handler_name](self, cargo)

    def click(self, x, y, base = BASE_ZERO):
        if self.scope(x, y, self.explicit(base)):
            self.run_sensor_handle("click", (x, y))
        else:
            self.run_sensor_handle("release", (x, y))

    def keydown(self, key):
        self.run_sensor_handle("key", key)

    @abstractmethod
    def scope(self, x, y, position):
        result = x == position.position.x.value and y == position.position.y.value
        return result

    def draw(self, draw_obj, base = BASE_ZERO):
        getattr(draw_obj, "draw" + type(self).__name__)(self.explicit(base), self.color, self.border_width)

class Rect(WidgetBase):
    def __init__(self, x, y, width, height, color, border_width = 0):
        super().__init__(Base(Vector(x, y), Vector(width, height)), color, border_width=border_width)

    def get_block_width(self, base = BASE_ZERO):
        return self.position.position.x.explicit(base.size.x) + self.position.size.x.explicit(base.size.x)

    def get_block_height(self, base = BASE_ZERO):
        return self.position.position.y.explicit(base.size.y) + self.position.size.y.explicit(base.size.y)

    def scope(self, x, y, position):
        x_min = position.position.x.value
        x_max = position.position.x.value + position.size.x.value
        y_min = position.position.y.value
        y_max = position.position.y.value + position.size.y.value
        return x_min < x < x_max and y_min < y < y_max

w = Rect("21.2px", "-23.4%", 10, "20%", "green")
d = ConsoleDraw(w)
base = Base(Vector(9, 17), Vector(32, 29))
w.draw(d, base)
print(w.get_block_width(base))
print(w.get_block_height(base))

def click(widget, sensor):
    print("click", widget, sensor)

def release(widget, sensor):
    print("release", widget, sensor)

def key(widget, sensor):
    print("key", widget, sensor)

w.on("click", click)
w.on("release", release)
w.on("key", key)
w.click(40, 46, base)
w.keydown("a")


"""
d2 = CanvasDraw(w)
d2.draw()
"""
