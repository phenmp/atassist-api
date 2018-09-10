import json
import os


class Configuration(object):
    def __init__(self):
        self.__loadConfig()
        self.assetsUrl = self.__config["assets_url"]
        self.apiUrl = self.__config["api_url"]

        self.initMessageKey = self.__config["message_keys"]["init"]
        self.rankingsMessageKey = self.__config["message_keys"]["rankings"]
        self.warStatusMessageKey = self.__config["message_keys"]["war_status"]
        self.indexMessageKey = self.__config["message_keys"]["index"]
        self.rankIdMessageKey = self.__config["message_keys"]["rank_id"]

        self.indexGuild = self.__config["index_guild"]
        self.indexLeft = self.__config["index_left"]
        self.indexRight = self.__config["index_right"]

        self.xmlFiles = self.__config["xml_files"]
        self.initDataFile = self.__config["init_data_file"]

        self.cardsIndex = self.__config["cards"]
        self.mythicsIndex = self.__config["mythics"]
        self.pcIndex = self.__config["power_combos"]
        self.combosIndex = self.__config["combos"]
        self.missionsIndex = self.__config["missions"]

        self.paths = Paths(self.__config["paths"])

        self.font = self.__config["font"]
        self.imageQuality = self.__config["image_quality"]
        self.cacheEnabled = self.__config["cache_enabled"]
        self.updateXmlOnLoad = self.__config["onload_xml_update"]
        self.adventureIsland = self.__config["adventure_map"]

        self.stills = os.listdir(self.paths.stillsPath)

    def __loadConfig(self):
        with open('config/config.json', 'r') as f:
            self.__config = json.load(f)


class Paths(object):
    def __init__(self, paths):
        self.stillsPath = paths["stills_path"]
        self.framesPath = paths["frames_path"]
        self.savePath = paths["save_path"]
        self.cachePath = paths["cache_path"]
