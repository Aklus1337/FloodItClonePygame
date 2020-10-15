import pygame, random
pygame.init()
FONT = pygame.font.SysFont('arial', 20, True)

class PyGameButton():
    def __init__(self, color, x, y, width, height, text = None, colorNumber = False, font=FONT):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.colorNumber = colorNumber
        self.font = font

    def draw(self, window):
        pygame.draw.rect(window, self.color, (self.x, self.y, self.width, self.height), 0)
        if self.text is not None: #if the button has any text in it, print it
            text = self.font.render(str(self.text), 1, (0,0,0))
            window.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        d = dict()
        d[0] = False #no, we didnt click the button
        d[1] = None #we do nothing
        if pos[0] > self.x and pos[0] < self.x +self.width:
            if pos[1] > self.y and pos[1] <self.y + self.height:
                d[0] = True #yes, we clicked the button
                if self.colorNumber:
                    d[1] = int(self.text)
                else:
                    if self.text is not None and self.text != "BG":
                        d[1] = self.text #return number that is on button's text if there is any
                    else:
                        d[1] = list()
                        for x in range (0,3):
                            d[1].append(random.randint(0,255))
                return d
        return d


class Pallete:
    def __init__(self, x, y, color, width):
        self.x = x
        self.y = y
        self.color = color
        self.width = width
    def draw(self, window, COLORS):

        pygame.draw.rect(window, COLORS[self.color], (self.x, self.y, 50, 50), 0)
    def isOver(self, pos):
        d = list()
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.width:
                d.append(True)
                d.append(self.color)
                return d
        d.append(False)
        return d
