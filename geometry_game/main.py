import pygame
import numpy as np
import sys
from geometry_game.ui import GlassButton, ModernInputBox, main_font, title_font, draw_background
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
    RED
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
    
    # Transform type buttons
    scale_button = GlassButton(250, 20, 120, 40, "Scale")
    rotate_x_button = GlassButton(380, 20, 120, 40, "Rotate X")
    rotate_y_button = GlassButton(510, 20, 120, 40, "Rotate Y")
    rotate_z_button = GlassButton(640, 20, 120, 40, "Rotate Z")
    translate_button = GlassButton(770, 20, 120, 40, "Translate")

    input_boxes = {
        "scale_x": ModernInputBox(250, 70, 80, 35, placeholder="X"),
        "scale_y": ModernInputBox(340, 70, 80, 35, placeholder="Y"),
        "scale_z": ModernInputBox(430, 70, 80, 35, placeholder="Z"),
        
        "rotate_angle": ModernInputBox(250, 70, 120, 35, placeholder="Angle"),
        
        "translate_x": ModernInputBox(250, 70, 80, 35, placeholder="X"),
        "translate_y": ModernInputBox(340, 70, 80, 35, placeholder="Y"),
        "translate_z": ModernInputBox(430, 70, 80, 35, placeholder="Z"),
    }

    apply_button = GlassButton(520, 70, 100, 35, "Apply")

    current_transform_type = None

    # Auto-rotation
    auto_rotate = True
    rotation_angle = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

            if add_transform_button.is_clicked(event):
                current_transform_type = None

            if scale_button.is_clicked(event):
                current_transform_type = "scale"

            if rotate_x_button.is_clicked(event):
                current_transform_type = "rotate_x"

            if rotate_y_button.is_clicked(event):
                current_transform_type = "rotate_y"

            if rotate_z_button.is_clicked(event):
                current_transform_type = "rotate_z"

            if translate_button.is_clicked(event):
                current_transform_type = "translate"

            if apply_button.is_clicked(event) and current_transform_type:
                if current_transform_type == "scale":
                    new_transform = Transformation(
                        "scale",
                        {
                            "x": input_boxes["scale_x"].text or "1.0",
                            "y": input_boxes["scale_y"].text or "1.0",
                            "z": input_boxes["scale_z"].text or "1.0",
                        },
                    )
                    transformations.append(new_transform)

                elif current_transform_type.startswith("rotate"):
                    new_transform = Transformation(
                        current_transform_type,
                        {"angle": input_boxes["rotate_angle"].text or "45.0"},
                    )
                    transformations.append(new_transform)

                elif current_transform_type == "translate":
                    new_transform = Transformation(
                        "translate",
                        {
                            "x": input_boxes["translate_x"].text or "0.5",
                            "y": input_boxes["translate_y"].text or "0.5",
                            "z": input_boxes["translate_z"].text or "0.5",
                        },
                    )
                    transformations.append(new_transform)

            for box_name, box in input_boxes.items():
                box.handle_event(event)

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

        draw_background(screen)

        add_transform_button.draw(screen)
        scale_button.draw(screen)
        rotate_x_button.draw(screen)
        rotate_y_button.draw(screen)
        rotate_z_button.draw(screen)
        translate_button.draw(screen)

        if current_transform_type == "scale":
            text_surf = main_font.render("Scale (X, Y, Z):", True, TEXT_COLOR)
            screen.blit(text_surf, (20, 80))
            input_boxes["scale_x"].draw(screen)
            input_boxes["scale_y"].draw(screen)
            input_boxes["scale_z"].draw(screen)
            apply_button.draw(screen)

        elif current_transform_type and current_transform_type.startswith("rotate"):
            axis = current_transform_type.split("_")[1].upper()
            text_surf = main_font.render(f"Rotate {axis} (degrees):", True, TEXT_COLOR)
            screen.blit(text_surf, (20, 80))
            input_boxes["rotate_angle"].draw(screen)
            apply_button.draw(screen)

        elif current_transform_type == "translate":
            text_surf = main_font.render("Translate (X, Y, Z):", True, TEXT_COLOR)
            screen.blit(text_surf, (20, 80))
            input_boxes["translate_x"].draw(screen)
            input_boxes["translate_y"].draw(screen)
            input_boxes["translate_z"].draw(screen)
            apply_button.draw(screen)

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
                screen, ACCENT_PRIMARY, projected_points[edge[0]], projected_points[edge[1]], 2
            )

        for point in projected_points:
            pygame.draw.circle(screen, WHITE, (int(point[0]), int(point[1])), 5)

        help_text = main_font.render("Press SPACE to toggle auto-rotation", True, TEXT_COLOR)
        screen.blit(help_text, (WIDTH - 300, HEIGHT - 50))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
