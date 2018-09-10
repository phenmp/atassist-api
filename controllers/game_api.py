from flask import jsonify
import urllib.request as urllib
from flask import json

import os.path
import os

import xml.etree.ElementTree as ET

from utils.files import getFullPath


class GameApi:
    def __init__(self, config):
        self.config = config

    def getGuildWarStatus(self, context):
        print(json.dumps(context.__dict__))

        req = '{0}getGuildWarStatus{1}'.format(
            self.config.apiUrl,
            self.__getUrlAuthSection(context)
        )
        f = urllib.urlopen(req)
        resp = f.read().decode('utf-8')
        return resp

    def setActiveDeck(self, context):
        req = '{0}setActiveDeck&deck_id={1}{2}'.format(self.config.apiUrl, context.deck,
                                                       self.__getUrlAuthSection(context))
        f = urllib.urlopen(req)
        resp = f.read().decode('utf-8')
        return json.loads(resp)

    def startPracticeVsMe(self, context):
        req = '{0}startPracticeBattle&target_user_id={1}{2}'.format(self.config.apiUrl, context.userId,
                                                                    self.__getUrlAuthSection(context))
        f = urllib.urlopen(req)
        resp = f.read()

    def surrender(self, context):
        req = '{0}forfeitBattle{1}'.format(self.config.apiUrl, self.__getUrlAuthSection(context))
        f = urllib.urlopen(req)
        resp = f.read().decode('utf-8')
        print(resp)

    def useEnergyPlusFive(self, context):
        req = '{0}useItem&number=1&item_id=1002{1}'.format(self.config.apiUrl, self.__getUrlAuthSection(context))
        f = urllib.urlopen(req)
        s = f.read().decode('utf-8')
        return json.loads(s)

    def useEnergyPlusTen(self, context):
        req = '{0}useItem&number=1&item_id=1003{1}'.format(self.config.apiUrl, self.__getUrlAuthSection(context))
        f = urllib.urlopen(req)
        s = f.read().decode('utf-8')
        return json.loads(s)

    def turnOnAutoBattle(self, context):
        req = '{0}setUserFlag&flag=autopilot&value=1{1}'.format(self.config.apiUrl, self.__getUrlAuthSection(context))
        f = urllib.urlopen(req)
        s = f.read().decode('utf-8')
        return json.loads(s)

    def turnOffAutoBattle(self, context):
        req = '{0}setUserFlag&flag=autopilot&value=0{1}'.format(self.config.apiUrl, self.__getUrlAuthSection(context))
        f = urllib.urlopen(req)
        s = f.read().decode('utf-8')
        return json.loads(s)

    def startAdventureMission(self, context, level_id):
        req = '{0}startMission&mission_id={1}{2}'.format(self.config.apiUrl, level_id,
                                                         self.__getUrlAuthSection(context))
        f = urllib.urlopen(req)
        s = f.read().decode('utf-8')
        return json.loads(s)

    def finishAdventureBattle(self, context, battle_id):
        req = '{0}playCard&skip=true&host_id={1}&battle_id={2}{3}'.format(self.config.apiUrl, context.userId, battle_id,
                                                                          self.__getUrlAuthSection(context))
        f = urllib.urlopen(req)
        s = f.read().decode('utf-8')
        return json.loads(s)

    # XML api
    def updateXMLFiles(self):
        for parser in self.config.xmlFiles:
            f = urllib.urlopen(str(self.config.assetsUrl + parser))
            response = f.read()

            target = open(getFullPath('resources', 'xml_files', parser), 'wb')
            target.truncate()
            target.write(response)
            target.close()
            f.close()

    def checkForUpdates(self):
        for i in range(self.config.cardsIndex, self.config.combosIndex):
            if (not (os.path.isfile(self.config.xmlFiles[i]))):
                print("Missing XML file, updating all.")
                self.updateXMLFiles()
                return
        for counter in self.config.xmlFiles:
            f = urllib.urlopen(self.config.assetsUrl + counter)
            response = f.read()
            target = open(counter, 'rb')
            the_file = target.read()
            if (the_file == response):
                print('{0} contains no new updates'.format(counter))
            else:
                print('{0} has new updates!!!'.format(counter))
            target.close()
            f.close()

    # Init API
    def __getUserInitFilePath(self, userId):
        initFilename = "{0}_{1}".format(userId, self.config.initDataFile)
        return getFullPath('resources', 'init_files', initFilename)

    def updateInitFile(self, context):
        req = "{0}{1}&api_stat_time=249{2}".format(self.config.apiUrl, self.config.initMessageKey,
                                                   self.__getUrlAuthSection(context))

        f = urllib.urlopen(req)
        response = f.read()

        userInitFilePath = self.__getUserInitFilePath(context.userId)

        target = open(userInitFilePath, 'wb')
        target.truncate()

        target.write(response)
        target.close()

    def getInit(self, context):
        userInitFilePath = self.__getUserInitFilePath(context.userId)

        if (os.path.exists(userInitFilePath)):
            f = open(userInitFilePath, "r")
            s = f.read()
            result = json.loads(s)
        else:
            result = self.updateAndGetInitFile(context)
        return result

    def updateAndGetInitFile(self, context):
        print('[GameAPI] updateAndGetInitFile')
        req = "{0}{1}{2}".format(self.config.apiUrl, self.config.initMessageKey, self.__getUrlAuthSection(context))

        f = urllib.urlopen(req)
        response = f.read().decode('utf-8')

        userInitFilePath = self.__getUserInitFilePath(context.userId)

        target = open(userInitFilePath, 'w')
        target.truncate()

        target.write(response)
        target.close()

        return json.loads(response)

    def isInActiveBattle(self, context):
        json = self.updateAndGetInitFile(context)
        return 'active_battle_data' in json

    # cards
    def __getXmlFile(self, fileType):
        filePath = getFullPath('resources', 'xml_files', self.config.xmlFiles[fileType])

        if (not (os.path.isfile(filePath))):
            self.updateXMLFiles()

        xmlFile = ET.parse(filePath)

        return xmlFile.getroot()

    def getCards(self):
        return self.__getXmlFile(self.config.cardsIndex)

    def getPC(self):
        return self.__getXmlFile(self.config.pcIndex)

    def getMythics(self):
        return self.__getXmlFile(self.config.mythicsIndex)

    def getCombos(self):
        return self.__getXmlFile(self.config.combosIndex)

    def getMissions(self):
        return self.__getXmlFile(self.config.missionsIndex)

    # Guild war
    def getGuildScoresIndiv(self, context, war):
        req = "{0}getRankings&ranking_id=event_guild&ranking_index={1}{2}".format(self.config.apiUrl, str(50000 + war),
                                                                                  self.__getUrlAuthSection(context))
        f = urllib.urlopen(req)
        response = f.read().decode('utf-8')
        return json.loads(response)

    def getLeftPullTab(self, context):
        req = "{0}getRankings&ranking_id=event_guild_war&ranking_index=0{1}".format(self.config.apiUrl,
                                                                                    self.__getUrlAuthSection(context))
        f = urllib.urlopen(req)
        response = f.read().decode('utf-8')
        return json.loads(response)

    def getRightPullTab(self, context):
        req = "{0}getRankings&ranking_id=event_guild_war&ranking_index=1{1}".format(self.config.apiUrl,
                                                                                    self.__getUrlAuthSection(context))
        f = urllib.urlopen(req)
        response = f.read().decode('utf-8')
        return json.loads(response)

    # Guild Siege
    def getSiegeStatus(self, context):
        req = "{0}getGuildSiegeStatus{1}".format(self.config.apiUrl, self.__getUrlAuthSection(context))
        f = urllib.urlopen(req)
        s = f.read().decode('utf-8')
        return json.loads(s)

    def getSiegeLeftTab(self, context):
        req = "{0}getRankings&ranking_id=event_guild_siege&ranking_index=0{1}".format(self.config.apiUrl,
                                                                                      self.__getUrlAuthSection(context))
        f = urllib.urlopen(req)
        s = f.read().decode('utf-8')
        return json.loads(s)

    def getSiegeRightTab(self, context):
        req = "{0}getRankings&ranking_id=event_guild_siege&ranking_index=1{1}".format(self.config.apiUrl,
                                                                                      self.__getUrlAuthSection(context))
        f = urllib.urlopen(req)
        s = f.read().decode('utf-8')
        return json.loads(s)

    # utils
    def __getUrlAuthSection(self, context):
        return "&user_id={0}&password={1}".format(context.userId, context.password)
