from combat import Combat
from player import Player
from enemy import Enemy, Boss
from items import Items
import time
import json
from utils import clear_screen, print_slowly, print_separator, get_choice, press_enter_to_continue

class Game:
    def __init__(self, player):
        self.player = player
        self.current_room = 1  # player's starting room
        self.enemy = None  # current enemy, created when combat starts

    # manages room transitions
    def move_to_next_room(self):
        self.current_room += 1
        print(f"You move to room {self.current_room}.")
        self.enemy = Enemy.generate_enemy()
        print(f"You encounter a {self.enemy.name}!")

    def handle_combat(self, defeat_message="You have been defeated.", flee_message="You managed to escape!"):
        result = self.combat()
        if result == "enemy":
            print_slowly(defeat_message)
            return False
        elif result == "run":
            print_slowly(flee_message)
            return "run"
        return True

    # manages the combat loop
    def combat(self):
        combat = Combat(self.player, self.enemy)
        while self.player.is_alive() and self.enemy.is_alive():
            result = combat.player_turn()
            if result == "distract":
                print("You distracted the Clicker! It won't attack this turn.")
            elif result == "run":
                return "run"
            elif isinstance(result, Enemy):
                print(f"A new enemy has joined the fight: {result.name}!")
                self.enemy = result
                combat.enemy = result
            else:
                combat.enemy_attack()
            combat_result = combat.check_combat_result()
            if combat_result == "enemy":
                return "enemy"
            elif combat_result == "player":
                return "player"

    # saves the game state to a JSON file
    def save_game(self):
        game_state = {
            "player": {
                "name": self.player.name,
                "health": self.player.health,
                "max_health": self.player.max_health,
                "base_attack": self.player.base_attack,
                "melee_weapon": {
                    "name": self.player.melee_weapon.name,
                    "item_type": self.player.melee_weapon.item_type,
                    "value": self.player.melee_weapon.value
                } if self.player.melee_weapon else None,
                "ranged_weapon": {
                    "name": self.player.ranged_weapon.name,
                    "item_type": self.player.ranged_weapon.item_type,
                    "value": self.player.ranged_weapon.value
                } if self.player.ranged_weapon else None,
                "inventory": [
                    {
                        "name": item.name,
                        "item_type": item.item_type,
                        "value": item.value
                    } for item in self.player.inventory
                ]
            },
            "current_room": self.current_room,
            "enemy": {
                "name": self.enemy.name,
                "health": self.enemy.health,
                "attack": self.enemy.attack,
                "type": self.enemy.type
            } if self.enemy else None
        }
        with open("save_game.json", "w") as f:
            json.dump(game_state, f, indent=4)
        print("--- Game saved successfully! ---")

    # loads the game state from a JSON file
    def load_game(self):
        try:
            with open("save_game.json", "r") as f:
                game_state = json.load(f)
            player_data = game_state["player"]
            self.player = Player(
                name=player_data["name"],
                health=player_data["health"],
                max_health=player_data["max_health"],
                base_attack=player_data["base_attack"]
            )
            if player_data["melee_weapon"]:
                self.player.melee_weapon = Items(
                    name=player_data["melee_weapon"]["name"],
                    item_type=player_data["melee_weapon"]["item_type"],
                    value=player_data["melee_weapon"]["value"]
                )
            if player_data["ranged_weapon"]:
                self.player.ranged_weapon = Items(
                    name=player_data["ranged_weapon"]["name"],
                    item_type=player_data["ranged_weapon"]["item_type"],
                    value=player_data["ranged_weapon"]["value"]
                )
            self.player.inventory = [
                Items(name=item["name"], item_type=item["item_type"], value=item["value"])
                for item in player_data["inventory"]
            ]
            self.current_room = game_state["current_room"]
            enemy_data = game_state.get("enemy")
            if enemy_data:
                self.enemy = Enemy(
                    name=enemy_data["name"],
                    health=enemy_data["health"],
                    attack=enemy_data["attack"],
                    enemy_type=enemy_data["type"]
                )
            else:
                self.enemy = None
            print("Game loaded successfully!")
        except FileNotFoundError:
            print("No saved game found.")

    def run(self):
        if self.current_room <= 1:
            if not self.room1(): return
        if self.current_room <= 2:
            if not self.room2(): return
        if self.current_room <= 3:
            if not self.room3(): return
        if self.current_room <= 4:
            if not self.room4(): return
        if self.current_room <= 5:
            if not self.room5(): return
        if self.current_room <= 6:
            if not self.room6(): return
        self.room7()

    def room1(self):
        self.current_room = 1
        clear_screen()
        print_separator()
        print_slowly("Chapter 1: Fish Production Facility")
        print_separator()
        print_slowly("You find yourself in the facility's closed-circuit fish production area. Water has risen to your knees and algae covers everything.")
        print_slowly("This room is the only path to the rest of the facility.")
        print_slowly("You cannot take the normal routes — you'll have to navigate through narrow passages and half-submerged tanks.")
        print_separator()

        print_slowly(f"Player HP: {self.player.health}/{self.player.max_health}")
        print_slowly("What do you want to do?")
        print("1. Pass through the broken filtration system")
        print("2. Weave between the overturned tanks")
        choice = get_choice(["1", "2"])
        if choice == "1":
            print_slowly("You struggle through the narrow passage but manage to push forward.")
            print_slowly("But at the end of the corridor, an Infected is waiting for you!")
            self.enemy = Enemy("Infected", 30, 5, "Infected")
            result = self.handle_combat(defeat_message="The Infected defeated you. Game over.")
            if not result:
                return False
            elif result == True:
                print_slowly("You defeated the Infected! Moving forward.")
        elif choice == "2":
            print_slowly("You carefully slip between the tanks.")
            print_slowly("But at the end of the tanks, an Infected is waiting for you!")
            self.enemy = Enemy("Infected", 30, 5, "Infected")
            result = self.handle_combat(defeat_message="The Infected defeated you. Game over.")
            if not result:
                return False
            elif result == True:
                print_slowly("You defeated the Infected! Moving forward.")

        # give items
        harpoon = Items("Harpoon Tip", "weapon_melee", 10)
        self.player.melee_weapon = harpoon
        print_slowly("You find a heavy stainless-steel Harpoon Tip on the table. You pick it up — a stronger close-range weapon than your fists.")

        med_aid = Items("Med-Aid", "aid", 25)
        self.player.inventory.append(med_aid)
        print_slowly("There's a first aid kit on the wall panel. You take the Med-Aid.")
        print_separator()
        time.sleep(1)
        press_enter_to_continue()
        return True

    def room2(self):
        self.current_room = 2
        clear_screen()
        print_separator()
        print_slowly("Chapter 2: Hatchery Corridor")
        print_separator()
        print_slowly("Water has risen to your knees. You sense a Runner approaching from the ripples in the dark water.")
        print_slowly("Runners are fast, aggressive mutated creatures. Fleeing is difficult, but fighting is risky too.")
        print_slowly("You could attack with your harpoon tip, but timing is critical.")
        print_slowly("To the left, there's a narrow escape corridor.")
        print_separator()
        print_slowly("What do you want to do?")
        print("1. Confront the Runner")
        print("2. Go left and escape through the narrow corridor")
        choice = get_choice(["1", "2"])
        if choice == "1":
            self.enemy = Enemy("Runner", 50, 10, "Runner")
            result = self.handle_combat(defeat_message="The Runner defeated you. Game over.")
            if not result:
                return False
            elif result == True:
                print_slowly("You defeated the Runner! Moving forward.")
        elif choice == "2":
            print_slowly("You try to run but the Runner is fast. It catches you and attacks — you take 10 damage.")
            self.player.take_damage(10)
            print_slowly(f"Player HP: {self.player.health}/{self.player.max_health}")
            if not self.player.is_alive():
                print_slowly("The Runner defeated you. Game over.")
                return False
            else:
                print_slowly("You managed to escape, but took damage. Moving forward.")

        # offer heal option
        print_slowly("Before moving to the next chapter, you consider using your Med-Aid. But you might want to save it for later.")
        print_slowly("What do you want to do?")
        print("1. Use Med-Aid to heal")
        print("2. Save the Med-Aid and keep moving")
        choice = get_choice(["1", "2"])
        if choice == "1":
            med_aid = next((item for item in self.player.inventory if item.name == "Med-Aid"), None)
            if med_aid:
                self.player.heal(med_aid.value)
                self.player.inventory.remove(med_aid)
                print_slowly(f"You used the Med-Aid and healed for {med_aid.value} HP! Current HP: {self.player.health}/{self.player.max_health}")
            else:
                print_slowly("You don't have any Med-Aid! Moving forward.")
        time.sleep(1)
        press_enter_to_continue()
        return True

    def room3(self):
        self.current_room = 3
        clear_screen()
        print_separator()
        print_slowly("Chapter 3: Algae Laboratory")
        print_separator()
        print_slowly("This room is still lit by a faint green glow.")
        print_slowly("On the tables you find an experimental Fortified-Aid — it doesn't just restore HP, it permanently increases your maximum health.")
        print_slowly("You spot a Pneumatic Pistol half-submerged in the water.")
        print_slowly("There's a horde of Infected wandering the room.")
        print_slowly("You grab the pistol, but to get the Fortified-Aid you'll need to face the horde.")
        print_slowly("A risky decision awaits. Can you defeat them, or should you try to escape?")
        print_separator()
        # give item
        self.player.ranged_weapon = Items("Pneumatic Pistol", "weapon_ranged", 20)
        print_slowly("You pick up the Pneumatic Pistol.")

        print_slowly(f"Player HP: {self.player.health}/{self.player.max_health}")
        print_slowly("What do you want to do?")
        print("1. Attack the Infected horde")
        print("2. Try to escape from the Infected horde")
        choice = get_choice(["1", "2"])
        if choice == "1":
            self.enemy = Enemy("Infected", 80, 15, "Infected")
            result = self.handle_combat(defeat_message="The Infected defeated you. Game over.")
            if not result:
                return False
            elif result == True:
                print_slowly("You defeated the Infected! You pick up the Fortified-Aid.")
                print_slowly("Your max HP permanently increased by 20, and you healed for 40 HP!")
                self.player.max_health_increase(20)
                self.player.heal(40)
                print_slowly(f"Player HP: {self.player.health}/{self.player.max_health}")
                print_slowly("You find an emergency bulletin board on the wall...")
                print_slowly("You note your progress. Progress saved.")
                self.current_room = 4
                self.save_game()
                time.sleep(2)
        elif choice == "2":
            print_slowly("You try to flee but there are too many. They catch you and attack — you take 15 damage.")
            self.player.take_damage(15)
            if not self.player.is_alive():
                print_slowly("The Infected defeated you. Game over.")
                return False
            else:
                print_slowly("You managed to escape, but took damage. Moving forward.")
                print_slowly(f"Player HP: {self.player.health}/{self.player.max_health}")
                time.sleep(1)
        press_enter_to_continue()
        return True

    def room4(self):
        self.current_room = 4
        clear_screen()
        print_separator()
        print_slowly("Chapter 4: Main Control Room")
        print_separator()
        print_slowly("This is the facility's main control room. Massive monitors and control panels surround you.")
        print_slowly("In this room, you encounter a Clicker — an evolved, more intelligent form of the Infected.")
        print_slowly("Clickers communicate through loud clicking sounds.")
        print_slowly("They may have lost their sight, but they are extremely sensitive to sound. Silent movement and careful choices are essential.")
        print_slowly("You advance through the control panels..")
        print_separator()

        # give items
        iron_pipe = Items("Iron Pipe", "weapon_melee", 20)
        self.player.melee_weapon = iron_pipe
        print_slowly("You find a heavy Iron Pipe in the corner. You pick it up.")


        print_slowly(f"Player HP: {self.player.health}/{self.player.max_health}")
        print_slowly("What do you want to do?")
        print("1. Attack the Clicker with the Iron Pipe")
        print("2. Try to escape from the Clicker")
        print("3. Use a Clicker Sound to distract it for one turn")
        choice = get_choice(["1", "2", "3"])
        if choice == "1":
            self.enemy = Enemy("Clicker", 80, 15, "Clicker")
            self.enemy.health -= 15  # stealth first strike advantage
            print_slowly("You sneak up and land a powerful blow with the Iron Pipe! 15 damage dealt!")
            result = self.handle_combat(defeat_message="The Clicker defeated you. Game over.")
            if not result:
                return False
            elif result == True:
                print_slowly("You defeated the Clicker!")
        elif choice == "2":
            print_slowly("You try to escape but the Clicker is fast. It strikes you.")
            self.player.take_damage(15)
            print_slowly(f"You took 15 damage. Current HP: {self.player.health}/{self.player.max_health}")
            if not self.player.is_alive():
                print_slowly("The Clicker defeated you. Game over.")
                return False
            else:
                print_slowly("You managed to escape, but took damage. Moving forward.")
        elif choice == "3":
            print_slowly("You use a Clicker Sound — the Clicker pauses for a moment!")
            print_slowly("You seize the opportunity and strike! 20 damage dealt!")
            self.enemy = Enemy("Clicker", 80, 15, "Clicker")
            self.enemy.health -= 20  # distraction advantage
            result = self.handle_combat(defeat_message="The Clicker defeated you. Game over.")
            if not result:
                return False
            elif result == True:
                print_slowly("You defeated the Clicker!")
        med_aid = Items("Med-Aid", "aid", 25)
        self.player.inventory.append(med_aid)
        print_slowly("There's a first aid kit on the wall panel. You take the Med-Aid.")
        # offer heal option
        print_slowly("Before moving to the next chapter, you consider using your Med-Aid. But you might want to save it for later.")
        print_slowly("What do you want to do?")
        print("1. Use Med-Aid to heal")
        print("2. Save the Med-Aid and keep moving")
        choice = get_choice(["1", "2"])
        if choice == "1":
            med_aid = next((item for item in self.player.inventory if item.name == "Med-Aid"), None)
            if med_aid:
                self.player.heal(med_aid.value)
                self.player.inventory.remove(med_aid)
                print_slowly(f"You used the Med-Aid and healed for {med_aid.value} HP! Current HP: {self.player.health}/{self.player.max_health}")
            else:
                print_slowly("You don't have any Med-Aid! Moving forward.")
        time.sleep(1)
        press_enter_to_continue()
        return True

    def room5(self):
        self.current_room = 5
        clear_screen()
        print_separator()
        print_slowly("Chapter 5: Decontamination Tunnel")
        print_separator()
        print_slowly("This tunnel is the only path to the rest of the facility.")
        print_slowly("UV lights flicker and the algae in the water glows strangely.")
        print_slowly("Lingering too long could expose you to harmful UV radiation.")
        print_slowly("In the tunnel you find a more advanced Harpoon Rifle.")
        print_slowly("You can drop your old pistol and take this powerful weapon.")
        print_slowly("But the tunnel narrows ahead, and two Runners are sprinting toward you.")
        print_separator()
        print_slowly(f"Player HP: {self.player.health}/{self.player.max_health}")
        print_slowly("What do you want to do?")
        print("1. Take the Harpoon Rifle and attack the Runners")
        print("2. Use your melee weapon against the Runners")
        print("3. Try shooting with your pistol (makes noise, attracts more enemies)")
        print("4. Try to escape from the Runners")
        choice = get_choice(["1", "2", "3", "4"])
        if choice == "1":
            print_slowly("You grab the Harpoon Rifle — a massive advantage against Runners.")
            self.player.ranged_weapon = Items("Harpoon Rifle", "weapon_ranged", 40)
            self.enemy = Enemy("Runner", 100, 10, "Runner")
            result = self.handle_combat(defeat_message="The Runner defeated you. Game over.")
            if not result:
                return False
            elif result == True:
                print_slowly("You defeated the Runner! Moving forward.")
        elif choice == "2":
            print_slowly("You fight the Runners with your melee weapon.")
            self.enemy = Enemy("Runner", 90, 10, "Runner")
            result = self.handle_combat(defeat_message="The Runner defeated you. Game over.")
            if not result:
                return False
            elif result == True:
                print_slowly("You defeated the Runner! Moving forward.")
        elif choice == "3":
            print_slowly("You fire your pistol. The sound will echo through the tunnel!")
            self.enemy = Enemy("Runner", 90, 10, "Runner")
            result = self.handle_combat(defeat_message="The Runner defeated you. Game over.")
            if not result:
                return False
            elif result == True:
                print_slowly("You defeated the Runner! But the gunshot attracted an Infected horde!")
                self.enemy = Enemy("Infected", 30, 8, "Infected")
                result = self.handle_combat(defeat_message="The Infected defeated you. Game over.")
                if not result:
                    return False
                elif result == True:
                    print_slowly("You defeated the Infected too! Moving forward.")
        elif choice == "4":
            print_slowly("You try to run but the Runners are too fast. They catch you!")
            self.player.take_damage(15)
            if not self.player.is_alive():
                print_slowly("The Runner defeated you. Game over.")
                return False
            else:
                print_slowly("You managed to escape, but took damage. Moving forward.")
        time.sleep(1)
        press_enter_to_continue()
        return True

    def room6(self):
        self.current_room = 6
        self.enemy = None
        clear_screen()
        print_separator()
        print_slowly("Chapter 6: Treatment Pools")
        print_separator()
        print_slowly("You're standing on narrow scaffolding above massive open-air pools.")
        print_slowly("The water below has turned black and thousands of Infected lurk beneath the surface.")
        print_slowly("Critical Decision: Do you pry off the rusty bolts to seal the path behind you, or spend ammunition to sprint across?")
        print_separator()
        print_slowly(f"Player HP: {self.player.health}/{self.player.max_health}")
        print_slowly("What do you want to do?")
        print("1. Pry off the rusty bolts and seal the path behind you")
        print("2. Spend ammunition and sprint across")
        choice = get_choice(["1", "2"])
        if choice == "1":
            print_slowly("You pry off the bolts and seal the path — blocking the Infected behind you.")
            print_slowly("But a Runner appears in front of you!")
            self.enemy = Enemy("Runner", 50, 10, "Runner")
            result = self.handle_combat(defeat_message="The Runner defeated you. Game over.")
            if not result:
                return False
            elif result == True:
                print_slowly("You defeated the Runner! Moving forward.")
        elif choice == "2":
            print_slowly("You spend ammunition and sprint across — risky but fast.")
            print_slowly("Infected are swimming toward you from below!")
            self.enemy = Enemy("Infected", 90, 10, "Infected")
            result = self.handle_combat(defeat_message="The Infected defeated you. Game over.")
            if not result:
                return False
            elif result == True:
                print_slowly("You defeated the Infected! Moving forward.")

        print_slowly("You spot a Fortified-Aid on the wall! You take it.")
        self.player.max_health_increase(20)
        self.player.heal(40)
        print_slowly("Your max HP permanently increased by 20, and you healed for 40 HP!")
        print_slowly(f"Player HP: {self.player.health}/{self.player.max_health}")
        med_aid = Items("Med-Aid", "aid", 25)
        self.player.inventory.append(med_aid)
        print_slowly("There's a first aid kit on the wall panel. You take the Med-Aid.")
        # offer heal option before boss
        print_slowly("Before entering the final room, you consider using your Med-Aid. But you might want to save it for the boss fight.")
        print_slowly("What do you want to do?")
        print("1. Use Med-Aid to heal")
        print("2. Save the Med-Aid and keep moving")
        choice = get_choice(["1", "2"])
        if choice == "1":
            med_aid = next((item for item in self.player.inventory if item.name == "Med-Aid"), None)
            if med_aid:
                self.player.heal(med_aid.value)
                self.player.inventory.remove(med_aid)
                print_slowly(f"You used the Med-Aid and healed for {med_aid.value} HP! Current HP: {self.player.health}/{self.player.max_health}")
            else:
                print_slowly("You don't have any Med-Aid! Moving forward.")

        print_slowly("You find the journal you've been logging your progress in...")
        print_slowly("You note your current status. Progress saved.")
        self.current_room = 7
        self.save_game()

        
        time.sleep(1)
        press_enter_to_continue()
        return True

    def room7(self):
        self.current_room = 7
        clear_screen()
        print_separator()
        print_slowly("Final Chapter: The Heart of the Facility — Main Treatment Unit and Exit")
        print_separator()
        print_slowly("This massive room houses the facility's main treatment unit — and the only way out.")
        print_slowly("But guarding this room is The Kraken — a Bloater Boss.")
        print_slowly("This creature is a former facility worker fused with a massive mutated parasite mass.")
        print_slowly("Clickers are roaming nearby. If you fire at the Boss, they'll hear it and summon more Infected.")
        print_slowly("You can use the pressure valves to stun the Boss, or silently attack its weak points with your melee weapon.")
        print_slowly("This will be the toughest fight yet. Think strategically and move carefully!")
        print_separator()
        print_slowly("What do you want to do?")
        print("1. Use your melee weapon to attack the Boss")
        print("2. Use the pressure valves to stun the Boss")
        print("3. Try shooting the Boss with your ranged weapon")
        choice = get_choice(["1", "2", "3"])
        if choice == "1":
            self.enemy = Boss("The Kraken", 100, 20, "Boss", special_attack="Tentacle Slam", max_health=100)
            result = self.handle_combat(defeat_message="The Kraken defeated you. Game over.")
            if not result:
                press_enter_to_continue()
                return False
            elif result == True:
                print_slowly("You defeated The Kraken! You open the exit using the terminal.")
        elif choice == "2":
            print_slowly("You use the pressure valves to stun the Boss! 15 damage dealt!")
            print_slowly("The Kraken's remaining health: 85/100")
            self.enemy = Boss("The Kraken", 100, 20, "Boss", special_attack="Tentacle Slam", max_health=100)
            self.enemy.health -= 15
            #
            result = self.handle_combat(defeat_message="The Kraken defeated you. Game over.")
            if not result:
                press_enter_to_continue()
                return False
            elif result == True:
                print_slowly("You defeated The Kraken! You open the exit using the terminal.")
        elif choice == "3":
            print_slowly("You fire your weapon. The Clickers will hear this!")
            self.enemy = Boss("The Kraken", 100, 20, "Boss", special_attack="Tentacle Slam", max_health=100)
            result = self.handle_combat(defeat_message="The Kraken defeated you. Game over.")
            if not result:
                press_enter_to_continue()
                return False
            elif result == True:
                print_slowly("You defeated The Kraken! But the Clickers heard the shots and summoned Infected!")
                self.enemy = Enemy("Infected", 90, 10, "Infected")
                result = self.handle_combat(defeat_message="The Infected defeated you. Game over.")
                if not result:
                    press_enter_to_continue()
                    return False
                elif result == True:
                    print_slowly("You defeated the Infected! You open the exit using the terminal. ")   
        print_slowly("The massive creature collapses back into the dark, stagnant water.")
        print_slowly("Your hands are shaking, but your mind stays focused. You reach the terminal.")
        print_slowly("You bypass the security protocols and override the floodgates. *Access Granted*.")
        print_slowly("Doors groan as they slide open, revealing the first rays of sunlight you've seen in days.")
        print_slowly("As you step outside, the salty sea breeze hits your face. The world is ruined, yes...")
        print_slowly("But as a master of the waters, you know that where there is a current, there is a way forward.")
        print_slowly("\nCongratulations! You survived the deep.")
        time.sleep(1)
        print_separator()
        print_slowly("Thanks for playing!")
        print_separator()
        press_enter_to_continue()