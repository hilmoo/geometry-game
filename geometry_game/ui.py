import pygame
from geometry_game.constants import (
    BUTTON_GLASS,
    BUTTON_BORDER,
    WHITE,
    BACKGROUND_GRADIENT,
    WIDTH,
    HEIGHT,
    TRANSFORM_COLORS,
    RED,
)

# Font setup
pygame.font.init()
title_font = pygame.font.Font(None, 36)
main_font = pygame.font.Font(None, 24)


def draw_background(surface):
    for i in range(HEIGHT):
        color = [
            BACKGROUND_GRADIENT[0][j]
            + (BACKGROUND_GRADIENT[1][j] - BACKGROUND_GRADIENT[0][j]) * (i / HEIGHT)
            for j in range(3)
        ]
        pygame.draw.line(surface, color, (0, i), (WIDTH, i))


class GlassButton:
    """A button with a semi-transparent glass-like appearance."""

    def __init__(self, x, y, width, height, text):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text

    def draw(self, surface):
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = self.rect.collidepoint(mouse_pos)

        button_color = (255, 255, 255, 80) if is_hovered else BUTTON_GLASS
        border_color = (255, 255, 255, 150) if is_hovered else BUTTON_BORDER

        button_surface = pygame.Surface(
            (self.rect.width, self.rect.height), pygame.SRCALPHA
        )
        pygame.draw.rect(
            button_surface,
            button_color,
            (0, 0, self.rect.width, self.rect.height),
            border_radius=10,
        )
        pygame.draw.rect(
            button_surface,
            border_color,
            (0, 0, self.rect.width, self.rect.height),
            width=2,
            border_radius=10,
        )

        surface.blit(button_surface, (self.rect.x, self.rect.y))

        text_surf = main_font.render(self.text, True, WHITE)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, event):
        return (
            event.type == pygame.MOUSEBUTTONDOWN
            and event.button == 1
            and self.rect.collidepoint(event.pos)
        )


class InputBox:
    """A text input box with selection highlighting and numeric input focus."""

    def __init__(self, x, y, width, height, text="0", placeholder=""):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text if text else "0"
        self.placeholder = placeholder
        self.active = False
        self.selected = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            was_active = self.active
            self.active = self.rect.collidepoint(event.pos)

            if self.active:
                self.selected = True

        if event.type == pygame.KEYDOWN and self.active:
            if event.key == pygame.K_RETURN:
                self.selected = False
                return self.text
            elif event.key == pygame.K_BACKSPACE:
                if self.selected:
                    self.text = ""
                    self.selected = False
                else:
                    self.text = self.text[:-1]

                if not self.text:
                    self.text = "0"
            else:
                if event.unicode.isdigit() or event.unicode in ".-":
                    if self.selected:
                        self.text = event.unicode
                        self.selected = False
                    else:
                        self.text += event.unicode
        return None

    def draw(self, surface):
        pygame.draw.rect(surface, BUTTON_GLASS, self.rect, border_radius=6)

        if self.text:
            if self.active and self.selected:
                text_surf = main_font.render(self.text, True, (255, 255, 255))
                text_rect = text_surf.get_rect(
                    midleft=(self.rect.left + 10, self.rect.centery)
                )
                selection_rect = text_rect.inflate(4, 4)
                pygame.draw.rect(
                    surface, (100, 100, 255), selection_rect, border_radius=3
                )

            text_color = (
                (255, 255, 255) if (self.active and self.selected) else (100, 0, 150)
            )
            text_surf = main_font.render(self.text, True, text_color)
            text_rect = text_surf.get_rect(
                midleft=(self.rect.left + 10, self.rect.centery)
            )
            surface.blit(text_surf, text_rect)
        else:
            text_surf = main_font.render(self.placeholder, True, (100, 0, 150))
            text_rect = text_surf.get_rect(
                midleft=(self.rect.left + 10, self.rect.centery)
            )
            surface.blit(text_surf, text_rect)


