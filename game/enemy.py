from __future__ import annotations

import random

from .character import Character


class Enemy(Character):
    """Enemy created dynamically by EnemyFactory."""

    MAX_CRIT_CHANCE = 0.50
    CRIT_CHANCE_PER_LUCK = 0.03

    def __init__(
        self,
        name: str,
        strength: int,
        defense: int,
        agility: int,
        intelligence: int,
        luck: int,
        exp_reward: int,
        major_stat: str | None = None,
    ) -> None:
        super().__init__(
            name, strength, defense, agility, intelligence, luck
        )

        self.hp = self.max_hp
        self.exp_reward = exp_reward

        stats = {
            "strength": self.strength,
            "defense": self.defense,
            "agility": self.agility,
            "intelligence": self.intelligence,
            "luck": self.luck,
        }

        if major_stat is not None:
            self.major_stat = major_stat
        else:
            highest_value = max(stats.values())
            tied_stats = [
                stat for stat, value in stats.items()
                if value == highest_value
            ]
            self.major_stat = random.choice(tied_stats)

    @property
    def crit_chance(self) -> float:
        return min(
            self.MAX_CRIT_CHANCE,
            self.luck * self.CRIT_CHANCE_PER_LUCK,
        )

    def take_damage(self, damage: float) -> None:
        self.hp = max(0, self.hp - damage)

        print(f"{self.name} took {damage:.1f} damage!")
        print(f"{self.name} HP: {self.hp:.1f}/{self.max_hp}")


class EnemyFactory:
    """Create dynamically scaled enemies with distinct stat profiles."""

    NAMES = [
        "Goblin",
        "Wolf",
        "Skeleton",
        "Bandit",
        "Orc",
        "Dark Mage",
        "Giant Spider",
        "Slime",
    ]

    STAT_PROFILES = {
        "Goblin": {
            "strength": 1,
            "defense": 0,
            "agility": 2,
            "intelligence": 0,
            "luck": 2,
            "major_stat": "luck",
        },
        "Wolf": {
            "strength": 2,
            "defense": 0,
            "agility": 4,
            "intelligence": 0,
            "luck": 1,
            "major_stat": "agility",
        },
        "Skeleton": {
            "strength": 1,
            "defense": 4,
            "agility": 0,
            "intelligence": 1,
            "luck": 0,
            "major_stat": "defense",
        },
        "Bandit": {
            "strength": 2,
            "defense": 1,
            "agility": 2,
            "intelligence": 1,
            "luck": 1,
            "major_stat": "strength",
        },
        "Orc": {
            "strength": 4,
            "defense": 3,
            "agility": -1,
            "intelligence": -1,
            "luck": 0,
            "major_stat": "strength",
        },
        "Dark Mage": {
            "strength": -1,
            "defense": 0,
            "agility": 1,
            "intelligence": 5,
            "luck": 1,
            "major_stat": "intelligence",
        },
        "Giant Spider": {
            "strength": 2,
            "defense": 1,
            "agility": 4,
            "intelligence": 2,
            "luck": 0,
            "major_stat": "agility",
        },
        "Slime": {
            "strength": 0,
            "defense": 5,
            "agility": -2,
            "intelligence": 1,
            "luck": 0,
            "major_stat": "defense",
        },
    }

    @staticmethod
    def create_enemy(player_level: int) -> Enemy:
        name = random.choice(EnemyFactory.NAMES)
        profile = EnemyFactory.STAT_PROFILES[name]
        base = player_level + random.randint(1, 5)

        stats: dict[str, int] = {}

        for stat in (
            "strength",
            "defense",
            "agility",
            "intelligence",
            "luck",
        ):
            modifier = profile[stat]
            minimum = max(1, base - 2 + modifier)
            maximum = max(minimum, base + 4 + modifier)
            stats[stat] = random.randint(minimum, maximum)

        exp_reward = random.randint(40, 80 + (player_level * 10))

        return Enemy(
            name,
            stats["strength"],
            stats["defense"],
            stats["agility"],
            stats["intelligence"],
            stats["luck"],
            exp_reward,
            major_stat=profile["major_stat"],
        )

