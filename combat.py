from player import Player
from enemy import Enemy
from items import Items
from utils import print_slowly, clear_screen, print_separator, get_choice
import random
import time

# combat class handles all combat mechanics between player and enemies
class Combat:
    def __init__(self, player, enemy):
        self.player = player
        self.enemy = enemy

    # handles the player's attack choices and calculates damage
    def player_attack(self):
        options = ["1"]
        print("Choose your attack:\n1. Fist (Base attack)")

        if self.player.melee_weapon:
            print(f"2. Melee Weapon ({self.player.melee_weapon.name})")
            options.append("2")
        if self.player.ranged_weapon:
            print(f"3. Ranged Weapon ({self.player.ranged_weapon.name})")
            options.append("3")

        weapon_choice = get_choice(options, "Choose an attack: ")

        damage = int(self.player.get_attack(weapon_choice) * self.critical_hit())
        self.enemy.take_damage(damage)

        # determine weapon name
        weapon_names = {
            "1": "Fist",
            "2": getattr(self.player.melee_weapon, 'name', 'Fist'),
            "3": getattr(self.player.ranged_weapon, 'name', 'Fist')
        }

        print_separator()
        print(f"You attacked with {weapon_names[weapon_choice]} and dealt {damage} damage!")
        print_separator()

        # Clicker noise mechanic
        if weapon_choice == "3" and self.enemy.type == "Clicker" and not self.enemy.is_alive():
            print("The gunshot attracted an Infected!")
            new_enemy = Enemy("Infected", 50, 15, "Infected")
            self.enemy = new_enemy
            return new_enemy  # signal that a new enemy appeared

        return None

    # manages the player's turn
    def player_turn(self):
        time.sleep(1.0)
        clear_screen()
        print_separator()
        print(f"PLAYER HP: {self.player.health}/{self.player.max_health} | {self.enemy.name} HP: {self.enemy.health}")
        print_separator()

        options = ["1", "2", "3"]
        print("1. Attack\n2. Heal\n3. Run")
        if self.enemy.type == "Clicker":
            print("4. Use Clicker Sound (Distract)")
            options.append("4")

        choice = get_choice(options, "What do you want to do? ")

        if choice == "1":
            return self.player_attack()

        elif choice == "2":
            aid_items = [i for i in self.player.inventory if i.item_type == "aid"]
            if not aid_items:
                print("No aid items left!")
                return None

            for idx, item in enumerate(aid_items):
                print(f"{idx + 1}. {item.name} (+{item.value} HP)")

            item_idx = int(get_choice([str(i + 1) for i in range(len(aid_items))], "Choose item: ")) - 1
            chosen_item = aid_items[item_idx]
            self.player.heal(chosen_item.value)
            self.player.inventory.remove(chosen_item)
            print(f"You used {chosen_item.name} and healed for {chosen_item.value} HP.")
            return None

        elif choice == "3":
            if self.enemy.type in ["Runner", "Boss"]:
                print(f"The {self.enemy.type} is too fast/strong! It attacks as you try to flee!")
                self.enemy_attack()
            else:
                return "run"

        elif choice == "4":
            print("The Clicker is distracted and misses its turn!")
            return "distract"

    # determines if a critical hit occurs (20% chance)
    def critical_hit(self):
        if random.random() < 0.2:
            print("\n*** CRITICAL HIT! ***\n")
            return 1.5
        return 1.0

    # handles the enemy's attack
    def enemy_attack(self):
        if self.enemy.is_alive():
            damage = self.enemy.attack
            self.player.take_damage(damage)
            print_separator()
            print(f"{self.enemy.name} dealt {damage} damage to you!")
            print_separator()
            print(f"PLAYER HP: {self.player.health}/{self.player.max_health}")
            print_separator()

    # checks the result of combat
    def check_combat_result(self):
        if not self.player.is_alive():
            print("You have been defeated!")
            return "enemy"
        elif not self.enemy.is_alive():
            print(f"You have defeated {self.enemy.name}!")
            return "player"
        else:
            return "ongoing"