class PopupMenu:
    """A popup menu that displays a list of selectable options."""

    def __init__(self, x, y, width, options):
        self.x = x
        self.y = y
        self.width = width
        self.options = options
        self.visible = False
        self.buttons = []
        self.just_opened = False
        self._create_buttons()

    def _create_buttons(self):
        self.buttons = []
        for i, option in enumerate(self.options):
            btn = GlassButton(self.x, self.y + i * 45, self.width, 40, option)
            self.buttons.append(btn)

    def show(self):
        self.visible = True
        self.just_opened = True

    def hide(self):
        self.visible = False
        self.just_opened = False

    def draw(self, surface):
        if not self.visible:
            return

        panel_height = len(self.options) * 45
        panel_rect = pygame.Rect(
            self.x - 5, self.y - 5, self.width + 10, panel_height + 10
        )
        panel_surface = pygame.Surface(
            (panel_rect.width, panel_rect.height), pygame.SRCALPHA
        )
        pygame.draw.rect(
            panel_surface,
            (30, 30, 60, 220),
            (0, 0, panel_rect.width, panel_rect.height),
            border_radius=12,
        )
        pygame.draw.rect(
            panel_surface,
            (120, 120, 180, 180),
            (0, 0, panel_rect.width, panel_rect.height),
            width=2,
            border_radius=12,
        )
        surface.blit(panel_surface, (panel_rect.x, panel_rect.y))

        for btn in self.buttons:
            btn.draw(surface)

    def handle_event(self, event):
        if not self.visible:
            return None

        for i, btn in enumerate(self.buttons):
            if btn.is_clicked(event):
                self.hide()
                return self.options[i]

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.just_opened:
                self.just_opened = False
                return None

            x, y = event.pos
            panel_height = len(self.options) * 45
            if not (
                self.x <= x <= self.x + self.width
                and self.y <= y <= self.y + panel_height
            ):
                self.hide()

        return None


