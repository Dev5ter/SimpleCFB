from random import randint, shuffle
from src.conference import Conference
from src.opponent_match import OpponentMatch
from src.ranker import APRanker, CFBRanker, RandomRanker
from src.settings import CFBGlobalSettings
from src.team import Team
from src.team_scheduler import TeamScheduler
from copy import deepcopy


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

        cons.append(Conference("ACC", acc_at, acc_co, "Atlantic", "Coastal"))

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

        cons.append(Conference("B10", big10_east, big10_west, "East", "West"))

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

        pac_east = []
        pac_east.append(Team("Kent State"))
        pac_east.append(Team("Washington"))
        pac_east.append(Team("Toledo"))
        pac_east.append(Team("Memphis"))
        pac_east.append(Team("Cincinnati"))
        pac_east.append(Team("Utah"))
        pac_east.append(Team("Stanford"))

        pac_west = []
        pac_west.append(Team("Sam Houston"))
        pac_west.append(Team("Texas Tech"))
        pac_west.append(Team("Southern Cali"))
        pac_west.append(Team("Temple"))
        pac_west.append(Team("Akron"))
        pac_west.append(Team("BYU"))
        pac_west.append(Team("Tulane"))

        cons.append(Conference("PAC", pac_east, pac_west, "East", "West"))

        fbs_east = []
        fbs_east.append(Team("Gardner Webb"))
        fbs_east.append(Team("Marshall"))
        fbs_east.append(Team("Wofford"))
        fbs_east.append(Team("UT Martin"))
        fbs_east.append(Team("East Carolina"))
        fbs_east.append(Team("Tulsa"))
        fbs_east.append(Team("Campbell"))

        fbs_west = []
        fbs_west.append(Team("Army"))
        fbs_west.append(Team("Air Force"))
        fbs_west.append(Team("Georgetown"))
        fbs_west.append(Team("Navy"))
        fbs_west.append(Team("James Madison"))
        fbs_west.append(Team("Troy"))
        fbs_west.append(Team("Uconn"))

        cons.append(Conference("FCS", fbs_east, fbs_west, "East", "West"))

        return cons


    def __init__(self):
        self.conferences: list[Conference] = self.set_up_season()
        self.team_ranks: list[Team] = []
        self.rank_sig: str = "NA"
        self.week: int = 1
        self.is_after_conference_championship: bool = False
        
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

        # Helper Classes
        self.team_scheduler = TeamScheduler(self)

        self.ap_ranker = APRanker(self)
        self.cfb_ranker = CFBRanker(self)
        self.random_ranker = RandomRanker(self)


    def get_scores(self):
        loser = randint(0,52)
        if loser == 1:
            loser = 7
        winner = randint(loser+1, 70+randint(1,10))
        return (winner, loser)


    def get_all_teams(self, shuffled: bool = False, must_be_conf: str = None) -> list[Team]:
        teams = []
        for con in self.conferences:
            if must_be_conf is not None and con.name != must_be_conf:
                continue

            for team in con.div1:
                teams.append(team)
            for team in con.div2:
                teams.append(team)
        if shuffled:
            shuffle(teams)
        return teams


    def get_this_week_matchups_sorted(self):
        teams = self.get_all_teams(shuffled=True)
        
        matches: list[list[Team]] = []

        for _ in range(len(teams) // 2):

            home: Team = teams[0]
            teams.remove(home)

            away: Team = home.opponents[self.week-1].opponent
            teams.remove(away)

            matches.append([home, away])

        matches.sort(key=self.sort_prime_time, reverse=True)
        return matches


    def play_week(self, print_stuff=True):
        matches = self.get_this_week_matchups_sorted()

        for i in range(len(matches)):
            home = matches[i][0]
            away = matches[i][1]
            
            if print_stuff:
                game_of_week: bool = i == (len(matches)-1)
                self._print_matchup(matches[i], game_of_week)

            if not CFBGlobalSettings.UseRandomRanker.value:
                winner, loser = (
                    self.ap_ranker.determine_winner(home, away)
                    if self.week < CFBGlobalSettings.WeekCFBStartsRanking.value 
                    else self.cfb_ranker.determine_winner(home, away)
                )
            else:
                winner, loser = self.random_ranker.determine_winner(home, away)

            scores = self.get_scores()
            self.handle_regular_game(winner, loser, scores, print_stuff)


    def _print_matchup(self, match, game_of_week=False, print_stuff=True):
            home = match[0]
            away = match[1]
            if print_stuff:
                if game_of_week:
                    print("NCAA GAME OF THE WEEK!!!")
                input(f"Match-up: {away.rank} {away.name} ({away.reg_wins}-{away.reg_losses}) @ {home.rank} {home.name} ({home.reg_wins}-{home.reg_losses})")


    def sort_prime_time(self, game):
        #print(type(game), len(game), game)
        viewers: int = 0
        if game[0].rank == "UR":
            viewers += (CFBGlobalSettings.NumOfTeamsRanked.value+1+game[0].total_losses)
        else:
            viewers += int(game[0].rank)

        if game[1].rank == "UR":
            viewers += (CFBGlobalSettings.NumOfTeamsRanked.value+1+game[1].total_losses)
        else:
            viewers += int(game[1].rank)
        return viewers


    def ranking(self, team):
        if team.rank == "UR":
            return CFBGlobalSettings.NumOfTeamsRanked.value + 1 + team.total_losses
        else:
            return int(team.rank)


    def print_standings(self):
        for con in self.conferences:
            con.div1.sort(key= lambda x: self.team_ranks.index(x))
            con.div2.sort(key= lambda x: self.team_ranks.index(x))

            print(f"{(con.name):^93}")
            print(f"{(con.div1_name):^46}{(con.div2_name):^46}")
            print("---------------------------------------------------------------------------------------------")
            for tea in range(CFBGlobalSettings.TeamsPerDivision.value):
                print(f"{(con.div1[tea].rank):>2} ({(con.div1[tea].prev_rank):>2}) {(con.div1[tea].name):<20} ({(con.div1[tea].total_wins):<2} - {(con.div1[tea].total_losses):>2}) ({(con.div1[tea].point_diff if self.rank_sig=='AP' else con.div1[tea].cfb_points):>4}) | {(con.div2[tea].rank):>2} ({(con.div2[tea].prev_rank):>2}) {(con.div2[tea].name):<20} ({(con.div2[tea].reg_wins):<2} - {(con.div2[tea].reg_losses):>2}) ({(con.div2[tea].point_diff if self.rank_sig=='AP' else con.div2[tea].cfb_points):>4})")

            input("")

    def print_top25(self):
        self.team_ranks.sort(key=lambda x: int(x.full_rank))
        print("-----------------------------------------------------")
        print("{0:^54}".format(f"{self.rank_sig} Top {CFBGlobalSettings.NumOfTeamsRanked.value}"))
        print("-----------------------------------------------------")
        print(f"Rk (+/-) |         Name         | Record | {'Point_Diff' if self.rank_sig=='AP' else 'CFB Points'}")
        print("-----------------------------------------------------")
        for i in range(CFBGlobalSettings.NumOfTeamsRanked.value):
            print(f"{(1+i):>2} ({(self.team_ranks[i].get_rank_difference()):>3}) | {(self.team_ranks[i].name):<20} | {(self.team_ranks[i].total_wins):>2} -{(self.team_ranks[i].total_losses):>2} | {(self.team_ranks[i].point_diff if self.rank_sig == 'AP' else self.team_ranks[i].cfb_points):>6}")
        print("")


    def conference_championships(self):
        for con in self.conferences:
            con.div1.sort(key= lambda x: int(x.full_rank))
            con.div2.sort(key= lambda x: int(x.full_rank))

            team1 = con.div1[0]
            team2 = con.div2[0]

            print(f"{con.name} Championship!!!")
            input(f"{team1.rank} {team1.name} ({team1.total_wins}-{team1.total_losses}) vs {team2.rank} {team2.name} ({team2.total_wins}-{team2.total_losses})")

            winner, loser = self.cfb_ranker.determine_winner(team1, team2)
            
            #print(f"0-{1+box} | {team1_wins}")
            scores = self.get_scores()
            print(f"{winner.name} {scores[0]} - {scores[1]} {loser.name} | {winner.name} wins!!!")
            
            winner.total_wins += 1 
            winner.reg_wins += 1

            winner.is_con_champion = True
            winner.opponents.append(OpponentMatch(loser, True, scores[0]-scores[1], (winner.rank, loser.rank), conference_champ_game=True, has_game_happened=True))

            loser.total_losses += 1
            loser.reg_losses += 1
            loser.opponents.append(OpponentMatch(winner, False, scores[1]-scores[0], (loser.rank, winner.rank), conference_champ_game=True, has_game_happened=True))


            input("\n")
        self.is_after_conference_championship = True
    
    def playoffs_four(self):
        teams = self.get_all_teams()
        teams.sort(key= self.ranking)

        # Semi Final 1 (1 v 4)
        team1 = teams[0]
        team2 = teams[3]
        team3 = teams[1]
        team4 = teams[2]

        input(f"CFB Playoffs Semi Final 1: {team1.rank} {team1.name} ({team1.total_wins}-{team1.total_losses}) vs {team2.rank} {team2.name} ({team2.total_wins}-{team2.total_losses})")

        winner, loser = self.cfb_ranker.determine_winner(team1, team2)
        scores = self.get_scores()
        winner.total_wins += 1
        loser.total_losses += 1
        teams.remove(loser)

        print(f"{winner.name} wins!!! ({scores[0]}-{scores[1]})")

        input("")

        # Semi Final 2 (2 v 3)
        input(f"CFB Playoffs Semi Final 2: {team3.rank} {team3.name} ({team3.total_wins}-{team3.total_losses}) vs {team4.rank} {team4.name} ({team4.total_wins}-{team4.total_losses})")

        winner, loser = self.cfb_ranker.determine_winner(team3, team4)
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

        winner, loser = self.cfb_ranker.determine_winner(team1, team2)
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

            winner, loser = self.cfb_ranker.determine_winner(teams[self.octo[i][1]], teams[self.octo[i][0]])

            winner = int(winner == teams[self.octo[i][1]])
            loser = int(not bool(winner))

            #print(f"0-{1+box} | {winner}")
            scores = self.get_scores()
            self.quarter[i].append(self.octo[i][winner])
            teams[self.octo[i][winner]].total_wins += 1
            teams[self.octo[i][winner]].opponents.append(OpponentMatch(teams[self.octo[i][loser]], True, scores[0]-scores[1], (teams[self.octo[i][winner]].rank, teams[self.octo[i][loser]].rank), po_octo=True, has_game_happened=True))
            teams[self.octo[i][loser]].total_losses += 1
            teams[self.octo[i][loser]].opponents.append(OpponentMatch(teams[self.octo[i][winner]], False, scores[1]-scores[0], (teams[self.octo[i][loser]].rank, teams[self.octo[i][winner]].rank), po_octo=True, has_game_happened=True))
            print(f"{teams[self.octo[i][winner]].name} {scores[0]} - {scores[1]} {teams[self.octo[i][loser]].name} | {teams[self.octo[i][winner]].name} wins!!!\n")

            self.menu_processor(allow_save_load=False, retry_counter=1)

        # Quarter Matches
        for i in range(4):
            input(f"CFB Championship Quarter Round {i+1}: {teams[self.quarter[i][0]].rank} {teams[self.quarter[i][0]].name} ({teams[self.quarter[i][0]].total_wins}-{teams[self.quarter[i][0]].total_losses}) vs {teams[self.quarter[i][1]].rank} {teams[self.quarter[i][1]].name} ({teams[self.quarter[i][1]].total_wins}-{teams[self.quarter[i][1]].total_losses})")

            winner, loser = self.cfb_ranker.determine_winner(teams[self.quarter[i][0]], teams[self.quarter[i][1]])
            
            winner = int(winner == teams[self.quarter[i][1]])
            loser = int(not bool(winner))

            #print(f"0-{1+box} | {winner}")
            scores = self.get_scores()
            self.semi[i//2].append(self.quarter[i][winner])
            teams[self.quarter[i][winner]].total_wins += 1
            teams[self.quarter[i][winner]].opponents.append(OpponentMatch(teams[self.quarter[i][loser]], True, scores[0]-scores[1], (teams[self.quarter[i][winner]].rank, teams[self.quarter[i][loser]].rank), po_quarter=True, has_game_happened=True))
            teams[self.quarter[i][loser]].total_losses += 1
            teams[self.quarter[i][loser]].opponents.append(OpponentMatch(teams[self.quarter[i][winner]], False, scores[1]-scores[0], (teams[self.quarter[i][loser]].rank, teams[self.quarter[i][winner]].rank), po_quarter=True, has_game_happened=True))

            print(f"{teams[self.quarter[i][winner]].name} {scores[0]} - {scores[1]} {teams[self.quarter[i][loser]].name} | {teams[self.quarter[i][winner]].name} wins!!!\n")

            self.menu_processor(allow_save_load=False, retry_counter=1)

        # Semi Matches
        for i in range(2):
            input(f"CFB Championship Semi Round {i+1}: {teams[self.semi[i][0]].rank} {teams[self.semi[i][0]].name} ({teams[self.semi[i][0]].total_wins}-{teams[self.semi[i][0]].total_losses}) vs {teams[self.semi[i][1]].rank} {teams[self.semi[i][1]].name} ({teams[self.semi[i][1]].total_wins}-{teams[self.semi[i][1]].total_losses})")

            winner, loser = self.cfb_ranker.determine_winner(teams[self.semi[i][1]], teams[self.semi[i][0]])

            winner = int(winner == teams[self.semi[i][1]])
            loser = int(not bool(winner))

            #print(f"0-{1+box} | {winner}")
            scores = self.get_scores()
            self.final.append(self.semi[i][winner])

            teams[self.semi[i][winner]].total_wins += 1
            teams[self.semi[i][winner]].opponents.append(OpponentMatch(teams[self.semi[i][loser]], True, scores[0]-scores[1], (teams[self.semi[i][winner]].rank, teams[self.semi[i][loser]].rank), po_semi=True, has_game_happened=True))
            teams[self.semi[i][loser]].total_losses += 1
            teams[self.semi[i][loser]].opponents.append(OpponentMatch(teams[self.semi[i][winner]], False, scores[1]-scores[0], (teams[self.semi[i][loser]].rank, teams[self.semi[i][winner]].rank), po_semi=True, has_game_happened=True))

            print(f"{teams[self.semi[i][winner]].name} {scores[0]} - {scores[1]} {teams[self.semi[i][loser]].name} | {teams[self.semi[i][winner]].name} wins!!!\n")

            self.menu_processor(allow_save_load=False, retry_counter=1)

        # The Championship
        input(f"CFB Championship!!! {teams[self.final[0]].rank} {teams[self.final[0]].name} ({teams[self.final[0]].total_wins}-{teams[self.final[0]].total_losses}) vs {teams[self.final[1]].rank} {teams[self.final[1]].name} ({teams[self.final[1]].total_wins}-{teams[self.final[1]].total_losses})")

        winner, loser = self.cfb_ranker.determine_winner(teams[self.final[1]], teams[self.final[0]])
        self.winner = winner

        winner = int(winner == teams[self.final[1]])
        loser = int(not bool(winner))

        scores = self.get_scores()
        teams[self.final[winner]].total_wins += 1
        teams[self.final[winner]].opponents.append(OpponentMatch(teams[self.final[loser]], True, scores[0]-scores[1], (teams[self.final[winner]].rank, teams[self.final[loser]].rank), (winner), po_final=True, has_game_happened=True))
        teams[self.final[int(not winner)]].total_losses += 1
        teams[self.final[loser]].opponents.append(OpponentMatch(teams[self.final[winner]], False, scores[1]-scores[0], (teams[self.final[loser]].rank, teams[self.final[winner]].rank), po_final=True, has_game_happened=True))

        print(f"{teams[self.final[winner]].name} {scores[0]} - {scores[1]} {teams[self.final[loser]].name} | {teams[self.final[winner]].name} wins!!!\n")
        print(f"{teams[self.final[winner]].name} are your CFB CHAMPIONS!!!!")
        print(f"Ranked: {teams[self.final[winner]].rank} | ({teams[self.final[winner]].total_wins}-{teams[self.final[winner]].total_losses})")

    def print_full_rankings(self):
        for t in range(len(self.team_ranks)):
            print(f"{(t+1):>2}) {(self.team_ranks[t].name):<20} ({self.team_ranks[t].total_wins}-{self.team_ranks[t].total_losses}) {self.team_ranks[t].point_diff if self.rank_sig == 'AP' else self.team_ranks[t].cfb_points}")

    def handle_regular_game(self, winner: Team, loser: Team, scores, print_stuff):
        points_diff = scores[0] - scores[1]
        winner.handle_win(points_diff, self.week-1, (winner.rank, loser.rank))
        loser.handle_loss(points_diff, self.week-1, (loser.rank, winner.rank))

        if print_stuff:
            print(f"{winner.name} {scores[0]} - {scores[1]} {loser.name}  | {winner.name} wins!\n")

    def menu_processor(self, allow_save_load: bool = True, retry_counter: int = 3):
        enter_counter = 0
        while True:
            allow_gw_rr: bool = self.week < CFBGlobalSettings.NumOfRegWeeks.value
            selection_string = (
                f" {'(FR):':<5} {'See Full Rankings':<18} | {'(A):':<5} {'Advance Week':<15} | {'(B):':<5} {'Show Bracket':<18}\n"
                f" {'(TD):':<5} {'Team Details':<18} | {'(ST):':<5} {f'Show Top {CFBGlobalSettings.NumOfTeamsRanked.value}':<15} | {'(SC):':<5} {'Show Confrences':<18}\n"
            )
            if allow_gw_rr:
                selection_string += (
                    f" {'(GW):':<5} {'Games of Week':<18} | {'(RR):':<5} {'ReRank Teams':<15}\n"
                )
            if allow_save_load:
                selection_string += (
                    f" {'(S):':<5} {'Save Season':<18} | {'(L):':<5} {'Load Season':<15}\n"
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
            if selection.lower() == "rr" and allow_gw_rr:
                if self.week < CFBGlobalSettings.WeekCFBStartsRanking.value:
                    self.ap_ranker.rank_teams()
                else:
                    self.cfb_ranker.rank_teams()
                self.print_top25()
                print("\n")
            if selection.lower() == "gw" and allow_gw_rr:
                top3_matches = self.get_this_week_matchups_sorted()[-3:][::-1]
                for i in range(3):
                    game_of_week: bool = i == 0
                    self._print_matchup(top3_matches[i], game_of_week)
                    print("\n")
                print("\n")
            if selection.lower()[:2] == "td":
                td_split = selection.lower().split(' ')
                if len(td_split) > 1:
                    for t in range(1, len(td_split)):
                        if td_split[t].isdigit() and int(td_split[t]) <= 100:
                            viewing = deepcopy(self.team_ranks)
                            viewing.sort(key=lambda x: int(x.full_rank))
                            viewing[int(td_split[t])-1].print_team_details()
                            print("\n")
                        else:
                            print("next time enter a digit\n")

                else:
                    tr = input("Enter the team's rank you want to see: ")
                    if tr.isdigit() and int(tr) <= (CFBGlobalSettings.NumOfConferences.value * CFBGlobalSettings.TeamsPerDivision.value * 2):
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
                
            if selection.lower() == "a" or enter_counter >= retry_counter:
                print("\n")
                return


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
                    file.write(f"{op.opponent.name},{op.win},{op.point_diff},{op.rank_history[0]},{op.rank_history[1]},{op.cfb_points},{op.is_conference_title},{op.is_playoff_octo},{op.is_playoff_quarter},{op.is_playoff_semi},{op.is_playoff_final},{op.has_game_happened},\n")
            file.write(f"{conf.div2_name}\n")
            for team in conf.div2:
                team: Team
                file.write(f"{team.name},{team.reg_wins},{team.reg_losses},{team.total_wins},{team.total_losses},{team.rank},{team.prev_rank},{team.full_rank},{team.point_diff},{team.cfb_points},\n")
                for op in team.opponents:
                    op: OpponentMatch
                    file.write(f"{op.opponent.name},{op.win},{op.point_diff},{op.rank_history[0]},{op.rank_history[1]},{op.cfb_points},{op.is_conference_title},{op.is_playoff_octo},{op.is_playoff_quarter},{op.is_playoff_semi},{op.is_playoff_final},{op.has_game_happened},\n")

        file.close()
        print(f"Saved season to {filepath}")


    def load_season(self):
        file_name = input("Enter name of load file: ")
        filepath = f"{self.SEASON_FOLDER}/{file_name}.cfb"

        file = open(file=filepath, mode='r')
        
        conf_data = file.readline().split(',')[:-1]
        self.week = int(conf_data[0])
        self.rank_sig = conf_data[1]

        for con in range(CFBGlobalSettings.NumOfConferences.value):
            self.conferences[con].name = file.readline()[:-1]
            self.conferences[con].div1_name = file.readline()[:-1]
            for div_team in range(CFBGlobalSettings.TeamsPerDivision.value):
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
                for _ in range(CFBGlobalSettings.NumOfRegWeeks.value):
                    op_data = file.readline().split(',')[:-1]
                    opponents.append(
                        OpponentMatch(
                            op=op_data[0],
                            win=op_data[1] == "True",
                            pd=int(op_data[2]),
                            rh=(op_data[3],op_data[4]),
                            cfb_p=(
                                int(op_data[5])
                                if op_data[5].isdigit() or op_data[5].lstrip('-').isdigit()
                                else "AP"
                            ),
                            conference_champ_game=op_data[6] == "True",
                            po_octo=op_data[7] == "True",
                            po_quarter=op_data[8] == "True",
                            po_semi=op_data[9] == "True",
                            po_final=op_data[10] == "True",
                            has_game_happened=(op_data[11] == "True"),
                        )
                    )
                self.conferences[con].div1[div_team].opponents = opponents

            self.conferences[con].div2_name = file.readline()[:-1]
            for div_team in range(CFBGlobalSettings.TeamsPerDivision.value):
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
                for _ in range(CFBGlobalSettings.NumOfRegWeeks.value):
                    op_data = file.readline().split(',')[:-1]
                    opponents.append(
                        OpponentMatch(
                            op=op_data[0],
                            win=op_data[1] == "True",
                            pd=int(op_data[2]),
                            rh=(op_data[3], op_data[4]),
                            cfb_p=(
                                int(op_data[5])
                                if op_data[5].isdigit() or op_data[5].lstrip('-').isdigit()
                                else "AP"
                            ),
                            conference_champ_game=op_data[6] == "True",
                            po_octo=op_data[7] == "True",
                            po_quarter=op_data[8] == "True",
                            po_semi=op_data[9] == "True",
                            po_final=op_data[10] == "True",
                            has_game_happened=(op_data[11] == "True"),
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
            if CFBGlobalSettings.AllConfChampInPlayoff.value:
                self.team_ranks.sort(key=lambda x: (not x.is_con_champion, int(x.full_rank)))
                cfp_teams = self.team_ranks[:limit]
            else:
                self.team_ranks.sort(key=lambda x: (not x.is_con_champion, int(x.full_rank)))
                cfp_teams = self.team_ranks[:CFBGlobalSettings.NumOfConfChampInPlayoff.value]
                self.team_ranks.sort(key=lambda x: int(x.full_rank))
                index = 0
                while len(cfp_teams) < limit:
                    if self.team_ranks[index] not in cfp_teams:
                        cfp_teams.append(self.team_ranks[index])
    
                    index += 1
            
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
            print("-----------------------------------------------------")
            print("| Sd  | Rk  |       Name        |  Conf  |  Record  |")
            print("-----------------------------------------------------")
            for i in range(1, 13):
                team = next((x for x in teams if x.cfp_seed == i), None)
                print(f"| {i:>2}) | {(team.full_rank if team else ' '):>2}) | {(team.name if team else ' '):^17} |  {(team.conference if team else ' '):^4}{('*' if team and team.is_con_champion else ' ')} | {(f'({team.total_wins:>2} - {team.total_losses:>2})' if team else ' '):<8}")
            
            print("\n\n--------------------")
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

        if not CFBGlobalSettings.AllConfChampInPlayoff.value:
            temp = made_it[:CFBGlobalSettings.NumOfConfChampInPlayoff.value]
            temp2 = made_it[CFBGlobalSettings.NumOfConfChampInPlayoff.value:]
            temp2.sort(key=lambda x: int(x.full_rank))
            temp.extend(temp2)
            made_it = temp

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
                print_reveal(revealed_teams, made_it, out)
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

    
    def main_game_loop(self):
        self.ap_ranker.rank_teams()
        self.team_scheduler.generate_schedules()
        self.menu_processor(retry_counter=1)
    
        self.print_top25()
        input("")
        self.print_standings()
        self.menu_processor()
    
        while self.week <= CFBGlobalSettings.NumOfRegWeeks.value:
            self.play_week(print_stuff=True)
            input("")
            self.menu_processor(retry_counter=1, allow_save_load=False)

            if not CFBGlobalSettings.UseRandomRanker.value:
                if self.week < CFBGlobalSettings.WeekCFBStartsRanking.value:
                    self.ap_ranker.rank_teams()
                else:
                    self.cfb_ranker.rank_teams()
            else:
                self.random_ranker.rank_teams()

            self.print_top25()
            input("")
            self.print_standings()
            input("")
            self.week += 1
            self.menu_processor()
    
        self.conference_championships()
        self.menu_processor(allow_save_load=False)
    
        self.cfb_ranker.rank_teams()
    
        if CFBGlobalSettings.isTwelveTeamPlayoff.value:
            self.cfp_teams_reveal()
            self.print_top25()
            self.menu_processor(allow_save_load=False)
            input("")
            self.playoffs_twelve()
        else:
            self.print_top25()
            self.menu_processor(allow_save_load=False)
            self.playoffs_four()
    
        input("")
        self.menu_processor(allow_save_load=False)
