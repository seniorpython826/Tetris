import os
import time

from core.config import GameConfig
from core.game_state import GameState
from core.renderer import Renderer
from input.factory import InputHandlerFactory

class TetrisGame:
    """Основной класс игры Tetris"""
    def __init__(self, config: GameConfig):
        self.config = config
        self.state = GameState(config)
        self.renderer = Renderer(config)
        self.input_handler = InputHandlerFactory.create_handler()

    def run(self) -> None:
        """Запуск основного игрового цикла"""
        if os.name == 'nt':
            os.system('color')

        while not self.state.game_over:
            current_time = time.time()

            if current_time - self.state.last_drop_time > self.state.drop_speed:
                if not self.state.move_piece(0, 1):
                    self.state.lock_piece()
                else:
                    self.state.last_drop_time = current_time

            self._process_input()
            self._render()

            time.sleep(0.01)

        self._render()
        if os.name == 'nt':
            os.system('pause')

    def _process_input(self) -> None:
        """Обработка пользовательского ввода"""
        cmd = self.input_handler.get_command()
        if cmd == 'left':
            self.state.move_piece(-1, 0)
        elif cmd == 'right':
            self.state.move_piece(1, 0)
        elif cmd == 'down':
            self.state.move_piece(0, 1)
            self.state.last_drop_time = time.time()
        elif cmd == 'up':
            self.state.rotate_piece()
        elif cmd == 'space':
            self.state.drop_piece()
        elif cmd == 'quit':
            self.state.game_over = True

    def _render(self) -> None:
        """Отрисовка игры"""
        self.renderer.render(
            board=self.state.board,
            current_piece=self.state.current_piece,
            piece_x=self.state.current_x,
            piece_y=self.state.current_y,
            piece_color_idx=self.state.current_color_idx,
            score=self.state.score,
            lines_cleared=self.state.lines_cleared,
            speed=self.state.drop_speed,
            game_over=self.state.game_over
        )

def main():
    """Точка входа в игру"""
    config = GameConfig()
    game = TetrisGame(config)
    game.run()

if __name__ == "__main__":
    main()
