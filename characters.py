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

class Assassin(Character):
    def __init__(self, player, name="Assassin"):
        super().__init__(name, player, play_order=0)

    def kill_other_character(self):
        char_list =CHARACTER_CLASSES.remove(Assassin)
        for i, character in enumerate(char_list):
            print(f"{i}: {character.name}")

        target_index = poll_for_index(char_list, "player")
        self.player.game.assassinated = char_list[target_index].name
        print(f"The assassin...")
class Thief(Character):
    def __init__(self, player, name='Thief'):
        super().__init__(name, player, play_order=1)

    def steal_other_character(self):
        char_list =  CHARACTER_CLASSES.remove(Assassin)
        char_list = char_list.remove(self.player.game.assassinated)
        char_list = char_list.remove(Thief)
        for i, character in enumerate(char_list):
            print(f"{i}: {character.name}")
        target_index = poll_for_index(char_list, "player")
        self.player.game.stolen = char_list[target_index].name
        print("The thief will steal")


class Wizard(Character):
    def __init__(self, player, name='Wizard'):
        super().__init__(name, player, play_order=2)

    def swap_cards(self, player_list):
        pass

class King(Character):
    def __init__(self, player, name='King', color='Y', play_order=3):
        super().__init__(name, player, color, play_order)

        self.add_action(
            "Collect yellow district income",
            self.collect_color_money
        )

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
        self.player.money += 1


class Architect(Character):
    def __init__(self, player,name='Architect', color=None, play_order=6):
        super().__init__(name, player, color, play_order)

    def architect_powers(self):
        cards_drew = [self.player.deck.draw_card() for _ in range(2)]
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
            print(f"{i}: {character.name}")
                     
