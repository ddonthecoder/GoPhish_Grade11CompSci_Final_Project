import pygame
import sys
import os
import math
import random

#init
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((800, 800))
my_font = pygame.font.SysFont("Times New Roman", 40)

#TEXTS
text_AI_HAND = my_font.render("AI's Hand", True, (255,255,255))
text_PLAYER_HAND = my_font.render("Your Hand", True, (255,255,255))

"""
Assigning each card to a seperate index via a dictionary might seem very
inefficient however, if I were to implement a for loop to 
assign the cards automatically, I wouldn't have the opportunity to 
self-define them and use already determined variables that
assign each card png to their associated card variable. 
"""

cards_deck = {
    #ACES
    1: {"rank": "A", "suit": "Clubs", "color": "Black", "pic": ""},
    2: {"rank": "A", "suit": "Spades", "color": "Black"},
    3: {"rank": "A", "suit": "Hearts", "color": "Red"},
    4: {"rank": "A", "suit": "Diamonds", "color": "Red"},
    
    #KINGS
    5: {"rank": "K", "suit": "Clubs", "color": "Black"},
    6: {"rank": "K", "suit": "Spades", "color": "Black"},
    7: {"rank": "K", "suit": "Hearts", "color": "Red"},
    8: {"rank": "A", "suit": "Diamonds", "color": "Red"},
    
    #QUEENS
    9: {"rank": "Q", "suit": "Clubs", "color": "Black"},
    10: {"rank": "Q", "suit": "Spades", "color": "Black"},
    11: {"rank": "Q", "suit": "Hearts", "color": "Red"},
    12: {"rank": "Q", "suit": "Diamonds", "color": "Red"},
    
    #JACKS
    13: {"rank": "J", "suit": "Clubs", "color": "Black"},
    14: {"rank": "J", "suit": "Spades", "color": "Black"},
    15: {"rank": "J", "suit": "Hearts", "color": "Red"},
    16: {"rank": "J", "suit": "Diamonds", "color": "Red"},
    
    #10
    17: {"rank": "10", "suit": "Clubs", "color": "Black"},
    18: {"rank": "10", "suit": "Spades", "color": "Black"},
    19: {"rank": "10", "suit": "Hearts", "color": "Red"},
    20: {"rank": "10", "suit": "Diamonds", "color": "Red"},
    
    #9
    21: {"rank": "9", "suit": "Clubs", "color": "Black"},
    22: {"rank": "9", "suit": "Spades", "color": "Black"},
    23: {"rank": "9", "suit": "Hearts", "color": "Red"},
    24: {"rank": "9", "suit": "Diamonds", "color": "Red"},
    
    #8
    25: {"rank": "8", "suit": "Clubs", "color": "Black"},
    26: {"rank": "8", "suit": "Spades", "color": "Black"},
    27: {"rank": "8", "suit": "Hearts", "color": "Red"},
    28: {"rank": "8", "suit": "Diamonds", "color": "Red"},
    
    #7
    29: {"rank": "7", "suit": "Clubs", "color": "Black"},
    30: {"rank": "7", "suit": "Spades", "color": "Black"},
    31: {"rank": "7", "suit": "Hearts", "color": "Red"},
    32: {"rank": "7", "suit": "Diamonds", "color": "Red"},
    
    #6
    33: {"rank": "6", "suit": "Clubs", "color": "Black"},
    34: {"rank": "6", "suit": "Spades", "color": "Black"},
    35: {"rank": "6", "suit": "Hearts", "color": "Red"},
    36: {"rank": "6", "suit": "Diamonds", "color": "Red"},
    
    #5
    37: {"rank": "5", "suit": "Clubs", "color": "Black"},
    38: {"rank": "5", "suit": "Spades", "color": "Black"},
    39: {"rank": "5", "suit": "Hearts", "color": "Red"},
    40: {"rank": "5", "suit": "Diamonds", "color": "Red"},
    
    #4
    41: {"rank": "4", "suit": "Clubs", "color": "Black"},
    42: {"rank": "4", "suit": "Spades", "color": "Black"},
    43: {"rank": "4", "suit": "Hearts", "color": "Red"},
    44: {"rank": "4", "suit": "Diamonds", "color": "Red"},
    
    #3
    45: {"rank": "3", "suit": "Clubs", "color": "Black"},
    46: {"rank": "3", "suit": "Spades", "color": "Black"},
    47: {"rank": "3", "suit": "Hearts", "color": "Red"},
    48: {"rank": "3", "suit": "Diamonds", "color": "Red"},
    
    #2
    49: {"rank": "2", "suit": "Clubs", "color": "Black"},
    50: {"rank": "2", "suit": "Spades", "color": "Black"},
    51: {"rank": "2", "suit": "Hearts", "color": "Red"},
    52: {"rank": "2", "suit": "Diamonds", "color": "Red"},

    #JOKERS
    53: {"rank": "JOKER", "color": "Black"},
    54: {"rank": "JOKER", "color": "Red"},
}

back_card_path = os.path.join("assets", "vfx", "classic-cards", "b2fv.png")
card_back_surf = pygame.image.load(back_card_path).convert_alpha()

CARD_DIR = "assets/vfx/classic-cards"

for card_id in cards_deck:
    file_path = os.path.join(CARD_DIR, f"{card_id}.png")
    if os.path.exists(file_path):
        cards_deck[card_id]["surf"] = pygame.image.load(file_path).convert_alpha()

full_deck = list(range(1, 55))
random.shuffle(full_deck)


player_deck = [full_deck.pop() for _ in range(7)]
bot_deck = [full_deck.pop() for _ in range(7)]

print(f"Player Hand: {player_deck}")
for card_id in player_deck:
    print(cards_deck[card_id])

print(f"Bot Hand: {bot_deck}")
for card_id in bot_deck:
    print(cards_deck[card_id])


print(f"Cards left: {len(full_deck)}")

def load_cards(cards_deck):
    for card_info in cards_deck:
        file = os.path.join("assets", f"{card_info}".png)
        image = pygame.image.load(file).convert_alpha()
        cards_deck[card_info]["surf"] = image
    return cards_deck

#Main loop
running = True
while running:
    #Event checker
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    #**BACKGROUND**
    #Green table surface
    screen.fill((0, 100, 10)) #Fill screen with black

    #Wood edges
    pygame.draw.rect(screen, (100, 50, 40), pygame.Rect(0,0,50,800)) #Left
    pygame.draw.rect(screen, (100, 50, 40), pygame.Rect(750,0,50,800)) #Right
    pygame.draw.rect(screen, (100, 50, 40), pygame.Rect(0,0,800,50)) #Top
    pygame.draw.rect(screen, (100, 50, 40), pygame.Rect(0,750,800,50)) #Bottom

    x_pos = 95
    for x in bot_deck:
        screen.blit(card_back_surf, (x_pos, 100))
        x_pos += 90 
    screen.blit(text_AI_HAND, (325, 50))
    
    x_pos = 95
    for cid in player_deck:
        image_to_draw = cards_deck[cid]["surf"]
        screen.blit(image_to_draw, (x_pos, 600))
        x_pos += 90 
    screen.blit(text_PLAYER_HAND, (325, 700))

    pygame.draw.rect(screen, (1, 46, 5), pygame.Rect(0,0))
    pygame.display.flip()
pygame.quit()