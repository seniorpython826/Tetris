from typing import List

class Shape:
    """Класс для представления фигуры тетрамино"""
    def __init__(self, matrix: List[List[int]], color_code: str, name: str):
        self.matrix = matrix
        self.color_code = color_code
        self.name = name
        self.width = len(matrix[0]) if matrix else 0
        self.height = len(matrix)

    def rotate(self) -> 'Shape':
        """Поворот фигуры на 90 градусов по часовой стрелке"""
        rotated = [list(row) for row in zip(*self.matrix[::-1])]
        return Shape(rotated, self.color_code, self.name)


class ShapeFactory:
    """Фабрика для создания фигур тетрамино"""
    SHAPES_DATA = [
        ([[1, 1, 1, 1]], "\033[36m", "I"),  # Голубой
        ([[1, 1], [1, 1]], "\033[33m", "O"),  # Желтый
        ([[1, 1, 1], [0, 1, 0]], "\033[35m", "T"),  # Пурпурный
        ([[1, 1, 1], [1, 0, 0]], "\033[34m", "J"),  # Синий
        ([[1, 1, 1], [0, 0, 1]], "\033[37m", "L"),  # Белый
        ([[0, 1, 1], [1, 1, 0]], "\033[32m", "S"),  # Зеленый
        ([[1, 1, 0], [0, 1, 1]], "\033[31m", "Z")  # Красный
    ]

    @classmethod
    def create_shape(cls, shape_idx: int) -> Shape:
        """Создание фигуры по индексу"""
        matrix, color, name = cls.SHAPES_DATA[shape_idx]
        return Shape(matrix, color, name)

    @classmethod
    def get_shape_count(cls) -> int:
        """Количество доступных фигур"""
        return len(cls.SHAPES_DATA)
