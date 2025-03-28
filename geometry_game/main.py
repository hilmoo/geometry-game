import pygame
import numpy as np
import sys
from geometry_game.ui import (
    GlassButton,
    ModernInputBox,
    main_font,
    title_font,
    draw_background,
    PopupMenu,
    PopupForm,
)
from geometry_game.geometry import Transformation, project_point, transform_vertices
from geometry_game.constants import (
    WIDTH,
    HEIGHT,
    WHITE,
    ACCENT_PRIMARY,
    TEXT_COLOR,
    CAMERA_DISTANCE,
    SCALE,
    INITIAL_VERTICES,
    EDGES,
    RED,
)


def main():
    # Initialize pygame
    pygame.init()

    # Window setup
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("3D Matrix Transformation")

    # Convert vertices to numpy array
    initial_vertices = np.array(INITIAL_VERTICES, dtype=float)

    clock = pygame.time.Clock()
    running = True

    # Object state
    transformations = []

    # UI Elements
    add_transform_button = GlassButton(20, 20, 200, 50, "Add Transformation")

    # Transform popup menu
    transform_menu = PopupMenu(
        20, 80, 200, ["Scale", "Rotate X", "Rotate Y", "Rotate Z", "Translate"]
    )

    # Transformation forms
    popup_forms = {
        "Scale": PopupForm(
            "Scale Transformation",
            [
                {"name": "x", "label": "Scale X:", "placeholder": "1.0", "value": "1"},
                {"name": "y", "label": "Scale Y:", "placeholder": "1.0", "value": "1"},
                {"name": "z", "label": "Scale Z:", "placeholder": "1.0", "value": "1"},
            ],
        ),
        "Rotate X": PopupForm(
            "Rotate X Transformation",
            [
                {
                    "name": "angle",
                    "label": "Angle (degrees):",
                    "placeholder": "45.0",
                    "value": "45",
                }
            ],
        ),
        "Rotate Y": PopupForm(
            "Rotate Y Transformation",
            [
                {
                    "name": "angle",
                    "label": "Angle (degrees):",
                    "placeholder": "45.0",
                    "value": "45",
                }
            ],
        ),
        "Rotate Z": PopupForm(
            "Rotate Z Transformation",
            [
                {
                    "name": "angle",
                    "label": "Angle (degrees):",
                    "placeholder": "45.0",
                    "value": "45",
                }
            ],
        ),
        "Translate": PopupForm(
            "Translate Transformation",
            [
                {
                    "name": "x",
                    "label": "Translate X:",
                    "placeholder": "0.5",
                    "value": "0",
                },
                {
                    "name": "y",
                    "label": "Translate Y:",
                    "placeholder": "0.5",
                    "value": "0",
                },
                {
                    "name": "z",
                    "label": "Translate Z:",
                    "placeholder": "0.5",
                    "value": "0",
                },
            ],
        ),
    }

    current_popup_form = None

    # Auto-rotation
    auto_rotate = True
    rotation_angle = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            # Add debug information for button click
            if add_transform_button.is_clicked(event):
                print("Add transform button clicked!")  # Debug output
                transform_menu.show()

            # Handle transform menu
            transform_option = transform_menu.handle_event(event)
            if transform_option:
                print(f"Selected option: {transform_option}")  # Debug output
                popup_forms[transform_option].show()
                current_popup_form = transform_option
                print(
                    f"Showing form: {current_popup_form}, Visible: {popup_forms[transform_option].visible}"
                )  # Debug

            # Handle form popup
            if current_popup_form:
                print(
                    f"Current form: {current_popup_form}, Visible: {popup_forms[current_popup_form].visible}"
                )  # Debug
                form_result = popup_forms[current_popup_form].handle_event(event)
                if form_result and form_result.get("action") == "apply":
                    print(f"Form applied: {form_result}")  # Debug
                    values = form_result.get("values", {})

                    if current_popup_form == "Scale":
                        new_transform = Transformation(
                            "scale",
                            {
                                "x": values.get("x", "1"),
                                "y": values.get("y", "1"),
                                "z": values.get("z", "1"),
                            },
                        )
                        transformations.append(new_transform)

                    elif current_popup_form == "Rotate X":
                        new_transform = Transformation(
                            "rotate_x", {"angle": values.get("angle", "45")}
                        )
                        transformations.append(new_transform)

                    elif current_popup_form == "Rotate Y":
                        new_transform = Transformation(
                            "rotate_y", {"angle": values.get("angle", "45")}
                        )
                        transformations.append(new_transform)

                    elif current_popup_form == "Rotate Z":
                        new_transform = Transformation(
                            "rotate_z", {"angle": values.get("angle", "45")}
                        )
                        transformations.append(new_transform)

                    elif current_popup_form == "Translate":
                        new_transform = Transformation(
                            "translate",
                            {
                                "x": values.get("x", "0"),
                                "y": values.get("y", "0"),
                                "z": values.get("z", "0"),
                            },
                        )
                        transformations.append(new_transform)

                    current_popup_form = None

            # Delete transformation buttons
            for i, transform in enumerate(transformations):
                delete_button_rect = pygame.Rect(WIDTH - 40, 200 + i * 30, 30, 20)
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if delete_button_rect.collidepoint(event.pos):
                        transformations.pop(i)
                        break

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                auto_rotate = not auto_rotate

        if auto_rotate:
            rotation_angle += 1
            if rotation_angle >= 360:
                rotation_angle = 0

        # Drawing
        draw_background(screen)

        # Draw regular UI elements first
        add_transform_button.draw(screen)

        # Draw transformations list
        text_surf = main_font.render("Applied Transformations:", True, TEXT_COLOR)
        screen.blit(text_surf, (20, 170))

        for i, transform in enumerate(transformations):
            text = f"{i+1}. {transform.get_display_text()}"
            text_surf = main_font.render(text, True, TEXT_COLOR)
            screen.blit(text_surf, (40, 200 + i * 30))

            delete_button_rect = pygame.Rect(WIDTH - 40, 200 + i * 30, 30, 20)
            pygame.draw.rect(screen, RED, delete_button_rect)
            text_surf = main_font.render("X", True, WHITE)
            screen.blit(text_surf, (WIDTH - 30, 200 + i * 30))

        # Apply transformations and render the 3D object
        auto_rotation = Transformation("rotate_y", {"angle": str(rotation_angle)})
        view_transformations = transformations.copy()
        if auto_rotate:
            view_transformations.append(auto_rotation)

        transformed_vertices = transform_vertices(
            initial_vertices, view_transformations
        )

        projected_points = []
        for vertex in transformed_vertices:
            point_2d = project_point(vertex, CAMERA_DISTANCE)
            x = point_2d[0] * SCALE + WIDTH // 2
            y = point_2d[1] * SCALE + HEIGHT // 2
            projected_points.append((x, y))

        for edge in EDGES:
            pygame.draw.line(
                screen,
                ACCENT_PRIMARY,
                projected_points[edge[0]],
                projected_points[edge[1]],
                2,
            )

        for point in projected_points:
            pygame.draw.circle(screen, WHITE, (int(point[0]), int(point[1])), 5)

        help_text = main_font.render(
            "Press SPACE to toggle auto-rotation", True, TEXT_COLOR
        )
        screen.blit(help_text, (WIDTH - 300, HEIGHT - 50))

        # Draw popups last to ensure they appear on top of everything else
        transform_menu.draw(screen)

        if current_popup_form and popup_forms[current_popup_form].visible:
            popup_forms[current_popup_form].draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
