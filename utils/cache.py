import os

from PIL import Image

import constants
from configuration import Configuration
from utils.files import getFullPath


class Cache:
    def __init__(self):
        config = Configuration()
        self.cachePath = config.paths.cachePath
        self.cacheEnabled = config.cacheEnabled
        self.defaultImageQuality = config.imageQuality

        self.files = []

         # todo: clear config

        self.updateFileList()


    def updateFileList(self):
        self.files = os.listdir(getFullPath(self.cachePath))
        self.files.sort()

    def getCardFromCache(self, card):
        name = self.getNameFromCard(card)

        if name in self.files:
            image = Image.open(getFullPath(self.cachePath, name))
        else:
            image = None
        return image

    def saveCardToCache(self, card):
        if self.cacheEnabled:
            name = self.getNameFromCard(card)

            card.image.save(
                getFullPath(self.cachePath, name),
                quality=self.defaultImageQuality)

            self.updateFileList()

    def getNameFromCard(self, card):
        if card.type == constants.COMBO:
            # TODO hash these for better efficiency
            name = str(card.id) + str(card.char.id) + str(card.item.id) + str(card.char.health) + str(
                card.char.attack) + str(card.item.health) + str(card.item.attack)
        else:
            name = str(card.id) + str(card.level)

        return "{0}.png".format(name)
