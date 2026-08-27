===== main.py =====

from game.game import Game

if __name__ == "__main__":
    Game().run()



===== game/__init__.py =====

"""Simple terminal RPG game package."""



===== game/character.py =====

from __future__ import annotations


class Character:
    """Base class shared by players and enemies."""

    def __init__(
        self,
        name: str,
        strength: int,
        defense: int,
        agility: int,
        intelligence: int,
        luck: int,
    ) -> None:
        self.name = name
        self.strength = strength
        self.defense = defense
        self.agility = agility
        self.intelligence = intelligence
        self.luck = luck

    @property
    def max_hp(self) -> int:
        """Return maximum HP based on Defense."""
        return 50 + (self.defense * 4)

    @property
    def attack_power(self) -> int:
        """Return base attack power based on Strength."""
        return self.strength * 2

    def show_stats(self) -> None:
        print(f"\n--- {self.name}'s Stats ---")
        print(f"Strength:     {self.strength}")
        print(f"Defense:      {self.defense}")
        print(f"Agility:      {self.agility}")
        print(f"Intelligence: {self.intelligence}")
        print(f"Luck:         {self.luck}")
