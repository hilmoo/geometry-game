import pygame
from constants import BLACK, GRAY, WHITE


class Button:
    def __init__(self, x, y, width, height, text, color=GRAY):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.hover_color = (
            min(color[0] + 30, 255),
            min(color[1] + 30, 255),
            min(color[2] + 30, 255),
        )
        self.active_color = color

    def draw(self, surface, font):
        mouse_pos = pygame.mouse.get_pos()
        current_color = (
            self.hover_color if self.rect.collidepoint(mouse_pos) else self.active_color
        )

        pygame.draw.rect(surface, current_color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)  # Border

        text_surf = font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            return self.rect.collidepoint(event.pos)
        return False


class InputBox:
    def __init__(self, x, y, width, height, text=""):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.active = False
        self.color = GRAY
        self.active_color = WHITE

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.active = self.rect.collidepoint(event.pos)

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                return self.text
            elif event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            else:
                if (
                    event.unicode.isdigit()
                    or event.unicode == "."
                    or event.unicode == "-"
                ):
                    self.text += event.unicode
        return None

    def draw(self, surface, font):
        color = self.active_color if self.active else self.color

        pygame.draw.rect(surface, color, self.rect)
        pygame.draw.rect(surface, BLACK, self.rect, 2)

        text_surf = font.render(self.text, True, BLACK)
        text_rect = text_surf.get_rect(midleft=(self.rect.left + 5, self.rect.centery))
        surface.blit(text_surf, text_rect)
