import pygame

AZURE = (193,205,205)
BLACK = (  0,  0,  0)
WHITE = (255,255,255)
RED   = (255,  0,  0)

class Widget_base:
    def __init__(self, color = None):
        self.color = color
        self.vector = [0, 0]

    def draw(self):
        pass

    def force(self, vector):
        self.vector[0] = self.vector[0] + vector[0]
        self.vector[1] = self.vector[1] + vector[1]

    def reset(self):
        self.velocity = [0, 0]

    def move(self):
        pass

class Rectangle_base(Widget_base):
    def __init__(self, x, y, color = None):
        self.x = x
        self.y = y
        return super().__init__(color)

    def move(self):
        self.x = self.x + self.vector[0]
        self.y = self.y + self.vector[1]

class Rectangle(Rectangle_base):
    def __init__(self, x, y, width, height, color = None):
        self.width = width
        self.height = height
        return super().__init__(x, y, color)

    def draw(self, i_x, i_y, surface):
        #print("RECTANGLE", self.x + i_x, self.y + i_y, self.width, self.height, self.color, self.vector)
        pygame.draw.rect(surface, self.color, pygame.Rect(self.x + i_x, self.y + i_y, self.width, self.height))

    def is_inside(self, i_x, i_y, pos_x, pos_y):
        horizontal = self.x + i_x <= pos_x <= self.x + i_x + self.width
        vertical = self.y + i_y <= pos_y <= self.y + i_y + self.height
        return horizontal and vertical

class Image(Rectangle):
    def __init__(self, image_name, x, y, width = 0, height = 0):
        self.image_name = image_name
        #self.pic = pygame.image.load(self.image_name)
        return super().__init__(x, y, width, height, None)

    def draw(self, i_x, i_y):
        print("IMAGE:", self.image_name, self.x + i_x, self.y + i_y, self.width, self.height, self.color, self.vector)
        #screen.blit(pygame.transform.scale(pic, (500, 500)), (0, 0))

class Text(Rectangle):
    def __init__(self, x, y, width, height, text_value, color = None):
        self.text_value = text_value
        return super().__init__(x, y, width, height, color)

    def draw(self, i_x, i_y):
        print("TEXT:", self.text_value, self.x + i_x, self.y + i_y, self.width, self.height, self.color, self.vector)

class Circle(Rectangle_base):
    def __init__(self, x, y, radius, color = None):
        self.radius = radius
        return super().__init__(x, y, color)

    def draw(self, i_x, i_y, surface):
        #print("CIRCLE   ", self.x + i_x, self.y + i_y, self.radius, self.color, self.vector)
        pygame.draw.circle(surface, self.color, (self.x + i_x, self.y + i_y), self.radius)

    def is_inside(self, i_x, i_y, pos_x, pos_y):
        return (pos_x-(self.x+i_x))**2 + (pos_y-(self.y+i_y))**2 < self.radius**2

class Ellipse(Rectangle_base):
    def __init__(self, x, y, radius_x, radius_y, color = None):
        self.radius_x = radius_x
        self.radius_y = radius_y
        return super().__init__(x, y, color)

    def draw(self, i_x, i_y):
        print("ELLIPSE  ", self.x+i_x, self.y+i_y, self.radius_x, self.radius_y, self.color, self.vector)

    def is_inside(self, i_x, i_y, pos_x, pos_y):
        return (pos_x-(self.x+i_x))**2 / self.radius_x**2 + (pos_y-(self.y+i_y))**2 / self.radius_y**2 < 1

class Layout(Widget_base):
    def __init__(self, x, y, widgets):
        self.x = x
        self.y = y
        self.widgets = widgets
        return super().__init__(None)

    def __getitem__(self, key):
        return self.widgets[key]

    def draw(self, i_x, i_y, surface):
        for i in self.widgets:
            i.draw(self.x + i_x, self.y + i_y, surface)

    def move(self):
        self.x = self.x + self.vector[0]
        self.y = self.y + self.vector[1]
        for i in self.widgets:
            i.move()

class All:
    def __init__(self):
        pygame.init()
        self.SCREEN_WIDTH = 500
        self.SCREEN_HEIGHT = 500
        self.screen = pygame.display.set_mode([500, 500])
        self.caption = "PYGAME TEST"
        pygame.display.set_caption(self.caption)
        self.running = True
        self.FPS = 24
        self.clock = pygame.time.Clock()

        # USER DEFINED
        self.layout = Layout(50, 50, [Layout(120, 20, [Rectangle(10, 10, 10, 10, WHITE), Circle(15, 50, 20, RED)]), Rectangle(0, 0, 100, 200, AZURE)])
        #self.layout[1].force([5, -2])

    def event_handling(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

    def draw(self):
        self.layout.draw(0, 0, self.screen)
        pygame.draw.rect(self.screen, WHITE, pygame.Rect(185, 120, 3, 3))

    def update(self):
        #self.layout[1].force([1, 0])
        self.layout.move()

    def run(self):
        while self.running:
            self.event_handling()
            self.update()
            self.screen.fill(BLACK)
            self.draw()
            pygame.display.flip()
            self.clock.tick(self.FPS)
        pygame.quit()

if __name__ == "__main__":
    All().run()