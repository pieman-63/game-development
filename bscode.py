import random


class Character:
    """Base class for Player and Enemy."""

    def __init__(self, name, strength, defense, agility, intelligence):
        self.name = name
        self.strength = strength
        self.defense = defense
        self.agility = agility
        self.intelligence = intelligence

    @property
    def max_hp(self):
        return 50 + (self.defense * 5)

    @property
    def attack_power(self):
        return self.strength * 2

    def show_stats(self):
        print(f"\n--- {self.name}'s Stats ---")
        print(f"Strength:     {self.strength}")
        print(f"Defense:      {self.defense}")
        print(f"Agility:      {self.agility}")
        print(f"Intelligence: {self.intelligence}")


class Player(Character):
    """The player character."""

    STAT_POOL = 20
    MAX_CRIT_CHANCE = 0.75
    POTIONS_PER_BATTLE = 3

    def __init__(self, name, strength, defense, agility, intelligence):
        super().__init__(
            name,
            strength,
            defense,
            agility,
            intelligence
        )

        self.level = 1
        self.exp = 0
        self.exp_to_next_level = 100
        self.hp = self.max_hp

    def gain_exp(self, amount):
        self.exp += amount
        print(f"\nYou gained {amount} EXP!")

        while self.exp >= self.exp_to_next_level:
            self.exp -= self.exp_to_next_level
            self.level_up()

    def level_up(self):
        self.level += 1

        print("\n======================")
        print(f" LEVEL UP! You are now level {self.level}!")
        print("======================")

        # Overall stat increase
        self.strength += 1
        self.defense += 1
        self.agility += 1
        self.intelligence += 1

        # Increase EXP requirement
        self.exp_to_next_level = int(
            self.exp_to_next_level * 1.25
        )

        # Fully restore HP
        self.hp = self.max_hp

        print("All stats increased by 1!")
        print("Your HP has been fully restored.")

    def stat_growth_from_enemy(self, enemy):
        """
        If the enemy's major stat is greater than
        the player's corresponding stat, increase it.
        """

        stat_name = enemy.major_stat

        enemy_value = getattr(enemy, stat_name)
        player_value = getattr(self, stat_name)

        if enemy_value > player_value:
            setattr(self, stat_name, player_value + 1)

            print(
                f"\nEnemy's major stat was {stat_name.upper()}!"
            )
            print(
                f"Your {stat_name} increased by 1!"
            )

    def take_damage(self, damage):
        self.hp -= damage

        if self.hp < 0:
            self.hp = 0

        print(f"You took {damage} damage!")
        print(f"HP: {self.hp}/{self.max_hp}")

    def heal(self, amount):
        """Heal the player. Returns True if healing occurred."""

        if self.hp >= self.max_hp:
            print("Your HP is already full!")
            return False

        old_hp = self.hp

        self.hp += amount

        if self.hp > self.max_hp:
            self.hp = self.max_hp

        actual_healing = self.hp - old_hp

        print(f"You recovered {actual_healing} HP.")
        print(f"HP: {self.hp}/{self.max_hp}")

        return True

    def show_stats(self):
        super().show_stats()

        print(f"Level:        {self.level}")
        print(f"EXP:          {self.exp}/{self.exp_to_next_level}")
        print(f"HP:           {self.hp}/{self.max_hp}")


class Enemy(Character):
    """Enemy created dynamically."""

    MAX_CRIT_CHANCE = 0.50

    def __init__(
        self,
        name,
        strength,
        defense,
        agility,
        intelligence,
        exp_reward
    ):
        super().__init__(
            name,
            strength,
            defense,
            agility,
            intelligence
        )

        self.hp = self.max_hp
        self.exp_reward = exp_reward

        # Determine the enemy's major stat.
        stats = {
            "strength": self.strength,
            "defense": self.defense,
            "agility": self.agility,
            "intelligence": self.intelligence
        }

        highest_value = max(stats.values())

        # Find all stats tied for the highest value.
        tied_stats = [
            stat
            for stat, value in stats.items()
            if value == highest_value
        ]

        # Randomly select one if there is a tie.
        self.major_stat = random.choice(tied_stats)

    def take_damage(self, damage):
        self.hp -= damage

        if self.hp < 0:
            self.hp = 0

        print(f"{self.name} took {damage} damage!")
        print(f"{self.name} HP: {self.hp}/{self.max_hp}")


