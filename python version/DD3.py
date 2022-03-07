import pygame

AZURE  = ( 193, 205, 205)
BLACK  = (   0,   0,   0)
GREEN  = (   0, 255,   0)
WHITE  = ( 255, 255, 255)
RED    = ( 255,   0,   0)
YELLOW = ( 255, 255,   0)

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

    def is_inside(self, i_x, i_y, pos_x, pos_y):
        pass

    def click_sensor(self):
        pass

    def release_sensor(self):
        pass

    def sensor(self, i_x, i_y, pos_x, pos_y):
        if self.is_inside(self, i_x, i_y, pos_x, pos_y):
            self.click_sensor()
        else:
            self.release_sensor()

class Rectangle_base(Widget_base):
    def __init__(self, x, y, color = None):
        self.x = x
        self.y = y
        return super().__init__(color)

    def move(self):
        self.x = self.x + self.vector[0]
        self.y = self.y + self.vector[1]

class Rectangle(Rectangle_base):
    def __init__(self, x, y, width, height, color):
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
    def __init__(self, x, y, radius, color):
        self.radius = radius
        return super().__init__(x, y, color)

    def draw(self, i_x, i_y, surface):
        #print("CIRCLE   ", self.x + i_x, self.y + i_y, self.radius, self.color, self.vector)
        pygame.draw.circle(surface, self.color, (round(self.x + i_x), round(self.y + i_y)), round(self.radius))

    def is_inside(self, i_x, i_y, pos_x, pos_y):
        return (pos_x-(self.x+i_x))**2 + (pos_y-(self.y+i_y))**2 < self.radius**2

class Ellipse(Rectangle_base):
    def __init__(self, x, y, radius_x, radius_y, color):
        self.radius_x = radius_x
        self.radius_y = radius_y
        return super().__init__(x, y, color)

    def draw(self, i_x, i_y, surface):
        #print("ELLIPSE  ", self.x+i_x, self.y+i_y, self.radius_x, self.radius_y, self.color, self.vector)
        pygame.draw.ellipse(surface, self.color, pygame.Rect(self.x+i_x-self.radius_x, self.y+i_y-self.radius_y, 2*self.radius_x, 2*self.radius_y))

    def is_inside(self, i_x, i_y, pos_x, pos_y):
        return (pos_x-(self.x+i_x))**2 / self.radius_x**2 + (pos_y-(self.y+i_y))**2 / self.radius_y**2 < 1

class Layout(Widget_base):
    def __init__(self, x, y, widgets):
        self.x = x
        self.y = y
        self.widgets = widgets
        return super().__init__(None)

    def add(self, value):
        self.widgets.append(value)

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

class Paintware:
    def __init__(self):
        pygame.init()
        self.SCREEN_WIDTH = 500
        self.SCREEN_HEIGHT = 500
        self.caption = "PYGAME TEST"
        self.screen = pygame.display.set_mode([500, 500])
        self.running = True
        self.FPS = 24
        self.clock = pygame.time.Clock()
        pygame.display.set_caption(self.caption)
        self.mouse_x = -1
        self.mouse_y = -1
        self.click = False

    def init(self):
        pass

    def mouse_sensor_handling(self, x, y, click):
        pass

    def sensors_handling(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self.click = True
            elif event.type == pygame.MOUSEBUTTONUP:
                self.click = False
            self.mouse_x, self.mouse_y = pygame.mouse.get_pos()
            self.mouse_sensor_handling(self.mouse_x, self.mouse_y, self.click)

    def run(self):
        self.init()
        while self.running:
            self.sensors_handling()
            self.layout.move()
            self.screen.fill(BLACK)
            self.layout.draw(0, 0, self.screen)
            #pygame.draw.rect(self.screen, WHITE, pygame.Rect(150, 250, 3, 3))
            pygame.display.flip()
            self.clock.tick(self.FPS)
        pygame.display.quit()
        pygame.quit()

class DD3(Paintware):
    def init(self):
        self.layout = Layout(50, 50, [Layout(120, 20, 
                                             [Rectangle(10, 10, 10, 10, WHITE), 
                                              Circle(15, 50, 20, RED), 
                                              Ellipse(10, 90, 20, 40, GREEN)]), 
                                      Rectangle(0, 0, 100, 200, AZURE)])
        #self.layout[1].force([5, -2])
        self.layout[0].force([1, 0])

    def mouse_sensor_handling(self, x, y, click):
        if (self.layout[0][1].is_inside(self.layout[0].x + self.layout.x, self.layout[0].y + self.layout.y, x, y)):
            self.layout[0][1].color = AZURE
        else:
            self.layout[0][1].color = RED
        if (self.layout[0][2].is_inside(self.layout[0].x + self.layout.x, self.layout[0].y + self.layout.y, x, y) and click):
            self.layout[0][2].color = YELLOW
        else:
            self.layout[0][2].color = GREEN
            

if __name__ == "__main__":
    DD3().run()
