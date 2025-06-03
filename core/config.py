from dataclasses import dataclass

@dataclass
class GameConfig:
    """Конфигурация игры"""
    width: int = 10
    height: int = 20
    initial_drop_speed: float = 0.5
    speed_increase: float = 0.95
    empty_cell: str = "·"
    filled_cell: str = "■"
