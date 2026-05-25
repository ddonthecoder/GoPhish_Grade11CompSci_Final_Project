import pygame
import sys
import os
import math
import random
import pygame_widgets
from pygame_widgets.button import Button

# **INIT**
pygame.init()
pygame.font.init()



# Use 'screen' everywhere as your single main display window
screen = pygame.display.set_mode((800, 800))
pygame.display.set_caption("Go Fish Game")





# Setup our smart locator for assets
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

#====BUTTONS====:
#**REQUEST**
can_request = True

# CLick funcs.
def on_request_click():
    if can_request:
        print("Can request")
    else:
        print("Can't request")

def disable_request_button():
    global can_request
    can_request = False
    request.inactiveColour = (100,100,100)
    request.hover = (100,100,100)

def enable_request_button():
    global can_request
    can_request = True
    request.inactiveColour = (200,50,0)
    request.hover = (150,0,0)

request = Button(
    # Mandatory Parameters
    screen,  # Changed 'win' to 'screen' to match our display target
    0,  # X-coordinate
    650,  # Y-coordinate
    266,  # Width
    150,  # Height

    # Optional Parameters
    text='Request',  
    fontSize=50,  
    margin=20,  
    inactiveColour=(200, 50, 0),  
    hoverColour=(150, 0, 0),  
    pressedColour=(0, 200, 20),  
    radius=20,  
    onClick=on_request_click  
)
#**GO FISH**
can_go_fish = True

def on_go_fish_click():
    if can_request:
        print("Can go fish")
    else:
        print("Can't go fish")

def disable_go_fish_button():
    global can_go_fish
    can_go_fish = False
    go_fish.inactiveColour = (100,100,100)
    go_fish.hover = (100,100,100)

def enable_go_fish_button():
    global can_go_fish
    can_go_fish = True
    go_fish.inactiveColour = (200,50,0)
    go_fish.hover = (150,0,0)

go_fish = Button(
    # Mandatory Parameters
    screen,  # Changed 'win' to 'screen' to match our display target
    266,  # X-coordinate
    650,  # Y-coordinate
    266,  # Width
    150,  # Height

    # Optional Parameters
    text='Go Fish!',  
    fontSize=50,  
    margin=20,  
    inactiveColour=(200, 50, 0),  
    hoverColour=(150, 0, 0),  
    pressedColour=(0, 200, 20),  
    radius=20,  
    onClick=on_go_fish_click
)

#**SEND**
can_send = True

def on_send_click():
    if can_request:
        print("Can send")
    else:
        print("Can't send")

def disable_send_button():
    global can_send
    can_send = False
    send.inactiveColour = (100,100,100)
    send.hover = (100,100,100)

def enable_send_button():
    global can_send
    can_send = True
    send.inactiveColour = (200,50,0)
    send.hover = (150,0,0)

send = Button(
    # Mandatory Parameters
    screen,  # Changed 'win' to 'screen' to match our display target
    532,  # X-coordinate
    650,  # Y-coordinate
    266,  # Width
    150,  # Height

    # Optional Parameters
    text='Send',  
    fontSize=50,  
    margin=20,  
    inactiveColour=(200, 50, 0),  
    hoverColour=(150, 0, 0),  
    pressedColour=(0, 200, 20),  
    radius=20,  
    onClick=on_send_click
)

# FONTS
bold_font = pygame.font.SysFont("Calibri", 25, bold=True)
italic_font = pygame.font.SysFont("Calibri", 30, italic=True)

# TEXTS
text_AI_HAND = bold_font.render("AI", True, (50, 50, 50))
text_PLAYER_HAND = bold_font.render("You", True, (50, 50, 50))
text_CHAT = italic_font.render("Chat", True, (50, 50, 50))

