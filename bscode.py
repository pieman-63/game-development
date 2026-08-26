import random


class Character:
    """Base class for Player and Enemy."""

    def __init__(
        self,
        name,
        strength,
        defense,
        agility,
        intelligence,
        luck
    ):
        self.name = name
        self.strength = strength
        self.defense = defense
        self.agility = agility
        self.intelligence = intelligence
        self.luck = luck

    @property
    def max_hp(self):
        # Defense remains valuable, but HP scaling is slightly reduced.
        return 50 + (self.defense * 4)

    @property
    def attack_power(self):
        return self.strength * 2

    def show_stats(self):
        print(f"\n--- {self.name}'s Stats ---")
        print(f"Strength:     {self.strength}")
        print(f"Defense:      {self.defense}")
        print(f"Agility:      {self.agility}")
        print(f"Intelligence: {self.intelligence}")
        print(f"Luck:         {self.luck}")


class Player(Character):
    """The player character."""

    STAT_POOL = 20

    # Luck remains useful, but no longer becomes overwhelmingly strong.
    CRIT_CHANCE_PER_LUCK = 0.025
    MAX_CRIT_CHANCE = 0.50

    STARTING_POTIONS = 3

    def __init__(
        self,
        name,
        strength,
        defense,
        agility,
        intelligence,
        luck
    ):
        super().__init__(
            name,
            strength,
            defense,
            agility,
            intelligence,
            luck
        )

        self.level = 1
        self.exp = 0
        self.exp_to_next_level = 100

        self.hp = self.max_hp

        # Persistent inventory.
        self.inventory = {
            "potion": self.STARTING_POTIONS
        }

    @property
    def crit_chance(self):
        return min(
            self.MAX_CRIT_CHANCE,
            self.luck * self.CRIT_CHANCE_PER_LUCK
        )

    @property
    def stat_growth_cap(self):
        """
        Maximum stat value for stat growth from enemies.

        Example:
        Level 1 -> 2
        Level 2 -> 7
        Level 3 -> 12
        Level 10 -> 47
        """
        return max(1, (self.level * 5) - 3)

    def gain_exp(self, amount):
        """
        Gain EXP.

        Luck gives the player a small EXP bonus
        per point of Luck.
        """

        # Reduced from 2% to 1% per Luck.
        exp_bonus = int(amount * (self.luck * 0.01))
        total_exp = amount + exp_bonus

        self.exp += total_exp

        print(f"\nYou gained {total_exp} EXP!")

        if exp_bonus > 0:
            print(
                f"Luck bonus: +{exp_bonus} EXP "
                f"({self.luck} Luck)"
            )

        while self.exp >= self.exp_to_next_level:
            self.exp -= self.exp_to_next_level
            self.level_up()

    def level_up(self):
        self.level += 1

        print("\n======================")
        print(f" LEVEL UP! You are now level {self.level}!")
        print("======================")

        # Overall stat increase.
        self.strength += 1
        self.defense += 1
        self.agility += 1
        self.intelligence += 1
        self.luck += 1

        # Increase EXP requirement.
        self.exp_to_next_level = int(
            self.exp_to_next_level * 1.25
        )

        # Fully restore HP on level up.
        self.hp = self.max_hp

        print("All stats increased by 1!")
        print("Your HP has been fully restored.")

    def stat_growth_from_enemy(self, enemy):
        """
        If the enemy's major stat is greater than
        the player's corresponding stat, increase it.

        Stat growth from this system is capped based
        on the player's level.
        """

        stat_name = enemy.major_stat

        enemy_value = getattr(enemy, stat_name)
        player_value = getattr(self, stat_name)

        if enemy_value <= player_value:
            return

        if player_value >= self.stat_growth_cap:
            print(
                f"\nYour {stat_name} is already at "
                f"its current growth cap ({self.stat_growth_cap})."
            )
            return

        new_value = min(
            player_value + 1,
            self.stat_growth_cap
        )

        setattr(self, stat_name, new_value)

        print(
            f"\nEnemy's major stat was "
            f"{stat_name.upper()}!"
        )

        print(
            f"Your {stat_name} increased "
            f"from {player_value} to {new_value}!"
        )

    def take_damage(self, damage):
        self.hp -= damage

        if self.hp < 0:
            self.hp = 0

        print(f"You took {damage:.1f} damage!")
        print(f"HP: {self.hp:.1f}/{self.max_hp}")

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

        print(f"You recovered {actual_healing:.1f} HP.")
        print(f"HP: {self.hp:.1f}/{self.max_hp}")

        return actual_healing > 0

    def use_potion(self):
        """Use one potion from the persistent inventory."""

        if self.inventory["potion"] <= 0:
            print("You have no healing potions!")
            return False

        if self.hp >= self.max_hp:
            print("Your HP is already full!")
            return False

        # Potion healing scales slightly with level.
        minimum_heal = 12 + (self.level * 2)
        maximum_heal = 20 + (self.level * 2)

        heal_amount = random.randint(
            minimum_heal,
            maximum_heal
        )

        old_hp = self.hp

        self.hp += heal_amount

        if self.hp > self.max_hp:
            self.hp = self.max_hp

        actual_healing = self.hp - old_hp

        self.inventory["potion"] -= 1

        print("\nYou used a healing potion!")
        print(f"You recovered {actual_healing:.1f} HP.")
        print(f"HP: {self.hp:.1f}/{self.max_hp}")
        print(
            f"Potions remaining: "
            f"{self.inventory['potion']}"
        )

        return True

    def show_inventory(self):
        print("\n======================")
        print("       INVENTORY")
        print("======================")

        print(
            f"Potion: "
            f"{self.inventory['potion']}"
        )


