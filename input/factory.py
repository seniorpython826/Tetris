import os

from .base import InputHandler
from .windows import WindowsInputHandler
from .unix import UnixInputHandler

class InputHandlerFactory:
    """Фабрика для создания обработчиков ввода"""
    @staticmethod
    def create_handler() -> InputHandler:
        if os.name == 'nt':
            return WindowsInputHandler()
        return UnixInputHandler()
