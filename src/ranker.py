from __future__ import annotations
from abc import ABC, abstractmethod
from random import randint, shuffle
from typing import TYPE_CHECKING

from src.settings import CFBGlobalSettings

if TYPE_CHECKING:
    from src.cfb import CFB
    from src.opponent_match import OpponentMatch
    from src.team import Team


class Ranker(ABC):
    def __init__(self, cfb: CFB, rank_sig: str):
        self.cfb: CFB = cfb
        self.rank_sig = rank_sig

    @abstractmethod
    def determine_winner(self, home: Team, away: Team):
        pass

    @abstractmethod
    def rank_teams(self):
        pass

    def label_top_teams(self, update_prev_rank: bool = True):
        for t in range(len(self.cfb.team_ranks)):
            if update_prev_rank:
                self.cfb.team_ranks[t].prev_rank = self.cfb.team_ranks[t].rank
            self.cfb.team_ranks[t].full_rank = str(t+1)
            self.cfb.team_ranks[t].rank = str(t+1) if t < CFBGlobalSettings.NumOfTeamsRanked.value else "UR"


class APRanker(Ranker):
    def __init__(self, cfb: CFB):
        super().__init__(cfb, "AP")
        self.weights = {
            1:  randint(8,12),
            2:  randint(18,22),
            3:  randint(30,34),
            4:  randint(38,42),
            5:  randint(45,49),
            6:  randint(51,55),
            7:  randint(58,62),
            8:  randint(67,71),
            9:  randint(74,78),
            10: randint(81,85),
            11: randint(88,92),
            12: randint(98,102),
            13: randint(103,107),
            20: randint(108,112),
        }

    def determine_winner(self, home: Team, away: Team):
        box = home.reg_wins - away.reg_wins
        if box < 0:
            temp: Team = home
            home = away
            away = temp
            box = abs(box)

        win_home = randint(0, 1+box)
        if win_home:
            return (home, away)
        return (away, home)

    def rank_teams(self):
        self.cfb.team_ranks = self.cfb.get_all_teams(shuffled=True)
        self.cfb.team_ranks.sort(key = lambda x: (x.reg_wins + (x.point_diff/(self.weights[self.cfb.week]))), reverse=True)

        self.label_top_teams()

        self.cfb.rank_sig = self.rank_sig


class CFBRanker(Ranker):
    def __init__(self, cfb: CFB):
        super().__init__(cfb, "CFB")

    def determine_winner(self, home: Team, away: Team):
        pd = int(home.full_rank) - int(away.full_rank)
        odds = randint(1,100)
        line = 50 - pd 

        if line < 5:  line = 5
        if line > 95: line = 95

        while odds == line:
            odds = randint(1,100)
        
        if odds < line:
            return (home, away)
        return (away, home)


    def rank_teams(self):
        self.cfb.team_ranks = self.cfb.get_all_teams(shuffled=True)
        self.cfb.team_ranks.sort(key = lambda x: x.calc_cfb_points(), reverse=True)

        self.label_top_teams()

        self.cfb.team_ranks.sort(key = lambda x: (x.calc_cfb_points(), x.total_wins, x.point_diff, x.prev_rank), reverse=True)

        for repeat_checks in range(25):
            not_moved: bool = True
            for i in range(len(self.cfb.team_ranks)-1):
                for op_match in self.cfb.team_ranks[i].opponents[::-1]:
                    if op_match.has_game_happened and not op_match.win and self.cfb.team_ranks[i+1] == op_match.opponent:
                        # print(f"SWITCH: {self.team_ranks[i].name}")
                        temp: OpponentMatch = self.cfb.team_ranks[i+1]
                        self.cfb.team_ranks[i+1] = self.cfb.team_ranks[i]
                        self.cfb.team_ranks[i] = temp
                        not_moved = False
                        break
            if not_moved:
                break

        self.label_top_teams(update_prev_rank=False)
        
        self.cfb.rank_sig = self.rank_sig


class RandomRanker(Ranker):
    def __init__(self, cfb):
        super().__init__(cfb, "RNG")

    def determine_winner(self, home: Team, away: Team):
        tmp = [home, away]
        shuffle(tmp)
        return tuple(tmp)

    def rank_teams(self):
        shuffle(self.cfb.team_ranks)
        self.label_top_teams()
        self.cfb.rank_sig = self.rank_sig
