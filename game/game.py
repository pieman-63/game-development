from __future__ import annotations

from .combat import Combat
from .enemy import EnemyFactory
from .player import Player


class Game:
    """Control character creation, menus, and the game loop."""

    REST_HEAL_PERCENT = 0.30

    def __init__(self) -> None:
        self.player: Player | None = None

    def create_player(self) -> Player:
        """Create a player using exactly the available stat points."""
        while True:
            print("\n======================")
            print("   CHARACTER CREATION")
            print("======================")

            name = input("Enter your character's name: ").strip()
            if not name:
                name = "Hero"

            stats = {
                "strength": 1,
                "defense": 1,
                "agility": 1,
                "intelligence": 1,
                "luck": 1,
            }

            points_left = Player.STAT_POOL - 5

            print(
                f"\nYou have {Player.STAT_POOL} total "
                "points to distribute."
            )

            print("\nStats:")
            print("Strength     - Damage")
            print("Defense      - HP and damage reduction")
            print("Agility      - Dodging and escape")
            print("Intelligence - Enemy abilities / ambushes")
            print("Luck         - Critical hits and EXP")
            print("\nMinimum value for each stat: 1")

            while points_left > 0:
                print("\n----------------------")
                print(f"Points remaining: {points_left}")

                for stat, value in stats.items():
                    print(f"{stat.capitalize():13}: {value}")

                print("\nEnter a stat to increase.")
                print("You must spend all points before confirming.")

                choice = input("> ").strip().lower()

                if choice not in stats:
                    print("Invalid stat.")
                    continue

                amount_text = input(
                    f"How many points to add to {choice}? "
                ).strip()

                try:
                    amount = int(amount_text)
                except ValueError:
                    print("Please enter a number.")
                    continue

                if amount <= 0:
                    print("Amount must be positive.")
                    continue

                if amount > points_left:
                    print("You don't have that many points.")
                    continue

                stats[choice] += amount
                points_left -= amount

            print("\n======================")
            print(" FINAL CHARACTER")
            print("======================")
            print(f"Name: {name}")

            for stat, value in stats.items():
                print(f"{stat.capitalize()}: {value}")

            print(f"Unused points: {points_left}")

            while True:
                confirm = input(
                    "\nConfirm character? (y/n): "
                ).strip().lower()

                if confirm == "y":
                    self.player = Player(
                        name,
                        stats["strength"],
                        stats["defense"],
                        stats["agility"],
                        stats["intelligence"],
                        stats["luck"],
                    )
                    return self.player

                if confirm == "n":
                    print("\nRestarting character creation...")
                    break

                print("Please enter y or n.")

    def rest(self) -> None:
        """Restore 30% of maximum HP."""
        assert self.player is not None

        if self.player.hp >= self.player.max_hp:
            print("Your HP is already full!")
            return

        old_hp = self.player.hp
        recovery = self.player.max_hp * self.REST_HEAL_PERCENT
        self.player.hp = min(
            self.player.max_hp,
            self.player.hp + recovery,
        )

        actual_recovery = self.player.hp - old_hp

        print(
            f"You rested and restored "
            f"{actual_recovery:.1f} HP."
        )
        print(
            f"HP: {self.player.hp:.1f}/{self.player.max_hp}"
        )

    def main_menu(self) -> None:
        """Run the main game menu."""
        assert self.player is not None

        while self.player.hp > 0:
            print("\n======================")
            print("        MAIN MENU")
            print("======================")
            print("1. Find enemy")
            print("2. View stats")
            print("3. Rest")
            print("4. Inventory")
            print("5. Quit")

            choice = input("> ").strip()

            if choice == "1":
                enemy = EnemyFactory.create_enemy(self.player.level)
                combat = Combat(self.player, enemy)
                survived = combat.run()

                if not survived and self.player.hp > 0:
                    print("You returned to safety.")

            elif choice == "2":
                self.player.show_stats()

            elif choice == "3":
                self.rest()

            elif choice == "4":
                self.player.show_inventory()

            elif choice == "5":
                print("\nThanks for playing!")
                return

            else:
                print("Invalid choice.")

        print("\n======================")
        print("       GAME OVER")
        print("======================")
        print(
            f"{self.player.name} reached "
            f"level {self.player.level}."
        )
        print(f"Final EXP: {self.player.exp}")
        print(
            f"Potions remaining: "
            f"{self.player.inventory['potion']}"
        )

    def run(self) -> None:
        """Start the game."""
        print("======================")
        print("     Simple Game")
        print("======================")

        self.create_player()
        assert self.player is not None

        self.player.show_stats()
        input("\nPress Enter to begin...")
        self.main_menu()

