import time
import os 

#general utility functions

# Print slowly for better storytelling effect
def print_slowly(text, delay=0.05):
    try:
        for char in text:
            print(char, end='', flush=True)
            time.sleep(delay)
        print()
    except KeyboardInterrupt:
        print()  

# Clear the console screen
def clear_screen():
    os.system('cls' if os.name == 'nt' else 'clear')

# Print a separator line for better readability
def print_separator():
    print("-" * 50)

# Get user choice from a list of valid options
def get_choice(valid_choices):
    while True:
        choice = input("Choose an option: ")
        if choice in valid_choices:
            return choice
        else:
            print("Invalid choice, please try again.")
            
def press_enter_to_continue():
    input("\n[ Press Enter to continue ]")