import pygame
from pygame.sprite import Sprite


class Dot(Sprite):
    """Dot on the board with own position and color"""

    def __init__(self, board, color, center=(0, 0), active=False):
        """Init dot"""

        super().__init__()
        self.settings = board.settings
        self.screen = board.screen
        self.active = active

        # circle parameters
        self.color = color
        self.center = center
        self.radius = self.settings.dot_radius

        # rectangle where circle placed
        self.image = pygame.Surface([self.radius * 2, self.radius * 2])
        self.image.fill(self.settings.screen_background)
        pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
        self.rect = self.image.get_rect()
        self.rect.center = self.center

    def collide(self, position):
        return self.rect.collidepoint(position)

    def activate(self, color):
        if ~self.active:
            self.active = True
            self.color = color
            pygame.draw.circle(self.image, self.color, (self.radius, self.radius), self.radius)
