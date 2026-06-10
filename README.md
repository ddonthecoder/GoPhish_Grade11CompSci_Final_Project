README File

Go-Phish: The Deep Sea Heist
Developed by: Deegayu Dewage Don
Date: July 10, 2026

Description:
An aquatic, tactical spin-off of the classic "Go-Fish" card game where players face off against a memory-adapting shark AI in a race to collect 13 books from the deep ocean floor.

Features:
Adaptive AI System: Features three difficulty tiers: 
Pufferfish (fully randomized moves)
Barracuda (tracks your last 3 requests)
Great White (remembers all revealed cards and metrics).


Color-Matching Mechanics: Adds a strategic twist to standard Go-Fish by requiring players to match both the card Rank and Color (Red/Black) to successfully steal cards.


Deep Sea Vision: Successfully matching a card triggers a 5-second visualization effect, highlighting newly stolen cards on your interface


Real-time Chat Log: A rolling text engine updates every action, draw, and AI decision frame-by-frame for tactical game tracking.

Hybrid GUI Architecture: Utilizes optimized, manually handled Pygame surfaces for interactive gameplay buttons alongside a traditional widget layout for menus.

Installation:
This game requires Python 3.x and two external libraries. To install the required packages, open your terminal or command prompt and run the following commands:

Pygame (Handles graphics, window drawing, and frame loops)
pip install pygame

Pygame Widgets (Manages the UI buttons on the main menu, difficulty selection, and game-over screens)
pip install pygame_widgets

Running the Game:

Ensure the assets folder structure mirrors the root directory (`assets/vfx/classic-cards/`), then run:

python main.py

*(Note: If card assets are missing, the program will dynamically generate beautiful text-based geometric vector card fallbacks automatically).*

Known Bugs:
Widget Event Overlap: When exiting the "How To Play" menu using a mouse click, if your cursor is floating exactly where a main menu button is located, it may accidentally trigger that button simultaneously. *Workaround: Use any keyboard key to close the instructions panel safely.
Rapid-Click Queue Stacking: Clicking custom game buttons extremely fast during the resolving phase can occasionally cause visual log messages to lag slightly behind the current state processing.

Cheat Codes:
To facilitate faster evaluation and testing of end-game loops, the following strategies and shortcuts apply:

The "Great White" Card Leak: Because the AI prints partial match hints directly to the Chat Log (e.g., *"Hint: Shark has Black Qs"*), you can entirely bypass testing your memory by reading the rolling log history. This allows you to secure continuous turns without failing a guess.
Debugging Deck Depletion: For rapid QA testing of the Game Over layout screen without playing all 13 books, developers can manually adjust line 258 from list(range(1, 53))`to a smaller collection like list(range(1, 20)). This shrinks the game loop down to a 2-minute session.

Support:
For technical issues, asset rendering problems, or general troubleshooting, please reach out via GitHub Issues or contact the developer directly at “ddewa2@ocdsb.ca”

Sources:
A complete breakdown of resources, assets, and design concepts utilized can be found below:

Reference Tracker & Project Documentation 
https://docs.google.com/document/d/1gtFB6av1qQVTPzrYEQm5CayylFC5F0mTiQElDLoVS0E/edit?usp=sharing 

Pygame Documentation (Display, Surface, Event):
Consulted for building the manual custom button collision loops (`collidepoint`) and handling `MOUSEBUTTONDOWN` events to completely replace heavy widgets inside volatile game states.


Pygame_Widgets Library Repositories:
Referenced to configure the clean `WidgetHandler.removeWidget()` framework used when swapping cleanly between menu states and clean boards.

Traditional Go-Fish Rulesets: 
Adapted to construct the unique base rules, modified with the binary variant matrix rule (splitting standard suites into explicit Red and Black tracking elements).