class EnemyFactory:
    """
    Creates enemies on the fly.

    Every time create_enemy() is called,
    a completely new enemy is generated.
    """

    NAMES = [
        "Goblin",
        "Wolf",
        "Skeleton",
        "Bandit",
        "Orc",
        "Dark Mage",
        "Giant Spider",
        "Slime"
    ]

    @staticmethod
    def create_enemy(player_level):
        name = random.choice(EnemyFactory.NAMES)

        # Enemy becomes somewhat stronger as
        # the player's level increases.
        base = player_level + random.randint(1, 5)

        strength = random.randint(
            max(1, base - 2),
            base + 4
        )

        defense = random.randint(
            max(1, base - 2),
            base + 4
        )

        agility = random.randint(
            max(1, base - 2),
            base + 4
        )

        intelligence = random.randint(
            max(1, base - 2),
            base + 4
        )

        exp_reward = random.randint(
            40,
            80 + (player_level * 10)
        )

        return Enemy(
            name,
            strength,
            defense,
            agility,
            intelligence,
            exp_reward
        )


class Combat:
    """Handles battles between the player and an enemy."""

    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy
        self.defending = False
        self.potions_left = Player.POTIONS_PER_BATTLE

    def player_attack(self):
        # Enemy agility gives it a chance to dodge.
        dodge_chance = min(
            0.40,
            self.enemy.agility * 0.02
        )

        if random.random() < dodge_chance:
            print(
                f"{self.enemy.name} dodged your attack!"
            )
            return

        damage = self.player.attack_power

        # Agility gives the player a chance for a critical hit.
        crit_chance = min(
            Player.MAX_CRIT_CHANCE,
            self.player.agility * 0.03
        )

        if random.random() < crit_chance:
            damage = int(damage * 1.5)
            print("CRITICAL HIT!")

        # Enemy defense reduces damage.
        damage -= self.enemy.defense // 2

        damage = max(1, damage)

        self.enemy.take_damage(damage)

    def enemy_attack(self):
        # Player agility gives a chance to dodge.
        dodge_chance = min(
            0.30,
            self.player.agility * 0.015
        )

        if random.random() < dodge_chance:
            print("You dodged the enemy's attack!")
            return

        damage = self.enemy.attack_power

        # Enemy intelligence gives a chance for a critical hit.
        crit_chance = min(
            Enemy.MAX_CRIT_CHANCE,
            self.enemy.intelligence * 0.02
        )

        if random.random() < crit_chance:
            damage = int(damage * 1.5)
            print(f"{self.enemy.name} landed a CRITICAL HIT!")

        # Player defense reduces damage.
        damage -= self.player.defense // 2

        damage = max(1, damage)

        if self.defending:
            damage //= 2
            damage = max(1, damage)

            print(
                "Your defensive stance reduced the damage!"
            )

        self.player.take_damage(damage)

    def player_heal(self):
        """Use a potion if one is available."""

        if self.potions_left <= 0:
            print("You have no healing potions left!")
            return False

        if self.player.hp >= self.player.max_hp:
            print("Your HP is already full!")
            return False

        heal_amount = random.randint(8, 15)

        healed = self.player.heal(heal_amount)

        if healed:
            self.potions_left -= 1

            print(
                f"Potions remaining: "
                f"{self.potions_left}/{Player.POTIONS_PER_BATTLE}"
            )

        return healed

    def attempt_escape(self):
        """
        Escape chance is affected by the difference
        between player and enemy agility.
        """

        base_chance = 0.50

        agility_difference = (
            self.player.agility - self.enemy.agility
        )

        escape_chance = (
            base_chance +
            (agility_difference * 0.03)
        )

        # Keep escape chance between 20% and 80%.
        escape_chance = max(
            0.20,
            min(0.80, escape_chance)
        )

        if random.random() < escape_chance:
            print("You escaped!")
            return True

        print("You failed to escape!")
        return False

    def run(self):
        print("\n======================")
        print(f"A wild {self.enemy.name} appeared!")
        print("======================")

        print(
            f"Major stat: "
            f"{self.enemy.major_stat.upper()}"
        )

        self.enemy.show_stats()

        print(
            f"\nHealing potions: "
            f"{self.potions_left}/{Player.POTIONS_PER_BATTLE}"
        )

        while self.player.hp > 0 and self.enemy.hp > 0:
            self.defending = False

            print("\n----------------------")
            print(
                f"{self.player.name}: "
                f"{self.player.hp}/{self.player.max_hp} HP"
            )

            print(
                f"{self.enemy.name}: "
                f"{self.enemy.hp}/{self.enemy.max_hp} HP"
            )

            print(
                f"Potions: "
                f"{self.potions_left}/{Player.POTIONS_PER_BATTLE}"
            )

            print("\n1. Attack")
            print("2. Defend")
            print("3. Heal")
            print("4. Run")

            choice = input("> ").strip()

            turn_used = False

            if choice == "1":
                self.player_attack()
                turn_used = True

            elif choice == "2":
                self.defending = True
                print("You brace yourself!")
                turn_used = True

            elif choice == "3":
                # Healing at full HP or without potions
                # does not consume the player's turn.
                turn_used = self.player_heal()

            elif choice == "4":
                escaped = self.attempt_escape()

                if escaped:
                    return False

                turn_used = True

            else:
                print("Invalid choice.")
                continue

            # Enemy gets a turn only if the player
            # actually performed an action.
            if turn_used and self.enemy.hp > 0:
                self.enemy_attack()

        if self.player.hp <= 0:
            return False

        print("\n======================")
        print(f"You defeated the {self.enemy.name}!")
        print("======================")

        # EXP reward
        self.player.gain_exp(self.enemy.exp_reward)

        # Stat growth based on major stat
        self.player.stat_growth_from_enemy(self.enemy)

        # Small chance of healing after victory
        if random.random() < 0.25:
            heal_amount = random.randint(5, 15)

            print("\nVictory recovery!")
            self.player.heal(heal_amount)

        return True


