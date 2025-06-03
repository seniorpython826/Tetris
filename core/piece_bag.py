from collections import deque
import random
from typing import Deque

from .shapes import ShapeFactory

class PieceBag:
    """Мешок с фигурами для случайного выбора с гарантией равномерного распределения"""
    def __init__(self):
        self._pieces: Deque[int] = deque()
        self._refill_bag()

    def _refill_bag(self) -> None:
        """Заполнение мешка всеми фигурами в случайном порядке"""
        pieces = list(range(ShapeFactory.get_shape_count()))
        random.shuffle(pieces)
        self._pieces.extend(pieces)

    def get_next_piece(self) -> int:
        """Получение следующей фигуры"""
        if not self._pieces:
            self._refill_bag()
        return self._pieces.popleft()
