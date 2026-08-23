from random import shuffle

def poll_for_index(possible_values, poll_type):
    poll = f"Press key to select {poll_type} : "
    while True:
        pressed_key = input(poll)
        if pressed_key.isdigit() and int(pressed_key) < len(possible_values):
            return int(pressed_key)
        print('Please type a valid number')

class Action:
    def __init__(self, name, callback, description=""):
        self.name = name
        self.callback = callback
        self.description = description

    def play(self):
        return self.callback()

    def __str__(self):
        return self.name

class Character:
    def __init__(self, name, player, color=None, play_order=0):
        self.name = name
        self.color = color
        self.player = player
        self.play_order = play_order

    def __str__(self):
        return self.name

    def collect_color_money(self):
        if self.color is not None:
            for dist in self.player.played_districts:
                if dist.color == self.color:
                    self.player.money += 1

    def add_action(self, name, callback, description=""):
        action = Action(name, callback, description)
        self.player.available_actions.append(action)

    def on_turn_start(self):
        pass

    def other_character_classes(self, excluded_classes=None):
        excluded_classes = excluded_classes or []
        return [
            character_class
            for character_class in CHARACTER_CLASSES
            if character_class is not self.__class__
            and character_class not in excluded_classes
        ]

class Assassin(Character):
    def __init__(self, player, name="Assassin"):
        super().__init__(name, player, play_order=0)

        self.add_action(
            "Assassinate a character",
            self.kill_other_character
        )

    def kill_other_character(self):
        character_classes = self.other_character_classes()
        for i, character_class in enumerate(character_classes):
            print(f"{i}: {character_class.__name__}")

        target_index = poll_for_index(character_classes, "character")
        target_name = character_classes[target_index].__name__
        self.player.game.assassinated = target_name
        print(f"The assassin killed the {target_name}.")

class Thief(Character):
    def __init__(self, player, name='Thief'):
        super().__init__(name, player, play_order=1)

        self.add_action(
            "Steal from a character",
            self.steal_other_character
        )

    def steal_other_character(self):
        excluded_classes = [Assassin]
        if self.player.game.assassinated is not None:
            excluded_classes.extend([
                character_class
                for character_class in CHARACTER_CLASSES
                if character_class.__name__ == self.player.game.assassinated
            ])
        character_classes = self.other_character_classes(excluded_classes)
        for i, character_class in enumerate(character_classes):
            print(f"{i}: {character_class.__name__}")
        target_index = poll_for_index(character_classes, "character")
        target_name = character_classes[target_index].__name__
        self.player.game.stolen = target_name
        print(f"The thief will steal from the {target_name}.")


class Wizard(Character):
    def __init__(self, player, name='Wizard'):
        super().__init__(name, player, play_order=2)

        self.add_action(
            "Use Wizard power",
            self.use_wizard_power
        )

    def use_wizard_power(self):
        options = [
            "Exchange hand with another player",
            "Discard cards and draw replacements"
        ]
        for i, option in enumerate(options):
            print(f"{i}: {option}")
        selected_option = poll_for_index(options, "wizard power")
        if selected_option == 0:
            self.swap_cards()
        else:
            self.discard_and_draw()

    def swap_cards(self):
        if self.player.game is None:
            print("Wizard needs a game with players to exchange cards.")
            return

        possible_targets = [
            player
            for player in self.player.game.players
            if player is not self.player
        ]
        if not possible_targets:
            print("No player available to exchange cards with.")
            return

        print("Select player:")
        for i, target in enumerate(possible_targets):
            print(f"{i}: {target.player_name}")
        target_index = poll_for_index(possible_targets, "player")
        target = possible_targets[target_index]
        self.player.cards, target.cards = target.cards, self.player.cards
        print(f"{self.player.player_name} exchanged cards with {target.player_name}.")

    def discard_and_draw(self):
        if self.player.game is None:
            print("Wizard needs a game deck to draw replacement cards.")
            return

        if not self.player.cards:
            print("No cards to discard.")
            return

        possible_counts = list(range(len(self.player.cards) + 1))
        print("Select number of cards to discard:")
        for count in possible_counts:
            print(f"{count}: {count}")
        discard_count = poll_for_index(possible_counts, "number of cards")

        for _ in range(discard_count):
            print("Select card to discard:")
            for i, card in enumerate(self.player.cards):
                print(f"{i}: {card}")
            card_index = poll_for_index(self.player.cards, "card")
            discarded = self.player.cards.pop(card_index)
            self.player.game.deck.add_card(discarded)

        drawn_cards = [
            self.player.game.deck.draw_card()
            for _ in range(discard_count)
        ]
        self.player.cards.extend(drawn_cards)
        print(f"{self.player.player_name} discarded and drew {discard_count} cards.")