cards_deck = {
    # ACES
    1: {"rank": "A", "suit": "Clubs", "color": "Black"},
    2: {"rank": "A", "suit": "Spades", "color": "Black"},
    3: {"rank": "A", "suit": "Hearts", "color": "Red"},
    4: {"rank": "A", "suit": "Diamonds", "color": "Red"},
    
    # KINGS
    5: {"rank": "K", "suit": "Clubs", "color": "Black"},
    6: {"rank": "K", "suit": "Spades", "color": "Black"},
    7: {"rank": "K", "suit": "Hearts", "color": "Red"},
    8: {"rank": "K", "suit": "Diamonds", "color": "Red"}, # Fixed your card 8 rank typo
    
    # QUEENS
    9: {"rank": "Q", "suit": "Clubs", "color": "Black"},
    10: {"rank": "Q", "suit": "Spades", "color": "Black"},
    11: {"rank": "Q", "suit": "Hearts", "color": "Red"},
    12: {"rank": "Q", "suit": "Diamonds", "color": "Red"},
    
    # JACKS
    13: {"rank": "J", "suit": "Clubs", "color": "Black"},
    14: {"rank": "J", "suit": "Spades", "color": "Black"},
    15: {"rank": "J", "suit": "Hearts", "color": "Red"},
    16: {"rank": "J", "suit": "Diamonds", "color": "Red"},
    
    # 10
    17: {"rank": "10", "suit": "Clubs", "color": "Black"},
    18: {"rank": "10", "suit": "Spades", "color": "Black"},
    19: {"rank": "10", "suit": "Hearts", "color": "Red"},
    20: {"rank": "10", "suit": "Diamonds", "color": "Red"},
    
    # 9
    21: {"rank": "9", "suit": "Clubs", "color": "Black"},
    22: {"rank": "9", "suit": "Spades", "color": "Black"},
    23: {"rank": "9", "suit": "Hearts", "color": "Red"},
    24: {"rank": "9", "suit": "Diamonds", "color": "Red"},
    
    # 8
    25: {"rank": "8", "suit": "Clubs", "color": "Black"},
    26: {"rank": "8", "suit": "Spades", "color": "Black"},
    27: {"rank": "8", "suit": "Hearts", "color": "Red"},
    28: {"rank": "8", "suit": "Diamonds", "color": "Red"},
    
    # 7
    29: {"rank": "7", "suit": "Clubs", "color": "Black"},
    30: {"rank": "7", "suit": "Spades", "color": "Black"},
    31: {"rank": "7", "suit": "Hearts", "color": "Red"},
    32: {"rank": "7", "suit": "Diamonds", "color": "Red"},
    
    # 6
    33: {"rank": "6", "suit": "Clubs", "color": "Black"},
    34: {"rank": "6", "suit": "Spades", "color": "Black"},
    35: {"rank": "6", "suit": "Hearts", "color": "Red"},
    36: {"rank": "6", "suit": "Diamonds", "color": "Red"},
    
    # 5
    37: {"rank": "5", "suit": "Clubs", "color": "Black"},
    38: {"rank": "5", "suit": "Spades", "color": "Black"},
    39: {"rank": "5", "suit": "Hearts", "color": "Red"},
    40: {"rank": "5", "suit": "Diamonds", "color": "Red"},
    
    # 4
    41: {"rank": "4", "suit": "Clubs", "color": "Black"},
    42: {"rank": "4", "suit": "Spades", "color": "Black"},
    43: {"rank": "4", "suit": "Hearts", "color": "Red"},
    44: {"rank": "4", "suit": "Diamonds", "color": "Red"},
    
    # 3
    45: {"rank": "3", "suit": "Clubs", "color": "Black"},
    46: {"rank": "3", "suit": "Spades", "color": "Black"},
    47: {"rank": "3", "suit": "Hearts", "color": "Red"},
    48: {"rank": "3", "suit": "Diamonds", "color": "Red"},
    
    # 2
    49: {"rank": "2", "suit": "Clubs", "color": "Black"},
    50: {"rank": "2", "suit": "Spades", "color": "Black"},
    51: {"rank": "2", "suit": "Hearts", "color": "Red"},
    52: {"rank": "2", "suit": "Diamonds", "color": "Red"},

    # JOKERS
    53: {"rank": "JOKER", "color": "Black"},
    54: {"rank": "JOKER", "color": "Red"},
}

# --- STABLE CHROMBOOK FILE PATH LOADING ---
back_card_path = os.path.join(BASE_DIR, "assets", "vfx", "classic-cards", "b2fv.png")
card_back_surf = pygame.image.load(back_card_path).convert_alpha()

CARD_DIR = os.path.join(BASE_DIR, "assets", "vfx", "classic-cards")

for card_id in cards_deck:
    file_path = os.path.join(CARD_DIR, f"{card_id}.png")
    if os.path.exists(file_path):
        cards_deck[card_id]["surf"] = pygame.image.load(file_path).convert_alpha()
    else:
        # Prevent crashes if assets are misplaced
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

    # Clear screen with card table green background
    screen.fill((0, 100, 10))

    stroke_color = (50, 50, 50)
    corner_roundness = 8
    stroke_thickness = 3 

    # PLAYER_TAB UI
    pygame.draw.rect(screen, (235, 235, 235), pygame.Rect(95, 600, 610, 30), border_radius=corner_roundness)
    pygame.draw.rect(screen, stroke_color, pygame.Rect(95, 600, 610, 30), width=stroke_thickness, border_radius=corner_roundness)
    screen.blit(text_PLAYER_HAND, (375, 602))

    # AI Name tag UI
    pygame.draw.rect(screen, (235, 235, 235), pygame.Rect(95, 60, 610, 30), border_radius=corner_roundness)
    pygame.draw.rect(screen, stroke_color, pygame.Rect(95, 60, 610, 30), width=stroke_thickness, border_radius=corner_roundness)
    screen.blit(text_AI_HAND, (375, 62))

    # Draw AI Backwards Cards
    x_pos = 95
    for x in bot_deck:
        screen.blit(card_back_surf, (x_pos, 100))
        x_pos += 90 
    
    # Draw Player Front Face Cards
    x_pos = 95
    for cid in player_deck:
        image_to_draw = cards_deck[cid]["surf"]
        screen.blit(image_to_draw, (x_pos, 500))
        
        x_pos += 90 
    
    # TEXT CHAT PANEL
    pygame.draw.rect(screen, (235, 235, 235), pygame.Rect(0, 650, 800, 150))
    pygame.draw.rect(screen, stroke_color, pygame.Rect(0, 650, 800, 150), width=stroke_thickness)
    
    # Update and render interactive widget buttons cleanly
    pygame_widgets.update(events)
    
    # Kept flip() and removed duplicate update() call to fix frame staggering
    pygame.display.flip()

pygame.quit()
