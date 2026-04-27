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
        print("Choose your attack:")
        print("1. Fist (Base attack)")
        if self.player.melee_weapon:
            print(f"2. Melee Weapon ({self.player.melee_weapon.name})")
        if self.player.ranged_weapon:
            print(f"3. Ranged Weapon ({self.player.ranged_weapon.name})")   
       
        weapon_choice = input("Choose an attack (1, 2, 3): ")
        if weapon_choice not in ["1", "2", "3"]:
            print("Invalid choice, defaulting to Fist.")
            weapon_choice = "1"
        elif weapon_choice == "2" and self.player.melee_weapon is None:
            print("You don't have a melee weapon, defaulting to Fist.")
            weapon_choice = "1"
        elif weapon_choice == "3" and self.player.ranged_weapon is None:
            print("You don't have a ranged weapon, defaulting to Fist.")
            weapon_choice = "1"  

        damage = self.player.get_attack(weapon_choice)
        damage = int(damage * self.critical_hit())
        self.enemy.take_damage(damage)

        if weapon_choice == "1":
            weapon_name = "Fist"
        elif weapon_choice == "2":
            weapon_name = self.player.melee_weapon.name
        elif weapon_choice == "3":
            weapon_name = self.player.ranged_weapon.name
        print_separator()
        print(f"You attacked with {weapon_name} and dealt {damage} damage!")
        print_separator()

        if weapon_choice == "3" and self.enemy.type == "Clicker":
            if not self.enemy.is_alive():
                print(f"You have defeated {self.enemy.name}!")
                # create a new enemy attracted by the noise
                new_enemy = Enemy("Infected", 50, 15, "Infected")
                print("You managed to take down the Clicker, but the gunshot attracted an Infected!")
                print(f"A new enemy has joined the fight: {new_enemy.name}!")
                self.enemy = new_enemy 
                return new_enemy 
        return None
    
    # manages the player's turn
    def player_turn(self):
        time.sleep(1.5)
        clear_screen()
        print_separator()
        print(f"HP: {self.player.health}/{self.player.max_health}")
        print(f"{self.enemy.name} HP: {self.enemy.health}")
        print_separator()
        print("Your turn!")
        print("What do you want to do?")
        print("1. Attack")
        print("2. Heal")
        print("3. Run")
        if self.enemy.type == "Clicker":
            print("4. Use Clicker Sound (Distract the Clicker for one turn)")
        choice = input("Choose an action (1, 2, 3): ")
        if choice == "1":
            result = self.player_attack()
            if result:  # a new enemy has appeared
                return result
            return None
        elif choice == "2":
            if "aid" in [item.item_type for item in self.player.inventory]:
                aid_items = [item for item in self.player.inventory if item.item_type == "aid"]
                print(f"Aid items ({len(aid_items)} available):")
                for idx, item in enumerate(aid_items):
                    print(f"{idx + 1}. {item.name} (Heals {item.value} HP)")
                item_choice = int(input("Enter the number of the aid item you want to use: ")) - 1
                if 0 <= item_choice < len(aid_items):
                    chosen_item = aid_items[item_choice]
                    self.player.heal(chosen_item.value)
                    self.player.inventory.remove(chosen_item)
                    print(f"You used {chosen_item.name} and healed for {chosen_item.value} HP.")
                else:
                    print("Invalid choice, you lose your turn.")    
            else:
                print("You don't have any aid items.")
        elif choice == "3":
            if self.enemy.type == "Runner":
                print("You try to run, but the Runner attacks you as you flee!")
                self.enemy_attack()
                return "run" 
            elif self.enemy.type == "Boss":
                print("The Kraken won't let you escape! It attacks!")
                self.enemy_attack()
            else:
                print("You successfully ran away!")
                return "run"
        elif choice == "4" and self.enemy.type == "Clicker":
            print("You use a Clicker sound to distract the Clicker. It won't attack this turn!")
            return "distract"
        else:
            print("Invalid choice, you lose your turn.")    

    # handles the enemy's attack
    def enemy_attack(self):
        damage = self.enemy.attack
        self.player.take_damage(damage)
        print_separator()
        print(f"{self.enemy.name} attacked you for {damage} damage.")
        print_separator()
        print(f"HP: {self.player.health}/{self.player.max_health}")
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

    # determines if a critical hit occurs (20% chance)
    def critical_hit(self):
        if random.random() < 0.2:
            print_separator()
            print("CRITICAL HIT!")
            print_separator()
            return 1.5
        return 1.0