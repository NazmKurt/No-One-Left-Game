# No One Left 🎮

A text-based survival RPG set in a Last of Us inspired world. You play as an Engineer trapped inside a contaminated facility overrun by the infected. Fight your way through 7 chapters, make strategic decisions, and face The Kraken in the final showdown.

---

## 🎯 Features

- **7 unique chapters** with branching story choices
- **Turn-based combat system** with melee, ranged, and fist attacks
- **3 enemy types**: Infected, Runner, Clicker — each with unique behaviors
- **Boss fight**: The Kraken (Bloater) with enrage mechanic
- **Critical hit system** (20% chance for 1.5x damage)
- **Inventory system** with Med-Aid and Fortified-Aid items
- **Save / Load system** using JSON — progress saved at checkpoint rooms
- **Strategic decisions**: using loud weapons attracts more enemies
- **ASCII art** title screen powered by pyfiglet

---

## 🕹️ How to Play

- Navigate through chapters by making choices
- In combat, choose to **Attack**, **Heal**, or **Run**
- Use **melee weapons** for silent kills — avoid using ranged weapons near Clickers
- Collect **Med-Aid** to restore HP and **Fortified-Aid** to permanently increase max HP
- Progress is automatically saved at Chapter 3 and Chapter 6

---

## 🚀 Installation

**Requirements:** Python 3.8+

```bash
# Clone the repository
git clone https://github.com/NazmKurt/No-One-Left-Game.git
cd No-One-Left-Game

# Install dependencies
pip install -r requirements.txt

# Run the game
python main.py
```

---

## 📁 Project Structure
No-One-Left-Game/
│
├── main.py          # Entry point — game menu and intro
├── game.py          # Game loop, room logic, save/load
├── combat.py        # Turn-based combat system
├── player.py        # Player class
├── enemy.py         # Enemy and Boss classes
├── items.py         # Item class
├── utils.py         # Utility functions (print_slowly, clear_screen, etc.)
│
├── requirements.txt
├── .gitignore
└── README.md

---

## 🐍 Python Concepts Used

- Object-Oriented Programming (classes, inheritance, `super()`, `@staticmethod`)
- File I/O with JSON (save/load system)
- Modular project structure
- Exception handling (`try/except`)
- List comprehensions
- `random` module for critical hits and enemy generation
- `time` and `os` modules for UI polish

---

## 👤 Developer

**Nazım Kurt** — 2026  
Python student project — built as a final capstone project.