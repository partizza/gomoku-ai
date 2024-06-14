import pygame
from pygame.sprite import Sprite


class Button(Sprite):

    def __init__(self, width, height, center, textSurf, background, label):
        super().__init__()
        # button rectangle
        self.image = pygame.Surface((width, height))
        self.image.fill(background)
        self.rect = self.image.get_rect()
        self.rect.center = center
        self.label = label

        # button text
        self.textSurf = textSurf
        W = self.textSurf.get_width()
        H = self.textSurf.get_height()
        self.image.blit(textSurf, (width/2 - W/2, height/2 - H/2))

    def collide(self, position):
        return self.rect.collidepoint(position)
