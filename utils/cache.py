import os
from PIL import Image

from configuration import Configuration
from utils.files import getFullPath

from models.card_basic import CardBasic


class Cache:
    def __init__(self):
        self.config = Configuration()
        self.updateFileList()


    def updateFileList(self):
        self.files = os.listdir(getFullPath(self.config.paths.cachePath))
        self.files.sort()

    def getCardFromCache(self, card):
        name = self.getNameFromCard(card)

        if name in self.files:
            image = Image.open(getFullPath(self.config.paths.cachePath, name))
        else:
            image = None
        return image

    def saveCardToCache(self, card):
        if self.config.cacheEnabled:
            name = self.getNameFromCard(card)
            card.image.save(
                getFullPath(self.config.paths.cachePath, name),
                quality=self.config.imageQuality)
            self.updateFileList()

    def getNameFromCard(self, card):
        if card.type == CardBasic.COMBO:
            # TODO hash these for better efficiency
            name = str(card.id) + str(card.char.id) + str(card.item.id) + str(card.char.health) + str(
                card.char.attack) + str(card.item.health) + str(card.item.attack)
        else:
            name = str(card.id) + str(card.level)

        return "{0}.png".format(name)
