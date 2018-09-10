from controllers.game_api import GameApi

from configuration import Configuration
from models.deck import Deck


class Bot:
    # Constants
    ARENA = 0
    RUMBLE = 1

    def __init__(self):
        self.config = Configuration()
        self.api = GameApi(self.config)

        self.my_hand = None
        self.enemy_hand = None
        self.field = []
        self.style = self.ARENA

    def initializeGame(self, style=0):
        resp = self.api.updateAndGetInitFile()
        # prioritize drunk and craze
        # choose item over character
        # go two wide when opponent opens with precombo
        # resp['active_battle_data']['attack_commander']        #returns 3003 for Tina
        # resp['active_battle_data']['attack_commander_level']  #returns level for hero
        # resp['active_battle_data']['defend_commander']        #returns 3003 for Tina
        # resp['active_battle_data']['defend_commander_level']  #returns level for hero
        # Update my hand and enemy's first card

        self.my_hand = Deck()
        self.my_hand.updateAsMyDeck()
        self.enemy_hand = Deck()
        self.enemy_hand.updateAsEnemyDeck()

    def getSuggestion(self):
        print("NOT IMPLEMENTED")
