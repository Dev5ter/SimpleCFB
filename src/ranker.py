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
    def calc_teams_score(self, team: Team) -> int:
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
            0:  randint(1,2),
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

    def calc_teams_score(self, team):
        return team.reg_wins + (team.point_diff/(self.weights[self.cfb.week-1]))

    def rank_teams(self):
        self.cfb.team_ranks = self.cfb.get_all_teams(shuffled=True)
        self.cfb.team_ranks.sort(key = lambda x: self.calc_teams_score(x), reverse=True)

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


    def calc_teams_score(self, team: Team):
        points = 0

        for op_match in team.opponents:
            if op_match.has_game_happened is False:
                continue

            win = op_match.win
            pd = op_match.point_diff
            op = op_match.opponent

            this_point = 0
            if win:
                if op.rank.isdigit():
                    this_point += ((50 - int(op.rank)) + (2 * op.reg_wins) + (pd  // 7)) #  pd 3
                    if int(op.rank) <= 15:
                        this_point += 5
                else:
                    this_point += 14 + (2 * op.reg_wins) + (pd // 10) #  pd 7
            else:
                # pd for loss is negative
                if op.rank.isdigit():
                    this_point -= (int(op.rank) + 20 + (-pd // 10)) #  pd 7 
                else:
                    this_point -= ((int(op.full_rank) // 2) + 25 + (op.reg_losses*2) + (-pd // 7))
            
            op_match.cfb_points = this_point

            points += this_point

        team.cfb_points = points + 100
        return points


    def rank_teams(self):
        self.cfb.team_ranks = self.cfb.get_all_teams(shuffled=True)
        self.cfb.team_ranks.sort(key = lambda x: self.calc_teams_score(x), reverse=True)

        self.label_top_teams()

        self.cfb.team_ranks.sort(key = lambda x: (self.calc_teams_score(x), x.total_wins, x.point_diff, x.prev_rank), reverse=True)

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
        super().__init__(cfb, "RTS")

    def determine_winner(self, home: Team, away: Team):
        tmp = [home, away]
        shuffle(tmp)
        return tuple(tmp)

    def calc_teams_score(self, team):
        pass

    def rank_teams(self):
        self.cfb.team_ranks = self.cfb.get_all_teams(shuffled=True)
        self.label_top_teams()
        self.cfb.rank_sig = self.rank_sig
