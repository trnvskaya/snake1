"""This module defines user interface"""
import pygame


class Button:
    """This class defines button object"""
    def __init__(self, surface, color, x, y, width, height, text, text_color):
        """Initializes button object"""
        self.surface = surface
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.text_color = text_color
        self.font = pygame.font.Font(None, 36)

    def draw(self):
        """Draws button"""
        pygame.draw.rect(self.surface, self.color, self.rect)
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        self.surface.blit(text_surf, text_rect)

    def is_clicked(self, event):
        """Checks if button was clicked"""
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                return True
        return False


class Label:
    """This class defines label object"""
    def __init__(self, surface, text, x, y, width, height, text_color):
        """Initialize the label object"""
        self.surface = surface
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.text_color = text_color
        self.font = pygame.font.Font(None, 48)

    def draw(self):
        """Draw the label"""
        text_surf = self.font.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        self.surface.blit(text_surf, text_rect)
