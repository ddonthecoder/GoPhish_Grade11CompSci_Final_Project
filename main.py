import pygame
import sys
import os
import random
import pygame_widgets
from pygame_widgets.button import Button

# **INIT**
pygame.init()
pygame.font.init()

screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Go Fish Game")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# ==========================================================
# STEP 1: ONE GAME STATE TO RULE THEM ALL
# ==========================================================
# Options: "START", "REQUEST", "GO_FISH", "SEND"
game_state = "START" 

# This single function handles what buttons look like depending on the game_state
def update_button_visuals():
    if game_state == "REQUEST":
        request.disable()
        go_fish.enable()
        send.enable()
    elif game_state == "GO_FISH":
        request.enable()
        go_fish.disable()
        send.enable()
    elif game_state == "SEND":
        request.enable()
        go_fish.enable()
        send.disable()
    else: # "START" or default phase
        request.enable()
        go_fish.disable()
        send.disable()

# ==========================================================
# STEP 2: SIMPLIFIED CLICK FUNCTIONS
# ==========================================================
def on_request_click():
    global game_state
    game_state = "REQUEST"
    print("Player is making a request!")
    update_button_visuals()

def on_go_fish_click():
    global game_state
    game_state = "GO_FISH"
    print("Player goes fishing!")
    update_button_visuals()

def on_send_click():
    global game_state
    game_state = "SEND"
    print("Player sends a card!")
    update_button_visuals()

# ==========================================================
# STEP 3: INITIALIZE WIDGET BUTTONS
# ==========================================================
request = Button(
    screen, 0, 650, 266, 150, text='Request', fontSize=50, margin=20,  
    inactiveColour=(200, 50, 0), hoverColour=(150, 0, 0), pressedColour=(0, 200, 20),  
    radius=20, onClick=on_request_click  
)

go_fish = Button(
    screen, 266, 650, 266, 150, text='Go Fish!', fontSize=50, margin=20,  
    inactiveColour=(200, 50, 0), hoverColour=(150, 0, 0), pressedColour=(0, 200, 20),  
    radius=20, onClick=on_go_fish_click
)

send = Button(
    screen, 532, 650, 266, 150, text='Send', fontSize=50, margin=20,  
    inactiveColour=(200, 50, 0), hoverColour=(150, 0, 0), pressedColour=(0, 200, 20),  
    radius=20, onClick=on_send_click
)

# Set the initial button states on launch
update_button_visuals()

# FONTS & TEXT SURFACE CREATION
bold_font = pygame.font.SysFont("Calibri", 25, bold=True)
text_AI_HAND = bold_font.render("AI", True, (50, 50, 50))
text_PLAYER_HAND = bold_font.render("You", True, (50, 50, 50))
text_DYHA = bold_font.render("Do you have a...", True, (0, 0, 0))

# --- ASSETS AND DECKS SETUP ---
# Dummy asset fallbacks to keep things running stable
card_back_surf = pygame.Surface((70, 100))
card_back_surf.fill((0, 0, 150))

cards_deck = {
    1: {"rank": "A", "suit": "Clubs", "color": "Black"},
    2: {"rank": "A", "suit": "Spades", "color": "Black"},
    3: {"rank": "A", "suit": "Hearts", "color": "Red"},
    4: {"rank": "A", "suit": "Diamonds", "color": "Red"},
    5: {"rank": "K", "suit": "Clubs", "color": "Black"},
    6: {"rank": "K", "suit": "Spades", "color": "Black"},
    7: {"rank": "K", "suit": "Hearts", "color": "Red"},
    8: {"rank": "K", "suit": "Diamonds", "color": "Red"}, 
    9: {"rank": "Q", "suit": "Clubs", "color": "Black"},
    10: {"rank": "Q", "suit": "Spades", "color": "Black"},
    11: {"rank": "Q", "suit": "Hearts", "color": "Red"},
    12: {"rank": "Q", "suit": "Diamonds", "color": "Red"},
    13: {"rank": "J", "suit": "Clubs", "color": "Black"},
    14: {"rank": "J", "suit": "Spades", "color": "Black"},
    15: {"rank": "J", "suit": "Hearts", "color": "Red"},
    16: {"rank": "J", "suit": "Diamonds", "color": "Red"},
    17: {"rank": "10", "suit": "Clubs", "color": "Black"},
    18: {"rank": "10", "suit": "Spades", "color": "Black"},
    19: {"rank": "10", "suit": "Hearts", "color": "Red"},
    20: {"rank": "10", "suit": "Diamonds", "color": "Red"},
    21: {"rank": "9", "suit": "Clubs", "color": "Black"},
    22: {"rank": "9", "suit": "Spades", "color": "Black"},
    23: {"rank": "9", "suit": "Hearts", "color": "Red"},
    24: {"rank": "9", "suit": "Diamonds", "color": "Red"},
    25: {"rank": "8", "suit": "Clubs", "color": "Black"},
    26: {"rank": "8", "suit": "Spades", "color": "Black"},
    27: {"rank": "8", "suit": "Hearts", "color": "Red"},
    28: {"rank": "8", "suit": "Diamonds", "color": "Red"},
    29: {"rank": "7", "suit": "Clubs", "color": "Black"},
    30: {"rank": "7", "suit": "Spades", "color": "Black"},
    31: {"rank": "7", "suit": "Hearts", "color": "Red"},
    32: {"rank": "7", "suit": "Diamonds", "color": "Red"},
    33: {"rank": "6", "suit": "Clubs", "color": "Black"},
    34: {"rank": "6", "suit": "Spades", "color": "Black"},
    35: {"rank": "6", "suit": "Hearts", "color": "Red"},
    36: {"rank": "6", "suit": "Diamonds", "color": "Red"},
    37: {"rank": "5", "suit": "Clubs", "color": "Black"},
    38: {"rank": "5", "suit": "Spades", "color": "Black"},
    39: {"rank": "5", "suit": "Hearts", "color": "Red"},
    40: {"rank": "5", "suit": "Diamonds", "color": "Red"},
    41: {"rank": "4", "suit": "Clubs", "color": "Black"},
    42: {"rank": "4", "suit": "Spades", "color": "Black"},
    43: {"rank": "4", "suit": "Hearts", "color": "Red"},
    44: {"rank": "4", "suit": "Diamonds", "color": "Red"},
    45: {"rank": "3", "suit": "Clubs", "color": "Black"},
    46: {"rank": "3", "suit": "Spades", "color": "Black"},
    47: {"rank": "3", "suit": "Hearts", "color": "Red"},
    48: {"rank": "3", "suit": "Diamonds", "color": "Red"},
    49: {"rank": "2", "suit": "Clubs", "color": "Black"},
    50: {"rank": "2", "suit": "Spades", "color": "Black"},
    51: {"rank": "2", "suit": "Hearts", "color": "Red"},
    52: {"rank": "2", "suit": "Diamonds", "color": "Red"},
    53: {"rank": "JOKER", "color": "Black"},
    54: {"rank": "JOKER", "color": "Red"},
}

