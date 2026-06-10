# Name: Deegayu Dewage Don
# Date: July 10, 2026
# Title: Go-Phish
# Description: A spin off of the classic "Go-Fish" Game

# Initialization 
import pygame
import sys
import os
import random
import pygame_widgets
from pygame_widgets.button import Button
from pygame_widgets.widget import WidgetHandler

pygame.init()
pygame.font.init()

SCREEN_W = 1000
SCREEN_H = 780
screen = pygame.display.set_mode((SCREEN_W, SCREEN_H))
pygame.display.set_caption("Go-Phish: The Deep Sea Heist")

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CARD_DIR = os.path.join(BASE_DIR, "assets", "vfx", "classic-cards")

# Colors
GREEN_BG   = (12,  85,  30)
DARK_GREEN = (5,   50,  18)
WHITE      = (255, 255, 255)
BLACK      = (0,   0,   0)
LIGHT_GREY = (215, 215, 215)
DARK_GREY  = (60,  60,  60)
GOLD       = (218, 175,  18)
BLUE_BTN   = (30,  80,  180)
BLUE_HOV   = (50,  110, 220)
RED_BTN    = (175, 28,  28)
RED_HOV    = (215, 55,  55)
TEAL       = (0,  145, 135)
CREAM      = (245, 232, 195)
PANEL_BG   = (10,  35,  12)
OCEAN_BLUE = (0,   60,  140)
GREY_BTN   = (70,  70,  70)
GREY_HOV   = (90,  90,  90)

# Fonts
font_big   = pygame.font.SysFont("Calibri", 30, bold=True)
font_med   = pygame.font.SysFont("Calibri", 20)
font_small = pygame.font.SysFont("Calibri", 17)
font_title = pygame.font.SysFont("Calibri", 56, bold=True)
font_chat  = pygame.font.SysFont("Calibri", 16)
font_btn   = pygame.font.SysFont("Calibri", 19, bold=True)

# Layout
AI_HAND_Y      = 32
SCORE_Y        = 168
CHAT_TOP       = 192
CHAT_BOTTOM    = 390
PLAYER_HAND_Y  = 445
PLAYER_BOOKS_Y = 558
INSTRUCT_Y     = 580
BTN_ROW1_Y     = 610
BTN_ROW2_Y     = 660
BTN_H          = 42
CARD_W = 68
CARD_H = 98

# Card data
RANKS  = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
SUITS  = ["Clubs", "Spades", "Hearts", "Diamonds"]
COLORS = {"Clubs": "Black", "Spades": "Black", "Hearts": "Red", "Diamonds": "Red"}

cards_deck = {}
card_id = 1
for rank in RANKS:
    for suit in SUITS:
        cards_deck[card_id] = {"rank": rank, "suit": suit, "color": COLORS[suit], "surf": None}
        card_id += 1

# Card images
back_surf = None
back_card_path = os.path.join(CARD_DIR, "b2fv.png")
if os.path.exists(back_card_path):
    back_surf = pygame.transform.scale(
        pygame.image.load(back_card_path).convert_alpha(), (CARD_W, CARD_H))

for cid in cards_deck:
    png_path = os.path.join(CARD_DIR, f"{cid}.png")
    if os.path.exists(png_path):
        cards_deck[cid]["surf"] = pygame.transform.scale(
            pygame.image.load(png_path).convert_alpha(), (CARD_W, CARD_H))