class PopupForm:
    """A form dialog that collects input values for transformations."""

    def __init__(self, title, fields, apply_text="Apply"):
        self.title = title
        self.fields = fields
        self.apply_text = apply_text
        self.visible = False
        self.just_opened = False
        self.width = 450
        self.height = 70 + len(fields) * 50 + 60
        self.x = (WIDTH - self.width) // 2
        self.y = (HEIGHT - self.height) // 2

        self.input_boxes = {}
        self._create_input_boxes()

        self.apply_button = GlassButton(
            self.x + (self.width - 120) // 2,
            self.y + self.height - 50,
            120,
            40,
            self.apply_text,
        )

    def _create_input_boxes(self):
        self.input_boxes = {}
        for i, field in enumerate(self.fields):
            self.input_boxes[field["name"]] = InputBox(
                self.x + 150,
                self.y + 70 + i * 50,
                self.width - 170,
                35,
                text=field.get("value", "0"),
                placeholder=field.get("placeholder", ""),
            )

    def show(self):
        self.visible = True
        self.just_opened = True

    def hide(self):
        self.visible = False
        self.just_opened = False

    def draw(self, surface):
        if not self.visible:
            return

        panel_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(
            panel_surface,
            (30, 30, 60, 230),
            (0, 0, self.width, self.height),
            border_radius=15,
        )
        pygame.draw.rect(
            panel_surface,
            (120, 120, 180, 180),
            (0, 0, self.width, self.height),
            width=2,
            border_radius=15,
        )

        title_surf = title_font.render(self.title, True, WHITE)
        title_rect = title_surf.get_rect(center=(self.width // 2, 30))
        panel_surface.blit(title_surf, title_rect)

        for i, field in enumerate(self.fields):
            label_surf = main_font.render(
                field.get("label", field["name"]), True, WHITE
            )
            panel_surface.blit(label_surf, (20, 75 + i * 50))

        surface.blit(panel_surface, (self.x, self.y))

        for box in self.input_boxes.values():
            box.draw(surface)

        self.apply_button.draw(surface)

    def get_values(self):
        return {name: box.text for name, box in self.input_boxes.items()}

    def handle_event(self, event):
        if not self.visible:
            return None

        for box_name, box in self.input_boxes.items():
            box.handle_event(event)

        if self.apply_button.is_clicked(event):
            result = {"action": "apply", "values": self.get_values()}
            self.hide()
            return result

        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.just_opened:
                self.just_opened = False
                return None

            x, y = event.pos
            if not (
                self.x <= x <= self.x + self.width
                and self.y <= y <= self.y + self.height
            ):
                self.hide()
                return {"action": "cancel"}

        return None

    def reset_values(self):
        """Reset all input boxes to their default values from fields definition"""
        for field in self.fields:
            field_name = field["name"]
            default_value = field.get("value", "0")
            if field_name in self.input_boxes:
                self.input_boxes[field_name].text = default_value
                self.input_boxes[field_name].selected = False


class TransformListPopup:
    """A popup that displays and manages the list of applied transformations."""

    def __init__(self, transformations):
        self.transformations = transformations
        self.visible = False
        self.just_opened = False
        self.width = 500
        self.max_visible_items = 10
        self.item_height = 40
        self.padding = 20
        self.title_height = 50

        self._update_size_and_position()

    def _update_size_and_position(self):
        items_count = max(1, min(len(self.transformations), self.max_visible_items))
        content_height = items_count * self.item_height
        self.height = self.title_height + content_height + self.padding * 2

        self.x = (WIDTH - self.width) // 2
        self.y = (HEIGHT - self.height) // 2

        self.total_content_height = len(self.transformations) * self.item_height
        visible_content_height = self.max_visible_items * self.item_height
        self.max_scroll = max(0, self.total_content_height - visible_content_height)
        self.scroll_offset = 0

    def update_transformations(self, transformations):
        """Update transformation list and recalculate sizes"""
        self.transformations = transformations
        self._update_size_and_position()

    def show(self):
        self.visible = True
        self.just_opened = True
        self.scroll_offset = 0

    def hide(self):
        self.visible = False
        self.just_opened = False

    def handle_event(self, event):
        if not self.visible:
            return None

        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 4:  # Scroll up
                self.scroll_offset = max(0, self.scroll_offset - 20)
                return None
            elif event.button == 5:  # Scroll down
                self.scroll_offset = min(self.max_scroll, self.scroll_offset + 20)
                return None

            if event.button == 1:
                for i, transform in enumerate(self.transformations):
                    item_y = (
                        self.title_height + i * self.item_height - self.scroll_offset
                    )

                    if (
                        item_y + self.item_height > self.title_height
                        and item_y < self.height - self.padding
                    ):
                        delete_btn_x = self.x + self.width - 50
                        delete_btn_y = self.y + item_y + 10
                        delete_btn_rect = pygame.Rect(
                            delete_btn_x, delete_btn_y, 20, 20
                        )

                        if delete_btn_rect.collidepoint(event.pos):
                            return {"action": "delete", "index": i}

                if self.just_opened:
                    self.just_opened = False
                    return None

                if not pygame.Rect(
                    self.x, self.y, self.width, self.height
                ).collidepoint(event.pos):
                    self.hide()
                    return {"action": "close"}

        return None

    def draw(self, surface):
        if not self.visible:
            return

        panel_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        pygame.draw.rect(
            panel_surface,
            (30, 30, 60, 220),
            (0, 0, self.width, self.height),
            border_radius=15,
        )
        pygame.draw.rect(
            panel_surface,
            (120, 120, 180, 180),
            (0, 0, self.width, self.height),
            width=2,
            border_radius=15,
        )

        title_surf = title_font.render("Applied Transformations", True, WHITE)
        title_rect = title_surf.get_rect(center=(self.width // 2, 25))
        panel_surface.blit(title_surf, title_rect)

        content_rect = pygame.Rect(
            self.padding,
            self.title_height,
            self.width - self.padding * 2,
            self.height - self.title_height - self.padding,
        )

        panel_surface.set_clip(content_rect)

        if not self.transformations:
            no_trans_surf = main_font.render(
                "No transformations applied yet", True, WHITE
            )
            no_trans_rect = no_trans_surf.get_rect(
                center=(self.width // 2, self.title_height + 20)
            )
            panel_surface.blit(no_trans_surf, no_trans_rect)
        else:
            for i, transform in enumerate(self.transformations):
                item_y = self.title_height + i * self.item_height - self.scroll_offset

                if (
                    item_y + self.item_height > self.title_height
                    and item_y < self.height - self.padding
                ):
                    item_bg = pygame.Rect(
                        self.padding,
                        item_y,
                        self.width - self.padding * 2,
                        self.item_height - 5,
                    )
                    pygame.draw.rect(
                        panel_surface,
                        (120, 120, 180, 180),
                        item_bg,
                        border_radius=8,
                    )

                    text = f"{i+1}. {transform.get_display_text()}"
                    text_surf = main_font.render(text, True, WHITE)
                    panel_surface.blit(
                        text_surf,
                        (
                            self.padding + 10,
                            item_y + (self.item_height - text_surf.get_height()) // 2,
                        ),
                    )

                    x_text = main_font.render("X", True, RED)
                    x_rect = x_text.get_rect(
                        center=(self.width - 40, item_y + self.item_height // 2)
                    )
                    panel_surface.blit(x_text, x_rect)

        panel_surface.set_clip(None)

        if self.transformations and self.total_content_height > (
            self.height - self.title_height - self.padding * 2
        ):
            visible_ratio = min(
                1.0,
                (self.height - self.title_height - self.padding * 2)
                / self.total_content_height,
            )
            scrollbar_height = max(
                30,
                int(
                    visible_ratio * (self.height - self.title_height - self.padding * 2)
                ),
            )
            scroll_ratio = (
                self.scroll_offset / self.max_scroll if self.max_scroll > 0 else 0
            )
            scrollbar_y = self.title_height + int(
                scroll_ratio
                * (
                    self.height
                    - self.title_height
                    - self.padding * 2
                    - scrollbar_height
                )
            )

            pygame.draw.rect(
                panel_surface,
                (180, 180, 220, 150),
                (self.width - 15, scrollbar_y, 10, scrollbar_height),
                border_radius=5,
            )

        surface.blit(panel_surface, (self.x, self.y))
