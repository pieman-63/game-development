from __future__ import annotations

import random

from .enemy import Enemy, EnemyFactory
from .player import Player


class Combat:
    """Handle combat between a player and one or more enemies."""

    DEFEND_HEAL_PERCENT = 0.08
    DEFEND_STREAK_LIMIT = 3
    BUDDY_CALL_CHANCE = 0.75
    AMBUSH_INTELLIGENCE_THRESHOLD = 8
    MAX_AMBUSH_CHANCE = 0.35

    def __init__(self, player: Player, enemy: Enemy) -> None:
        self.player = player
        self.enemy = enemy
        self.buddies: list[Enemy] = []
        self.defending = False
        self.defend_streak = 0

    def all_enemies(self) -> list[Enemy]:
        """Return all living enemies in the encounter."""
        enemies: list[Enemy] = []

        if self.enemy.hp > 0:
            enemies.append(self.enemy)

        enemies.extend(
            buddy for buddy in self.buddies if buddy.hp > 0
        )

        return enemies

    def player_attack(self, target: Enemy) -> None:
        """Attack a selected enemy."""
        dodge_chance = min(0.40, target.agility * 0.02)

        if random.random() < dodge_chance:
            print(f"{target.name} dodged your attack!")
            return

        damage = float(self.player.attack_power)

        if random.random() < self.player.crit_chance:
            damage *= 1.5
            print("CRITICAL HIT!")

        damage -= target.defense * 0.5
        damage = max(1.0, damage)

        target.take_damage(damage)

    def enemy_attack_single(self, enemy: Enemy) -> None:
        """Perform one enemy attack against the player."""
        if enemy.hp <= 0:
            return

        dodge_chance = min(0.30, self.player.agility * 0.015)

        if random.random() < dodge_chance:
            print(f"You dodged the {enemy.name}'s attack!")
            return

        damage = float(enemy.attack_power)

        if random.random() < enemy.crit_chance:
            damage *= 1.5
            print(f"{enemy.name} landed a CRITICAL HIT!")

        damage -= self.player.defense * 0.5
        damage = max(1.0, damage)

        if self.defending:
            damage *= 0.50
            damage = max(0.5, damage)
            print("Your defensive stance reduced the damage!")

        self.player.take_damage(damage)

    def enemy_attack(self) -> None:
        """Give all living enemies a turn."""
        for enemy in self.all_enemies():
            if self.player.hp <= 0:
                break
            self.enemy_attack_single(enemy)

    def player_defend(self) -> None:
        """Defend and restore a percentage of maximum HP."""
        self.defending = True
        self.defend_streak += 1

        heal_amount = self.player.max_hp * self.DEFEND_HEAL_PERCENT
        self.player.heal(heal_amount)

        print("You brace yourself!")
        print(f"Defend streak: {self.defend_streak}")

        if self.defend_streak > self.DEFEND_STREAK_LIMIT:
            self.enemy_calls_buddy()

    def enemy_calls_buddy(self) -> None:
        """Give the main enemy a chance to summon one buddy."""
        if self.enemy.hp <= 0 or self.buddies:
            return

        if random.random() >= self.BUDDY_CALL_CHANCE:
            print(
                f"\nThe {self.enemy.name} tried to call for help, "
                "but nobody came!"
            )
            return

        buddy = EnemyFactory.create_enemy(self.player.level)
        self.buddies.append(buddy)

        print("\n======================")
        print("      ENEMY BACKUP!")
        print("======================")
        print(
            f"The {self.enemy.name} called "
            f"a {buddy.name} to help!"
        )
        print(f"Buddy major stat: {buddy.major_stat.upper()}")
        buddy.show_stats()

        self.defend_streak = 0

    def player_heal(self) -> bool:
        """Use a potion if possible."""
        return self.player.use_potion()

    def attempt_escape(self) -> bool:
        """Attempt to escape based on the agility difference."""
        base_chance = 0.40

        agility_difference = (
            self.player.agility - self.enemy.agility
        )

        escape_chance = base_chance + (agility_difference * 0.03)
        escape_chance = max(0.20, min(0.80, escape_chance))

        if random.random() < escape_chance:
            print("You escaped!")
            return True

        print("You failed to escape!")
        return False

    def check_for_ambush(self) -> bool:
        """Check whether an intelligent enemy ambushes the player."""
        if self.enemy.intelligence < self.AMBUSH_INTELLIGENCE_THRESHOLD:
            return False

        intelligence_difference = (
            self.enemy.intelligence
            - self.AMBUSH_INTELLIGENCE_THRESHOLD
        )

        ambush_chance = min(
            self.MAX_AMBUSH_CHANCE,
            0.10 + (intelligence_difference * 0.025),
        )

        if random.random() >= ambush_chance:
            return False

        print("\n!!! AMBUSH !!!")
        print(
            f"The {self.enemy.name} used its high Intelligence "
            "to catch you off guard!"
        )

        damage = float(self.enemy.attack_power)
        damage -= self.player.defense * 0.5
        damage = max(1.0, damage * 0.75)

        print(f"The ambush deals {damage:.1f} damage!")
        self.player.take_damage(damage)

        return True

    def victory_rewards(self) -> None:
        """Give EXP, stat growth, potion drops, and recovery."""
        self.player.gain_exp(self.enemy.exp_reward)
        self.player.stat_growth_from_enemy(self.enemy)

        for buddy in self.buddies:
            if buddy.hp <= 0:
                print(f"\nYou also defeated the {buddy.name}!")
                self.player.gain_exp(buddy.exp_reward)
                self.player.stat_growth_from_enemy(buddy)

        if random.random() < 0.25:
            self.player.inventory["potion"] += 1
            print("\nYou found a healing potion!")
            print(f"Potions: {self.player.inventory['potion']}")

        if random.random() < 0.25:
            heal_amount = random.randint(5, 15)
            print("\nVictory recovery!")
            self.player.heal(heal_amount)

    def choose_attack_target(self) -> Enemy:
        """Ask the player which living enemy to attack."""
        living_enemies = self.all_enemies()

        if len(living_enemies) == 1:
            return living_enemies[0]

        print("\nChoose a target:")

        for index, enemy in enumerate(living_enemies, start=1):
            print(
                f"{index}. {enemy.name} - "
                f"{enemy.hp:.1f}/{enemy.max_hp} HP"
            )

        while True:
            choice = input("> ").strip()

            try:
                index = int(choice) - 1
            except ValueError:
                print("Please enter a valid number.")
                continue

            if 0 <= index < len(living_enemies):
                return living_enemies[index]

            print("Invalid target.")

    def run(self) -> bool:
        """Run the battle and return whether the player won."""
        print("\n======================")
        print(f"A wild {self.enemy.name} appeared!")
        print("======================")
        print(f"Major stat: {self.enemy.major_stat.upper()}")
        self.enemy.show_stats()

        if self.check_for_ambush() and self.player.hp <= 0:
            return False

        while self.player.hp > 0 and self.all_enemies():
            self.defending = False

            print("\n----------------------")
            print(
                f"{self.player.name}: "
                f"{self.player.hp:.1f}/{self.player.max_hp} HP"
            )

            print("\nEnemies:")
            for enemy in self.all_enemies():
                print(
                    f"- {enemy.name}: "
                    f"{enemy.hp:.1f}/{enemy.max_hp} HP"
                )

            print(f"\nPotions: {self.player.inventory['potion']}")
            print("\n1. Attack")
            print("2. Defend")
            print("3. Heal")
            print("4. Run")

            choice = input("> ").strip()
            turn_used = False

            if choice == "1":
                target = self.choose_attack_target()
                self.player_attack(target)
                self.defend_streak = 0
                turn_used = True

            elif choice == "2":
                self.player_defend()
                turn_used = True

            elif choice == "3":
                turn_used = self.player_heal()
                if turn_used:
                    self.defend_streak = 0

            elif choice == "4":
                if self.attempt_escape():
                    return False

                self.defend_streak = 0
                turn_used = True

            else:
                print("Invalid choice.")
                continue

            if turn_used and self.player.hp > 0:
                self.enemy_attack()

        if self.player.hp <= 0:
            return False

        print("\n======================")
        print("     VICTORY!")
        print("======================")
        print(f"You defeated the {self.enemy.name}!")

        self.victory_rewards()
        return True

