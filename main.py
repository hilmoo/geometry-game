import pygame
import numpy as np
import sys
from ui import Button, InputBox
from geometry import Transformation, project_point, transform_vertices
from constants import (
    WIDTH,
    HEIGHT,
    WHITE,
    BLACK,
    RED,
    GREEN,
    BLUE,
    GRAY,
    CAMERA_DISTANCE,
    SCALE,
    INITIAL_VERTICES,
    EDGES,
)


def main():
    # Initialize pygame
    pygame.init()

    # Window setup
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("3D Matrix Transformation")

    # Font setup
    font = pygame.font.SysFont("Arial", 16)

    # Convert vertices to numpy array
    initial_vertices = np.array(INITIAL_VERTICES, dtype=float)

    clock = pygame.time.Clock()
    running = True

    # Object state
    transformations = []

    add_transform_button = Button(10, 10, 180, 30, "Add Transformation", GREEN)
    scale_button = Button(200, 10, 100, 30, "Scale", BLUE)
    rotate_x_button = Button(310, 10, 100, 30, "Rotate X", BLUE)
    rotate_y_button = Button(420, 10, 100, 30, "Rotate Y", BLUE)
    rotate_z_button = Button(530, 10, 100, 30, "Rotate Z", BLUE)
    translate_button = Button(640, 10, 100, 30, "Translate", BLUE)

    input_boxes = {
        "scale_x": InputBox(200, 50, 60, 30, "1.0"),
        "scale_y": InputBox(270, 50, 60, 30, "1.0"),
        "scale_z": InputBox(340, 50, 60, 30, "1.0"),
        "rotate_angle": InputBox(200, 50, 60, 30, "45.0"),
        "translate_x": InputBox(200, 50, 60, 30, "0.5"),
        "translate_y": InputBox(270, 50, 60, 30, "0.5"),
        "translate_z": InputBox(340, 50, 60, 30, "0.5"),
    }

    apply_button = Button(200, 90, 100, 30, "Apply", GREEN)

    current_transform_type = None

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
                            "x": input_boxes["scale_x"].text,
                            "y": input_boxes["scale_y"].text,
                            "z": input_boxes["scale_z"].text,
                        },
                    )
                    transformations.append(new_transform)

                elif current_transform_type.startswith("rotate"):
                    new_transform = Transformation(
                        current_transform_type,
                        {"angle": input_boxes["rotate_angle"].text},
                    )
                    transformations.append(new_transform)

                elif current_transform_type == "translate":
                    new_transform = Transformation(
                        "translate",
                        {
                            "x": input_boxes["translate_x"].text,
                            "y": input_boxes["translate_y"].text,
                            "z": input_boxes["translate_z"].text,
                        },
                    )
                    transformations.append(new_transform)

            for box_name, box in input_boxes.items():
                box.handle_event(event)

            for i, transform in enumerate(transformations):
                delete_button_rect = pygame.Rect(WIDTH - 40, 150 + i * 30, 30, 20)
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

        screen.fill(WHITE)

        add_transform_button.draw(screen, font)
        scale_button.draw(screen, font)
        rotate_x_button.draw(screen, font)
        rotate_y_button.draw(screen, font)
        rotate_z_button.draw(screen, font)
        translate_button.draw(screen, font)

        if current_transform_type == "scale":
            text_surf = font.render("Scale (X, Y, Z):", True, BLACK)
            screen.blit(text_surf, (10, 60))
            input_boxes["scale_x"].draw(screen, font)
            input_boxes["scale_y"].draw(screen, font)
            input_boxes["scale_z"].draw(screen, font)
            apply_button.draw(screen, font)

        elif current_transform_type and current_transform_type.startswith("rotate"):
            axis = current_transform_type.split("_")[1].upper()
            text_surf = font.render(f"Rotate {axis} (degrees):", True, BLACK)
            screen.blit(text_surf, (10, 60))
            input_boxes["rotate_angle"].draw(screen, font)
            apply_button.draw(screen, font)

        elif current_transform_type == "translate":
            text_surf = font.render("Translate (X, Y, Z):", True, BLACK)
            screen.blit(text_surf, (10, 60))
            input_boxes["translate_x"].draw(screen, font)
            input_boxes["translate_y"].draw(screen, font)
            input_boxes["translate_z"].draw(screen, font)
            apply_button.draw(screen, font)

        text_surf = font.render("Applied Transformations:", True, BLACK)
        screen.blit(text_surf, (10, 130))

        for i, transform in enumerate(transformations):
            text = f"{i+1}. {transform.get_display_text()}"
            text_surf = font.render(text, True, BLACK)
            screen.blit(text_surf, (30, 150 + i * 30))

            delete_button_rect = pygame.Rect(WIDTH - 40, 150 + i * 30, 30, 20)
            pygame.draw.rect(screen, RED, delete_button_rect)
            text_surf = font.render("X", True, WHITE)
            screen.blit(text_surf, (WIDTH - 30, 150 + i * 30))

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
                screen, BLACK, projected_points[edge[0]], projected_points[edge[1]], 2
            )

        for point in projected_points:
            pygame.draw.circle(screen, RED, (int(point[0]), int(point[1])), 5)

        help_text = font.render("Press SPACE to toggle auto-rotation", True, BLACK)
        screen.blit(help_text, (WIDTH - 250, HEIGHT - 30))

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()