class Game:
    """Controls the overall game."""

    def __init__(self):
        self.player = None

    def create_player(self):
        """Create a player using exactly the available stat points."""

        while True:
            print("\n======================")
            print("   CHARACTER CREATION")
            print("======================")

            name = input(
                "Enter your character's name: "
            ).strip()

            if not name:
                name = "Hero"

            stats = {
                "strength": 1,
                "defense": 1,
                "agility": 1,
                "intelligence": 1
            }

            # Four points are automatically spent
            # to satisfy the minimum of 1 in each stat.
            points_left = Player.STAT_POOL - 4

            print(
                f"\nYou have {Player.STAT_POOL} total points "
                "to distribute."
            )

            print("\nStats:")
            print("Strength     - Damage")
            print("Defense      - HP and damage reduction")
            print("Agility      - Critical hits and dodging")
            print("Intelligence - Enemy abilities and critical hits")
            print("\nMinimum value for each stat: 1")

            while points_left > 0:
                print("\n----------------------")
                print(f"Points remaining: {points_left}")

                for stat, value in stats.items():
                    print(f"{stat.capitalize():13}: {value}")

                print("\nEnter a stat to increase.")
                print(
                    "You must spend all points before confirming."
                )

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
                    print(
                        "You don't have that many points."
                    )
                    continue

                stats[choice] += amount
                points_left -= amount

            # Confirmation screen
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
                        stats["intelligence"]
                    )

                    return self.player

                if confirm == "n":
                    print(
                        "\nRestarting character creation..."
                    )
                    break

                print("Please enter y or n.")

    def main_menu(self):
        while self.player.hp > 0:
            print("\n======================")
            print("        MAIN MENU")
            print("======================")

            print("1. Find enemy")
            print("2. View stats")
            print("3. Rest")
            print("4. Quit")

            choice = input("> ").strip()

            if choice == "1":
                enemy = EnemyFactory.create_enemy(
                    self.player.level
                )

                combat = Combat(
                    self.player,
                    enemy
                )

                survived = combat.run()

                if not survived and self.player.hp > 0:
                    print("You returned to safety.")

            elif choice == "2":
                self.player.show_stats()

            elif choice == "3":
                self.player.hp = self.player.max_hp
                print("You rested and restored your HP.")

            elif choice == "4":
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

    def run(self):
        print("======================")
        print("     TERMINAL RPG")
        print("======================")

        self.create_player()

        self.player.show_stats()

        input("\nPress Enter to begin...")

        self.main_menu()


if __name__ == "__main__":
    game = Game()
    game.run()

