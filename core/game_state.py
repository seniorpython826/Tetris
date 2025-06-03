import time
from typing import Optional

from .config import GameConfig
from .board import Board
from .piece_bag import PieceBag
from .shapes import Shape, ShapeFactory


class GameState:
    """Состояние игры"""

    def __init__(self, config: GameConfig):
        self.config = config
        self.board = Board(config.width, config.height)
        self.piece_bag = PieceBag()
        self.current_piece: Optional[Shape] = None
        self.next_piece: Optional[Shape] = None
        self.current_x = 0
        self.current_y = 0
        self.current_color_idx = 0
        self.next_color_idx = 0
        self.score = 0
        self.lines_cleared = 0
        self.game_over = False
        self.drop_speed = config.initial_drop_speed
        self.last_drop_time = time.time()
        self._initialize_game()

    def _initialize_game(self) -> None:
        """Инициализация новой игры"""
        self._new_piece()
        self._prepare_next_piece()

    def _new_piece(self) -> None:
        """Создание новой фигуры"""
        if self.next_piece:
            self.current_piece = self.next_piece
            self.current_color_idx = self.next_color_idx
        else:
            piece_idx = self.piece_bag.get_next_piece()
            self.current_piece = ShapeFactory.create_shape(piece_idx)
            self.current_color_idx = piece_idx

        self.current_x = self.config.width // 2 - self.current_piece.width // 2
        self.current_y = 0

        if self.board.is_collision(self.current_piece, self.current_x, self.current_y):
            self.game_over = True

    def _prepare_next_piece(self) -> None:
        """Подготовка следующей фигуры"""
        piece_idx = self.piece_bag.get_next_piece()
        self.next_piece = ShapeFactory.create_shape(piece_idx)
        self.next_color_idx = piece_idx

    def rotate_piece(self) -> None:
        """Поворот текущей фигуры"""
        if not self.current_piece:
            return

        rotated = self.current_piece.rotate()
        old_piece = self.current_piece
        old_x = self.current_x

        self.current_piece = rotated
        self.current_x = min(max(self.current_x, 0),
                             self.config.width - self.current_piece.width)

        if self.board.is_collision(self.current_piece, self.current_x, self.current_y):
            self.current_piece = old_piece
            self.current_x = old_x

    def move_piece(self, dx: int, dy: int) -> bool:
        """Перемещение фигуры"""
        self.current_x += dx
        self.current_y += dy

        if self.board.is_collision(self.current_piece, self.current_x, self.current_y):
            self.current_x -= dx
            self.current_y -= dy
            return False
        return True

    def drop_piece(self) -> None:
        """Мгновенное падение фигуры"""
        while self.move_piece(0, 1):
            pass
        self.lock_piece()

    def lock_piece(self) -> None:
        """Фиксация фигуры на поле"""
        if not self.current_piece:
            return

        self.board.place_piece(self.current_piece,
                               self.current_x, self.current_y,
                               self.current_color_idx)

        cleared = self.board.clear_lines()
        self._update_game_stats(cleared)
        self._new_piece()
        self._prepare_next_piece()
        self.last_drop_time = time.time()

    def _update_game_stats(self, lines_cleared: int) -> None:
        """Обновление статистики игры"""
        if not lines_cleared:
            return

        self.lines_cleared += lines_cleared
        if self.lines_cleared % 10 == 0:
            self.drop_speed *= self.config.speed_increase

        self.score += [100, 300, 500, 800][min(lines_cleared - 1, 3)]
