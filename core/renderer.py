import os
from typing import Optional

from .config import GameConfig
from .board import Board
from .shapes import Shape, ShapeFactory


class Renderer:
    """Класс для отрисовки игры"""

    def __init__(self, config: GameConfig):
        self.config = config
        self.color_reset = "\033[0m"

    def clear_screen(self) -> None:
        """Очистка экрана"""
        os.system('cls' if os.name == 'nt' else 'clear')

    def render(self, board: Board, current_piece: Optional[Shape],
               piece_x: int, piece_y: int, piece_color_idx: int,
               score: int, lines_cleared: int, speed: float, game_over: bool) -> None:
        """Отрисовка игрового состояния"""
        self.clear_screen()

        print("╔" + "═" * (self.config.width * 2) + "╗")

        for y in range(self.config.height):
            print("║", end="")
            for x in range(self.config.width):
                if (current_piece and not game_over and
                        self._is_piece_cell(current_piece, piece_x, piece_y, x, y)):
                    color = ShapeFactory.SHAPES_DATA[piece_color_idx][1]
                    print(f"{color}{self.config.filled_cell}{self.color_reset}", end=" ")
                else:
                    self._render_board_cell(board, x, y)
            print("║")

        print("╚" + "═" * (self.config.width * 2) + "╝")
        print(f"\nСчет: {score}")
        print(f"Линии: {lines_cleared}")
        print(f"Скорость: {1 / speed:.1f} фигур/сек")

        if game_over:
            print("\nИГРА ОКОНЧЕНА!")
            print("Нажмите любую клавишу для выхода...")

    @staticmethod
    def _is_piece_cell(piece: Shape, piece_x: int, piece_y: int, x: int, y: int) -> bool:
        """Проверяет, является ли клетка частью текущей фигуры"""
        for py, row in enumerate(piece.matrix):
            for px, cell in enumerate(row):
                if cell and piece_y + py == y and piece_x + px == x:
                    return True
        return False

    def _render_board_cell(self, board: Board, x: int, y: int) -> None:
        """Отрисовка клетки поля"""
        if board.grid[y][x]:
            color_idx = board.grid[y][x] - 1
            color = ShapeFactory.SHAPES_DATA[color_idx][1]
            print(f"{color}{self.config.filled_cell}{self.color_reset}", end=" ")
        else:
            print(f"{self.config.empty_cell}", end=" ")