class Enemy(Character):
    """Enemy created dynamically."""

    MAX_CRIT_CHANCE = 0.50
    CRIT_CHANCE_PER_LUCK = 0.03

    def __init__(
        self,
        name,
        strength,
        defense,
        agility,
        intelligence,
        luck,
        exp_reward,
        major_stat=None
    ):
        super().__init__(
            name,
            strength,
            defense,
            agility,
            intelligence,
            luck
        )

        self.hp = self.max_hp
        self.exp_reward = exp_reward

        stats = {
            "strength": self.strength,
            "defense": self.defense,
            "agility": self.agility,
            "intelligence": self.intelligence,
            "luck": self.luck
        }

        if major_stat is not None:
            self.major_stat = major_stat
        else:
            highest_value = max(stats.values())

            tied_stats = [
                stat
                for stat, value in stats.items()
                if value == highest_value
            ]

            self.major_stat = random.choice(tied_stats)

    @property
    def crit_chance(self):
        return min(
            self.MAX_CRIT_CHANCE,
            self.luck * self.CRIT_CHANCE_PER_LUCK
        )

    def take_damage(self, damage):
        self.hp -= damage

        if self.hp < 0:
            self.hp = 0

        print(
            f"{self.name} took {damage:.1f} damage!"
        )

        print(
            f"{self.name} HP: "
            f"{self.hp:.1f}/{self.max_hp}"
        )


