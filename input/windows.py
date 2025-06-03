import msvcrt
from typing import Optional

from .base import InputHandler

class WindowsInputHandler(InputHandler):
    """Обработчик ввода для Windows"""
    SPECIAL_KEYS = {
        b'H': 'up',
        b'P': 'down',
        b'K': 'left',
        b'M': 'right'
    }

    def get_command(self) -> Optional[str]:
        if not msvcrt.kbhit():
            return None

        ch = msvcrt.getch()
        if ch == b'\xe0':  # Специальные клавиши
            ch = msvcrt.getch()
            return self.SPECIAL_KEYS.get(ch, None)
        elif ch == b' ':
            return 'space'
        elif ch == b'q':
            return 'quit'
        return None
