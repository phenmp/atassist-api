import time
from texttable import Texttable

import constants

from configuration import Configuration
from controllers import GameApi


class Guild(object):
    def __init__(self):
        self.configuration = Configuration()
        self.api = GameApi(self.configuration)

        self.current_war = constants.WARCOUNT
        self.rumble = False
        curr_time = time.time()
        curr_war = constants.WARCOUNT
        start = constants.WARSTART
        end = start + constants.WARDURATION

        while not self.rumble and end < curr_time:
            if start <= curr_time <= end:
                self.rumble = True
            else:
                start += constants.WARPERIOD
                end = start + constants.WARDURATION
                curr_war += 1

        self.current_war = curr_war
        if not self.rumble:
            self.current_war -= 1

    def getGuildScores(self, war):
        data = self.api.getGuildScoresIndiv(war)
        tab = Texttable()
        scores = []

        for entry in data['rankings']['data']:
            scores.append([int(entry['rank']), entry['name'], entry['stat']])

        return scores

    def printGuildScores(self, war):
        data = self.api.getGuildScoresIndiv(war)
        tab = Texttable()

        scores = []
        scores = self.getGuildScores(war)

        if len(scores) % 2 != 0:
            scores.append([len(scores), '', ''])
        scores.sort(key=lambda x: x[0])

        # make table double wide to fit on terminal screen
        dw = [[]]
        mid = int(len(scores) / 2)

        for i in range(0, mid):
            dw.append(
                [scores[i][0], scores[i][1], scores[i][2], scores[i + mid][0], scores[i + mid][1], scores[i + mid][2]])

        tab.add_rows(dw)
        tab.set_cols_align(['r', 'r', 'r', 'r', 'r', 'r'])
        tab.set_cols_width([5, 20, 10, 5, 20, 10])
        tab.header(['Rank', 'Name', 'Score', 'Rank', 'Name', 'Score'])
        print(tab.draw())

    def printMatches(self):
        resp = self.api.getGuildWarStatus()
        matches = [[]]
        tab = Texttable()

        if not resp['guild_war_active']:
            print("No guild war in progress")
            return

        for match in resp['guild_war_matches']:
            result = int(match['us_kills']) - int(match['them_kills'])
            winner = 'Win'
            if result < 0:
                winner = 'Loss'
            matches.append([match['them_name'].encode('utf8'), match['us_kills'], match['them_kills'], result, winner])

        if len(matches) > 1:
            tab.add_rows(matches[1:])
            tab.set_cols_align(['r', 'r', 'r', 'r', 'r'])
            tab.set_cols_width([40, 15, 15, 10, 12])
            tab.header(['Enemy', 'Our Score', 'Their Score', 'Diff', 'Result'])
            print(tab.draw())

    def printAverages(self):
        left = self.api.getLeftPullTab()
        right = self.api.getRightPullTab()
        main = self.api.getGuildWarStatus()
        overnine = [0] * 2
        lessfive = [0] * 2
        count = [0] * 2
        total = [0] * 2
        avr = [0] * 2
        names = [None] * 2

        for player in left['rankings']['data']:
            if int(player['stat']) >= 900:
                overnine[0] = overnine[0] + 1
            if int(player['stat']) <= 500:
                lessfive[0] = lessfive[0] + 1
            count[0] += 1

        for player in right['rankings']['data']:
            if int(player['stat']) >= 900:
                overnine[1] = overnine[1] + 1
            if int(player['stat']) <= 500:
                lessfive[1] = lessfive[1] + 1
                count[1] += 1

        total[0] = int(main['guild_war_matches'][0]['us_kills'])
        total[1] = int(main['guild_war_matches'][0]['them_kills'])
        names[0] = main['guild_war_current_match']['us_name'].encode('utf8')
        names[1] = main['guild_war_current_match']['them_name'].encode('utf8')

        print('*****************************************************************************')
        print('Current Match')
        print('{0} vs {1}'.format(names[0], names[1]))
        print('Players: {0} vs {1}'.format(count[0], count[1]))
        print('Totals : {0} vs {1}'.format(total[0], total[1]))
        avr = [0, 0]
        if count[0] != 0:
            avr[0] = total[0] / count[0]
        if count[1] != 0:
            avr[1] = total[1] / count[1]

        print('Average: {0} vs {1}'.format(avr[0], avr[1]))
        print('900+   : {0} vs {1}'.format(overnine[0], overnine[1]))
        print('500-   : {0} vs {1}'.format(lessfive[0], lessfive[1]))

        if total[0] > total[1]:
            print('Winning by {0}'.format(total[0] - total[1]))
        elif total[1] > total[0]:
            print('Losing by {0}'.format(total[1] - total[0]))
        else:
            print('Tied!')
        print('*****************************************************************************\n')

    def printSiegeStats(self):
        main = self.api.getSiegeStatus()
        left = self.api.getSiegeLeftTab()
        right = self.api.getSiegeRightTab()
        overnine = [0] * 2
        lessfive = [0] * 2
        count = [0] * 2
        total = [0] * 2
        avr = [0] * 2
        names = [None] * 2
        wins = [0] * 2
        losses = [0] * 2
        amb = [0] * 2
        destroyed = [0] * 2

        for island in main['guild_siege_status']['locations']:
            if int(main['guild_siege_status']['locations'][island]['hp']) == 0:
                destroyed[0] += 1000
        for island in main['guild_siege_status']['enemy_locations']:
            if int(main['guild_siege_status']['enemy_locations'][island]['hp']) == 0:
                destroyed[1] += 1000

        for player in left['rankings']['data']:
            score = int(player['stat'])

            if score >= 80:
                overnine[0] = overnine[0] + 1
            if score <= 50:
                lessfive[0] = lessfive[0] + 1

            count[0] += 1
            wins[0] += int(score / 10)
            losses[0] += int(score % 10)

            if score == 10:
                amb[0] += 1
                wins[0] -= 1
                losses[0] += 10

        for player in right['rankings']['data']:
            score = int(player['stat'])

            if score >= 80:
                overnine[1] = overnine[1] + 1
            if score <= 50:
                lessfive[1] = lessfive[1] + 1

            count[1] += 1
            wins[1] += int(score / 10)
            losses[1] += int(score % 10)

            if score == 10:
                amb[1] += 1
                wins[1] -= 1
                losses[1] += 10

        total[0] = int(main['guild_siege_status']['points'])
        total[1] = int(main['guild_siege_status']['enemy_points'])
        names[0] = 'TheGuild of Calamitous Intent'
        names[1] = main['guild_siege_status']['enemy_faction_name']
        avr = [0, 0]

        if count[0] != 0:
            avr[0] = (int(((total[0] - destroyed[1]) / count[0]) * 100)) / 100.0

        if count[1] != 0:
            avr[1] = (int(((total[1] - destroyed[0]) / count[1]) * 100)) / 100.0

        print('\n\n*****************************************************************************')
        print(' {0} vs {1}'.format(names[0], names[1]))
        print(' Players: {0} vs {1}'.format(count[0], count[1]))
        print(' Totals : {0} vs {1}'.format(total[0], total[1]))
        print(' Average: {0} vs {1}'.format(avr[0], avr[1]))
        print(' Wins   : {0} vs {1}'.format(wins[0], wins[1]))
        print(' Losses : {0} vs {1}'.format(losses[0], losses[1]))
        print(' 80+    : {0} vs {1}'.format(overnine[0], overnine[1]))
        print(' 50-    : {0} vs {1}'.format(lessfive[0], lessfive[1]))
        print(' 10     : {0} vs {1} (Counted as 10 losses)'.format(amb[0], amb[1]))
        print(' Used   : {0} vs {1}'.format(wins[0] + losses[0], wins[1] + losses[1]))
        print(' Left   : {0} vs {1}'.format(500 - wins[0] - losses[0], 500 - wins[1] - losses[1]))

        if total[0] > total[1]:
            print(' Winning by {0}'.format(total[0] - total[1]))
        elif total[1] > total[0]:
            print(' Losing by {0}'.format(total[1] - total[0]))
        else:
            print(' Tied!')
        print('*****************************************************************************\n')

    """
    Current War
    Print matches
    print all 50 scores
    print stats
    *print missing players
    *print thier missing players

    print all guild mates' scores
    print leaderboard
    """
