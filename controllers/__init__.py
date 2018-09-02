from flask import Blueprint, request, jsonify
from flask_restful import reqparse

from configuration import Configuration
from controllers.game_api import GameApi
from controllers.deck import Deck

from contexts.base_context import BaseContext
from contexts.deck_context import DeckContext

import pdb

api = Blueprint("api", __name__)

deckController = Deck()

# 1.  Print Deck
@api.route('/api/deck/print-deck', methods=['POST'])
def deck_print():
    context = DeckContext(request)

    shouldUpdateDeck = deckController.updateAsMyDeck(context)

    print('Update Deck: ', shouldUpdateDeck)
    
    # TODO: need a proper response here
    if not shouldUpdateDeck:
        return "No active battle data. Go attack someone!"
        
    return jsonify(deckController.printDeck(context))    

# 2.  Create Image of Deck
@api.route('/api/deck/create-deck-image', methods=['POST'])
def deck_create_image():
    context = DeckContext(request)

    shouldUpdateDeck = deckController.updateAsMyDeck(context)

    print('Update Deck: ', shouldUpdateDeck)
    # TODO: need a proper response here
    if not shouldUpdateDeck:
        return "No active battle data. Go attack someone!"
        
    return "Create Deck Image"

# 3. Create Image of Inventory
@api.route('/api/deck/create-inventory-image', methods=['POST'])
def create_inventory_image():
    context = DeckContext(request)

    cards = deckController.updateAsInventory(context)

    # TODO: 
    # filepath = deckController.createLargeDeckImage("",10)
    # validImage(filepath)

# @api.route('/api/deck/filter-inventory-trait', methods=['POST'])

# @api.route('/api/deck/filter-inventory-show', methods=['POST'])

# @api.route('/api/deck/analysis', methods=['POST'])
