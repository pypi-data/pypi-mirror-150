from colorama import Fore, Back, Style
from typing import Optional
import os
from .getchar import getchar

class Terminal:
    _instance = None
    _updating_line = ''

    INPUT_STYLE = f'{Fore.YELLOW} > {Style.RESET_ALL}'

    def __init__(self) -> None:
        if Terminal._instance is not None:
            raise RuntimeError('Only one instance of Terminal is allowed')
        Terminal._instance = self

    @staticmethod
    def clear() -> None:
        os.system('cls' if os.name == 'nt' else 'clear')

    @staticmethod
    def bell() -> None:
        print('\a', end='')

    @staticmethod
    def input(text: str) -> str:
        Terminal.clear()
        print(text)
        inp = input(Terminal.INPUT_STYLE)
        Terminal.clear()
        return inp

    @staticmethod
    def getchar() -> bytes:
        return getchar()

    @staticmethod
    def print(*args, sep: Optional[str] = ' ') -> None:
        if Terminal._updating_line:
            s = '\r' + sep.join(list(map(str, args)))
            print(s, end=f'{" " * (len(Terminal._updating_line) - len(s))}\n')
            print(Terminal._updating_line, end='')
        else:
            print(*args, sep=sep)

    @staticmethod
    def choise(text: str, choises: list[str]) -> str:
        inp = 0
        while not isinstance(inp, int) or inp < 1 or inp > len(choises):
            Terminal.clear()
            print(text)
            for i, c in enumerate(choises):
                print(f'{Fore.RED}[{Fore.YELLOW}{i + 1}{Fore.RED}]{Style.RESET_ALL} {c}')
            try:
                print(Terminal.INPUT_STYLE, end='')
                inp = int(Terminal.getchar())
            except ValueError:
                pass
        Terminal.clear()
        return choises[inp - 1]

    @staticmethod
    def select(text: str, choises: list[str]) -> str:
        selected = 0
        Terminal.clear()
        print(f'\x1B[{len(text.splitlines()) + len(choises) + 1}A')
        while True:
            print(text)
            for i, choise in enumerate(choises):
                print(f'{Back.LIGHTBLACK_EX if i == selected else Back.BLACK}'
                      f'{choise}'
                      f'{Style.RESET_ALL}')
            char1 = Terminal.getchar()
            if char1 == b'\r':
                break
            elif char1 != b'\xe0':
                print(f'\x1B[{len(text.splitlines()) + len(choises) + 1}A')
                continue
            char2 = Terminal.getchar()
            if char1 + char2 == b'\xe0H':
                selected -= 1
                if selected < 0:
                    selected = len(choises) - 1
            elif char1 + char2 == b'\xe0P':
                selected += 1
                if selected == len(choises):
                    selected = 0
            print(f'\x1B[{len(text.splitlines()) + len(choises) + 1}A')
        Terminal.clear()
        return choises[selected]