import itertools
from collections.abc import Iterator


class Connect4Controller:
    def __init__(self, player_token_types: tuple[str, str] = ("X", "O")):
        self._placeholder = "."
        self._board = [[self._placeholder for _ in range(5)] for _ in range(5)]
        self._player_token_types = player_token_types

    def cycle(self) -> Iterator[str]:
        yield from itertools.cycle(self._player_token_types)

    def start(self) -> None:
        for token in self.cycle():
            choice = self.get_input()
            self.insert_token(choice, token)
            self.print_board()

    @staticmethod
    def get_input() -> int:
        return int(input("Enter a number of column: \n")) - 1

    def insert_token(self, choice: int, token: str) -> None:
        for i, _row in enumerate(self._board[choice]):
            if self._board[choice][i] == ".":
                self._board[choice][i] = token
                break

    def print_board(self) -> None:
        for row in range(len(self._board[0]) - 1, -1, -1):
            for col in range(len(self._board)):
                print(self._board[col][row], end=" ")
            print()
        print(f"{' '.join(str(i) for i in range(1, len(self._board)+1))}")
