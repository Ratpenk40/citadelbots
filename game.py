from cards_library import CARD_TYPES, DECK_CONFIGS
from characters import *
from random import shuffle

def poll_player_for_input(possible_values, poll_type='district'):
    poll = f"Press key to select {poll_type} : "
    valid_input = False
    while not valid_input:
        pressed_key = input(poll)
        if pressed_key.isdigit():
            if int(pressed_key) <= len(possible_values):
                valid_input = True
                return int(pressed_key)

        print('Please type a valid number')

class Card:
    def __init__(self, name, value, color):
        self.name = name
        self.value = value
        self.color = color
    def __str__(self):
        return ' '.join([self.name, str(self.value), self.color])

class Deck:
    def __init__(self, cards):
        self.cards = cards

    def draw_card(self):
        return self.cards.pop(0)

    def shuffle(self):
        self.cards = shuffle(self.cards)



class Player:
    def __init__(self, deck, initial_money=2, initial_cards=4, human=True, name=''):
        self.cards = [deck.draw_card()] * initial_cards
        self.money = initial_money
        self.available_actions = ['ressources_gathering', 'play_district', 'end_turn']
        self.human = human
        self.played_districts = []
        self.character = None
        self.player_name = name

    def pick_character(self, character_deck):
        pressed_key = poll_player_for_input(character_deck, 'character')
        self.character = character_deck.characters.pop(pressed_key)
        # initialize character
        self.character = self.character(self)

    def ressource_gathering(self, deck, draw=True):
        if draw:
            cards_drew = [deck.draw_card()] * 2
            for card in cards_drew:
                print(card)
            if self.human:
                pressed_key = poll_player_for_input(cards_drew, 'card_draw')
                self.cards.append(cards_drew[pressed_key])
            else:
                selected_card = cards_drew[0] # for the moment only the first
            self.cards.append(selected_card)
        else: # money
            self.money += 2

        print(self.print_player_status())

    def play_district(self):
        possible_districts = [card for card in self.cards if card.value <= self.money]
        print("Select district:")
        for i, dist in enumerate(possible_districts):
            print(f"{i}: {dist.name}, {dist.value}, {dist.color}")
        if self.human:
            # Poll to get playable district
            sel_dist_index = poll_player_for_input(len(possible_districts), poll_type='district')
            selected_district = self.cards.pop(sel_dist_index)
            self.played_districts.append(selected_district)
            self.money -= selected_district

    def print_player_status(self):
        print(f"Money: {self.money}")
        print(f"Cards: {self.cards}")
        print(f"Played district: {self.played_districts}\n")

    def player_turn(self, deck):
        while len(self.available_actions) > 0:
            print("Available action remaining")
            for i, act in enumerate(self.available_actions):
                print(f"{i} : {act}")
            pressed_key = poll_player_for_input(self.available_actions)
            played_action = self.available_actions.pop(pressed_key)
            if played_action == 'ressources_gathering':
                self.ressource_gathering(deck)
            elif played_action == "play_district":
                self.play_district()
            elif played_action == 'end_turn':
                break
            else:
                pass

            self.print_player_status()

class Game:
    def __init__(self, n_players=4):
        self.n_players = n_players
        cards = [Card(c['name'], c['value'], c['color']) for c in DECK_CONFIGS['base']]
        self.deck = Deck(cards)
        self.deck.shuffle()
        self.players = [Player(self.deck, name=f"Player {i+1}") for i in range(self.n_players)]

    def game_turn(self):
        char_deck = CharacterDeck(self.n_players)
        for player in self.players:
            player.pick_character(char_deck)

        player_order = [player.character.play_order for player in self.players]

        

def main():

    print(deck.draw_card())
    # while game_not_ended:
    for i in range(10):
        player1 = Player(deck)
        player1.player_turn(deck)

    print(deck)

            
if __name__ == '__main__':
    main()
        



    














# import pygame

# # pygame setup
# pygame.init()
# screen = pygame.display.set_mode((1280, 720))
# clock = pygame.time.Clock()
# running = True
# dt = 0

# player_pos = pygame.Vector2(screen.get_width() / 2, screen.get_height() / 2)

# while running:
#     # poll for events
#     # pygame.QUIT event means the user clicked X to close your window
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False

#     # fill the screen with a color to wipe away anything from last frame
#     screen.fill("purple")

#     pygame.draw.circle(screen, "red", player_pos, 40)

#     keys = pygame.key.get_pressed()
#     if keys[pygame.K_w]:
#         player_pos.y -= 300 * dt
#     if keys[pygame.K_s]:
#         player_pos.y += 300 * dt
#     if keys[pygame.K_a]:
#         player_pos.x -= 300 * dt
#     if keys[pygame.K_d]:
#         player_pos.x += 300 * dt

#     # flip() the display to put your work on screen
#     pygame.display.flip()

#     # limits FPS to 60
#     # dt is delta time in seconds since last frame, used for framerate-
#     # independent physics.
#     dt = clock.tick(60) / 1000

# pygame.quit()