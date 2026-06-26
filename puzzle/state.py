from __future__ import annotations
from typing import List, Optional, Tuple


GOAL_STATE = (1, 2, 3, 4, 5, 6, 7, 8, 0)


class State:
    """Representa um estado do 8-puzzle como tupla imutável de 9 inteiros (0 = espaço vazio)."""

    def __init__(self, tiles: Tuple[int, ...], parent: Optional["State"] = None, action: Optional[str] = None, cost: int = 0):
        if len(tiles) != 9 or set(tiles) != set(range(9)):
            raise ValueError("Estado inválido: deve conter exatamente os valores 0-8.")
        self.tiles = tiles
        self.parent = parent
        self.action = action
        self.cost = cost

    @property
    def is_goal(self) -> bool:
        return self.tiles == GOAL_STATE

    @property
    def blank_index(self) -> int:
        return self.tiles.index(0)

    def neighbors(self) -> List["State"]:
        """Retorna uma lista de estados vizinhos alcançáveis a partir deste estado."""
        moves = {
            "UP": -3,
            "DOWN": 3,
            "LEFT": -1,
            "RIGHT": 1,
        }

        blank = self.blank_index
        row, col = divmod(blank, 3)
        children: List["State"] = []

        for action, delta in moves.items():
            if action == "UP" and row == 0:
                continue
            if action == "DOWN" and row == 2:
                continue
            if action == "LEFT" and col == 0:
                continue
            if action == "RIGHT" and col == 2:
                continue

            new_index = blank + delta
            new_tiles = list(self.tiles)
            new_tiles[blank], new_tiles[new_index] = new_tiles[new_index], new_tiles[blank]

            children.append(
                State(
                    tuple(new_tiles),
                    parent=self,
                    action=action,
                    cost=self.cost + 1,
                )
            )

        return children

    def path(self) -> List["State"]:
        """Retorna a sequência de estados do estado inicial até este."""
        states: List["State"] = []
        current: Optional["State"] = self
        while current is not None:
            states.append(current)
            current = current.parent
        states.reverse()
        return states

    def actions(self) -> List[str]:
        """Retorna a sequência de ações do estado inicial até este."""
        return [state.action for state in self.path() if state.action is not None]

    def __eq__(self, other: object) -> bool:
        return isinstance(other, State) and self.tiles == other.tiles

    def __hash__(self) -> int:
        return hash(self.tiles)

    def __lt__(self, other: "State") -> bool:
        return self.cost < other.cost

    def __repr__(self) -> str:
        t = self.tiles
        return (
            f"+-------+\n"
            f"| {t[0]} {t[1]} {t[2]} |\n"
            f"| {t[3]} {t[4]} {t[5]} |\n"
            f"| {t[6]} {t[7]} {t[8]} |\n"
            f"+-------+"
        ).replace("0", " ")