class EnemyFactory:
    """
    Creates enemies on the fly.

    Enemy types have different stat tendencies,
    making encounters more strategically distinct.
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

    # Enemy profiles.
    #
    # "major_stat" defines the archetype's preferred
    # stat and is used to make enemy identity more reliable.
    STAT_PROFILES = {
        "Goblin": {
            "strength": 1,
            "defense": 0,
            "agility": 2,
            "intelligence": 0,
            "luck": 2,
            "major_stat": "luck"
        },

        "Wolf": {
            "strength": 2,
            "defense": 0,
            "agility": 4,
            "intelligence": 0,
            "luck": 1,
            "major_stat": "agility"
        },

        "Skeleton": {
            "strength": 1,
            "defense": 4,
            "agility": 0,
            "intelligence": 1,
            "luck": 0,
            "major_stat": "defense"
        },

        "Bandit": {
            "strength": 2,
            "defense": 1,
            "agility": 2,
            "intelligence": 1,
            "luck": 1,
            "major_stat": "strength"
        },

        "Orc": {
            "strength": 4,
            "defense": 3,
            "agility": -1,
            "intelligence": -1,
            "luck": 0,
            "major_stat": "strength"
        },

        "Dark Mage": {
            "strength": -1,
            "defense": 0,
            "agility": 1,
            "intelligence": 5,
            "luck": 1,
            "major_stat": "intelligence"
        },

        "Giant Spider": {
            "strength": 2,
            "defense": 1,
            "agility": 4,
            "intelligence": 2,
            "luck": 0,
            "major_stat": "agility"
        },

        "Slime": {
            "strength": 0,
            "defense": 5,
            "agility": -2,
            "intelligence": 1,
            "luck": 0,
            "major_stat": "defense"
        }
    }

    @staticmethod
    def create_enemy(player_level):
        name = random.choice(EnemyFactory.NAMES)

        profile = EnemyFactory.STAT_PROFILES[name]

        # Enemy scaling remains intentionally challenging.
        base = player_level + random.randint(1, 5)

        stats = {}

        for stat in [
            "strength",
            "defense",
            "agility",
            "intelligence",
            "luck"
        ]:
            modifier = profile[stat]

            minimum = max(
                1,
                base - 2 + modifier
            )

            maximum = max(
                minimum,
                base + 4 + modifier
            )

            stats[stat] = random.randint(
                minimum,
                maximum
            )

        exp_reward = random.randint(
            40,
            80 + (player_level * 10)
        )

        return Enemy(
            name,
            stats["strength"],
            stats["defense"],
            stats["agility"],
            stats["intelligence"],
            stats["luck"],
            exp_reward,
            major_stat=profile["major_stat"]
        )


class Combat:
    """Handles battles between the player and enemy."""

    # Percentage of maximum HP restored by defending.
    # This remains intentionally strong.
    DEFEND_HEAL_PERCENT = 0.08

    # Number of consecutive Defend actions before
    # the enemy can call a buddy.
    DEFEND_STREAK_LIMIT = 3

    # Chance that the enemy calls a buddy after
    # the player exceeds the defend streak limit.
    BUDDY_CALL_CHANCE = 0.75

    # Intelligence needed before ambushes become possible.
    AMBUSH_INTELLIGENCE_THRESHOLD = 8

    # Maximum ambush chance.
    MAX_AMBUSH_CHANCE = 0.35

    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy

        # Additional enemies called during combat.
        self.buddies = []

        self.defending = False

        # Number of consecutive Defend actions.
        self.defend_streak = 0

    def all_enemies(self):
        """Return the main enemy and all living buddies."""

        enemies = []

        if self.enemy.hp > 0:
            enemies.append(self.enemy)

        enemies.extend(
            buddy
            for buddy in self.buddies
            if buddy.hp > 0
        )

        return enemies

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

        # Damage is deliberately kept as a float.
        damage = float(self.player.attack_power)

        # Luck affects critical chance.
        crit_chance = self.player.crit_chance

        if random.random() < crit_chance:
            damage *= 1.5
            print("CRITICAL HIT!")

        # Enemy defense reduces damage.
        damage -= self.enemy.defense * 0.5

        # Never deal less than 1 damage.
        damage = max(1.0, damage)

        self.enemy.take_damage(damage)

    def enemy_attack_single(self, enemy):
        """Perform one enemy attack against the player."""

        if enemy.hp <= 0:
            return

        # Player agility gives a chance to dodge.
        dodge_chance = min(
            0.30,
            self.player.agility * 0.015
        )

        if random.random() < dodge_chance:
            print(
                f"You dodged the {enemy.name}'s attack!"
            )
            return

        damage = float(enemy.attack_power)

        # Enemy Luck affects critical chance.
        if random.random() < enemy.crit_chance:
            damage *= 1.5

            print(
                f"{enemy.name} landed a "
                f"CRITICAL HIT!"
            )

        # Player defense reduces damage.
        damage -= self.player.defense * 0.5

        damage = max(1.0, damage)

        if self.defending:
            # Defending intentionally reduces the remaining
            # damage by 50%.
            damage *= 0.50

            damage = max(0.5, damage)

            print(
                "Your defensive stance reduced "
                "the damage!"
            )

        self.player.take_damage(damage)

    def enemy_attack(self):
        """
        All living enemies get a turn.

        This allows the buddy system to create a
        genuine multi-enemy encounter.
        """

        enemies = self.all_enemies()

        for enemy in enemies:
            if self.player.hp <= 0:
                break

            self.enemy_attack_single(enemy)

    def player_defend(self):
        """
        Defend for the turn.

        The player receives some HP recovery while
        also reducing the next incoming attack.
        """

        self.defending = True
        self.defend_streak += 1

        heal_amount = (
            self.player.max_hp *
            self.DEFEND_HEAL_PERCENT
        )

        self.player.heal(heal_amount)

        print("You brace yourself!")

        print(
            f"Defend streak: "
            f"{self.defend_streak}"
        )

        # The buddy event is checked after the player
        # reaches the fourth consecutive Defend.
        if self.defend_streak > self.DEFEND_STREAK_LIMIT:
            self.enemy_calls_buddy()

    def enemy_calls_buddy(self):
        """Give the enemy a chance to call another enemy."""

        # Only the main enemy can call a buddy.
        if self.enemy.hp <= 0:
            return

        # Only allow one buddy for now.
        if self.buddies:
            return

        if random.random() >= self.BUDDY_CALL_CHANCE:
            print(
                f"\nThe {self.enemy.name} tried to call "
                f"for help, but nobody came!"
            )
            return

        buddy = EnemyFactory.create_enemy(
            self.player.level
        )

        self.buddies.append(buddy)

        print("\n======================")
        print("      ENEMY BACKUP!")
        print("======================")

        print(
            f"The {self.enemy.name} called "
            f"a {buddy.name} to help!"
        )

        print(
            f"Buddy major stat: "
            f"{buddy.major_stat.upper()}"
        )

        buddy.show_stats()

        # Reset the streak so the event cannot trigger
        # repeatedly every single turn.
        self.defend_streak = 0

    def player_heal(self):
        """Use a potion if one is available."""

        return self.player.use_potion()

    def attempt_escape(self):
        """
        Escape chance is affected by the difference
        between player and enemy agility.
        """

        # Reduced from 50% to 40%.
        base_chance = 0.40

        agility_difference = (
            self.player.agility -
            self.enemy.agility
        )

        escape_chance = (
            base_chance +
            (agility_difference * 0.03)
        )

        escape_chance = max(
            0.20,
            min(0.80, escape_chance)
        )

        if random.random() < escape_chance:
            print("You escaped!")
            return True

        print("You failed to escape!")
        return False

    def check_for_ambush(self):
        """
        Intelligent enemies can ambush the player.

        Higher enemy Intelligence increases the chance.
        """

        if (
            self.enemy.intelligence
            < self.AMBUSH_INTELLIGENCE_THRESHOLD
        ):
            return False

        intelligence_difference = (
            self.enemy.intelligence
            - self.AMBUSH_INTELLIGENCE_THRESHOLD
        )

        ambush_chance = min(
            self.MAX_AMBUSH_CHANCE,
            0.10 + (
                intelligence_difference * 0.025
            )
        )

        if random.random() >= ambush_chance:
            return False

        print("\n!!! AMBUSH !!!")
        print(
            f"The {self.enemy.name} used its "
            f"high Intelligence to catch you off guard!"
        )

        # Ambush deals a slightly reduced opening attack.
        damage = float(self.enemy.attack_power)

        damage -= self.player.defense * 0.5

        damage = max(1.0, damage * 0.75)

        print(
            f"The ambush deals "
            f"{damage:.1f} damage!"
        )

        self.player.take_damage(damage)

        return True

    def victory_rewards(self):
        """Handle rewards after defeating an enemy."""

        # Main enemy reward.
        self.player.gain_exp(
            self.enemy.exp_reward
        )

        self.player.stat_growth_from_enemy(
            self.enemy
        )

        # Buddy reward.
        for buddy in self.buddies:
            if buddy.hp <= 0:
                print(
                    f"\nYou also defeated the "
                    f"{buddy.name}!"
                )

                self.player.gain_exp(
                    buddy.exp_reward
                )

                self.player.stat_growth_from_enemy(
                    buddy
                )

        # 25% chance of finding a potion.
        if random.random() < 0.25:
            self.player.inventory["potion"] += 1

            print(
                "\nYou found a healing potion!"
            )

            print(
                f"Potions: "
                f"{self.player.inventory['potion']}"
            )

        # Small chance of healing after victory.
        if random.random() < 0.25:
            heal_amount = random.randint(5, 15)

            print("\nVictory recovery!")
            self.player.heal(heal_amount)

    def choose_attack_target(self):
        """
        Choose which enemy the player attacks.

        If there is a buddy, the player gets to choose.
        """

        living_enemies = self.all_enemies()

        if len(living_enemies) == 1:
            return living_enemies[0]

        print("\nChoose a target:")

        for index, enemy in enumerate(
            living_enemies,
            start=1
        ):
            print(
                f"{index}. "
                f"{enemy.name} - "
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

    def player_attack_selected(self):
        """Attack a player-selected enemy."""

        target = self.choose_attack_target()

        # Enemy agility gives it a chance to dodge.
        dodge_chance = min(
            0.40,
            target.agility * 0.02
        )

        if random.random() < dodge_chance:
            print(
                f"{target.name} dodged your attack!"
            )
            return

        damage = float(self.player.attack_power)

        if random.random() < self.player.crit_chance:
            damage *= 1.5
            print("CRITICAL HIT!")

        damage -= target.defense * 0.5

        damage = max(1.0, damage)

        target.take_damage(damage)

    def run(self):
        print("\n======================")
        print(f"A wild {self.enemy.name} appeared!")
        print("======================")

        print(
            f"Major stat: "
            f"{self.enemy.major_stat.upper()}"
        )

        self.enemy.show_stats()

        # Check ambush before the normal battle loop.
        if self.check_for_ambush():
            if self.player.hp <= 0:
                return False

        while (
            self.player.hp > 0
            and len(self.all_enemies()) > 0
        ):
            self.defending = False

            print("\n----------------------")

            print(
                f"{self.player.name}: "
                f"{self.player.hp:.1f}/"
                f"{self.player.max_hp} HP"
            )

            print("\nEnemies:")

            for enemy in self.all_enemies():
                print(
                    f"- {enemy.name}: "
                    f"{enemy.hp:.1f}/"
                    f"{enemy.max_hp} HP"
                )

            print(
                f"\nPotions: "
                f"{self.player.inventory['potion']}"
            )

            print("\n1. Attack")
            print("2. Defend")
            print("3. Heal")
            print("4. Run")

            choice = input("> ").strip()

            turn_used = False

            if choice == "1":
                self.player_attack_selected()

                # Attacking breaks the defend streak.
                self.defend_streak = 0

                turn_used = True

            elif choice == "2":
                self.player_defend()
                turn_used = True

            elif choice == "3":
                # Healing at full HP or without potions
                # does not consume the player's turn.
                turn_used = self.player_heal()

                if turn_used:
                    self.defend_streak = 0

            elif choice == "4":
                escaped = self.attempt_escape()

                if escaped:
                    return False

                self.defend_streak = 0
                turn_used = True

            else:
                print("Invalid choice.")
                continue

            # Enemies get their turn only if the player
            # actually performed an action.
            if turn_used and self.player.hp > 0:
                self.enemy_attack()

        if self.player.hp <= 0:
            return False

        print("\n======================")
        print("     VICTORY!")
        print("======================")

        print(
            f"You defeated the {self.enemy.name}!"
        )

        self.victory_rewards()

        return True


class Game:
    """Controls the overall game."""

    # Rest now restores 30% instead of 50%.
    REST_HEAL_PERCENT = 0.30

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
                "intelligence": 1,
                "luck": 1
            }

            # Five points are automatically spent
            # to satisfy the minimum of 1 in each stat.
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
                print(
                    f"Points remaining: "
                    f"{points_left}"
                )

                for stat, value in stats.items():
                    print(
                        f"{stat.capitalize():13}: "
                        f"{value}"
                    )

                print("\nEnter a stat to increase.")
                print(
                    "You must spend all points "
                    "before confirming."
                )

                choice = input("> ").strip().lower()

                if choice not in stats:
                    print("Invalid stat.")
                    continue

                amount_text = input(
                    f"How many points to add "
                    f"to {choice}? "
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

            print("\n======================")
            print(" FINAL CHARACTER")
            print("======================")

            print(f"Name: {name}")

            for stat, value in stats.items():
                print(
                    f"{stat.capitalize()}: "
                    f"{value}"
                )

            print(
                f"Unused points: "
                f"{points_left}"
            )

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
                        stats["luck"]
                    )

                    return self.player

                if confirm == "n":
                    print(
                        "\nRestarting character "
                        "creation..."
                    )
                    break

                print("Please enter y or n.")

    def rest(self):
        """Restore 30% of the player's maximum HP."""

        if self.player.hp >= self.player.max_hp:
            print("Your HP is already full!")
            return

        old_hp = self.player.hp

        recovery = (
            self.player.max_hp *
            self.REST_HEAL_PERCENT
        )

        self.player.hp += recovery

        if self.player.hp > self.player.max_hp:
            self.player.hp = self.player.max_hp

        actual_recovery = self.player.hp - old_hp

        print(
            f"You rested and restored "
            f"{actual_recovery:.1f} HP."
        )

        print(
            f"HP: {self.player.hp:.1f}/"
            f"{self.player.max_hp}"
        )

    def main_menu(self):
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
                enemy = EnemyFactory.create_enemy(
                    self.player.level
                )

                combat = Combat(
                    self.player,
                    enemy
                )

                survived = combat.run()

                if (
                    not survived
                    and self.player.hp > 0
                ):
                    print(
                        "You returned to safety."
                    )

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

        print(
            f"Final EXP: {self.player.exp}"
        )

        print(
            f"Potions remaining: "
            f"{self.player.inventory['potion']}"
        )

    def run(self):
        print("======================")
        print("     Simple game")
        print("======================")

        self.create_player()

        self.player.show_stats()

        input("\nPress Enter to begin...")

        self.main_menu()


if __name__ == "__main__":
    game = Game()
    game.run()