# --- STABLE CHROMBOOK FILE PATH LOADING ---
back_card_path = os.path.join(BASE_DIR, "assets", "vfx", "classic-cards", "b2fv.png")
if os.path.exists(back_card_path):
    card_back_surf = pygame.image.load(back_card_path).convert_alpha()
else:
    card_back_surf = pygame.Surface((70, 100))
    card_back_surf.fill((0, 0, 150))

CARD_DIR = os.path.join(BASE_DIR, "assets", "vfx", "classic-cards")

for card_id in cards_deck:
    file_path = os.path.join(CARD_DIR, f"{card_id}.png")
    if os.path.exists(file_path):
        cards_deck[card_id]["surf"] = pygame.image.load(file_path).convert_alpha()
    else:
        fallback = pygame.Surface((70, 100))
        fallback.fill((200, 0, 0))
        cards_deck[card_id]["surf"] = fallback

# --- DECK GENERATION ---
full_deck = list(range(1, 55))
random.shuffle(full_deck)

player_deck = [full_deck.pop() for _ in range(7)]
bot_deck = [full_deck.pop() for _ in range(7)]

# Main loop
running = True
while running:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            running = False

    # 1. Clear Screen / Draw Background Table Green
    screen.fill((0, 100, 10))

    stroke_color = (50, 50, 50)
    corner_roundness = 8
    stroke_thickness = 3 

    # Draw Player Label Panel
    pygame.draw.rect(screen, (235, 235, 235), pygame.Rect(95, 600, 610, 30), border_radius=corner_roundness)
    pygame.draw.rect(screen, stroke_color, pygame.Rect(95, 600, 610, 30), width=stroke_thickness, border_radius=corner_roundness)
    screen.blit(text_PLAYER_HAND, (375, 602))

    # Draw AI Label Panel
    pygame.draw.rect(screen, (235, 235, 235), pygame.Rect(95, 60, 610, 30), border_radius=corner_roundness)
    pygame.draw.rect(screen, stroke_color, pygame.Rect(95, 60, 610, 30), width=stroke_thickness, border_radius=corner_roundness)
    screen.blit(text_AI_HAND, (375, 62))
    
    # Draw Chat Box Background Window
    pygame.draw.rect(screen, (255, 255, 255), pygame.Rect(20, 350, 300, 120), border_radius=corner_roundness)
    pygame.draw.rect(screen, stroke_color, pygame.Rect(20, 350, 300, 120), width=2, border_radius=corner_roundness)

    # 2. CHAT TEXT RENDERING BASED ON GAME STATE
    # If the state has been set to "REQUEST", show the text inside the chat box window
    if game_state == "REQUEST":
        screen.blit(text_DYHA, (35, 395)) 

    # Draw Cards
    x_pos = 95
    for x in bot_deck:
        screen.blit(card_back_surf, (x_pos, 100))
        x_pos += 90 
    
    x_pos = 95
    for cid in player_deck:
        image_to_draw = cards_deck[cid]["surf"]
        screen.blit(image_to_draw, (x_pos, 500))
        x_pos += 90 

    # 3. Update Widget Buttons Last (Keeping them visible on top)
    pygame_widgets.update(events)
    pygame.display.flip()

pygame.quit()
