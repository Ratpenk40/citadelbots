from cards_library import CARD_TYPES, DECK_CONFIGS
from characters import *
from random import shuffle

def poll_player_for_input(possible_values, poll_type='district'):
    poll = f"Press key to select {poll_type} : "
    valid_input = False
    while not valid_input:
        pressed_key = input(poll)
        if pressed_key.isdigit():
            if int(pressed_key) < len(possible_values):
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
        shuffle(self.cards)

class Player:
    def __init__(self, deck, initial_money=2, initial_cards=4, human=True, name='', game=None):
        self.cards = [deck.draw_card() for _ in range(initial_cards)]
        self.money = initial_money
        self.available_actions = []
        self.human = human
        self.played_districts = []
        self.character = None
        self.player_name = name
        self.game = game
        self.first_finished = False
        self.city_completed = False

    def __str__(self):
        return self.player_name

    def pick_character(self, character_deck):
        character_deck.print_available_characters()
        pressed_key = poll_player_for_input(character_deck, 'character')
        character_class = character_deck.characters.pop(pressed_key)
        self.character = character_class(self)
        print(f"{self.player_name} picked {self.character.name}")

    def ressource_gathering(self, deck, draw=True):
        if draw:
            cards_drew = [deck.draw_card() for _ in range(2)]
            for card in cards_drew:
                print(card)
            if self.human:
                pressed_key = poll_player_for_input(cards_drew, 'card_draw')
                selected_card = cards_drew[pressed_key]
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
            sel_dist_index = poll_player_for_input(possible_districts, poll_type='district')
            selected_district = possible_districts[sel_dist_index]
            self.cards.remove(selected_district)
            self.played_districts.append(selected_district)
            self.money -= selected_district.value

    def print_player_status(self):
        print(f"Money: {self.money}")
        print(f"Cards:")
        for c in self.cards:
            print(f"\t-{c}")
        print(f"Played district: ")
        for d in self.played_districts:
            print(f"\t-{d}")
        print("\n")

    def player_turn(self, deck):
        if self.game.assassinated == self.character.name:
            self.game.assassinated = None
            return
        if self.game.stolen == self.character.name:
            thief = [
            player
            for player in self.player.game.players
            if player is not self.player and
                player.character is not None
                and player.character.name == "Thief"
            ][0]
            thief.money += self.money
            self.money = 0

        character_actions = [
            action
            for action in self.available_actions
            if isinstance(action, Action)
        ]
        self.available_actions = [
            'ressources_gathering',
            'play_district',
            *character_actions,
            'end_turn'
        ]
        while len(self.available_actions) > 0:
            print("Available action remaining")
            for i, act in enumerate(self.available_actions):
                print(f"{i} : {act}")
            pressed_key = poll_player_for_input(self.available_actions, "type of action")
            played_action = self.available_actions.pop(pressed_key)
            if isinstance(played_action, Action):
                played_action.play()
            elif played_action == 'ressources_gathering':
                ress_gath_actions = ["Draw", "Money"]
                for i, act in enumerate(ress_gath_actions):
                    print(f"{i}: {act}")
                draw_key = poll_player_for_input(ress_gath_actions, 'select ressource gathering type')
                print(draw_key)
                self.ressource_gathering(deck, ress_gath_actions[draw_key] == 'Draw')
            elif played_action == "play_district":
                self.play_district()
            elif played_action == 'end_turn':
                break
            else:
                pass

            self.print_player_status()

class Game:
    def __init__(self, n_players=2):
        self.n_players = n_players
        card_types_by_name = {card_type['name']: card_type for card_type in CARD_TYPES}
        cards = [
            Card(card_type['name'], card_type['value'], card_type['color'])
            for card_name, count in DECK_CONFIGS['base'].items()
            for card_type in [card_types_by_name[card_name]]
            for _ in range(count)
        ]
        self.deck = Deck(cards)
        self.deck.shuffle()
        self.players = [
            Player(self.deck, name=f"Player {i+1}", game=self)
            for i in range(self.n_players)
        ]
        self.game_finished = False

    def game_turn(self):
        char_deck = CharacterDeck(self.n_players)
        for player in self.players:
            print(f"{player} must pick a character")
            player.pick_character(char_deck)
            print('\n')

        players_in_turn_order = sorted(
            self.players,
            key=lambda player: player.character.play_order
        )
        for player in players_in_turn_order:
            print(f"{player.character.name}: {player.player_name}'s turn")
            player.player_turn(self.deck)
            if len(player.played_districts) >= 7:
                player.city_completed = True
                if not self.game_finished:
                    self.game_finished = True
                    player.first_finish = True

    def play_game(self):
        while not self.game_finished:
            self.game_turn()
        
        

def main():
    game = Game()
    game.game_turn()

            
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
