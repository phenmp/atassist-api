from controllers.game_api import GameApi
from configuration import Configuration

api = GameApi(Configuration())

print(api.getMissions())