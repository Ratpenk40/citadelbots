import numpy as np
class Character:
    def __init__(self, name, player, color=None, play_order=0):
        self.name = name
        self.color = color
        self.player = player
        self.play_order = play_order

    def __str__(self):
        print(self.name)

    def collect_color_money(self):
        if self.color is not None:
            for dist in self.player.played_district:
                if dist.color == self.color:
                    self.player.money += 1
    

class Assassin(Character):
    def __init__(self, name="Assassin"):
        super().__init__(name, play_order=0)

    def kill_other_character(self, character_list):
        pass

class Thief(Character):
    def __init__(self, name='Thief'):
        super().__init__(name, play_order=1)

    def steal_other_character(self, character_list):
        pass

class Wizard(Character):
    def __init__(self, name='Wizard'):
        super().__init__(name, play_order=2)

    def swap_cards(self, player_list):
        pass

class King(Character):
    def __init__(self, player, name='King', color='Y', play_order=3):
        super().__init__(name, player, color, play_order)

class Bishop(Character):
    def __init__(self, player, name='Bishop', color="B", play_order=4):
        super().__init__(name, player, color, play_order)

class Merchant(Character):
    def __init__(self,player, name='Merchant', color="G", play_order=5):
        super().__init__(name, player, color, play_order)

class Architect(Character):
    def __init__(self, player,name='Architect', color=None, play_order=6):
        super().__init__(name, player, color, play_order)

class Condottiere(Character):
    def __init__(self,  player,name='Condottiere', color='R', play_order=7):
        super().__init__(name, player, color, play_order)


class CharacterDeck:
    def __init__(self, n_players):
        self.n_players = n_players
        self.visible = []
        self.characters = [
            Assassin,
            Thief,
            Wizard,
            King,
            Bishop,
            Merchant,
            Architect,
            Condottiere
        ]

        sel_hidden = np.random.randint(0, len(self.characters), 1)
        self.hidden = self.characters.pop(sel_hidden)
        valid = False

        if self.n_player == 7:
            n_player_picks = 6
        else:
            n_player_picks = self.n_players
        while not valid:
            sel_visible = np.random.randint(0, len(self.characters), 6 - n_player_picks)
            if King in np.array(self.characters)[sel_visible]:
                continue
            for sv in sel_visible:
                self.visible.append(self.characters.pop(sv))
            valid = True
                     