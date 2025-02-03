from random import choice, randint, shuffle
from typing import Union
from copy import deepcopy

class Team:

    def __init__(self, n) -> None:
        self.name = n
        self.reg_wins: int = 0
        self.reg_losses: int = 0
        self.total_wins: int = 0
        self.total_losses: int = 0
        self.rank: str = "UR"
        self.prev_rank: str = "UR"
        self.full_rank: str = 0
        self.cfp_seed: str = "OUT" # Add Load/Save
        self.point_diff = 0
        self.cfb_points = 0
        self.is_con_champion: bool = False # Add Load/Save
        self.opponents: list[OpponentMatch] = []

    def handle_win(self, points) -> None:
        self.reg_wins += 1
        self.total_wins += 1
        self.point_diff += points

    def handle_loss(self, points) -> None:
        self.reg_losses += 1
        self.total_losses += 1
        self.point_diff -= points
    
    def get_rank_difference(self) -> str:
        if self.rank == "UR":
            return "THIS SHOULD NOT HAPPEN"

        if self.rank == self.prev_rank:
            return "~ "
        
        if self.prev_rank == "UR":
            return "UR"

        r = int(self.rank)
        pr = int(self.prev_rank)
        if r > pr:
            return str(f"-{r-pr}")
        return str(f"+{pr-r}")
    
    def get_ranked_and_unranked_records(self):
        rw = 0
        rl = 0
        urw = 0
        url = 0
        for op in self.opponents:
            op: OpponentMatch
            if op.opponent.rank.isdigit():
                if op.win:
                    rw += 1
                else:
                    rl += 1
            elif op.win:
                urw += 1
            else:
                url += 1
    
        return rw, rl, urw, url

    def print_team_details(self, show_cfp_points: bool = True):
        rw, rl, urw, url = self.get_ranked_and_unranked_records()
        print(f"{self.name} ({self.total_wins}-{self.total_losses}) CFP: {self.cfb_points if show_cfp_points else '???'} PD: {self.point_diff} RR: ({rw}-{rl}) URR: ({urw}-{url})")

        if self.opponents == []:
            return

        print("Faced: ")
        name_length = max([len(x.opponent.name) for x in self.opponents]) + 1
        for op_match in self.opponents:
            op = op_match.opponent

            if op_match.is_conference_title:
                print("\n---------------- Conference Championship -----------------------")
            if op_match.is_playoff_octo:
                print("\n------------------ Playoff Octo Round --------------------------")
            if op_match.is_playoff_quarter:
                print("\n---------------- Playoff Quarter Round -------------------------")
            if op_match.is_playoff_semi:
                print("\n----------------- Playoff Semi Round ---------------------------")
            if op_match.is_playoff_final:
                print("\n---------------- Playoff Championship --------------------------")

            print(f"  - {'W' if op_match.win else 'L'} ({op.rank:>2}) {op.name:<{name_length}} ({op.total_wins}-{op.total_losses}) PD: {op_match.point_diff:<4} CFB_P: {(op_match.cfb_points if show_cfp_points else '???'):>3}")
    
    def calc_cfb_points(self):
        points = 0

        for op_match in self.opponents:
            win = op_match.win
            pd = op_match.point_diff
            op = op_match.opponent

            this_point = 0
            if win:
                if op.rank.isdigit():
                    this_point += 50 - int(op.rank) + (2 * op.reg_wins) + (pd  // 7) #  pd 3
                else:
                    this_point += 12 + (2 * op.reg_wins) + (pd // 14) #  pd 7
            else:
                if op.rank.isdigit():
                    this_point -= (int(op.rank) + 15 - (pd // 9)) #  pd 7
                else:
                    this_point -= ((int(op.full_rank) // 2) + 25 + op.reg_losses - (pd // 5))
            
            op_match.cfb_points = this_point

            points += this_point

        self.cfb_points = points
        return points


class OpponentMatch:
    def __init__(self, op, win, pd, cfb_p="AP", conference_champ_game=False, po_octo=False, po_quarter=False, po_semi=False, po_final=False):
        self.opponent: Team = op
        self.win: bool = win
        self.point_diff: int = pd
        self.cfb_points: Union[int, str] = cfb_p
        self.is_conference_title: bool = conference_champ_game
        self.is_playoff_octo: bool = po_octo
        self.is_playoff_quarter: bool = po_quarter
        self.is_playoff_semi: bool = po_semi
        self.is_playoff_final: bool = po_final


class Conference:
    name: str
    div1: list[Team]
    div2: list[Team]
    div1_name: str
    div2_name: str

    def __init__(self, n, t1, t2, dn1, dn2) -> None:
        self.name = n
        self.div1 = t1
        self.div2 = t2
        self.div1_name = dn1
        self.div2_name = dn2


class CFB:

    def set_up_season(self):
        cons = []

        sec_east: list[Team] = []
        sec_east.append(Team("Tennessee"))
        sec_east.append(Team("Georgia"))
        sec_east.append(Team("Florida"))
        sec_east.append(Team("Kentucky"))
        sec_east.append(Team("South Carolina"))
        sec_east.append(Team("Missouri"))
        sec_east.append(Team("Vanderbilt"))

        sec_west: list[Team] = []
        sec_west.append(Team("Alabama"))
        sec_west.append(Team("Ole Miss"))
        sec_west.append(Team("LSU"))
        sec_west.append(Team("Mississippi State"))
        sec_west.append(Team("Texas A&M"))
        sec_west.append(Team("Auburn"))
        sec_west.append(Team("Arkansas"))

        cons.append(Conference("SEC", sec_east, sec_west, "East", "West"))

        acc_at = []
        acc_at.append(Team("Clemson"))
        acc_at.append(Team("Florida State"))
        acc_at.append(Team("NC State"))
        acc_at.append(Team("Syracuse"))
        acc_at.append(Team("Louisville"))
        acc_at.append(Team("Wake Forest"))
        acc_at.append(Team("Boston College"))

        acc_co = []
        acc_co.append(Team("North Carolina"))
        acc_co.append(Team("Duke"))
        acc_co.append(Team("Pitt"))
        acc_co.append(Team("Miami"))
        acc_co.append(Team("Georgia Tech"))
        acc_co.append(Team("Virginia"))
        acc_co.append(Team("Virginia Tech"))

        cons.append(Conference("ACC", acc_at, acc_co, "Atlantic", "Costal"))

        big10_east = []
        big10_east.append(Team("Michigan"))
        big10_east.append(Team("Ohio State"))
        big10_east.append(Team("Penn State"))
        big10_east.append(Team("Maryland"))
        big10_east.append(Team("Michigan State"))
        big10_east.append(Team("Rutgers"))
        big10_east.append(Team("Indiana"))

        big10_west = []
        big10_west.append(Team("Illinois"))
        big10_west.append(Team("Iowa"))
        big10_west.append(Team("Purdue"))
        big10_west.append(Team("Minnesota"))
        big10_west.append(Team("Wisconsin"))
        big10_west.append(Team("Nebraska"))
        big10_west.append(Team("Northwestern"))

        cons.append(Conference("Big 10", big10_east, big10_west, "East", "West"))

        tot_east = []
        tot_east.append(Team("TCU"))
        tot_east.append(Team("Kansas"))
        tot_east.append(Team("Kansas State"))
        tot_east.append(Team("Notre Dame"))
        tot_east.append(Team("Frenso State"))
        tot_east.append(Team("UCLA"))
        tot_east.append(Team("Oregon"))

        tot_west = []
        tot_west.append(Team("Texas"))
        tot_west.append(Team("Oklahoma"))
        tot_west.append(Team("Baylor"))
        tot_west.append(Team("Liberty"))
        tot_west.append(Team("Boise State"))
        tot_west.append(Team("Arizona"))
        tot_west.append(Team("App State"))

        cons.append(Conference("OCT", tot_east, tot_west, "East", "West"))

        fbs_east = []
        fbs_east.append(Team("Gardner Webb"))
        fbs_east.append(Team("Marshall"))
        fbs_east.append(Team("Wofford"))
        fbs_east.append(Team("UT Martin"))
        fbs_east.append(Team("East Carolina"))
        fbs_east.append(Team("Tulsa"))
        fbs_east.append(Team("BYU"))

        fbs_west = []
        fbs_west.append(Team("Army"))
        fbs_west.append(Team("Air Force"))
        fbs_west.append(Team("Tulane"))
        fbs_west.append(Team("Navy"))
        fbs_west.append(Team("James Madison"))
        fbs_west.append(Team("Troy"))
        fbs_west.append(Team("Uconn"))

        cons.append(Conference("FBS", fbs_east, fbs_west, "East", "West"))

        return cons

    def __init__(self) -> None:
        self.conferences: list[Conference] = self.set_up_season()
        self.team_ranks: list[Team] = []
        self.rank_sig: str = "NA"
        self.week: int = 1
        self.is_after_conference_championship: bool = False
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
        self.octo = [
            (7,8),
            (4,11),
            (6,9),
            (5,10),
        ]
        self.quarter = [
            [0,],
            [3,],
            [1,],
            [2,],
        ]
        self.semi = [
            [],
            [],
        ]
        self.final = []
        self.winner: Team = None
        self.SEASON_FOLDER = "saved_seasons"

    def get_scores(self):
        loser = randint(0,52)
        if loser == 1:
            loser = 7
        winner = randint(loser+1, 80+randint(0,9))
        return (winner, loser)

    def play_week(self, print_stuff=True):
        teams = []
        for con in self.conferences:
            for team in con.div1:
                teams.append(team)
            for team in con.div2:
                teams.append(team)

        matches: list[list[Team]] = []

        for _ in range(len(teams) // 2):

            home: Team = choice(teams)
            teams.remove(home)

            away: Team = choice(teams)
            teams.remove(away)

            matches.append([home, away])

        matches.sort(key=self.sort_prime_time, reverse=True)

        for i in range(len(matches)):
            home = matches[i][0]
            away = matches[i][1]
            if print_stuff:
                if i == (len(matches)-1):
                    print("NCAA GAME OF THE WEEK!!!")
                input(f"Match-up: {away.rank} {away.name} ({away.reg_wins}-{away.reg_losses}) @ {home.rank} {home.name} ({home.reg_wins}-{home.reg_losses})")

            winner, loser = self.determine_winner_ap(home, away) if self.week < 7 else self.determine_winner_cfb(home, away)
            scores = self.get_scores()
            self.handle_regular_game(winner, loser, scores, print_stuff)
            winner.opponents.append(OpponentMatch(loser, True, scores[0]-scores[1]))
            loser.opponents.append(OpponentMatch(winner, False, scores[1]-scores[0]))

    def sort_prime_time(self, game):
        #print(type(game), len(game), game)
        viewers: int = 0
        if game[0].rank == "UR":
            viewers += (26+game[0].total_losses)
        else:
            viewers += int(game[0].rank)

        if game[1].rank == "UR":
            viewers += (26+game[1].total_losses)
        else:
            viewers += int(game[1].rank)
        return viewers

    def ranking(self, tea):
        if tea.rank == "UR":
            return 26 + tea.total_losses
        else:
            return int(tea.rank)

    def print_standings(self):
        for con in self.conferences:
            con.div1.sort(key= lambda x: self.team_ranks.index(x))
            con.div2.sort(key= lambda x: self.team_ranks.index(x))

            print(f"{(con.name):^93}")
            print(f"{(con.div1_name):^46}{(con.div2_name):^46}")
            print("---------------------------------------------------------------------------------------------")
            for tea in range(7):
                print(f"{(con.div1[tea].rank):>2} ({(con.div1[tea].prev_rank):>2}) {(con.div1[tea].name):<20} ({(con.div1[tea].total_wins):<2} - {(con.div1[tea].total_losses):>2}) ({(con.div1[tea].point_diff if self.rank_sig=='AP' else con.div1[tea].cfb_points):>4}) | {(con.div2[tea].rank):>2} ({(con.div2[tea].prev_rank):>2}) {(con.div2[tea].name):<20} ({(con.div2[tea].reg_wins):<2} - {(con.div2[tea].reg_losses):>2}) ({(con.div2[tea].point_diff if self.rank_sig=='AP' else con.div2[tea].cfb_points):>4})")

            input("")

    def print_top25(self):
        self.team_ranks.sort(key=lambda x: int(x.full_rank))
        print("-----------------------------------------------------")
        print("{0:^54}".format(f"{self.rank_sig} Top 25"))
        print("-----------------------------------------------------")
        print(f"Rk (+/-) |         Name         | Record | {'Point_Diff' if self.rank_sig=='AP' else 'CFB Points'}")
        print("-----------------------------------------------------")
        for i in range(25):
            print(f"{(1+i):>2} ({(self.team_ranks[i].get_rank_difference()):>3}) | {(self.team_ranks[i].name):<20} | {(self.team_ranks[i].total_wins):>2} -{(self.team_ranks[i].total_losses):>2} | {(self.team_ranks[i].point_diff if self.rank_sig == 'AP' else self.team_ranks[i].cfb_points):>6}")
        print("")

    def make_ap_top25(self):
        self.team_ranks = []
        for con in self.conferences:
            for t in con.div1:
                self.team_ranks.append(t)
            for t in con.div2:
                self.team_ranks.append(t)
        shuffle(self.team_ranks)
        self.team_ranks.sort(key = lambda x: (x.reg_wins + (x.point_diff/(self.weights[self.week]))), reverse=True)

        for t in range(len(self.team_ranks)):
            self.team_ranks[t].prev_rank = self.team_ranks[t].rank
            self.team_ranks[t].full_rank = str(t+1)
            self.team_ranks[t].rank = str(t+1) if t < 25 else "UR"


        self.rank_sig = "AP"
    
    def make_cfb_top_25(self):
        self.team_ranks = []
        for con in self.conferences:
            for t in con.div1:
                self.team_ranks.append(t)
            for t in con.div2:
                self.team_ranks.append(t)
        shuffle(self.team_ranks)

        self.team_ranks.sort(key = lambda x: x.calc_cfb_points(), reverse=True)
        for t in range(len(self.team_ranks)):
            self.team_ranks[t].prev_rank = self.team_ranks[t].rank
            self.team_ranks[t].full_rank = str(t+1)
            self.team_ranks[t].rank = str(t+1) if t < 25 else "UR"

        self.team_ranks.sort(key = lambda x: (x.calc_cfb_points(), x.total_wins, x.point_diff, x.prev_rank), reverse=True)

        for repeat_checks in range(25):
            not_moved: bool = True
            for i in range(len(self.team_ranks)-1):
                for op_match in self.team_ranks[i].opponents[::-1]:
                    if not op_match.win and self.team_ranks[i+1] == op_match.opponent:
                        # print(f"SWITCH: {self.team_ranks[i].name}")
                        temp: OpponentMatch = self.team_ranks[i+1]
                        self.team_ranks[i+1] = self.team_ranks[i]
                        self.team_ranks[i] = temp
                        not_moved = False
                        break
            if not_moved:
                break

        for t in range(len(self.team_ranks)):
            self.team_ranks[t].full_rank = str(t+1)
            self.team_ranks[t].rank = str(t+1) if t < 25 else "UR"

        self.rank_sig = "CFB"

    def conference_championships(self):
        for con in self.conferences:
            con.div1.sort(key= lambda x: int(x.full_rank))
            con.div2.sort(key= lambda x: int(x.full_rank))

            team1 = con.div1[0]
            team2 = con.div2[0]

            print(f"{con.name} Championship!!!")
            input(f"{team1.rank} {team1.name} ({team1.total_wins}-{team1.total_losses}) vs {team2.rank} {team2.name} ({team2.total_wins}-{team2.total_losses})")

            winner, loser = self.determine_winner_cfb(team1, team2)
            
            #print(f"0-{1+box} | {team1_wins}")
            scores = self.get_scores()
            print(f"{winner.name} {scores[0]} - {scores[1]} {loser.name} | {winner.name} wins!!!")
            
            winner.total_wins += 1 
            winner.reg_wins += 1

            winner.is_con_champion = True
            winner.opponents.append(OpponentMatch(loser, True, scores[0]-scores[1], conference_champ_game=True))

            loser.total_losses += 1
            loser.reg_losses += 1
            loser.opponents.append(OpponentMatch(winner, False, scores[1]-scores[0], conference_champ_game=True))


            input("\n")
        self.is_after_conference_championship = True
    
    def playoffs_four(self):
        teams = []
        for con in self.conferences:
            for team in con.div1:
                teams.append(team)
            for team in con.div2:
                teams.append(team)
        teams.sort(key= self.ranking)

        # Semi Final 1 (1 v 4)
        team1 = teams[0]
        team2 = teams[3]
        team3 = teams[1]
        team4 = teams[2]

        input(f"CFB Playoffs Semi Final 1: {team1.rank} {team1.name} ({team1.total_wins}-{team1.total_losses}) vs {team2.rank} {team2.name} ({team2.total_wins}-{team2.total_losses})")

        winner, loser = self.determine_winner_cfb(team1, team2)
        scores = self.get_scores()
        winner.total_wins += 1
        loser.total_losses += 1
        teams.remove(loser)

        print(f"{winner.name} wins!!! ({scores[0]}-{scores[1]})")

        input("")

        # Semi Final 2 (2 v 3)
        input(f"CFB Playoffs Semi Final 2: {team3.rank} {team3.name} ({team3.total_wins}-{team3.total_losses}) vs {team4.rank} {team4.name} ({team4.total_wins}-{team4.total_losses})")

        winner, loser = self.determine_winner_cfb(team3, team4)
        scores = self.get_scores()

        winner.total_wins += 1
        print(f"{winner.name} wins!!! ({scores[0]}-{scores[1]})")

        loser.total_losses += 1
        teams.remove(loser)

        input("")

        # Final
        team1 = teams[0]
        team2 = teams[1]

        input(f"CFB Championship: {team1.rank} {team1.name} ({team1.total_wins}-{team1.total_losses}) vs {team2.rank} {team2.name} ({team2.total_wins}-{team2.total_losses})")

        winner, loser = self.determine_winner_cfb(team1, team2)
        scores = self.get_scores()

        winner.total_wins += 1
        print(f"{winner.name} wins!!! ({scores[0]}-{scores[1]})")

        loser.total_losses += 1
        teams.remove(loser)

        input("")
        
        print(f"{teams[0].name} are your CFB CHAMPIONS!!!")
        print(f"Ranked: {teams[0].rank} ({teams[0].total_wins}-{teams[0].total_losses})")
            
    def playoffs_twelve(self):
        teams = self.get_cfp_12_teams()

        # Octo Matches
        for i in range(4):
            input(f"CFB Championship Octo Round {i+1}: {teams[self.octo[i][0]].rank} {teams[self.octo[i][0]].name} ({teams[self.octo[i][0]].total_wins}-{teams[self.octo[i][0]].total_losses}) vs {teams[self.octo[i][1]].rank} {teams[self.octo[i][1]].name} ({teams[self.octo[i][1]].total_wins}-{teams[self.octo[i][1]].total_losses})")

            winner, loser = self.determine_winner_cfb(teams[self.octo[i][1]], teams[self.octo[i][0]])

            winner = int(winner == teams[self.octo[i][1]])
            loser = int(not bool(winner))

            #print(f"0-{1+box} | {winner}")
            scores = self.get_scores()
            self.quarter[i].append(self.octo[i][winner])
            teams[self.octo[i][winner]].total_wins += 1
            teams[self.octo[i][winner]].opponents.append(OpponentMatch(teams[self.octo[i][loser]], True, scores[0]-scores[1], po_octo=True))
            teams[self.octo[i][loser]].total_losses += 1
            teams[self.octo[i][loser]].opponents.append(OpponentMatch(teams[self.octo[i][winner]], False, scores[1]-scores[0], po_octo=True))
            print(f"{teams[self.octo[i][winner]].name} {scores[0]} - {scores[1]} {teams[self.octo[i][loser]].name} | {teams[self.octo[i][winner]].name} wins!!!\n")

            self.menu_processor(allow_save_load=False)

        # Quarter Matches
        for i in range(4):
            input(f"CFB Championship Quarter Round {i+1}: {teams[self.quarter[i][0]].rank} {teams[self.quarter[i][0]].name} ({teams[self.quarter[i][0]].total_wins}-{teams[self.quarter[i][0]].total_losses}) vs {teams[self.quarter[i][1]].rank} {teams[self.quarter[i][1]].name} ({teams[self.quarter[i][1]].total_wins}-{teams[self.quarter[i][1]].total_losses})")

            winner, loser = self.determine_winner_cfb(teams[self.quarter[i][0]], teams[self.quarter[i][1]])
            
            winner = int(winner == teams[self.quarter[i][1]])
            loser = int(not bool(winner))

            #print(f"0-{1+box} | {winner}")
            scores = self.get_scores()
            self.semi[i//2].append(self.quarter[i][winner])
            teams[self.quarter[i][winner]].total_wins += 1
            teams[self.quarter[i][winner]].opponents.append(OpponentMatch(teams[self.quarter[i][loser]], True, scores[0]-scores[1], po_quarter=True))
            teams[self.quarter[i][loser]].total_losses += 1
            teams[self.quarter[i][loser]].opponents.append(OpponentMatch(teams[self.quarter[i][winner]], False, scores[1]-scores[0], po_quarter=True))

            print(f"{teams[self.quarter[i][winner]].name} {scores[0]} - {scores[1]} {teams[self.quarter[i][loser]].name} | {teams[self.quarter[i][winner]].name} wins!!!\n")

            self.menu_processor(allow_save_load=False)

        # Semi Matches
        for i in range(2):
            input(f"CFB Championship Semi Round {i+1}: {teams[self.semi[i][0]].rank} {teams[self.semi[i][0]].name} ({teams[self.semi[i][0]].total_wins}-{teams[self.semi[i][0]].total_losses}) vs {teams[self.semi[i][1]].rank} {teams[self.semi[i][1]].name} ({teams[self.semi[i][1]].total_wins}-{teams[self.semi[i][1]].total_losses})")

            winner, loser = self.determine_winner_cfb(teams[self.semi[i][1]], teams[self.semi[i][0]])

            winner = int(winner == teams[self.semi[i][1]])
            loser = int(not bool(winner))

            #print(f"0-{1+box} | {winner}")
            scores = self.get_scores()
            self.final.append(self.semi[i][winner])

            teams[self.semi[i][winner]].total_wins += 1
            teams[self.semi[i][winner]].opponents.append(OpponentMatch(teams[self.semi[i][loser]], True, scores[0]-scores[1], po_semi=True))
            teams[self.semi[i][loser]].total_losses += 1
            teams[self.semi[i][loser]].opponents.append(OpponentMatch(teams[self.semi[i][winner]], False, scores[1]-scores[0], po_semi=True))

            print(f"{teams[self.semi[i][winner]].name} {scores[0]} - {scores[1]} {teams[self.semi[i][loser]].name} | {teams[self.semi[i][winner]].name} wins!!!\n")

            self.menu_processor(allow_save_load=False)

        # The Championship
        input(f"CFB Championship!!! {teams[self.final[0]].rank} {teams[self.final[0]].name} ({teams[self.final[0]].total_wins}-{teams[self.final[0]].total_losses}) vs {teams[self.final[1]].rank} {teams[self.final[1]].name} ({teams[self.final[1]].total_wins}-{teams[self.final[1]].total_losses})")

        winner, loser = self.determine_winner_cfb(teams[self.final[1]], teams[self.final[0]])
        self.winner = winner

        winner = int(winner == teams[self.final[1]])
        loser = int(not bool(winner))

        scores = self.get_scores()
        teams[self.final[winner]].total_wins += 1
        teams[self.final[winner]].opponents.append(OpponentMatch(teams[self.final[loser]], True, scores[0]-scores[1], po_final=True))
        teams[self.final[int(not winner)]].total_losses += 1
        teams[self.final[loser]].opponents.append(OpponentMatch(teams[self.final[winner]], False, scores[1]-scores[0], po_final=True))

        print(f"{teams[self.final[winner]].name} {scores[0]} - {scores[1]} {teams[self.final[loser]].name} | {teams[self.final[winner]].name} wins!!!\n")
        print(f"{teams[self.final[winner]].name} are your CFB CHAMPIONS!!!!")
        print(f"Ranked: {teams[self.final[winner]].rank} | ({teams[self.final[winner]].total_wins}-{teams[self.final[winner]].total_losses})")

    def print_full_rankings(self):
        for t in range(len(self.team_ranks)):
            print(f"{(t+1):>2}) {(self.team_ranks[t].name):<20} ({self.team_ranks[t].total_wins}-{self.team_ranks[t].total_losses}) {self.team_ranks[t].point_diff if self.rank_sig == 'AP' else self.team_ranks[t].cfb_points}")

    def handle_regular_game(self, winner: Team, loser: Team, scores, print_stuff):
        points_diff = scores[0] - scores[1]
        winner.handle_win(points_diff)
        loser.handle_loss(points_diff)

        if print_stuff:
            print(f"{winner.name} {scores[0]} - {scores[1]} {loser.name}  | {winner.name} wins!\n")
        #return winner, loser

    def menu_processor(self, allow_save_load: bool = True):
        enter_counter = 0
        while True:
            selection_string = (
                " (FR): See Full Rankings | (A): Advance Week | (B): Show Bracket\n"
                " (TD): Team Details | (ST): Show Top 25 | (SC): Show Confrences\n"
            )
            if allow_save_load:
                selection_string += (
                    " (S): Save Season | (L): Load Season \n"
                )
            selection = input(
                selection_string +
                " Selection: "
            )

            print("\n")
            if selection.lower() == "s" and allow_save_load:
                self.save_season()
                print("\n")
            if selection.lower() == "l" and allow_save_load:
                self.load_season()
                print("\n")
            if selection.lower() == "b":
                cfp = self.get_cfp_12_teams(get_first_two_out=True)
                self.view_bracket(cfp)
                print("\n")
            if selection.lower() == "st":
                self.print_top25()
                print("\n")
            if selection.lower() == "sc":
                self.print_standings()
                print("\n")
            if selection.lower() == "fr":
                self.print_full_rankings()
                print("\n")
            if selection.lower() == "rr":
                self.make_cfb_top_25()
                self.print_top25()
                print("\n")
            if selection.lower() == "td":
                tr = input("Enter the team's rank you want to see: ")
                if tr.isdigit():
                    viewing = deepcopy(self.team_ranks)
                    viewing.sort(key=lambda x: int(x.full_rank))
                    viewing[int(tr)-1].print_team_details()
                    print("\n")
                else:
                    print("next time enter a digit\n")

            if selection == "":
                enter_counter += 1
            else:
                enter_counter = 0
                
            if selection.lower() == "a" or enter_counter >= 3:
                print("\n")
                return
            
    def determine_winner_ap(self, home: Team, away: Team):
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

    def determine_winner_cfb(self, home: Team, away: Team):
        pd = int(home.full_rank) - int(away.full_rank)
        odds = randint(1,100)
        line = 50 - pd 

        if line < 5:  line = 5
        if line > 95: line = 95

        while odds == line:
            odds = randint(1,100)

        # print("DW_CFB: ", home.name, away.name, " ODDS: ", odds, " LINES: ", line)
        
        if odds < line:
            return (home, away)
        return (away, home)

    def save_season(self):
        file_name = input("Enter name of save file: ")
        filepath = f"{self.SEASON_FOLDER}/{file_name}.cfb"

        file = open(file=filepath, mode='w')
        
        file.write(f"{self.week},{self.rank_sig},\n")

        for conf in self.conferences:
            conf: Conference
            file.write(f"{conf.name}\n{conf.div1_name}\n")
            for team in conf.div1:
                team: Team
                file.write(f"{team.name},{team.reg_wins},{team.reg_losses},{team.total_wins},{team.total_losses},{team.rank},{team.prev_rank},{team.full_rank},{team.point_diff},{team.cfb_points},\n")
                for op in team.opponents:
                    op: OpponentMatch
                    file.write(f"{op.opponent.name},{op.win},{op.point_diff},{op.cfb_points},{op.is_conference_title},{op.is_playoff_octo},{op.is_playoff_quarter},{op.is_playoff_semi},{op.is_playoff_final},\n")
            file.write(f"{conf.div2_name}\n")
            for team in conf.div2:
                team: Team
                file.write(f"{team.name},{team.reg_wins},{team.reg_losses},{team.total_wins},{team.total_losses},{team.rank},{team.prev_rank},{team.full_rank},{team.point_diff},{team.cfb_points},\n")
                for op in team.opponents:
                    op: OpponentMatch
                    file.write(f"{op.opponent.name},{op.win},{op.point_diff},{op.cfb_points},{op.is_conference_title},{op.is_playoff_octo},{op.is_playoff_quarter},{op.is_playoff_semi},{op.is_playoff_final},\n")

        file.close()

    def load_season(self):
        file_name = input("Enter name of load file: ")
        filepath = f"{self.SEASON_FOLDER}/{file_name}.cfb"

        file = open(file=filepath, mode='r')
        
        conf_data = file.readline().split(',')[:-1]
        self.week = int(conf_data[0])
        self.rank_sig = conf_data[1]

        for con in range(5):
            self.conferences[con].name = file.readline()[:-1]
            self.conferences[con].div1_name = file.readline()[:-1]
            for div_team in range(7):
                team_data = file.readline().split(',')[:-1]
                self.conferences[con].div1[div_team].name = team_data[0]
                self.conferences[con].div1[div_team].reg_wins = int(team_data[1])
                self.conferences[con].div1[div_team].reg_losses = int(team_data[2])
                self.conferences[con].div1[div_team].total_wins = int(team_data[3])
                self.conferences[con].div1[div_team].total_losses = int(team_data[4])
                self.conferences[con].div1[div_team].rank = team_data[5]
                self.conferences[con].div1[div_team].prev_rank = team_data[6]
                self.conferences[con].div1[div_team].full_rank = team_data[7]
                self.conferences[con].div1[div_team].point_diff = int(team_data[8])
                self.conferences[con].div1[div_team].cfb_points = int(team_data[9])

                opponents = []
                for _ in range(self.week - 1):
                    op_data = file.readline().split(',')[:-1]
                    opponents.append(
                        OpponentMatch(
                            op=op_data[0],
                            win=op_data[1] == "True",
                            pd=int(op_data[2]),
                            cfb_p=(
                                int(op_data[3])
                                if op_data[3].isdigit() or op_data[3].lstrip('-').isdigit()
                                else "AP"
                            ),
                            conference_champ_game=op_data[4] == "True",
                            po_octo=op_data[5] == "True",
                            po_quarter=op_data[6] == "True",
                            po_semi=op_data[7] == "True",
                            po_final=op_data[8] == "True",
                        )
                    )
                self.conferences[con].div1[div_team].opponents = opponents

            self.conferences[con].div2_name = file.readline()[:-1]
            for div_team in range(7):
                team_data = file.readline().split(',')[:-1]
                self.conferences[con].div2[div_team].name = team_data[0]
                self.conferences[con].div2[div_team].reg_wins = int(team_data[1])
                self.conferences[con].div2[div_team].reg_losses = int(team_data[2])
                self.conferences[con].div2[div_team].total_wins = int(team_data[3])
                self.conferences[con].div2[div_team].total_losses = int(team_data[4])
                self.conferences[con].div2[div_team].rank = team_data[5]
                self.conferences[con].div2[div_team].prev_rank = team_data[6]
                self.conferences[con].div2[div_team].full_rank = team_data[7]
                self.conferences[con].div2[div_team].point_diff = int(team_data[8])
                self.conferences[con].div2[div_team].cfb_points = int(team_data[9])

                opponents = []
                for _ in range(self.week - 1):
                    op_data = file.readline().split(',')[:-1]
                    opponents.append(
                        OpponentMatch(
                            op=op_data[0],
                            win=op_data[1] == "True",
                            pd=int(op_data[2]),
                            cfb_p=(
                                int(op_data[3])
                                if op_data[3].isdigit() or op_data[3].lstrip('-').isdigit()
                                else "AP"
                            ),
                            conference_champ_game=op_data[4] == "True",
                            po_octo=op_data[5] == "True",
                            po_quarter=op_data[6] == "True",
                            po_semi=op_data[7] == "True",
                            po_final=op_data[8] == "True",
                        )
                    )
                self.conferences[con].div2[div_team].opponents = opponents


        file.close()

        # Look up teams names from loading process
        for conf in self.conferences:
            for d1 in conf.div1:
                for to in d1.opponents:
                    to.opponent = self.return_team_by_name(to.opponent)
            for d2 in conf.div2:
                for to in d2.opponents:
                    to.opponent = self.return_team_by_name(to.opponent)
        

        # re rank to match saved status
        self.team_ranks.sort(key=lambda x: int(x.full_rank))

        print("Loading Successful!\n")

    def return_team_by_name(self, name: str) -> Team:
        teams = [x for x in self.team_ranks if x.name == name]
        if teams == []:
            print("ERROR NO TEAM FOUND: ", name)
        else:
            return teams[0]

    def get_cfp_12_teams(self, get_first_two_out:bool = False) -> list[Team]:
        cfp_teams = []
        limit = 14 if get_first_two_out else 12

        if self.is_after_conference_championship: 
            self.team_ranks.sort(key=lambda x: (not x.is_con_champion, int(x.full_rank)))
            cfp_teams = self.team_ranks[:limit]
        else:
            for con in self.conferences:
                teams = []
                for d1 in con.div1:
                    teams.append(d1)
                for d2 in con.div2:
                    teams.append(d2)

                teams.sort(key=lambda x: int(x.full_rank))
                cfp_teams.append(teams[0])
            index = 0
            while len(cfp_teams) < limit:
                if self.team_ranks[index] not in cfp_teams:
                    cfp_teams.append(self.team_ranks[index])

                index += 1
        if get_first_two_out:
            f2o = cfp_teams[-2:]
            cfp_teams = cfp_teams[:-2]
        cfp_teams.sort(key=lambda x: int(x.full_rank))
        
        if get_first_two_out:
            cfp_teams += f2o 

        for team_seed in range(1, limit+1):
            cfp_teams[team_seed-1].cfp_seed = team_seed

        return cfp_teams
    
    def cfp_teams_reveal(self):

        def print_reveal(teams: list[Team], other_made_it, outs):
            print("--------------------------------------------")
            print("| Sd  | Rk  |       Name        |  Record  |")
            print("--------------------------------------------")
            for i in range(1, 13):
                team = next((x for x in teams if x.cfp_seed == i), None)
                print(f"| {i:>2}) | {(team.full_rank if team else ' '):>2}) | {(team.name if team else ' '):^17} | {(f'({team.total_wins:>2} - {team.total_losses:>2})' if team else ' '):<8}")
            
            print("\n\n-----------------")
            print(f"First Out: {outs[0].name if len(teams)==12 else ' '}")
            print(f"Second Out: {outs[1].name if len(teams)==12 else ' '}")
            
            if len(teams) != 12:
                print("\n\nUnplaced Teams")
                unrevealed = other_made_it+outs 
                unrevealed.sort(key=lambda x: x.name)
                for up_teams in unrevealed:
                    up_teams: Team
                    print(f"{up_teams.name:<17}: ({up_teams.prev_rank:>2}) ({up_teams.total_wins:>2} - {up_teams.total_losses:>2})")

        cfp_teams = self.get_cfp_12_teams(get_first_two_out=True)
        made_it = cfp_teams[:12]
        made_it.sort(key=lambda x: (not x.is_con_champion, int(x.full_rank)))
        out = cfp_teams[-2:]

        revealed_teams = []
        print_reveal(revealed_teams, made_it, out)
        input("\n")
        for i in range(12):
            revealed_teams.append(made_it.pop(0))
            print_reveal(revealed_teams, made_it, out)

            if i == 10:
                input("")
                comb = made_it + out 
                comb.sort(key = lambda x: x.name)
                for team in comb:
                    print("\n")
                    team.print_team_details(show_cfp_points=False)
                    print("\n")

            input("")
            
    
    def view_bracket(self, cfp_teams: list[Team]):
        NAME_WIDTH = 17
        counter = 1
        for cfp_team in cfp_teams:
            if counter == 13:
                print("\n-------------FIRST-TWO-OUT--------------\n")
            print(f"Seed {cfp_team.cfp_seed}: {cfp_team.name} ({cfp_team.full_rank})")
            counter += 1

        QUARTER_1 = cfp_teams[self.quarter[0][1]] if len(self.quarter[0]) > 1 else None
        QUARTER_2 = cfp_teams[self.quarter[1][1]] if len(self.quarter[1]) > 1 else None
        QUARTER_3 = cfp_teams[self.quarter[2][1]] if len(self.quarter[2]) > 1 else None
        QUARTER_4 = cfp_teams[self.quarter[3][1]] if len(self.quarter[3]) > 1 else None

        SEMI_1 = cfp_teams[self.semi[0][0]] if len(self.semi[0]) > 0 else None
        SEMI_2 = cfp_teams[self.semi[0][1]] if len(self.semi[0]) > 1 else None
        SEMI_3 = cfp_teams[self.semi[1][0]] if len(self.semi[1]) > 0 else None
        SEMI_4 = cfp_teams[self.semi[1][1]] if len(self.semi[1]) > 1 else None

        FINAL_1 = cfp_teams[self.final[0]] if len(self.final) > 0 else None
        FINAL_2 = cfp_teams[self.final[1]] if len(self.final) > 1 else None

        WINNER = self.winner
        

        print(
            f"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
            f"~                                                                                                                      \n"
            f"~   {cfp_teams[8].cfp_seed:>2}) {cfp_teams[8].name:<{NAME_WIDTH}}                                                      \n"
            f"~   ______________________                                                                                             \n"
            f"~                         |                                                                                            \n"
            f"~                         |{(QUARTER_1.cfp_seed if QUARTER_1 else ' '):>2}) {(QUARTER_1.name if QUARTER_1 else ' '):<{NAME_WIDTH}}                                                           \n"
            f"~   {cfp_teams[7].cfp_seed:>2}) {cfp_teams[7].name:<{NAME_WIDTH}} |_____________________                               \n"
            f"~   ______________________|                     |                                                                      \n"
            f"~                                               |{(SEMI_1.cfp_seed if SEMI_1 else ' '):>2}) {(SEMI_1.name if SEMI_1 else ' '):<{NAME_WIDTH}}          \n"
            f"~                          {cfp_teams[0].cfp_seed:>2}) {cfp_teams[0].name:<{NAME_WIDTH}}|_____________________           \n"
            f"~                         ______________________|                     |                                                  \n"
            f"~                                                                     |                                                  \n"
            f"~                                                                     |                                                  \n"
            f"~   {cfp_teams[11].cfp_seed:>2}) {cfp_teams[11].name:<{NAME_WIDTH}}                                             |        \n"
            f"~   ______________________                                            |{(FINAL_1.cfp_seed if FINAL_1 else ' '):>2}) {(FINAL_1.name if FINAL_1 else ' '):<{NAME_WIDTH}}       \n"
            f"~                         |                                           |______________________                            \n"
            f"~                         |{(QUARTER_2.cfp_seed if QUARTER_2 else ' '):>2}) {(QUARTER_2.name if QUARTER_2 else ' '):<{NAME_WIDTH}}                      |                      |                           \n"
            f"~   {cfp_teams[4].cfp_seed:>2}) {cfp_teams[4].name:<{NAME_WIDTH}} |_____________________                      |                      |     \n"
            f"~   ______________________|                     |                     |                      |                           \n"
            f"~                                               |{(SEMI_2.cfp_seed if SEMI_2 else ' '):>2}) {(SEMI_2.name if SEMI_2 else ' '):<{NAME_WIDTH}}|                      |                           \n"
            f"~                          {cfp_teams[3].cfp_seed:>2}) {cfp_teams[3].name:<{NAME_WIDTH}}|_____________________|                      |     \n"
            f"~                         ______________________|                                            |                           \n"
            f"~                                                                                            |                           \n"
            f"~                                                                                            |                           \n"
            f"~   {cfp_teams[9].cfp_seed:>2}) {cfp_teams[9].name:<{NAME_WIDTH}}                                                                    |     \n"
            f"~   ______________________                                                                   |                           \n"
            f"~                         |                                                                  |{(WINNER.cfp_seed if WINNER else ' '):>2}) {(WINNER.name if WINNER else ' '):<{NAME_WIDTH}}  \n"
            f"~                         |{(QUARTER_3.cfp_seed if QUARTER_3 else ' '):>2}) {(QUARTER_3.name if QUARTER_3 else ' '):<{NAME_WIDTH}}                                             |________________________   \n"
            f"~   {cfp_teams[6].cfp_seed:>2}) {cfp_teams[6].name:<{NAME_WIDTH}} |_____________________                                             |     \n"
            f"~   ______________________|                     |                                            |      \n"
            f"~                                               |{(SEMI_3.cfp_seed if SEMI_3 else ' '):>2}) {(SEMI_3.name if SEMI_3 else ' '):<{NAME_WIDTH}}                       |      \n"
            f"~                          {cfp_teams[1].cfp_seed:>2}) {cfp_teams[1].name:<{NAME_WIDTH}}|_____________________                       |     \n"
            f"~                         ______________________|                     |                      |      \n"
            f"~                                                                     |                      |      \n"
            f"~                                                                     |                      |      \n" 
            f"~   {cfp_teams[10].cfp_seed:>2}) {cfp_teams[10].name:<{NAME_WIDTH}}                                             |                      |   \n"
            f"~   ______________________                                            |{(FINAL_2.cfp_seed if FINAL_2 else ' '):>2}) {(FINAL_2.name if FINAL_2 else ' '):<{NAME_WIDTH}} |      \n"
            f"~                         |                                           |______________________|               \n"
            f"~                         |{(QUARTER_4.cfp_seed if QUARTER_4 else ' '):>2}) {(QUARTER_4.name if QUARTER_4 else ' '):<{NAME_WIDTH}}                      |                 \n"
            f"~   {cfp_teams[5].cfp_seed:>2}) {cfp_teams[5].name:<{NAME_WIDTH}} |_____________________                      |                            \n"
            f"~   ______________________|                     |                     |               \n"
            f"~                                               |{(SEMI_4.cfp_seed if SEMI_4 else ' '):>2}) {(SEMI_4.name if SEMI_4 else ' '):<{NAME_WIDTH}}|               \n"
            f"~                          {cfp_teams[2].cfp_seed:>2}) {cfp_teams[2].name:<{NAME_WIDTH}}|_____________________|                            \n"
            f"~                         ______________________|                                            \n"
            f"~                                                                                       \n"
            f"~                                                                                       \n"
            f"~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~\n"
        )
        