def make_fallback_surf(rank, suit, color):
    surf = pygame.Surface((CARD_W, CARD_H))
    surf.fill(WHITE)
    pygame.draw.rect(surf, (180, 180, 180), (0, 0, CARD_W, CARD_H), 2)
    text_color = (180, 0, 0) if color == "Red" else (10, 10, 10)
    sym_map = {"Hearts": "♥", "Diamonds": "♦", "Clubs": "♣", "Spades": "♠"}
    sym = sym_map.get(suit, "?")
    surf.blit(font_small.render(rank, True, text_color), (4, 3))
    surf.blit(font_small.render(sym,  True, text_color), (4, 20))
    big_font = pygame.font.SysFont("Calibri", 30)
    big = big_font.render(sym, True, text_color)
    surf.blit(big, (CARD_W//2 - big.get_width()//2, CARD_H//2 - big.get_height()//2))
    return surf

for cid in cards_deck:
    if cards_deck[cid]["surf"] is None:
        cards_deck[cid]["surf"] = make_fallback_surf(
            cards_deck[cid]["rank"], cards_deck[cid]["suit"], cards_deck[cid]["color"])

if back_surf is None:
    back_surf = pygame.Surface((CARD_W, CARD_H))
    back_surf.fill((18, 38, 130))
    pygame.draw.rect(back_surf, GOLD, (4, 4, CARD_W-8, CARD_H-8), 3)
    lbl = font_med.render("?", True, GOLD)
    back_surf.blit(lbl, (CARD_W//2 - lbl.get_width()//2, CARD_H//2 - lbl.get_height()//2))

# ============================================================
# I realised that using the pygame_widgets library was not sufficient to handle the complex elements that was in my code so I decided to replace it for a dictionary with a rect, colours, label, and action. Used with the help of AI. 
# Drawn manually every frame. Clicked by checking mouse pos on MOUSEBUTTONDOWN.
# No external library state


custom_buttons = []   # list of dicts, rebuilt each time phase changes

def make_custom_btn(x, y, w, h, label, bg, hover_bg, action):
    return {
        "rect":     pygame.Rect(x, y, w, h),
        "label":    label,
        "bg":       bg,
        "hover_bg": hover_bg,
        "action":   action,
    }

def draw_custom_buttons(mouse_pos):
    for btn in custom_buttons:
        color = btn["hover_bg"] if btn["rect"].collidepoint(mouse_pos) else btn["bg"]
        pygame.draw.rect(screen, color, btn["rect"], border_radius=7)
        pygame.draw.rect(screen, WHITE,  btn["rect"], 1, border_radius=7)
        lbl = font_btn.render(btn["label"], True, WHITE)
        screen.blit(lbl, lbl.get_rect(center=btn["rect"].center))

def handle_custom_click(pos):
    for btn in custom_buttons:
        if btn["rect"].collidepoint(pos):
            btn["action"]()
            return

def build_rank_buttons_custom():
    custom_buttons.clear()
    player_ranks = get_ranks_in_hand(player_hand)

    row1 = ["A", "2", "3", "4", "5", "6", "7"]
    row2 = ["8", "9", "10", "J", "Q", "K"]
    bw, bh, gap = 110, BTN_H, 12

    def make_action(r):
        def action():
            if r in get_ranks_in_hand(player_hand):
                pick_rank(r)
        return action

    total1 = len(row1) * bw + (len(row1)-1) * gap
    sx1 = (SCREEN_W - total1) // 2
    for i, r in enumerate(row1):
        have = r in player_ranks
        custom_buttons.append(make_custom_btn(
            sx1 + i*(bw+gap), BTN_ROW1_Y, bw, bh, r,
            BLUE_BTN if have else GREY_BTN,
            BLUE_HOV if have else GREY_HOV,
            make_action(r)
        ))

    total2 = len(row2) * bw + (len(row2)-1) * gap
    sx2 = (SCREEN_W - total2) // 2
    for i, r in enumerate(row2):
        have = r in player_ranks
        custom_buttons.append(make_custom_btn(
            sx2 + i*(bw+gap), BTN_ROW2_Y, bw, bh, r,
            BLUE_BTN if have else GREY_BTN,
            BLUE_HOV if have else GREY_HOV,
            make_action(r)
        ))

def build_color_buttons_custom():
    custom_buttons.clear()
    bw, bh, gap = 200, BTN_H+8, 40
    total = 3*bw + 2*gap
    sx = (SCREEN_W - total) // 2
    y  = BTN_ROW1_Y + 10
    custom_buttons.append(make_custom_btn(sx,           y, bw, bh, "Red",    RED_BTN,    RED_HOV,             lambda: pick_color("Red")))
    custom_buttons.append(make_custom_btn(sx+bw+gap,    y, bw, bh, "Black",  (30,30,30), (70,70,70),          lambda: pick_color("Black")))
    custom_buttons.append(make_custom_btn(sx+2*(bw+gap),y, bw, bh, "Cancel", DARK_GREY,  (95,95,95),          cancel_color))

# pygame_widgets buttons  (menu / difficulty / game-over only)

menu_buttons     = []
diff_buttons     = []
gameover_buttons = []

clock = pygame.time.Clock()

def clear_pw_buttons(btn_list):
    for btn in btn_list:
        WidgetHandler.removeWidget(btn)
    btn_list.clear()

def clear_all_pw_buttons():
    clear_pw_buttons(menu_buttons)
    clear_pw_buttons(diff_buttons)
    clear_pw_buttons(gameover_buttons)
    custom_buttons.clear()   # also wipe any in-game custom buttons

def make_pw_button(x, y, w, h, text, bg, hover, func):
    return Button(screen, x, y, w, h,
        text=text, fontSize=19, fontColour=WHITE,
        colour=bg, hoverColour=hover, borderRadius=7, onClick=func)

def build_menu_buttons():
    clear_all_pw_buttons()
    cx, bw, bh = SCREEN_W//2, 260, 52
    menu_buttons.append(make_pw_button(cx-bw//2, 320, bw, bh, "Play Game",   BLUE_BTN, BLUE_HOV,     go_to_difficulty))
    menu_buttons.append(make_pw_button(cx-bw//2, 392, bw, bh, "How To Play", TEAL,     (0,185,165),  go_to_howtoplay))
    menu_buttons.append(make_pw_button(cx-bw//2, 464, bw, bh, "Quit",        RED_BTN,  RED_HOV,      quit_game))

def build_difficulty_buttons():
    clear_all_pw_buttons()
    bw, bh = 210, 52
    diff_buttons.append(make_pw_button(100, 360, bw, bh, "Pufferfish (Easy)", (35,130,35),  (55,170,55),  lambda: start_game("easy")))
    diff_buttons.append(make_pw_button(395, 360, bw, bh, "Barracuda (Med)",   (170,120,0),  (215,160,0),  lambda: start_game("medium")))
    diff_buttons.append(make_pw_button(690, 360, bw, bh, "Great White (Hard)",RED_BTN,      RED_HOV,      lambda: start_game("hard")))
    diff_buttons.append(make_pw_button(SCREEN_W//2-80, 440, 160, 42, "Back",  DARK_GREY,    (95,95,95),   go_to_menu))

def build_gameover_buttons():
    clear_all_pw_buttons()
    bw, bh, gap = 220, 55, 40
    sx = (SCREEN_W - (2*bw+gap)) // 2
    gameover_buttons.append(make_pw_button(sx,       520, bw, bh, "Play Again",  BLUE_BTN, BLUE_HOV,    go_to_difficulty))
    gameover_buttons.append(make_pw_button(sx+bw+gap,520, bw, bh, "Main Menu",   TEAL,     (0,185,165), go_to_menu))

# DRAWING TOOL

def draw_text(surface, text, font, color, x, y, centered=False):
    rendered = font.render(text, True, color)
    if centered:
        surface.blit(rendered, rendered.get_rect(center=(x, y)))
    else:
        surface.blit(rendered, (x, y))

def draw_card(surface, cid, x, y, face_up=True):
    surface.blit(cards_deck[cid]["surf"] if face_up else back_surf, (x, y))

def draw_hand_row(surface, hand, y, face_up=True, highlight_ids=None):
    if not hand:
        return
    spacing = min(CARD_W+5, (SCREEN_W-100) // len(hand))
    total   = spacing*(len(hand)-1) + CARD_W
    start_x = (SCREEN_W - total) // 2
    for i, cid in enumerate(hand):
        cx = start_x + i*spacing
        if highlight_ids and cid in highlight_ids:
            pygame.draw.rect(surface, GOLD, (cx-3, y-3, CARD_W+6, CARD_H+6), 3)
        draw_card(surface, cid, cx, y, face_up)

# CARD LOGIC

def get_ranks_in_hand(hand):
    seen = []
    for cid in hand:
        r = cards_deck[cid]["rank"]
        if r not in seen:
            seen.append(r)
    return seen

def check_for_books(hand):
    books_found = []
    rank_counts = {}
    for cid in hand:
        r = cards_deck[cid]["rank"]
        rank_counts.setdefault(r, []).append(cid)
    for rank, ids in rank_counts.items():
        if len(ids) == 4:
            books_found.append(rank)
            for cid in ids:
                hand.remove(cid)
    return books_found

def transfer_cards(rank, color, from_hand, to_hand):
    matches = [cid for cid in from_hand
               if cards_deck[cid]["rank"] == rank and cards_deck[cid]["color"] == color]
    for cid in matches:
        from_hand.remove(cid)
        to_hand.append(cid)
    return matches

def has_rank(hand, rank):
    return any(cards_deck[cid]["rank"] == rank for cid in hand)

def draw_from_deck(deck, hand):
    if not deck:
        return None
    card = deck.pop()
    hand.append(card)
    return card

# AI SYSTEM

class SharkAI:
    def __init__(self, difficulty):
        self.difficulty = difficulty
        self.memory = []               # (rank, color) the AI knows PLAYER holds
        self.recent_player_requests = []

    def add_to_memory(self, rank, color):
        if (rank, color) not in self.memory:
            self.memory.append((rank, color))

    def remove_from_memory(self, rank, color):
        if (rank, color) in self.memory:
            self.memory.remove((rank, color))

    def clean_memory(self, player_hand):
        self.memory = [(r, c) for r, c in self.memory
                       if any(cards_deck[cid]["rank"]==r and cards_deck[cid]["color"]==c
                              for cid in player_hand)]

    def note_player_request(self, rank):
        self.recent_player_requests.append(rank)
        if len(self.recent_player_requests) > 3:
            self.recent_player_requests.pop(0)

    def choose_move(self, ai_hand, player_hand):
        ai_ranks = get_ranks_in_hand(ai_hand)
        if not ai_ranks:
            return None, None
        if self.difficulty == "easy":
            return random.choice(ai_ranks), random.choice(["Red", "Black"])
        if self.difficulty == "medium":
            for rr in self.recent_player_requests:
                if rr in ai_ranks:
                    return rr, random.choice(["Red", "Black"])
            return random.choice(ai_ranks), random.choice(["Red", "Black"])
        if self.difficulty == "hard":
            self.clean_memory(player_hand)
            for rank, color in self.memory:
                if rank in ai_ranks:
                    return rank, color
            return random.choice(ai_ranks), random.choice(["Red", "Black"])
        return None, None

# MESSAGE SYSTEM

chat_log  = []
msg_queue = []
msg_delay = 0
MSG_DELAY_FRAMES = 90

def queue_msg(msg):
    msg_queue.append(msg)

def update_chat():
    global msg_delay
    if not msg_queue:
        return
    if msg_delay > 0:
        msg_delay -= 1
        return
    chat_log.append(msg_queue.pop(0))
    while len(chat_log) > 7:
        chat_log.pop(0)
    msg_delay = MSG_DELAY_FRAMES

def is_queue_empty():
    return len(msg_queue) == 0

# PHASE CONSTANTS

PHASE_MENU        = "menu"
PHASE_DIFFICULTY  = "difficulty"
PHASE_HOW_TO_PLAY = "howtoplay"
PHASE_PICK_RANK   = "pick_rank"
PHASE_PICK_COLOR  = "pick_color"
PHASE_RESOLVING   = "resolving"
PHASE_AI_TURN     = "ai_turn"
PHASE_GAME_OVER   = "game_over"

# GAME States

phase          = PHASE_MENU
ocean_deck     = []
player_hand    = []
ai_hand        = []
player_books   = []
ai_books       = []
shark          = None
selected_rank  = None
selected_color = None
vision_cards   = []
vision_timer   = 0
ai_turn_delay  = 0
pending_action = ""

# GAME Setup

def start_game(difficulty):
    global ocean_deck, player_hand, ai_hand, player_books, ai_books
    global shark, phase, vision_cards, vision_timer
    global selected_rank, selected_color, chat_log, msg_queue, msg_delay
    global pending_action, ai_turn_delay

    ocean_deck    = list(range(1, 53))
    random.shuffle(ocean_deck)
    player_hand   = [ocean_deck.pop() for _ in range(7)]
    ai_hand       = [ocean_deck.pop() for _ in range(7)]
    player_books  = []
    ai_books      = []
    shark         = SharkAI(difficulty)
    vision_cards  = []
    vision_timer  = 0
    selected_rank = None
    selected_color= None
    pending_action= ""
    ai_turn_delay = 0
    chat_log      = []
    msg_queue     = []
    msg_delay     = 0

    found = check_for_books(player_hand); player_books.extend(found)
    found = check_for_books(ai_hand);    ai_books.extend(found)

    diff_names = {"easy": "Pufferfish", "medium": "Barracuda", "hard": "Great White"}
    queue_msg(f"Game started! Your opponent: the {diff_names[difficulty]}!")
    queue_msg("Pick a RANK (blue = you have it), then pick Red or Black.")
    queue_msg("Match both exactly to take cards and go again!")

    phase = PHASE_PICK_RANK
    # Clear ALL pygame_widgets buttons first, then build pure-pygame rank buttons
    clear_all_pw_buttons()
    build_rank_buttons_custom()

# Game navigation system

def go_to_menu():
    global phase
    phase = PHASE_MENU
    build_menu_buttons()

def go_to_difficulty():
    global phase
    phase = PHASE_DIFFICULTY
    build_difficulty_buttons()

def go_to_howtoplay():
    global phase
    phase = PHASE_HOW_TO_PLAY
    clear_all_pw_buttons()

def quit_game():
    pygame.quit()
    sys.exit()

# Player game logic

def pick_rank(rank):
    global selected_rank, phase
    selected_rank = rank
    phase = PHASE_PICK_COLOR
    queue_msg(f"You chose rank [{rank}]. Now pick Red or Black!")
    build_color_buttons_custom()

def cancel_color():
    global selected_rank, phase
    selected_rank = None
    phase = PHASE_PICK_RANK
    build_rank_buttons_custom()

def pick_color(color):
    global selected_color, phase, pending_action, vision_cards, vision_timer
    selected_color = color
    custom_buttons.clear()
    phase = PHASE_RESOLVING

    rank = selected_rank
    shark.note_player_request(rank)
    ai_has_rank = has_rank(ai_hand, rank)

    if not ai_has_rank:
        queue_msg(f"You asked: Do you have {color} {rank}s?")
        queue_msg(f"Shark has NO {rank}s at all... GO FISH!")
        drawn = draw_from_deck(ocean_deck, player_hand)
        if drawn is not None:
            dc, dr, ds = cards_deck[drawn]["color"], cards_deck[drawn]["rank"], cards_deck[drawn]["suit"]
            queue_msg(f"You drew: {dc} {dr} of {ds}.")
        else:
            queue_msg("The Ocean is empty ... nothing to draw!")
        new_books = check_for_books(player_hand)
        if new_books:
            player_books.extend(new_books)
            queue_msg(f"BOOK COMPLETE: {', '.join(new_books)}! Your score: {len(player_books)}")
        pending_action = "gameover" if is_game_over() else "ai_turn"
        if pending_action == "ai_turn":
            queue_msg("...- Shark's turn is next ...-")

    else:
        transferred = transfer_cards(rank, color, ai_hand, player_hand)
        if transferred:
            queue_msg(f"You asked: Do you have {color} {rank}s?")
            queue_msg(f"GOT IT! Shark gave you {len(transferred)} card(s)!")
            vision_cards = list(transferred)
            vision_timer = 300
            queue_msg("DEEP SEA VISION .. your new cards are highlighted above!")
            for cid in transferred:
                r2, s2, c2 = cards_deck[cid]["rank"], cards_deck[cid]["suit"], cards_deck[cid]["color"]
                queue_msg(f"  You received: {c2} {r2} of {s2}!")
            new_books = check_for_books(player_hand)
            if new_books:
                player_books.extend(new_books)
                queue_msg(f"BOOK COMPLETE: {', '.join(new_books)}! Your score: {len(player_books)}")
            pending_action = "gameover" if is_game_over() else "player_again"
            if pending_action == "player_again":
                queue_msg("Nice! Take another turn.")
        else:
            queue_msg(f"You asked: Do you have {color} {rank}s?")
            queue_msg(f"Shark has {rank}s, but NOT {color} ones!  GO FISH!")
            for cid in ai_hand:
                if cards_deck[cid]["rank"] == rank:
                    actual = cards_deck[cid]["color"]
                    queue_msg(f"Hint: Shark has {actual} {rank}s .. remember that!")
                    break
            drawn = draw_from_deck(ocean_deck, player_hand)
            if drawn is not None:
                dc, dr, ds = cards_deck[drawn]["color"], cards_deck[drawn]["rank"], cards_deck[drawn]["suit"]
                queue_msg(f"You drew: {dc} {dr} of {ds}.")
                if dr == rank:
                    shark.add_to_memory(dr, dc)
            else:
                queue_msg("The Ocean is empty .. nothing to draw!")
            new_books = check_for_books(player_hand)
            if new_books:
                player_books.extend(new_books)
                queue_msg(f"BOOK COMPLETE: {', '.join(new_books)}! Your score: {len(player_books)}")
            pending_action = "gameover" if is_game_over() else "ai_turn"
            if pending_action == "ai_turn":
                queue_msg("... Shark's turn is next ...")

def resolve_pending_action():
    global phase, pending_action, ai_turn_delay
    if pending_action == "player_again":
        pending_action = ""
        phase = PHASE_PICK_RANK
        build_rank_buttons_custom()
    elif pending_action == "ai_turn":
        pending_action = ""
        ai_turn_delay  = 0
        phase = PHASE_AI_TURN
    elif pending_action == "gameover":
        pending_action = ""
        phase = PHASE_GAME_OVER
        build_gameover_buttons()

# AI Turn

def run_ai_turn():
    global phase, pending_action

    if not ai_hand:
        queue_msg("Shark has no cards .. drawing from the Ocean.")
        drawn = draw_from_deck(ocean_deck, ai_hand)
        if drawn is None:
            queue_msg("Ocean is empty too! Shark skips.")
        pending_action = "gameover" if is_game_over() else "player_again"
        phase = PHASE_RESOLVING
        return

    rank, color = shark.choose_move(ai_hand, player_hand)
    if rank is None:
        pending_action = "player_again"
        phase = PHASE_RESOLVING
        return

    queue_msg(f"Shark asks YOU: Do you have any {color} {rank}s?")
    phase = PHASE_RESOLVING

    if not has_rank(player_hand, rank):
        queue_msg(f"You have NO {rank}s at all!  Shark goes fishing...")
        drawn = draw_from_deck(ocean_deck, ai_hand)
        queue_msg("Shark drew a card from the Ocean." if drawn else "Ocean is empty .. no card for Shark.")
        pending_action = "gameover" if is_game_over() else "player_again"
        if pending_action == "player_again":
            queue_msg("... Your turn ...")
    else:
        transferred = transfer_cards(rank, color, player_hand, ai_hand)
        if transferred:
            queue_msg(f"You gave Shark {len(transferred)} {color} {rank}(s)!  Ouch!")
            shark.remove_from_memory(rank, color)
            new_books = check_for_books(ai_hand)
            if new_books:
                ai_books.extend(new_books)
                queue_msg(f"Shark completed BOOK: {', '.join(new_books)}!  Shark score: {len(ai_books)}")
            pending_action = "gameover" if is_game_over() else "ai_turn"
            if pending_action == "ai_turn":
                queue_msg("Shark got a card .. it goes AGAIN!")
        else:
            queue_msg(f"You have {rank}s but NOT {color} ones!  Go Fish, Shark!")
            for cid in player_hand:
                if cards_deck[cid]["rank"] == rank:
                    shark.add_to_memory(rank, cards_deck[cid]["color"])
                    break
            drawn = draw_from_deck(ocean_deck, ai_hand)
            queue_msg("Shark drew from the Ocean." if drawn else "Ocean is empty .. nothing for Shark.")
            pending_action = "gameover" if is_game_over() else "player_again"
            if pending_action == "player_again":
                queue_msg("... Your turn ...")

def is_game_over():
    if len(player_books) + len(ai_books) >= 13:
        return True
    if not ocean_deck and not player_hand and not ai_hand:
        return True
    return False

# Draw functions

def draw_menu():
    screen.fill(DARK_GREEN)
    pygame.draw.rect(screen, OCEAN_BLUE, (0, 580, SCREEN_W, 200))
    pygame.draw.rect(screen, (0, 50, 120), (0, 640, SCREEN_W, 140))
    draw_text(screen, "Go-Phish",           font_title, GOLD,       SCREEN_W//2, 160, centered=True)
    draw_text(screen, "The Deep Sea Heist", font_big,   CREAM,      SCREEN_W//2, 230, centered=True)
    draw_text(screen, "Collect 13 Books before the Shark!", font_med, LIGHT_GREY, SCREEN_W//2, 270, centered=True)

def draw_difficulty():
    screen.fill(DARK_GREEN)
    draw_text(screen, "Choose Your Opponent", font_big, GOLD, SCREEN_W//2, 180, centered=True)
    info = [
        ("Pufferfish", "Picks both the rank and color randomly.  Easiest.",      (35,130,35)),
        ("Barracuda",  "Remembers your last 3 requests.  Medium.",       (170,120,0)),
        ("Great White","Tracks everything revealed (had chat reading abilities)",         (175,28,28)),
    ]
    for i, (name, desc, col) in enumerate(info):
        draw_text(screen, f"{name}:  {desc}", font_small, col, SCREEN_W//2, 268+i*30, centered=True)

def draw_howtoplay():
    screen.fill(PANEL_BG)
    draw_text(screen, "How To Play", font_big, GOLD, SCREEN_W//2, 45, centered=True)
    lines = [
        "GOAL: Collect the most Books (4 cards of same rank) before the game ends.",
        "",
        "YOUR TURN:",
        "  1. Click a blue RANK button  (only ranks you already hold are blue).",
        "  2. Click RED or BLACK for the color you think the Shark has.",
        "  3. Full match  (rank + color correct)  ->  take cards, go again",
        "  4. Partial match  (rank right, color wrong)  ->  Shark hints its color, Go Fish.",
        "  5. No match  (Shark has none of that rank)  ->  Go Fish.",
        "",
        "DEEP SEA VISION:",
        "  A full match highlights the cards you just won for 5 seconds.",
        "  The chat also lists every card you received so you can track your hand",
        "",
        "BOOKS:",
        "  All 4 of a rank = 1 Book. Books complete automatically.",
        "",
        "WINNING:",
        "  Game ends when all 13 Books are found.  Most Books wins!",
        "",
        "Click or press any key to go back.",
    ]
    y = 90
    for line in lines:
        draw_text(screen, line, font_small, LIGHT_GREY, 55, y)
        y += 26

def draw_game(mouse_pos):
    screen.fill(GREEN_BG)

    # Status bar
    pygame.draw.rect(screen, PANEL_BG, (0, 0, SCREEN_W, 30))
    draw_text(screen, f"Shark   Books: {len(ai_books)}   Cards: {len(ai_hand)}", font_med, LIGHT_GREY, 12, 5)
    draw_text(screen, f"Ocean: {len(ocean_deck)} cards remaining", font_med, LIGHT_GREY, 680, 5)

    # AI hand
    draw_hand_row(screen, ai_hand, AI_HAND_Y, face_up=False)

    # AI books strip
    pygame.draw.rect(screen, (8, 28, 8), (0, 140, SCREEN_W, 24))
    draw_text(screen, "Shark Books:  " + ("  ".join(ai_books) if ai_books else "(none yet)"),
              font_small, GOLD, 12, 144)

    # Score bar
    pygame.draw.rect(screen, (8, 55, 20), (0, SCORE_Y, SCREEN_W, 22))
    draw_text(screen, f"Your Books: {len(player_books)}    Shark Books: {len(ai_books)}    Total: {len(player_books)+len(ai_books)}/13",
              font_small, CREAM, SCREEN_W//2, SCORE_Y+5, centered=True)

    # Vision banner
    if vision_timer > 0:
        pygame.draw.rect(screen, (0, 80, 190), (0, 192, SCREEN_W, 28))
        draw_text(screen, "~~~ DEEP SEA VISION .. highlighted cards below are your new prizes ~~~",
                  font_small, GOLD, SCREEN_W//2, 198, centered=True)

    # Chat panel
    pygame.draw.rect(screen, PANEL_BG, (0, CHAT_TOP+28, SCREEN_W, 195))
    pygame.draw.line(screen, GOLD, (0, CHAT_TOP+28), (SCREEN_W, CHAT_TOP+28), 1)
    draw_text(screen, "Chat Log", font_chat, GOLD, 10, CHAT_TOP+30)
    for i, line in enumerate(chat_log):
        draw_text(screen, line, font_chat, LIGHT_GREY, 10, CHAT_TOP+48+i*22)

    # Divider
    pygame.draw.line(screen, GOLD, (0, CHAT_BOTTOM), (SCREEN_W, CHAT_BOTTOM), 2)

    # Player hand (highlighted if vision active)
    draw_hand_row(screen, player_hand, PLAYER_HAND_Y, face_up=True,
                  highlight_ids=vision_cards if vision_timer > 0 else None)

    # Player books strip
    pygame.draw.rect(screen, (8, 28, 8), (0, PLAYER_BOOKS_Y, SCREEN_W, 20))
    draw_text(screen, "Your Books:  " + ("  ".join(player_books) if player_books else "(none yet)"),
              font_small, GOLD, 12, PLAYER_BOOKS_Y+2)

    # Instruction label
    pygame.draw.rect(screen, (8, 50, 18), (0, INSTRUCT_Y, SCREEN_W, 22))
    if phase == PHASE_PICK_RANK:
        instr = "YOUR TURN:  Click a BLUE rank button below  (grey = you don't hold that rank)"
    elif phase == PHASE_PICK_COLOR:
        instr = f"You chose rank [{selected_rank}]  ..  now click RED or BLACK"
    elif phase == PHASE_AI_TURN:
        instr = "Shark is thinking..."
    elif phase == PHASE_RESOLVING:
        instr = "Reading the chat above..." if msg_queue else "Processing..."
    else:
        instr = ""
    draw_text(screen, instr, font_small, CREAM, SCREEN_W//2, INSTRUCT_Y+4, centered=True)

    # Draw pure-pygame rank/color buttons
    draw_custom_buttons(mouse_pos)

def draw_gameover():
    screen.fill(DARK_GREEN)
    pygame.draw.rect(screen, PANEL_BG, (170, 140, 660, 380), border_radius=14)
    p, a = len(player_books), len(ai_books)
    if p > a:   result_text, result_color = "YOU WIN!",      GOLD
    elif a > p: result_text, result_color = "SHARK WINS!",     RED_BTN
    else:       result_text, result_color = "It's a TIE!", CREAM
    draw_text(screen, "Game Over",   font_title, GOLD,        SCREEN_W//2, 185, centered=True)
    draw_text(screen, result_text,   font_big,   result_color, SCREEN_W//2, 270, centered=True)
    draw_text(screen, f"Your Books:    {p}",           font_med,   LIGHT_GREY, SCREEN_W//2, 330, centered=True)
    draw_text(screen, f"Shark Books:   {a}",           font_med,   LIGHT_GREY, SCREEN_W//2, 362, centered=True)
    draw_text(screen, f"Total Collected: {p+a} / 13",  font_small, LIGHT_GREY, SCREEN_W//2, 395, centered=True)
    if player_books:
        draw_text(screen, "Your Books: " + "  ".join(player_books),  font_small, GOLD,    SCREEN_W//2, 430, centered=True)
    if ai_books:
        draw_text(screen, "Shark Books: " + "  ".join(ai_books),     font_small, RED_BTN, SCREEN_W//2, 458, centered=True)

# Main loop

build_menu_buttons()

running = True
while running:
    mouse_pos = pygame.mouse.get_pos()
    events = pygame.event.get()

    for event in events:
        if event.type == pygame.QUIT:
            quit_game()
        if event.type == pygame.KEYDOWN:
            if phase == PHASE_HOW_TO_PLAY:
                go_to_menu()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if phase == PHASE_HOW_TO_PLAY:
                go_to_menu()
            elif phase in (PHASE_PICK_RANK, PHASE_PICK_COLOR):
                # Pure-pygame buttons handle their own clicks here
                handle_custom_click(event.pos)

    update_chat()

    if vision_timer > 0:
        vision_timer -= 1
        if vision_timer == 0:
            vision_cards = []

    if phase == PHASE_RESOLVING and is_queue_empty():
        resolve_pending_action()

    if phase == PHASE_AI_TURN:
        ai_turn_delay += 1
        if ai_turn_delay >= 90:
            ai_turn_delay = 0
            run_ai_turn()

    if phase == PHASE_MENU:
        draw_menu()
    elif phase == PHASE_DIFFICULTY:
        draw_difficulty()
    elif phase == PHASE_HOW_TO_PLAY:
        draw_howtoplay()
    elif phase == PHASE_GAME_OVER:
        draw_gameover()
    else:
        draw_game(mouse_pos)

    pygame_widgets.update(events)
    pygame.display.flip()
    clock.tick(60)

pygame.quit()
