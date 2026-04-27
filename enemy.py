import random

class Enemy:
    # enemy class represents the basic enemy with health, attack power 
    def __init__(self, name, health, attack, enemy_type):
        self.name = name
        self.health = health
        self.attack = attack
        self.type = enemy_type # enemy type can be "Infected", "Runner", "Clicker", etc.
    
    
    def take_damage(self, damage):
        self.health -= damage
        if self.health < 0:
            self.health = 0 # your health should not go below 0

    # checks if the enemy is still alive
    def is_alive(self):
        return self.health > 0
    
    # spwan a random enemy from a predefined list of enemy types
    @staticmethod
    def generate_enemy():
        enemy_types = [
            {"name": "Infected", "health": 30, "attack": 5, "type": "Infected"},
            {"name": "Runner", "health": 50, "attack": 10, "type": "Runner"},
            {"name": "Clicker", "health": 80, "attack": 15, "type": "Clicker"}
        ]
        enemy_data = random.choice(enemy_types) # rastgele bir düşman türü seçilir
        return Enemy(enemy_data["name"], enemy_data["health"], enemy_data["attack"], enemy_data["type"])

class Boss(Enemy):
    # inherits from Enemy class and adds special attack and enraged state for the boss
    def __init__(self, name, health, attack, enemy_type, special_attack, max_health, is_enraged=False):
        super().__init__(name, health, attack, enemy_type)
        self.special_attack = special_attack
        self.is_enraged = is_enraged 
        self.max_health = max_health 

    def take_damage(self, damage):
        super().take_damage(damage) 
        #  boss's attack increases when its health drops below 50%
        if self.health < self.max_health * 0.5 and not self.is_enraged:
            self.is_enraged = True
            self.attack += 10 # öfkelenince saldırısı artar
            print("\n" + "!" * 50)
            print("THE KRAKEN IS ENRAGED! ITS ATTACK HAS GROWN STRONGER!")
            print("!" * 50 + "\n")