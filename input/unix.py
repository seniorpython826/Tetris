import sys
import select
from typing import Optional

from .base import InputHandler

class UnixInputHandler(InputHandler):
    """Обработчик ввода для Linux/Mac"""
    SPECIAL_KEYS = {
        'A': 'up',
        'B': 'down',
        'D': 'left',
        'C': 'right'
    }

    def get_command(self) -> Optional[str]:
        if not select.select([sys.stdin], [], [], 0)[0]:
            return None

        ch = sys.stdin.read(1)
        if ch == '\x1b':  # Специальные клавиши
            sys.stdin.read(1)  # Пропускаем '['
            ch = sys.stdin.read(1)
            return self.SPECIAL_KEYS.get(ch, None)
        elif ch == ' ':
            return 'space'
        elif ch == 'q':
            return 'quit'
        return None
