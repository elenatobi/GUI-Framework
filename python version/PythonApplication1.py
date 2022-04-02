class ShapeBase:
    def __init__(self, x = 0, y = 0, color = "black"):
        self.x = x
        self.y = y
        self.color = color
        self.vector = [0, 0]

    def draw(self, inherit = [0, 0]):
        print("ABST:", self.x + inherit[0], self.y + inherit[1], self.color)

class Line(ShapeBase):
    def __init__(self, x=0, y=0, x1=0, y1=0, color="black"):
        super().__init__(x=x, y=y, color=color)
        self.x1 = x1
        self.y1 = y1

    def draw(self, inherit = [0, 0]):
        print("LINE:", self.x + inherit[0], self.y + inherit[1], self.x1 + inherit[0], self.y1 + inherit[1], self.color)

    def get_height(self):
        return abs(self.y1 - self.y)

class Rect(ShapeBase):
    def __init__(self, x=0, y=0, width = 0, height = 0, color="black"):
        super().__init__(x=x, y=y, color=color)
        self.width = width
        self.height = height

    def draw(self, inherit = [0, 0]):
        print("RECT:", self.x + inherit[0], self.y + inherit[1], self.width, self.height, self.color)

    def get_height(self):
        return self.height

class Circle(ShapeBase):
    def __init__(self, x=0, y=0, radius = 0, color="black"):
        super().__init__(x=x, y=y, color=color)
        self.radius = radius

    def draw(self, inherit = [0, 0]):
        print("CIRC:", self.x + inherit[0], self.y + inherit[1], self.radius, self.color)

    def get_height(self):
        return self.radius

class Ellipse(Rect):
    def draw(self, inherit = [0, 0]):
        print("ELLI:", self.x + inherit[0], self.y + inherit[1], self.width, self.height, self.color)

class Image(Rect):
    def __init__(self, x=0, y=0, width=0, height=0, source = ""):
        super().__init__(x=x, y=y, width=width, height=height, color="black")
        self.source = source

    def draw(self, inherit = [0, 0]):
        print("IMG1:", self.x + inherit[0], self.y + inherit[1], self.width, self.height, self.source)

class Text(Rect):
    def __init__(self, x=0, y=0, width=0, height=0, text_string = "" ,color="black"):
        super().__init__(x=x, y=y, width=width, height=height, color=color)
        self.text_string = text_string

    def draw(self, inherit = [0, 0]):
        print("TEXT:", self.x + inherit[0], self.y + inherit[1], self.width, self.height, self.text_string, self.color)

class LayoutBase(Rect):
    def __init__(self, x=0, y=0, width=0, height=0, widgets = [], color="white"):
        super().__init__(x=x, y=y, width=width, height=height, color=color)
        self.widgets = widgets

class Coordinator(LayoutBase):
    def draw(self, inherit=[0, 0]):
        print("COORDINATOR LAYOUT:")
        super().draw(inherit=inherit)
        for i in self.widgets:
            i.draw([self.x + inherit[0], self.y + inherit[1]])
        print("END")

class Linear(LayoutBase):
    def draw(self, inherit=[0, 0]):
        print("LINEAR LAYOUT:")
        super().draw(inherit=inherit)
        y_offset = 0
        for i in self.widgets:
            i.draw([self.x + inherit[0], self.y + inherit[1] + y_offset])
            y_offset = y_offset + i.get_height()
        print("END")

"""
LINEAR LAYOUT:
RECT: 1 2 30 30 white
RECT: 3 4 1 2 black
RECT: 5 7 1 4 black
RECT: 1 10 8 7 black
COORDINATOR LAYOUT:
RECT: 2 17 30 30 white
RECT: 3 19 3 4 black
RECT: 4 25 1 3 black
END
RECT: 1 45 3 2 black
#RECT: 2 50 5 5 black
END
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
#l.draw()

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
#c.draw()

FILE = "testGUI.kify"

def open_file(filename):
    f = open(filename, "r")
    lines = "".join(f.readlines())
    f.close()
    return lines

def to_tokens(lines):
    tokens = [[0, "", [""]]]
    ident = True
    attributes = False
    for char in lines:
        if char == " " and ident:
            tokens[-1][0] = tokens[-1][0] + 1
        elif char == "\n":
            tokens.append([0, "", [""]])
            ident = True
        elif char == "(":
            attributes = True
        elif char == ")":
            attributes = False
        elif char == ",":
            tokens[-1][2].append("")
        elif attributes and char.isalnum():
            tokens[-1][2][-1] = tokens[-1][2][-1] + char
        else:
            if not attributes:
                tokens[-1][1] = tokens[-1][1] + char
            ident = False
    return tokens

def parse(tokens):
    stack = [[]]
    level = 0
    for token in tokens:
        if token[0] > level:
            stack.append([])
            level = token[0]
        elif token[0] < level:
            widgets = stack.pop()
            stack[-1][-1].widgets = widgets
        
        if token[1] == "Coordinator":
            stack[-1].append(Coordinator(int(token[2][0]), int(token[2][1]), int(token[2][2]), int(token[2][3])))
        elif token[1] == "Linear":
            stack[-1].append(Linear(int(token[2][0]), int(token[2][1]), int(token[2][2]), int(token[2][3])))
        elif token[1] == "Rect":
            stack[-1].append(Rect(int(token[2][0]), int(token[2][1]), int(token[2][2]), int(token[2][3])))
    print(stack)
    stack[0][0].draw()

lines = open_file(FILE)
tokens = to_tokens(lines)
parse(tokens)
