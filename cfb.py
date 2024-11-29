from random import choice, randint, shuffle

class Team:
    name: str
    reg_wins: int = 0
    reg_losses: int = 0
    total_wins: int = 0
    total_losses: int = 0
    rank: str = "UR"
    prev_rank: str = "UR"
    point_diff = 0

    def __init__(self, n) -> None:
        self.name = n

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
    conferences: list[Conference]
    team_ranks: list[Team] = []

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
        self.conferences = self.set_up_season()
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

    def play_week(self, print_stuff=True):
        teams = []
        for con in self.conferences:
            for team in con.div1:
                teams.append(team)
            for team in con.div2:
                teams.append(team)

        matches: list[list[Team]] = []
        
        #teams = self.team_ranks[:]

        for _ in range(35):

            home = choice(teams)
            #home = teams[0]
            teams.remove(home)
            away = choice(teams)
            #away = teams[-1]
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

            box = home.reg_wins - away.reg_wins
            if box < 0:
                temp: Team = home
                home = away
                away = temp
                box = abs(box)

            win_home = randint(0, 1+box)
            # print(f"0-{1+box} | {win_home}")
            scores = self.get_scores()
            if win_home > 0:
                self.handle_regular_game(home, away, scores, print_stuff)
            else:
                self.handle_regular_game(away, home, scores, print_stuff)

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
                print(f"{(con.div1[tea].rank):>2} ({(con.div1[tea].prev_rank):>2}) {(con.div1[tea].name):<20} ({(con.div1[tea].total_wins):<2} - {(con.div1[tea].total_losses):>2}) ({(con.div1[tea].point_diff):>4}) | {(con.div2[tea].rank):>2} ({(con.div2[tea].prev_rank):>2}) {(con.div2[tea].name):<20} ({(con.div2[tea].reg_wins):<2} - {(con.div2[tea].reg_losses):>2}) ({(con.div2[tea].point_diff):>4})")

            input("")

    def make_top25(self, week: int):
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
            if t < 25:
                self.team_ranks[t].rank = str(t+1)
            else:
                self.team_ranks[t].rank = "UR"

        print("{0:^54}".format("Top 25"))
        print("-----------------------------------------------------")
        print("Rk (+/-) |         Name         | Record | Point_Diff")
        print("-----------------------------------------------------")
        for i in range(25):
            print(f"{(1+i):>2} ({(self.team_ranks[i].get_rank_difference()):>3}) | {(self.team_ranks[i].name):<20} | {(self.team_ranks[i].reg_wins):>2} -{(self.team_ranks[i].reg_losses):>2} | {(self.team_ranks[i].point_diff):>6}")
        print("")

    def print_top25(self):
        #Assumes ranks have already been given
        teams = []
        for con in self.conferences:
            for team in con.div1:
                teams.append(team)
            for team in con.div2:
                teams.append(team)
        teams.sort(key= self.ranking)
        teams = teams[:25]
        print("\nTop 25")
        for tea in teams:
            print(f"{tea.rank}) {tea.name}: {tea.total_wins}-{tea.total_losses}")

    def conference_championships(self):
        for con in self.conferences:
            con.div1.sort(key= lambda x: x.reg_wins, reverse=True)
            con.div2.sort(key= lambda x: x.reg_wins, reverse=True)

            team1 = con.div1[0]
            team2 = con.div2[0]

            print(f"{con.name} Championship!!!")
            input(f"{team1.rank} {team1.name} ({team1.total_wins}-{team1.total_losses}) vs {team2.rank} {team2.name} ({team2.total_wins}-{team2.total_losses})")

            box = team1.reg_wins - team2.reg_wins
            if box <= 0:
                temp: Team = team2
                team2 = team1
                team1 = temp
                box = abs(box)

            team1_wins = randint(0,1+box)
            #print(f"0-{1+box} | {team1_wins}")
            scores = self.get_scores()
            if team1_wins > 0:
                print(f"{team1.name} {scores[0]} - {scores[1]} {team2.name} | {team1.name} wins!!!")
                team2.reg_losses += 1
                team2.total_losses += 1
                team1.reg_wins += 1
                team1.total_wins += 1
            else: 
                print(f"{team2.name} {scores[0]} - {scores[1]} {team1.name} | {team2.name} wins!!!")
                team1.reg_losses += 1
                team1.total_losses += 1
                team2.reg_wins += 1
                team2.total_wins += 1

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

        box = team1.reg_wins - team2.reg_wins
        if box < 0:
            temp: Team = team2
            team2 = team1
            team1 = temp
            box = abs(box)

        team1_wins = randint(0,1+box)
        #print(f"0-{1+box} | {team1_wins}")
        scores = self.get_scores()
        if team1_wins > 0:
            team1.total_wins += 1
            team2.total_losses += 1
            print(f"{team1.name} wins!!! ({scores[0]}-{scores[1]})")
            teams.remove(team2)
        else:
            team2.total_wins += 1
            team1.total_losses += 1
            print(f"{team2.name} wins!!! ({scores[0]}-{scores[1]})")
            teams.remove(team1)
        input("")

        # Semi Final 2 (2 v 3)
        input(f"CFB Playoffs Semi Final 2: {team3.rank} {team3.name} ({team3.total_wins}-{team3.total_losses}) vs {team4.rank} {team4.name} ({team4.total_wins}-{team4.total_losses})")

        box = team3.reg_wins - team4.reg_wins
        if box < 0:
            temp: Team = team4
            team4 = team3
            team3 = temp
            box = abs(box)

        team1_wins = randint(0,1+box)
        #print(f"0-{1+box} | {team1_wins}")
        scores = self.get_scores()
        if team1_wins > 0:
            team3.total_wins += 1
            team4.total_losses += 1
            print(f"{team3.name} wins!!! ({scores[0]}-{scores[1]})")
            teams.remove(team4)
        else:
            team4.total_wins += 1
            team3.total_losses += 1
            print(f"{team4.name} wins!!! ({scores[0]}-{scores[1]})")
            teams.remove(team3)
        input("")

        # Final
        team1 = teams[0]
        team2 = teams[1]

        input(f"CFB Championship: {team1.rank} {team1.name} ({team1.total_wins}-{team1.total_losses}) vs {team2.rank} {team2.name} ({team2.total_wins}-{team2.total_losses})")

        box = team1.reg_wins - team2.reg_wins
        if box < 0:
            temp: Team = team2
            team2 = team1
            team1 = temp
            box = abs(box)

        team1_wins = randint(0,1+box)
        #print(f"0-{1+box} | {team1_wins}")
        scores = self.get_scores()
        if team1_wins > 0:
            print(f"{team1.name} wins!!! ({scores[0]}-{scores[1]})")
            team1.total_wins += 1
            team2.total_losses += 1
            teams.remove(team2)
        else:
            print(f"{team2.name} wins!!! ({scores[0]}-{scores[1]})")
            team2.total_wins += 1
            team1.total_losses += 1
            teams.remove(team1)
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

            box = teams[octo[i][1]].reg_wins - teams[octo[i][0]].reg_wins
            if box < 0:
                temp: Team = teams[octo[i][0]]
                teams[octo[i][0]] = teams[octo[i][1]]
                teams[octo[i][1]] = temp
                box = abs(box)

            winner = int(bool(randint(0,1+box)))
            loser = int(not bool(winner))
            #print(f"0-{1+box} | {winner}")
            scores = self.get_scores()
            quarter[i].append(octo[i][winner])
            teams[octo[i][winner]].total_wins += 1
            teams[octo[i][int(not winner)]].total_losses += 1
            print(f"{teams[octo[i][winner]].name} {scores[0]} - {scores[1]} {teams[octo[i][loser]].name} | {teams[octo[i][winner]].name} wins!!!\n")

        # Quarter Matches
        for i in range(4):
            input(f"CFB Championship Quarter Round {i+1}: {teams[quarter[i][0]].rank} {teams[quarter[i][0]].name} ({teams[quarter[i][0]].total_wins}-{teams[quarter[i][0]].total_losses}) vs {teams[quarter[i][1]].rank} {teams[quarter[i][1]].name} ({teams[quarter[i][1]].total_wins}-{teams[quarter[i][1]].total_losses})")

            box = teams[quarter[i][1]].reg_wins - teams[quarter[i][0]].reg_wins
            if box < 0:
                temp: Team = teams[quarter[i][0]]
                teams[quarter[i][0]] = teams[quarter[i][1]]
                teams[quarter[i][1]] = temp
                box = abs(box)

            winner = int(bool(randint(0,1+box)))
            loser = int(not bool(winner))
            #print(f"0-{1+box} | {winner}")
            scores = self.get_scores()
            semi[i%2].append(quarter[i][winner])
            teams[quarter[i][winner]].total_wins += 1
            teams[quarter[i][int(not winner)]].total_losses += 1
            print(f"{teams[quarter[i][winner]].name} {scores[0]} - {scores[1]} {teams[quarter[i][loser]].name} | {teams[quarter[i][winner]].name} wins!!!\n")

        # Semi Matches
        for i in range(2):
            input(f"CFB Championship Semi Round {i+1}: {teams[semi[i][0]].rank} {teams[semi[i][0]].name} ({teams[semi[i][0]].total_wins}-{teams[semi[i][0]].total_losses}) vs {teams[semi[i][1]].rank} {teams[semi[i][1]].name} ({teams[semi[i][1]].total_wins}-{teams[semi[i][1]].total_losses})")

            box = teams[semi[i][1]].reg_wins - teams[semi[i][0]].reg_wins
            if box < 0:
                temp: Team = teams[semi[i][0]]
                teams[semi[i][0]] = teams[semi[i][1]]
                teams[semi[i][1]] = temp
                box = abs(box)

            winner = int(bool(randint(0,1+box)))
            loser = int(not bool(winner))
            #print(f"0-{1+box} | {winner}")
            scores = self.get_scores()
            final.append(semi[i][winner])
            teams[semi[i][winner]].total_wins += 1
            teams[semi[i][int(not winner)]].total_losses += 1
            print(f"{teams[semi[i][winner]].name} {scores[0]} - {scores[1]} {teams[semi[i][loser]].name} | {teams[semi[i][winner]].name} wins!!!\n")

        # The Championship
        input(f"CFB Championship!!! {teams[final[0]].rank} {teams[final[0]].name} ({teams[final[0]].total_wins}-{teams[final[0]].total_losses}) vs {teams[final[1]].rank} {teams[final[1]].name} ({teams[final[1]].total_wins}-{teams[final[1]].total_losses})")

        box = teams[final[1]].reg_wins - teams[final[0]].reg_wins
        if box < 0:
            temp: Team = teams[final[0]]
            teams[final[0]] = teams[final[1]]
            teams[final[1]] = temp
            box = abs(box)

        winner = int(bool(randint(0,1+box)))
        loser = int(not bool(winner))
        #print(f"0-{1+box} | {winner}")
        scores = self.get_scores()
        teams[final[winner]].total_wins += 1
        teams[final[int(not winner)]].total_losses += 1
        print(f"{teams[final[winner]].name} {scores[0]} - {scores[1]} {teams[final[loser]].name} | {teams[final[winner]].name} wins!!!\n")

        print(f"{teams[final[winner]].name} are your CFB CHAMPIONS!!!!")
        print(f"Ranked: {teams[final[winner]].rank} | ({teams[final[winner]].total_wins}-{teams[final[winner]].total_losses})")

    def print_full_rankings(self):
        for t in range(len(self.team_ranks)):
            print(f"{(t+1):>2}) {(self.team_ranks[t].name):<20} ({self.team_ranks[t].total_wins}-{self.team_ranks[t].total_losses}) {self.team_ranks[t].point_diff}")

    def handle_regular_game(self, winner: Team, loser: Team, scores, print_stuff):
        points_diff = scores[0] - scores[1]
        winner.handle_win(points_diff)
        loser.handle_loss(points_diff)

        if print_stuff:
            print(f"{winner.name} {scores[0]} - {scores[1]} {loser.name}  | {winner.name} wins!\n")
        #return winner, loser

