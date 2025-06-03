from abc import ABC, abstractmethod
from typing import Optional

class InputHandler(ABC):
    """Абстрактный класс для обработки ввода"""
    @abstractmethod
    def get_command(self) -> Optional[str]:
        pass
