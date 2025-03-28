# Window settings
WIDTH, HEIGHT = 1000, 700

# Colors
WHITE = (255, 255, 255)
ACCENT_PRIMARY = (57, 255, 20)
TEXT_COLOR = (230, 230, 240)
BUTTON_GLASS = (255, 255, 255, 50)  # Semi-transparent white
BUTTON_BORDER = (255, 255, 255, 100)  # Border dengan sedikit transparansi
HIGHLIGHT_COLOR = (70, 70, 100)
TRANSFORM_COLORS = {
    "scale": (50, 200, 150),
    "rotate": (250, 100, 100),
    "translate": (250, 180, 50),
}
BACKGROUND_GRADIENT = [(120, 40, 200), (50, 10, 120)]  # Warna gradien ungu
RED = (255, 0, 0)


# Camera settings
CAMERA_DISTANCE = 5
SCALE = 100

INITIAL_VERTICES = [
    [-1, -1, -1],
    [1, -1, -1],
    [1, 1, -1],
    [-1, 1, -1],
    [-1, -1, 1],
    [1, -1, 1],
    [1, 1, 1],
    [-1, 1, 1],
]

EDGES = [
    (0, 1),
    (1, 2),
    (2, 3),
    (3, 0),
    (4, 5),
    (5, 6),
    (6, 7),
    (7, 4),
    (0, 4),
    (1, 5),
    (2, 6),
    (3, 7),
]
