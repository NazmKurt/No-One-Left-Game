class Player:
    # player class represents the main character controlled by the player, with health, attack power, and inventory
    def __init__(self,name, health, max_health, base_attack):
        self.name = name
        self.health = health
        self.max_health = max_health
        self.base_attack = base_attack
        # melee_weapon and ranged_weapon are initially None, they will be assigned when the player finds weapons in the game
        self.melee_weapon = None
        self.ranged_weapon = None
        self.inventory = [] # player's inventory to hold items like weapons, armor, and aid kits

    # calculates the player's attack damage based on the chosen weapon
    def get_attack(self, weapon_choice):
        if weapon_choice == "1":  # fist
            return self.base_attack
        elif weapon_choice == "2":  # melee
            return self.melee_weapon.value
        elif weapon_choice == "3":  # ranged
            return self.ranged_weapon.value
        else:
            return self.base_attack  # fallback

    # player takes damage and health is reduced
    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0 # player's health should not go below 0

    # player heals and health is increased, but should not exceed max_health
    def heal(self, amount):
        self.health += amount
        if self.health > self.max_health:
            self.health = self.max_health # health should not exceed max_health

    # increases the player's maximum health, used when the player finds certain items or reaches milestones in the game
    def max_health_increase(self, amount):
        self.max_health += amount
        
    # checks if the player is still alive
    def is_alive(self):
        return self.health > 0