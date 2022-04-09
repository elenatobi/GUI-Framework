import pygame

COLORS = {"black": (0, 0, 0), "green": (0, 255, 0), "red": (255, 0, 0), "blue": (0, 0, 255), "white": (255, 255, 255), "purple": (128, 0, 128), "grey": (128, 128, 128)}

class ShapeBase:
    def __init__(self, x = 0, y = 0, color = "black"):
        self.x = x
        self.y = y
        if color in COLORS.keys():
            self.color = color
        else:
            raise Exception(f"Invalid color keyword {color}")
        self.vector = [0, 0]

    def print_to_console(self, inherit = [0, 0]):
        print("ABST:", self.x + inherit[0], self.y + inherit[1], self.color)

    def set_content(self, content):
        pass

class Line(ShapeBase):
    def __init__(self, x=0, y=0, x1=0, y1=0, color="black"):
        super().__init__(x=x, y=y, color=color)
        self.x1 = x1
        self.y1 = y1

    def print_to_console(self, inherit = [0, 0]):
        print("LINE:", self.x + inherit[0], self.y + inherit[1], self.x1 + inherit[0], self.y1 + inherit[1], self.color)

    def draw(self, surface, inherit = [0, 0]):
        pygame.draw.line(surface, COLORS[self.color], [self.x + inherit[0], self.y + inherit[1]], [self.x1 + inherit[0], self.y1 + inherit[1]])

    def get_height(self):
        return abs(self.y1 - self.y)

class Rect(ShapeBase):
    def __init__(self, x=0, y=0, width = 0, height = 0, color="black"):
        super().__init__(x=x, y=y, color=color)
        self.width = width
        self.height = height

    def print_to_console(self, inherit = [0, 0]):
        print("RECT:", self.x + inherit[0], self.y + inherit[1], self.width, self.height, self.color)

    def draw(self, surface, inherit = [0, 0]):
        pygame.draw.rect(surface, COLORS[self.color], [self.x + inherit[0], self.y + inherit[1], self.width, self.height])

    def get_height(self):
        return self.height

    def apply(self, arr):
        arr = arr + [""]*(5-len(arr))
        if arr[0] != "":
            self.x = int(arr[0])
        if arr[1] != "":
            self.y = int(arr[1])
        if arr[2] != "":
            self.width = int(arr[2])
        if arr[3] != "":
            self.height = int(arr[3])
        if arr[4] != "":
            self.color = str(arr[4]).strip()

class Circle(ShapeBase):
    def __init__(self, x=0, y=0, radius = 0, color="black"):
        super().__init__(x=x, y=y, color=color)
        self.radius = radius

    def print_to_console(self, inherit = [0, 0]):
        print("CIRC:", self.x + inherit[0], self.y + inherit[1], self.radius, self.color)

    def draw(self, surface, inherit = [0, 0]):
        pygame.draw.circle(surface, COLORS[self.color], [self.x + inherit[0], self.y + inherit[1]], self.radius)

    def get_height(self):
        return self.radius

    def apply(self, arr):
        arr = arr + [""]*(5-len(arr))
        if arr[0] != "":
            self.x = int(arr[0])
        if arr[1] != "":
            self.y = int(arr[1])
        if arr[2] != "":
            self.radius = int(arr[2])
        if arr[3] != "":
            self.color = str(arr[3])

class Ellipse(Rect):
    def print_to_console(self, inherit = [0, 0]):
        print("ELLI:", self.x + inherit[0], self.y + inherit[1], self.width, self.height, self.color)

    def draw(self, surface, inherit = [0, 0]):
        pygame.draw.ellipse(surface, COLORS[self.color], [self.x + inherit[0], self.y + inherit[1], self.width, self.height])

class Image(Rect):
    def __init__(self, x=0, y=0, width=0, height=0, source = ""):
        super().__init__(x=x, y=y, width=width, height=height, color="black")
        self.source = source
        #print("." + source + ".")
        if source != "":
            self.image = pygame.image.load(source)
        else:
            self.image = None

    def print_to_console(self, inherit = [0, 0]):
        print("IMG1:", self.x + inherit[0], self.y + inherit[1], self.width, self.height, self.source)

    def draw(self, surface, inherit = [0, 0]):
        if self.width == 0 and self.height == 0:
            surface.blit(self.image, (self.x + inherit[0], self.y + inherit[1]))
        else:
            surface.blit(pygame.transform.scale(self.image, (self.width, self.height)), (self.x + inherit[0], self.y + inherit[1]))

    def get_height(self):
        if self.height == 0:
            return int(self.image.get_height())
        else:
            return self.height

    def set_content(self, content):
        self.source = content
        self.image = pygame.image.load(content)

class Text(Rect):
    def __init__(self, x=0, y=0, width=0, height=0, text_string = "" ,color="black"):
        super().__init__(x=x, y=y, width=width, height=height, color=color)
        self.text_string = text_string

    def print_to_console(self, inherit = [0, 0]):
        print("TEXT:", self.x + inherit[0], self.y + inherit[1], self.width, self.height, self.text_string, self.color)

    def draw(self, surface, inherit = [0, 0]):
        surface.blit(pygame.font.SysFont('Arial', self.height).render(self.text_string, False, COLORS[self.color]),(self.x + inherit[0], self.y + inherit[1]))

    def set_content(self, content):
        self.text_string = content

class LayoutBase(Rect):
    def __init__(self, x=0, y=0, width=0, height=0, widgets = [], color="white"):
        super().__init__(x=x, y=y, width=width, height=height, color=color)
        self.widgets = widgets

