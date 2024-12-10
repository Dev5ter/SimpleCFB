from random import choice, randint, shuffle
from typing import Union

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
        self.point_diff = 0
        self.opponents: list[OpponentMatch] = []
        self.cfb_points = 0

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
    
    def print_team_details(self):
        print(f"{self.name} ({self.total_wins}-{self.total_losses}) PD: {self.point_diff}")
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

            print(f"  - {'W' if op_match.win else 'L'} ({op.rank:>2}) {op.name:<{name_length}} ({op.total_wins}-{op.total_losses}) PD: {op_match.point_diff:<4} CFB_P: {op_match.cfb_points:>3}")
    
    def calc_cfb_points(self):
        points = 0

        for op_match in self.opponents:
            win = op_match.win
            pd = op_match.point_diff
            op = op_match.opponent

            this_point = 0
            if win:
                if op.rank.isdigit():
                    this_point += 53 - int(op.rank) + op.reg_wins + (pd  // 10)
                else:
                    this_point += 10 + (2 * op.reg_wins) + (pd // 15)
            else:
                if op.rank.isdigit():
                    this_point -= (int(op.rank) + 15 - (pd // 5))
                else:
                    this_point -= ((int(op.full_rank) // 2) + 25 + op.reg_losses - (pd // 3))
            
            op_match.cfb_points = this_point

            points += this_point

        self.cfb_points = points
        return points


class OpponentMatch:
    def __init__(self, op, win, pd, conference_champ_game=False, po_octo=False, po_quarter=False, po_semi=False, po_final=False):
        self.opponent: Team = op
        self.win: bool = win
        self.point_diff: int = pd
        self.cfb_points: Union[int, str] = "AP"
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

    def get_scores(self):
        loser = randint(0,52)
        if loser == 1:
            loser = 7
        winner = randint(loser+1, 80+randint(0,9))
        return (winner, loser)

    def play_week(self, week, print_stuff=True):
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

            winner, loser = self.determine_winner_ap(home, away) if week < 7 else self.determine_winner_cfb(home, away)
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
        print("-----------------------------------------------------")
        print("{0:^54}".format(f"{self.rank_sig} Top 25"))
        print("-----------------------------------------------------")
        print(f"Rk (+/-) |         Name         | Record | {'Point_Diff' if self.rank_sig=='AP' else 'CFB Points'}")
        print("-----------------------------------------------------")
        for i in range(25):
            print(f"{(1+i):>2} ({(self.team_ranks[i].get_rank_difference()):>3}) | {(self.team_ranks[i].name):<20} | {(self.team_ranks[i].reg_wins):>2} -{(self.team_ranks[i].reg_losses):>2} | {(self.team_ranks[i].point_diff if self.rank_sig == 'AP' else self.team_ranks[i].cfb_points):>6}")
        print("")

    def make_ap_top25(self, week: int):
        self.team_ranks = []
        for con in self.conferences:
            for t in con.div1:
                self.team_ranks.append(t)
            for t in con.div2:
                self.team_ranks.append(t)
        shuffle(self.team_ranks)
        self.team_ranks.sort(key = lambda x: (x.reg_wins + (x.point_diff/(self.weights[week+1]))), reverse=True)

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

        self.team_ranks.sort(key = lambda x: x.calc_cfb_points(), reverse=True)

        for i in range(len(self.team_ranks)-1):
            for op_match in self.team_ranks[i].opponents[::-1]:
                if not op_match.win and self.team_ranks[i+1] == op_match.opponent:
                    # print(f"SWITCH: {self.team_ranks[i].name}")
                    temp: OpponentMatch = self.team_ranks[i+1]
                    self.team_ranks[i+1] = self.team_ranks[i]
                    self.team_ranks[i] = temp
                    break

        for t in range(len(self.team_ranks)):
            self.team_ranks[t].full_rank = str(t+1)
            self.team_ranks[t].rank = str(t+1) if t < 25 else "UR"

        self.rank_sig = "CFB"

    def conference_championships(self):
        for con in self.conferences:
            con.div1.sort(key= lambda x: x.reg_wins, reverse=True)
            con.div2.sort(key= lambda x: x.reg_wins, reverse=True)

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
            winner.opponents.append(OpponentMatch(loser, True, scores[0]-scores[1], True))

            loser.total_losses += 1
            loser.reg_losses += 1
            loser.opponents.append(OpponentMatch(winner, False, scores[1]-scores[0], True))


            input("\n")
    
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
        teams = []
        for con in self.conferences:
            for team in con.div1:
                teams.append(team)
            for team in con.div2:
                teams.append(team)
        teams.sort(key= self.ranking)

        teams = teams[:12]

        octo = [
            (7,8),
            (5,10),
            (4,11),
            (6,9),
        ]
        quarter = [
            [0,],
            [2,],
            [3,],
            [1,],
        ]
        semi = [
            [],
            [],
        ]
        final = []

        # Octo Matches
        for i in range(4):
            input(f"CFB Championship Octo Round {i+1}: {teams[octo[i][0]].rank} {teams[octo[i][0]].name} ({teams[octo[i][0]].total_wins}-{teams[octo[i][0]].total_losses}) vs {teams[octo[i][1]].rank} {teams[octo[i][1]].name} ({teams[octo[i][1]].total_wins}-{teams[octo[i][1]].total_losses})")

            winner, loser = self.determine_winner_cfb(teams[octo[i][1]], teams[octo[i][0]])

            winner = int(winner == teams[octo[i][1]])
            loser = int(not bool(winner))

            #print(f"0-{1+box} | {winner}")
            scores = self.get_scores()
            quarter[i].append(octo[i][winner])
            teams[octo[i][winner]].total_wins += 1
            teams[octo[i][winner]].opponents.append(OpponentMatch(teams[octo[i][loser]], True, scores[0]-scores[1], po_octo=True))
            teams[octo[i][loser]].total_losses += 1
            teams[octo[i][loser]].opponents.append(OpponentMatch(teams[octo[i][winner]], False, scores[1]-scores[0], po_octo=True))
            print(f"{teams[octo[i][winner]].name} {scores[0]} - {scores[1]} {teams[octo[i][loser]].name} | {teams[octo[i][winner]].name} wins!!!\n")

        # Quarter Matches
        for i in range(4):
            input(f"CFB Championship Quarter Round {i+1}: {teams[quarter[i][0]].rank} {teams[quarter[i][0]].name} ({teams[quarter[i][0]].total_wins}-{teams[quarter[i][0]].total_losses}) vs {teams[quarter[i][1]].rank} {teams[quarter[i][1]].name} ({teams[quarter[i][1]].total_wins}-{teams[quarter[i][1]].total_losses})")

            winner, loser = self.determine_winner_cfb(teams[quarter[i][0]], teams[quarter[i][1]])
            
            winner = int(winner == teams[quarter[i][1]])
            loser = int(not bool(winner))

            #print(f"0-{1+box} | {winner}")
            scores = self.get_scores()
            semi[i%2].append(quarter[i][winner])
            teams[quarter[i][winner]].total_wins += 1
            teams[quarter[i][winner]].opponents.append(OpponentMatch(teams[quarter[i][loser]], True, scores[0]-scores[1], po_quarter=True))
            teams[quarter[i][loser]].total_losses += 1
            teams[quarter[i][loser]].opponents.append(OpponentMatch(teams[quarter[i][winner]], False, scores[1]-scores[0], po_quarter=True))

            print(f"{teams[quarter[i][winner]].name} {scores[0]} - {scores[1]} {teams[quarter[i][loser]].name} | {teams[quarter[i][winner]].name} wins!!!\n")

        # Semi Matches
        for i in range(2):
            input(f"CFB Championship Semi Round {i+1}: {teams[semi[i][0]].rank} {teams[semi[i][0]].name} ({teams[semi[i][0]].total_wins}-{teams[semi[i][0]].total_losses}) vs {teams[semi[i][1]].rank} {teams[semi[i][1]].name} ({teams[semi[i][1]].total_wins}-{teams[semi[i][1]].total_losses})")

            winner, loser = self.determine_winner_cfb(teams[semi[i][1]], teams[semi[i][0]])

            winner = int(winner == teams[semi[i][1]])
            loser = int(not bool(winner))

            #print(f"0-{1+box} | {winner}")
            scores = self.get_scores()
            final.append(semi[i][winner])

            teams[semi[i][winner]].total_wins += 1
            teams[semi[i][winner]].opponents.append(OpponentMatch(teams[semi[i][loser]], True, scores[0]-scores[1], po_semi=True))
            teams[semi[i][loser]].total_losses += 1
            teams[semi[i][loser]].opponents.append(OpponentMatch(teams[semi[i][winner]], False, scores[1]-scores[0], po_semi=True))

            print(f"{teams[semi[i][winner]].name} {scores[0]} - {scores[1]} {teams[semi[i][loser]].name} | {teams[semi[i][winner]].name} wins!!!\n")

        # The Championship
        input(f"CFB Championship!!! {teams[final[0]].rank} {teams[final[0]].name} ({teams[final[0]].total_wins}-{teams[final[0]].total_losses}) vs {teams[final[1]].rank} {teams[final[1]].name} ({teams[final[1]].total_wins}-{teams[final[1]].total_losses})")

        winner, loser = self.determine_winner_cfb(teams[final[1]], teams[final[0]])

        winner = int(winner == teams[final[1]])
        loser = int(not bool(winner))

        scores = self.get_scores()
        teams[final[winner]].total_wins += 1
        teams[final[winner]].opponents.append(OpponentMatch(teams[final[loser]], True, scores[0]-scores[1], po_final=True))
        teams[final[int(not winner)]].total_losses += 1
        teams[final[loser]].opponents.append(OpponentMatch(teams[final[winner]], False, scores[1]-scores[0], po_final=True))

        print(f"{teams[final[winner]].name} {scores[0]} - {scores[1]} {teams[final[loser]].name} | {teams[final[winner]].name} wins!!!\n")
        print(f"{teams[final[winner]].name} are your CFB CHAMPIONS!!!!")
        print(f"Ranked: {teams[final[winner]].rank} | ({teams[final[winner]].total_wins}-{teams[final[winner]].total_losses})")

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

    def menu_processor(self):
        enter_counter = 0
        while True:
            selection = input(
                " (FR): See Full Rankings | (A): Advance Week \n"
                " (TD): Team Details | (S): Save Season | (L): Load Season \n"
                " Selection: "
            )
            print("\n")
            if selection.lower() == "fr":
                self.print_full_rankings()
                print("\n")
            if selection.lower() == "td":
                tr = input("Enter the team's rank you want to see: ")
                if tr.isdigit():
                    self.team_ranks[int(tr)-1].print_team_details()
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