class King(Character):
    def __init__(self, player, name='King', color='Y', play_order=3):
        super().__init__(name, player, color, play_order)

        self.add_action(
            "Collect yellow district income",
            self.collect_color_money
        )

    def on_turn_start(self):
        for other_player in self.player.game.players:
            other_player.is_king = False
        self.player.is_king = True

class Bishop(Character):
    def __init__(self, player, name='Bishop', color="B", play_order=4):
        super().__init__(name, player, color, play_order)

        self.add_action(
            "Collect blue district income",
            self.collect_color_money
        )

class Merchant(Character):
    def __init__(self,player, name='Merchant', color="G", play_order=5):
        super().__init__(name, player, color, play_order)

        self.add_action(
            "Collect green district income",
            self.collect_color_money
        )

    def on_turn_start(self):
        self.player.money += 1


class Architect(Character):
    def __init__(self, player,name='Architect', color=None, play_order=6):
        super().__init__(name, player, color, play_order)

        self.add_action(
            "Use Architect power",
            self.architect_powers
        )

    def architect_powers(self):
        cards_drew = [self.player.game.deck.draw_card() for _ in range(2)]
        self.player.cards.extend(cards_drew)
        self.player.available_actions.extend(['play_district','play_district'])


class Condottiere(Character):
    def __init__(self,  player,name='Condottiere', color='R', play_order=7):
        super().__init__(name, player, color, play_order)

        self.add_action(
            "Collect red district income",
            self.collect_color_money
        )
        self.add_action(
            "Destroy a district",
            self.destroy_district
        )

    def destroy_district(self):
        if self.player.game is None:
            print("Condottiere needs a game with players to destroy a district.")
            return

        other_players = [
            player
            for player in self.player.game.players
            if player is not self.player
            and player.played_districts
            and not player.city_completed
            and not (
                player.character is not None
                and player.character.name == "Bishop"
            )
        ]
        possible_targets = [
            player
            for player in other_players
            if any(district.value - 1 <= self.player.money for district in player.played_districts)
        ]

        if not possible_targets:
            print("No district can be destroyed.")
            return

        print("Select player:")
        for i, target in enumerate(possible_targets):
            print(f"{i}: {target.player_name}")
        target_index = poll_for_index(possible_targets, "player")
        target = possible_targets[target_index]

        possible_districts = [
            district
            for district in target.played_districts
            if district.value - 1 <= self.player.money
        ]
        print("Select district to destroy:")
        for i, district in enumerate(possible_districts):
            destruction_cost = max(0, district.value - 1)
            print(f"{i}: {district.name}, cost to destroy: {destruction_cost}")
        district_index = poll_for_index(possible_districts, "district")
        district = possible_districts[district_index]
        destruction_cost = max(0, district.value - 1)

        target.played_districts.remove(district)
        self.player.money -= destruction_cost
        print(
            f"{self.player.player_name} destroyed {target.player_name}'s "
            f"{district.name} for {destruction_cost} gold."
        )


CHARACTER_CLASSES = [
    Assassin,
    Thief,
    Wizard,
    King,
    Bishop,
    Merchant,
    Architect,
    Condottiere
]


class CharacterDeck:
    def __init__(self, n_players):
        self.n_players = n_players
        self.visible = []
        self.characters = CHARACTER_CLASSES.copy()
        shuffle(self.characters)

        self.hidden = self.characters.pop()
        visible_count = self._visible_discard_count()
        while len(self.visible) < visible_count:
            character = self.characters.pop()
            if character is King:
                self.characters.insert(0, character)
                shuffle(self.characters)
                continue
            self.visible.append(character)

    def __len__(self):
        return len(self.characters)

    def _visible_discard_count(self):
        if self.n_players == 4:
            return 2
        if self.n_players == 5:
            return 1
        return 0

    def print_available_characters(self):
        print("Available characters:")
        for i, character in enumerate(self.characters):
            print(f"{i}: {character.__name__}")
                     
