from __future__ import annotations
from random import choice, shuffle
from typing import TYPE_CHECKING

from src.opponent_match import OpponentMatch
from src.settings import CFBGlobalSettings

if TYPE_CHECKING:
    from src.cfb import CFB
    from src.team import Team


class TeamScheduler:
    def __init__(self, cfb: CFB):
        self.cfb = cfb

        self.CONFERENCE_CYCLE = [
            (1, ((2,3), (4,5), (6,7))), # 1
            (2, ((1,5), (3,7), (4,6))), # 2
            (3, ((1,6), (2,5), (4,7))), # 3
            (4, ((1,7), (2,6), (3,5))), # 4
            (5, ((1,4), (2,7), (3,6))), # 5
            (6, ((1,3), (2,4), (5,7))), # 6
            (7, ((1,2), (3,4), (5,6))), # 7
        ]
        shuffle(self.CONFERENCE_CYCLE)

        self.OPP_CONF_CYCLE = [
            ((1,2), (3,4), (5,6)),
            ((1,3), (2,5), (4,6)),
            ((1,4), (2,6), (3,5)),
            ((1,5), (2,4), (3,6)),
            ((1,6), (2,3), (4,5)),
        ]
        shuffle(self.OPP_CONF_CYCLE)

    def generate_schedules(self):
        """
        Current Mode Ideas
        0: Pure Random w/o duplicates (V7 Default)
        1: Every Half Conference (6) + 1 Conf + 5 Non-Conf (V8 Option)
        """

        is_conf_week_pool = (
            [False, False, True, True, False, True, True, False, True, True, False, True]
            if CFBGlobalSettings.isConferenceOppOn.value
            else [False] * CFBGlobalSettings.NumOfRegWeeks.value
        )

        while len(is_conf_week_pool) < CFBGlobalSettings.NumOfRegWeeks.value:
            is_conf_week_pool.append(False)

        if len(is_conf_week_pool) > CFBGlobalSettings.NumOfRegWeeks.value:
            is_conf_week_pool = is_conf_week_pool[:CFBGlobalSettings.NumOfRegWeeks.value]

        while True:
            all_teams = self.cfb.get_all_teams()

            if len(all_teams[0].opponents) == CFBGlobalSettings.NumOfRegWeeks.value: # V8 Week Amount
                break

            is_conf_week = is_conf_week_pool.pop(0)

            if is_conf_week:
                counter = 7 - is_conf_week_pool.count(True)
                self._get_conf_week_matchups(self.CONFERENCE_CYCLE[counter-1][1], self.CONFERENCE_CYCLE[counter-1][0])
            elif CFBGlobalSettings.NumOfConferences.value == 6 and CFBGlobalSettings.isConferenceOppOn.value and CFBGlobalSettings.NonConfWeeksHaveUniqueConf.value:
                counter = 5 - is_conf_week_pool.count(False)
                self._get_unique_conf_matchup(self.OPP_CONF_CYCLE[counter-1])
            else:
                result = self._get_reg_week_matchup(all_teams)
                if result == -1:
                    is_conf_week_pool.insert(0, False)


    def _get_unique_conf_matchup(self, conf_order):
        for conf_pair in conf_order:
            con_1 = self.cfb.conferences[conf_pair[0]-1]
            con_1_teams = self.cfb.get_all_teams(True, con_1.name)
            con_2 = self.cfb.conferences[conf_pair[1]-1]
            con_2_teams = self.cfb.get_all_teams(True, con_2.name)
            
            for index in range(len(con_1_teams)):
                self._setup_matchup(con_1_teams[index], con_2_teams[index])


    def _get_conf_week_matchups(self, conf_order, counter):
        # conf_order example: ((1,2), (3,4), (5,6)),
        if counter != 8:
            for con in self.cfb.conferences:
                # Do the three reg SHUFFLE HOME/AWAY future

                for i in range(3):
                    self._setup_matchup(con.div1[conf_order[i][0]-1], con.div1[conf_order[i][1]-1])
                    self._setup_matchup(con.div2[conf_order[i][0]-1], con.div2[conf_order[i][1]-1])

                self._setup_matchup(con.div1[counter-1], con.div2[counter-1])


    def _get_reg_week_matchup(self, all_teams):
        Locked = False
        potential_pairings = []
        for _ in range(len(all_teams)//2):
            home: Team = choice(all_teams)
            all_teams.remove(home)

            possible_away_options = [x for x in all_teams if x.conference != home.conference]

            if len(possible_away_options) == 0:
                return -1

            away = choice(possible_away_options)

            ac = 0
            while away.name in home.get_all_cur_reg_season_opp():
                away = choice(all_teams)
                ac += 1
                if ac > 10:
                    #print(f"Dup found: {home.name} vs {away.name}! Locking and Retrying")
                    Locked = True
                    return -1
            all_teams.remove(away)

            potential_pairings.append((home, away))
        
        if not Locked:
            for pairing in potential_pairings:
                self._setup_matchup(pairing[0], pairing[1])


    def _setup_matchup(self, home: Team, away: Team):
            """ Takes 2 teams and adds them to OpponentMatch """
            home.opponents.append(OpponentMatch(away))
            away.opponents.append(OpponentMatch(home))
