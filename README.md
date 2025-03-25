# Geometry Game

A simple geometry game implemented in Python.

## Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.8 or higher
- Poetry 2.0 or higher

## Installation and Setup

1. Clone this repository:
  ```
  git clone https://github.com/yourusername/geometry-game.git
  cd geometry-game
  ```

2. Install dependencies using Poetry:
  ```
  poetry install
  ```

3. Activate the virtual environment:
  ```
  poetry env activate
  ```

## Running the Game

To start the geometry game:
```
poetry run python -m geometry_game
```

## Development

To add new dependencies:
```
poetry add package-name
```

To add development dependencies:
```
poetry add --group dev package-name
```

## Project Structure

```
geometry-game/
├── geometry_game/
│   ├── __init__.py
│   ├── main.py
│   └── ...
├── pyproject.toml
└── README.md
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.