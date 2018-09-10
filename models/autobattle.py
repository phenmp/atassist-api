import time

from controllers.game_api import GameApi
from configuration import Configuration


class AutoBattle:
    def __init__(self):
        self.configuration = Configuration()
        self.api = GameApi(self.configuration)
        self.refill_five = 0
        self.refill_ten = 0
        self.energy = 0
        self.energy_cost = 99
        self.max_energy = 0
        self.mission_id = '178'
        self.curr_b_id = '0'
        self.mission_name = ""
        self.mission_number = ""
        self.mission_desc = ""
        self.nixons = 0
        self.watts = 0
        self.turds = 0
        self.message_log = []

    def setupBot(self):
        incorrect = 1
        if self.configuration.adventureIsland == "":

            while incorrect:
                print("Note: you can set up a default map in the settings at the top of assist.py file")
                mission_id = input("Which map do you want to play (ie 26-3)?")

                print("Connecting to server...")
                success = self.updateMission(mission_id)

                if success:
                    print("{0} {1}: {2}, Energy Cost {3}".format(self.mission_number, self.mission_name,
                                                                 self.mission_desc, self.energy_cost))
                    inp = input("Correct (y/n)?")
                    if inp == 'Y' or inp == 'y':
                        incorrect = 0
        else:
            self.updateMission(self.configuration.adventureIsland)

        print("Connecting to server...")
        self.initializeUser()
        print("{0} {1}: {2}".format(self.mission_number, self.mission_name, self.mission_desc))
        print("Current Energy : {0}".format(self.energy))
        print("+5 Refills     : {0}".format(self.refill_five))
        print("+10 Refills    : {0}".format(self.refill_ten))

        five = self.refill_five + 1

        while five > self.refill_five:
            inp = input("How many +5 refills to use? ")
            five = int(inp)
            if five < 0:
                five = 0
                print("Using 0 +5 refills")

        self.refill_five -= five
        ten = self.refill_ten + 1

        while ten > self.refill_ten:
            inp = input("How many +10 refills to use? ")
            ten = int(inp)

            if ten < 0:
                ten = 0
                print("Using 0 +10 refills")

        self.refill_ten -= ten
        self.defaultDisplay(five, ten)
        print("Bot starting...")
        success = self.startBot(five, ten)

        return success

    def burnUpEnergy(self):
        incorrect = 1

        if self.configuration.adventureIsland == "":
            print("Note: you can set up a default map in the settings at the top of assist.py file")

            while incorrect:
                mission_id = input("Which map do you want to play (ie 26-3)?")

                print("Connecting to server...")
                success = self.updateMission(mission_id)

                if success:
                    print("{0} : {1} Energy Cost {2}".format(self.mission_number, self.mission_name, self.energy_cost))
                    inp = input("Correct (y/n)?")
                    if inp == 'Y' or inp == 'y':
                        incorrect = 0
        else:
            print("Updating mission info...")
            self.updateMission(self.configuration.adventureIsland)

        print("Updating user information...")
        self.initializeUser()
        self.defaultDisplay()
        print("Bot starting...")
        success = self.startBot()

        return success

    def startBot(self, five=0, ten=0):
        abort = 0
        self.turnOnAutoBattle()

        while not abort and (self.energy > self.energy_cost or five > 0 or ten > 0):
            while not abort and (self.energy < self.energy_cost):
                self.calibrateEnergy()
                full = 0

                while not full:
                    if ten > 0 and self.energy + 11 < self.max_energy:
                        success = self.useRefill(ten=1)
                        if success:
                            ten -= 1
                            self.message_log.append("Used +10 Refill")
                            self.energy += 10
                        else:
                            abort = 1
                    elif five > 0 and self.energy + 6 < self.max_energy:
                        success = self.useRefill(five=1)
                        if success:
                            five -= 1
                            self.energy += 5
                            self.message_log.append("Used +5 Refill")
                        else:
                            abort = 1
                    else:
                        full = 1
                    self.defaultDisplay(five, ten)
                    time.sleep(3)
            if not abort:
                self.defaultDisplay(five, ten)
                self.energy -= self.energy_cost
                self.fightMission()
                self.defaultDisplay(five, ten)
                time.sleep(3)

        return not abort

    def defaultDisplay(self, five=0, ten=0):
        print("{0} {1}: {2}".format(self.mission_number, self.mission_name, self.mission_desc))
        print("Current Energy : {0}".format(self.energy))
        print("+5 Refills     : {0}".format(self.refill_five))
        print("+10 Refills    : {0}".format(self.refill_ten))

        if five:
            print("Use {0} +5 refills".format(five))
        if ten:
            print("Use {0} +10 refills".format(ten))

        print('Totals: Nixons: {0}, Watts: {1}, Turds: {2}'.format(self.nixons, self.watts, self.turds))
        for index in range(len(self.message_log)):
            print(self.message_log[index])

    def calibrateEnergy(self):
        json = self.api.updateAndGetInitFile()
        self.energy = int(json['user_data']['energy'])
        self.refill_five = int(json['user_items']['1002']['number'])
        self.refill_ten = int(json['user_items']['1003']['number'])
        self.max_energy = int(json['user_data']['max_energy'])

    def testing(self):
        self.mission_id = '178'
        if self.fightMission():
            print("Testing finished successfully")

    def fightMission(self):
        print("starting battle vs {0}".format(self.mission_name))
        success = self.startBattle()

        if success:
            print("ending battle vs {0}".format(self.mission_name))
            success, nixons, watts, turds = self.endBattle()

        if success:
            self.nixons += nixons
            self.watts += watts
            self.turds += turds
            mess = 'you won {0} nixons, {1} watts, and {2} turds'.format(nixons, watts, turds)
            self.message_log.append(mess)
        else:
            success = 0

        return success

    def turnOnAutoBattle(self):
        resp = self.api.turnOnAutoBattle()
        success = 0

        if resp['result']:
            print("auto battle enabled")
            success = 1
        else:
            print("FAILURE")
            print(resp)
            success = 0

        return success

    def turnOffAutoBattle(self):
        resp = self.api.turnOffAutoBattle()
        success = 0

        if resp['result']:
            print("auto battle disabled")
            success = 1
        else:
            print("FAILURE")
            print(resp)
            success = 0

        return success

    def startBattle(self):
        response = self.api.startAdventureMission(self.mission_id)
        success = 0

        if response['result']:

            self.curr_b_id = str(response['battle_data']['battle_id'])
            success = 1
        else:
            print("FAILURE")
            print(response)
            success = 0

        return success

    def endBattle(self):
        response = self.api.finishAdventureBattle(self.curr_b_id)
        success = 0
        nixons = 0
        watts = 0
        turds = 0

        if response['result']:
            print("Battle ending...")
            nixons = response['battle_data']['rewards'][0]['gold']
            success = 1

            try:
                turds = response['battle_data']['rewards'][0]['items'][0]['number']
                watts = response['battle_data']['rewards'][0]['sp']
                success = 1
            except:
                turds, watts = 0, 0
        else:
            print("FAILURE")
            print(response)
            success = 0

        return success, nixons, watts, turds

    def initializeUser(self):
        json = self.api.updateAndGetInitFile()
        self.energy = int(json['user_data']['energy'])
        self.refill_five = int(json['user_items']['1002']['number'])
        self.refill_ten = int(json['user_items']['1003']['number'])
        self.max_energy = int(json['user_data']['max_energy'])

    def updateMission(self, mission):
        counter = 0
        lst = []

        while counter < len(mission) - 1 and mission[counter] != '-':
            counter += 1
        if counter == 2:
            mission_left = 10 * int(mission[0]) + int(mission[1])
        elif counter == 1:
            mission_left = int(mission[0])
        else:
            return 0

        mission_right = int(mission[len(mission) - 1])

        if mission_left > 30:
            mission_left = 30
        if mission_left < 0:
            mission_left = 1
        if mission_right > 3:
            mission_right = 3
        if mission_right < 1:
            mission_right = 1

        self.mission_id = str(mission_left * 3 + 101 + mission_right - 4)
        self.mission_number = str(mission_left) + "-" + str(mission_right)

        missions = self.api.getMissions()

        for mission in missions.findall('mission'):
            if mission.find('id').text == self.mission_id:
                self.energy_cost = int(int(mission.find('energy').text) +
                                       float(mission.find('energy_per_level').text) * 12)
                self.mission_name = mission.find('name').text
                self.mission_desc = mission.find('desc').text
        return 1

    def useRefill(self, five=0, ten=0):
        while ten:
            print("Using +10 refill")
            self.api.useEnergyPlusTen()
            self.refill_ten -= 1
            ten -= 1
        while five:
            print("Using +5 refill")
            self.api.useEnergyPlusFive()
            five -= 1
            self.refill_five -= 1
        return 1

    def updateEnergy(self):
        json = self.api.updateAndGetInitFile()
        self.energy = int(json['user_data']['energy'])
