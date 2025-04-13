import pygame
import numpy as np
import sys
from geometry_game.ui import (
    GlassButton,
    main_font,
    draw_background,
    PopupMenu,
    PopupForm,
    TransformListPopup,
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
)


def main():

    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("3D Matrix Transformation")

    initial_vertices = np.array(INITIAL_VERTICES, dtype=float)

    clock = pygame.time.Clock()
    running = True

    transformations = []

    view_transforms_button = GlassButton(20, 20, 250, 50, "Applied Transformations")
    add_transform_button = GlassButton(20, 80, 250, 50, "Add Transformation")

    transform_menu = PopupMenu(
        20,
        140,
        200,
        ["Scale", "Rotate X", "Rotate Y", "Rotate Z", "Translate", "Shear"],
    )

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
        "Shear": PopupForm(
            "Shear Transformation",
            [
                {
                    "name": "xy",
                    "label": "Shear XY:",
                    "placeholder": "0.0",
                    "value": "0",
                },
                {
                    "name": "xz",
                    "label": "Shear XZ:",
                    "placeholder": "0.0",
                    "value": "0",
                },
                {
                    "name": "yx",
                    "label": "Shear YX:",
                    "placeholder": "0.0",
                    "value": "0",
                },
                {
                    "name": "yz",
                    "label": "Shear YZ:",
                    "placeholder": "0.0",
                    "value": "0",
                },
                {
                    "name": "zx",
                    "label": "Shear ZX:",
                    "placeholder": "0.0",
                    "value": "0",
                },
                {
                    "name": "zy",
                    "label": "Shear ZY:",
                    "placeholder": "0.0",
                    "value": "0",
                },
            ],
        ),
    }

    current_popup_form = None
    transform_list_popup = TransformListPopup(transformations)

    auto_rotate = True
    rotation_angle = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if add_transform_button.is_clicked(event):
                transform_menu.show()

            if view_transforms_button.is_clicked(event):
                transform_list_popup.update_transformations(transformations)
                transform_list_popup.show()

            transform_option = transform_menu.handle_event(event)
            if transform_option:
                popup_forms[transform_option].reset_values()
                popup_forms[transform_option].show()
                current_popup_form = transform_option

            if transform_list_popup.visible:
                list_result = transform_list_popup.handle_event(event)
                if list_result:
                    if list_result.get("action") == "delete":
                        index = list_result.get("index")
                        if 0 <= index < len(transformations):
                            transformations.pop(index)
                            transform_list_popup.update_transformations(transformations)
                    elif list_result.get("action") == "close":
                        pass

            if current_popup_form:
                form_result = popup_forms[current_popup_form].handle_event(event)
                if form_result and form_result.get("action") == "apply":
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

                    elif current_popup_form == "Shear":
                        new_transform = Transformation(
                            "shear",
                            {
                                "xy": values.get("xy", "0"),
                                "xz": values.get("xz", "0"),
                                "yx": values.get("yx", "0"),
                                "yz": values.get("yz", "0"),
                                "zx": values.get("zx", "0"),
                                "zy": values.get("zy", "0"),
                            },
                        )
                        transformations.append(new_transform)

                    transform_list_popup.update_transformations(transformations)
                    current_popup_form = None

            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                auto_rotate = not auto_rotate

        if auto_rotate:
            rotation_angle += 1
            if rotation_angle >= 360:
                rotation_angle = 0

        draw_background(screen)

        view_transforms_button.draw(screen)
        add_transform_button.draw(screen)

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

        transform_menu.draw(screen)
        transform_list_popup.draw(screen)

        if current_popup_form and popup_forms[current_popup_form].visible:
            popup_forms[current_popup_form].draw(screen)

        if transform_list_popup and transform_list_popup.visible:
            transform_list_popup.draw(screen)

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
