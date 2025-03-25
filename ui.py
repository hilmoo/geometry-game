import pygame
from constants import BUTTON_GLASS, BUTTON_BORDER, WHITE, BACKGROUND_GRADIENT, WIDTH, HEIGHT

# Font setup
pygame.font.init()
title_font = pygame.font.Font(None, 36)
main_font = pygame.font.Font(None, 24)

def draw_background(surface):
    for i in range(HEIGHT):
        color = [
            BACKGROUND_GRADIENT[0][j] + (BACKGROUND_GRADIENT[1][j] - BACKGROUND_GRADIENT[0][j]) * (i / HEIGHT)
            for j in range(3)
        ]
        pygame.draw.line(surface, color, (0, i), (WIDTH, i))

class GlassButton:
    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
    
    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = self.rect.collidepoint(mouse_pos)
        
        button_color = (255, 255, 255, 80) if is_hovered else BUTTON_GLASS
        border_color = (255, 255, 255, 150) if is_hovered else BUTTON_BORDER
        
        button_surface = pygame.Surface((self.rect.width, self.rect.height), pygame.SRCALPHA)
        pygame.draw.rect(button_surface, button_color, (0, 0, self.rect.width, self.rect.height), border_radius=10)
        pygame.draw.rect(button_surface, border_color, (0, 0, self.rect.width, self.rect.height), width=2, border_radius=10)
        
        surface.blit(button_surface, (self.rect.x, self.rect.y))
        
        text_surf = main_font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, event):
        """Cek apakah tombol diklik"""
        return event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and self.rect.collidepoint(event.pos)



class ModernInputBox:
    def __init__(self, x, y, width, height, text='', placeholder=''):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.placeholder = placeholder
        self.active = False
        
    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)
        
        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                return self.text
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                # Only allow numeric input, decimal points, and minus signs
                if event.unicode.isdigit() or event.unicode in '.-':
                    self.text += event.unicode
        return None
        
    def draw(self, surface):
        # Background
        pygame.draw.rect(surface, BUTTON_GLASS, self.rect, border_radius=6)
        
        # Text rendering
        if self.text:
            text_surf = main_font.render(self.text, True, (100, 0, 150))
        else:
            text_surf = main_font.render(self.placeholder, True, (100, 0, 150))
        
        text_rect = text_surf.get_rect(midleft=(self.rect.left + 10, self.rect.centery))
        surface.blit(text_surf, text_rect)