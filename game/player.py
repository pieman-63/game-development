        self.exp = 0
        self.exp_to_next_level =0
        self.hp = self.max_hp

        self.inventory: dict[str, iself.luck * self.CRIT_CHANCE_PER_LUCK,
        )

    @property
    def stat_growth_cap(self) -> int:
        """Maximum value obtainable through enemy stat growth."""
        return max(1, (self.level * 5) - 3)

    def gain_exp(self, amount: int) -> None:
        """Gain EXP, including the Luck-based EXP bonus."""
        exp_bonus = int(amount * (self.luck * 0.01))
        tota
        print(f"\nYou gained {total_e            self.exp -= self.exp_to_next_level
            self.level_up()

    def level_up(self) -> None:
    
        self.exp_to_next_level = int(self.exp_to_next_level * 1.25)
        self.hp = self.max_hp

        print("All stats increased by 1!")
        print("Your HP has been fully restored.")

    def stat_growth_from_enemy(self, enemy: Enemy) -> None:
        """Increase a matching stat when an enemy has a higher major stat."""at_name = enemy.major_stat
        enemy_value = getattr(enemy, stat_name)
        player_value = getattr(self, stat_name)
from __future__ import annotations

import random
from typing import TYPE_CHECKING

from .character import Character

if TYPE_CHECKING:
    from .enemy import Enemy


class Player(Character):
    """The player character."""

    STAT_POOL = 25
    CRIT_CHANCE_PER_LUCK = 0.025
    MAX_CRIT_CHANCE = 0.50
    STARTING_POTIONS = 3

    def __init__(
        self,
        name: str,
        strength: int,
        defense: int,
        agility: int,
        intelligence: int,
        luck: int,
    ) -> None:
        super().__init__(
            name, strength, defense, agility, intelligence, luck
        )

        self.level = 1
        self.exp = 0
        self.exp_to_next_level = 100
        self.hp = self.max_hp

        self.inventory: dict[str, int] = {
            "potion": self.STARTING_POTIONS
        }

    @property
    def crit_chance(self) -> float:
        return min(
            self.MAX_CRIT_CHANCE,
            self.luck * self.CRIT_CHANCE_PER_LUCK,
        )

    @property
    def stat_growth_cap(self) -> int:
        """Maximum value obtainable through enemy stat growth."""
        return max(1, (self.level * 5) - 3)

    def gain_exp(self, amount: int) -> None:
        """Gain EXP, including the Luck-based EXP bonus."""
        exp_bonus = int(amount * (self.luck * 0.01))
        total_exp = amount + exp_bonus
        self.exp += total_exp

        print(f"\nYou gained {total_exp} EXP!")

        if exp_bonus > 0:
            print(f"Luck bonus: +{exp_bonus} EXP ({self.luck} Luck)")

        while self.exp >= self.exp_to_next_level:
            self.exp -= self.exp_to_next_level
            self.level_up()

    def level_up(self) -> None:
        self.level += 1

        print("\n======================")
        print(f" LEVEL UP! You are now level {self.level}!")
        print("======================")

        self.strength += 1
        self.defense += 1
        self.agility += 1
        self.intelligence += 1
        self.luck += 1

        self.exp_to_next_level = int(self.exp_to_next_level * 1.25)
        self.hp = self.max_hp

        print("All stats increased by 1!")
        print("Your HP has been fully restored.")

    def stat_growth_from_enemy(self, enemy: Enemy) -> None:
        """Increase a matching stat when an enemy has a higher major stat."""
        stat_name = enemy.major_stat
        enemy_value = getattr(enemy, stat_name)
        player_value = getattr(self, stat_name)

        if enemy_value <= player_value:
            return

        if player_value >= self.stat_growth_cap:
            print(
                f"\nYour {stat_name} is already at its current "
                f"growth cap ({self.stat_growth_cap})."
            )
            return

        new_value = min(player_value + 1, self.stat_growth_cap)
        setattr(self, stat_name, new_value)

        print(f"\nEnemy's major stat was {stat_name.upper()}!")
        print(
            f"Your {stat_name} increased "
            f"from {player_value} to {new_value}!"
        )

    def take_damage(self, damage: float) -> None:
        self.hp = max(0, self.hp - damage)

        print(f"You took {damage:.1f} damage!")
        print(f"HP: {self.hp:.1f}/{self.max_hp}")

    def heal(self, amount: float) -> bool:
        """Heal the player. Return True when HP actually increased."""
        if self.hp >= self.max_hp:
            print("Your HP is already full!")
            return False

        old_hp = self.hp
        self.hp = min(self.max_hp, self.hp + amount)
        actual_healing = self.hp - old_hp

        print(f"You recovered {actual_healing:.1f} HP.")
        print(f"HP: {self.hp:.1f}/{self.max_hp}")

        return actual_healing > 0

    def use_potion(self) -> bool:
        """Use one healing potion."""
        if self.inventory["potion"] <= 0:
            print("You have no healing potions!")
            return False

        if self.hp >= self.max_hp:
            print("Your HP is already full!")
            return False

        minimum_heal = 12 + (self.level * 2)
        maximum_heal = 20 + (self.level * 2)
        heal_amount = random.randint(minimum_heal, maximum_heal)

        old_hp = self.hp
        self.hp = min(self.max_hp, self.hp + heal_amount)
        actual_healing = self.hp - old_hp

        self.inventory["potion"] -= 1

        print("\nYou used a healing potion!")
        print(f"You recovered {actual_healing:.1f} HP.")
        print(f"HP: {self.hp:.1f}/{self.max_hp}")
        print(f"Potions remaining: {self.inventory['potion']}")

        return True

    def show_inventory(self) -> None:
        print("\n======================")
        print("       INVENTORY")
        print("======================")
        print(f"Potion: {self.inventory['potion']}")

