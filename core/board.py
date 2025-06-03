from typing import List

from .shapes import Shape

class Board:
    """Игровое поле"""
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.grid: List[List[int]] = [[0 for _ in range(width)] for _ in range(height)]
        self.color_reset = "\033[0m"

    def clear_lines(self) -> int:
        """Очистка заполненных линий и возврат количества очищенных"""
        lines_to_clear = [y for y in range(self.height) if all(self.grid[y])]
        for y in sorted(lines_to_clear, reverse=True):
            del self.grid[y]
            self.grid.insert(0, [0 for _ in range(self.width)])
        return len(lines_to_clear)

    def place_piece(self, piece: Shape, x: int, y: int, color_idx: int) -> None:
        """Размещение фигуры на поле"""
        for py, row in enumerate(piece.matrix):
            for px, cell in enumerate(row):
                if cell and y + py >= 0:
                    self.grid[y + py][x + px] = color_idx + 1

    def is_collision(self, piece: Shape, x: int, y: int) -> bool:
        """Проверка столкновений"""
        for py, row in enumerate(piece.matrix):
            for px, cell in enumerate(row):
                if not cell:
                    continue

                board_x = x + px
                board_y = y + py

                if (board_y >= self.height or
                        board_x < 0 or
                        board_x >= self.width or
                        (board_y >= 0 and self.grid[board_y][board_x])):
                    return True
        return False