class Coordinator(LayoutBase):
    def print_to_console(self, inherit=[0, 0]):
        print("COORDINATOR LAYOUT:")
        super().print_to_console(inherit=inherit)
        for i in self.widgets:
            i.print_to_console([self.x + inherit[0], self.y + inherit[1]])
        print("END")

    def draw(self, surface, inherit=[0, 0]):
        super().draw(surface, inherit=inherit)
        for i in self.widgets:
            i.draw(surface, [self.x + inherit[0], self.y + inherit[1]])

class Linear(LayoutBase):
    def print_to_console(self, inherit=[0, 0]):
        print("LINEAR LAYOUT:")
        super().print_to_console(inherit=inherit)
        y_offset = 0
        for i in self.widgets:
            i.print_to_console([self.x + inherit[0], self.y + inherit[1] + y_offset])
            y_offset = y_offset + i.y + i.get_height()
        print("END")

    def draw(self, surface, inherit=[0, 0]):
        super().draw(surface, inherit=inherit)
        y_offset = 0
        for i in self.widgets:
            i.draw(surface, [self.x + inherit[0], self.y + inherit[1] + y_offset])
            y_offset = y_offset + i.y + i.get_height()

"""
l = Linear(1, 2, 60, 100, 
           [Rect(2, 2, 1, 2), 
            Rect(4, 3, 1, 4), 
            Rect(0, 2, 8, 7), 
            Coordinator(1, 2, 30, 30, 
                        [Rect(1, 2, 3, 4), 
                         Rect(2, 8, 1, 3)]), 
            Rect(0, 0, 3, 2),
            Rect(1, 3, 5, 5),
            Circle(3, 2, 7, "red"),
            Circle(2, 3, 4, "purple"),
            Ellipse(5, 1, 7, 2, "green"),
            Image(3, 2, 10, 10, "realityvision.png")])
l.print_to_console()
"""

"""
c = Coordinator(1, 3, 1000, 1000, 
                [Rect(1, 2, 2, 3),
                 Rect(3, 2, 1, 2),
                 Linear(7, 8, 500, 500, 
                        [Rect(1, 2, 4, 5),
                         Ellipse(1, 3, 3, 4),
                         Coordinator(2, 7, 450, 450, 
                                     [Rect(2, 1, 5, 4),
                                      Rect(5, 7, 2, 3)]),
                         Image(4, 3, 3, 2, "realityvision.png")]),
                 Text(8, 555, 2, 11, "Hello world!"),
                 Line(8, 600, 11, 612)])
c.print_to_console()
"""

WIDGETS = {"Coordinator": Coordinator, "Linear": Linear, "Rect": Rect, "Image": Image}

def open_file(filename):
    f = open(filename, "r")
    lines = "".join(f.readlines())
    f.close()
    return lines

def to_tokens(lines):
    data_lines = lines.split("\n")
    tokens = []
    for data_line in data_lines:
        attribute_begin = data_line.find("(")
        attribute_end = data_line.find(")")
        blankspaces = len(data_line) - len(data_line.lstrip())
        widget = data_line[blankspaces:attribute_begin]
        attributes = data_line[attribute_begin+1:attribute_end].split(",")
        value = data_line[attribute_end+1:].strip()
        tokens.append([blankspaces, widget, attributes, value])
    return tokens

def to_layout(tokens):
    stack = [[]]
    level = 0
    row_number = 0
    for token in tokens:
        if token[0] > level:
            stack.append([])
            level = token[0]

        elif token[0] < level:
            widgets = stack.pop()
            stack[-1][-1].widgets = stack[-1][-1].widgets + widgets
            level = token[0]

        if token[1] in WIDGETS.keys():
            widget = WIDGETS[token[1]]()
            widget.apply(token[2])
            widget.set_content(token[3])
            stack[-1].append(widget)
        elif token[-1].strip() != "":
            raise Exception(f"Invalid widget name: \"{token[1]}\" on row number {row_number} in kify file")

        row_number = row_number + 1
    
    while len(stack) > 1:
        widgets = stack.pop()
        stack[-1][-1].widgets = stack[-1][-1].widgets + widgets

    #print("Parsed stack", stack)
    return stack[0][0]

def load_file(file): return to_layout(to_tokens(open_file(file)))


layout = load_file("testGUI.kify")
layout.print_to_console()


class App:
    def __init__(self, layout = Coordinator(), width = 500, height = 500):
        self.layout = layout
        self.width = width
        self.height = height
        self.running = True
        self.refresh = True
        pygame.init()
        self.screen = pygame.display.set_mode([self.width, self.height])

    def handle_sensor(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def __drawscreen(self):
        self.screen.fill(COLORS["grey"])
        #pygame.draw.circle(self.screen, COLORS["blue"], (250, 250), 75)
        self.layout.draw(self.screen)
        self.screen.set_at((10, 20), "blue")
        self.screen.set_at((30, 40), "blue")
        self.screen.set_at((50, 70), "blue")
        self.screen.set_at((10, 100), "blue")
        self.screen.set_at((20, 170), "blue")
        self.screen.set_at((30, 190), "blue")
        self.screen.set_at((40, 250), "blue")
        self.screen.set_at((10, 450), "blue")
        self.screen.set_at((30, 480), "blue")
        self.screen.set_at((12, 984), "blue")
        self.screen.set_at((542, 992), "blue")
        pygame.display.flip()

    def run(self):
        while self.running:
            self.handle_sensor()
            if self.refresh:
                print("CANVAS IS REFRESHING")
                self.__drawscreen()
                self.refresh = False
        pygame.quit()

App(layout, 1000, 1000).run()
