import time
from utils import print_slowly, clear_screen, print_separator, get_choice, press_enter_to_continue
from game import Game
from player import Player
import pyfiglet

clear_screen()
print_separator()
ascii_banner = pyfiglet.figlet_format("No One Left!")
print(ascii_banner)
print_separator()
print_slowly("Developed by Nazım Kurt | 2026")
print_separator()
time.sleep(1)
print("Game Menu:")
print("1. New Game")
print("2. Continue")
print_separator()
choice = get_choice(["1", "2"])

if choice == "1":
    player_name = input("Enter your name: ")
    player = Player(player_name, health=100, max_health=100, base_attack=10)
    game = Game(player)

elif choice == "2":
    player = Player("placeholder", health=100, max_health=100, base_attack=10)  
    game = Game(player)
    game.load_game()
    game.run()

clear_screen()
print_separator()
print_slowly("No One Left!")
print_separator()
print_slowly("A post-apocalyptic survival adventure set in an underwater research facility.")
print_slowly("You are a marine biologist who wakes up to find the facility overrun by infected creatures. Your goal is to escape while uncovering the mystery behind the outbreak.")
print_slowly("Explore the dark corridors, scavenge for supplies, and fight off the infected as you navigate through the dangers of the facility.")
print_separator()
print_slowly("Start your journey...")
press_enter_to_continue()
print_slowly("The first thing you feel as you open your eyes is cold water trickling down your temples.")
print_slowly("The only sound in your ears is the rhythmic metallic creaking of a broken filtration device... Creak... Creak...")
print_slowly("You had dedicated your life to protecting the ecosystem of this facility, keeping the waters clean and the creatures alive.")
print_slowly("But now, these corridors that once smelled of fresh algae and clean water reek only of decay and rust.")
print_slowly("In every corner of the facility, there are traces of what once lived here... but now there is only silence.")
print_slowly("The massive aquariums of the facility are empty and dark, nothing remains but wreckage..")
print_slowly("The outside world has been plunged into darkness ever since the 'Great Collapse'. Humanity was brought to its knees by a fungal infection; everyone you knew either turned into those rasping creatures or has long since been devoured.")
print_slowly("You slowly rise to your feet.")
print_slowly("The digital watch you use to measure the pH levels of the water blinks with a low battery warning.")
print_slowly("You must do the only thing you know to survive: Analyze, plan, and execute.")
print_slowly("You stand up, swaying slightly in the water. Your first goal is to escape this dark and dangerous facility.")
print_slowly("But first, you need to understand what happened here.")
print_slowly("And perhaps, in this dark world, there is still a glimmer of hope..")
print_slowly("...")
time.sleep(1)
press_enter_to_continue()

game.run()