from random import randint, shuffle
from src.conference import Conference
from src.opponent_match import OpponentMatch
from src.playoff import TradTwelvePlayoff
from src.ranker import APRanker, CFBRanker, RandomRanker
from src.save_load_file import SaveLoadFile
from src.settings import CFBGlobalSettings
from src.team import Team
from src.team_scheduler import TeamScheduler
from copy import deepcopy


class CFB:

    def __init__(self):
            self.conferences: list[Conference] = self.set_up_season()
            self.team_ranks: list[Team] = []
            self.rank_sig: str = "NA"
            self.week: int = 1
            self.is_after_conference_championship: bool = False
            
            self.winner: Team = None
            self.SEASON_FOLDER = "saved_seasons"
    
            # Post-Season Saving Flags
            self.PLAYOFF_REVEALED: bool = False
            self.HAVE_PLAYOFFS_STARTED: bool = False
    
            # Helper Classes
            self.save_load_file = SaveLoadFile(self)

            self.team_scheduler = TeamScheduler(self)
    
            self.ap_ranker = APRanker(self)
            self.cfb_ranker = CFBRanker(self)
            self.random_ranker = RandomRanker(self)
    
            self.trad_12_playoff = TradTwelvePlayoff(self)


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
        acc_at.append(Team("NC State"))
        acc_at.append(Team("Syracuse"))
        acc_at.append(Team("Clemson"))
        acc_at.append(Team("Florida State"))
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
        pac_east.append(Team("Uconn"))
        pac_east.append(Team("Washington"))
        pac_east.append(Team("Toledo"))
        pac_east.append(Team("Memphis"))
        pac_east.append(Team("Cincinnati"))
        pac_east.append(Team("Utah"))
        pac_east.append(Team("Stanford"))

        pac_west = []
        pac_west.append(Team("Sam Houston"))
        pac_west.append(Team("Texas Tech"))
        pac_west.append(Team("USC"))
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
        fbs_west.append(Team("Kent State"))

        cons.append(Conference("FCS", fbs_east, fbs_west, "East", "West"))

        return cons


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

        self.week += 1


    def _print_matchup(self, match, game_of_week=False, print_stuff=True):
            home = match[0]
            away = match[1]
            if print_stuff:
                if game_of_week:
                    print("NCAA GAME OF THE WEEK!!!")
                input(f"Match-up: {away.rank} {away.name} ({away.reg_wins}-{away.reg_losses}) @ {home.rank} {home.name} ({home.reg_wins}-{home.reg_losses})")


    def sort_prime_time(self, game):
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


    def print_standings(self, one_conference: str = None):
        for con in self.conferences:
            if one_conference is not None and con.name != one_conference:
                continue

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


    def conference_championships(self, print_stuff: bool = True):
        for con in self.conferences:
            con.div1.sort(key= lambda x: int(x.full_rank))
            con.div2.sort(key= lambda x: int(x.full_rank))

            team1 = con.div1[0]
            team2 = con.div2[0]

            if print_stuff:
                print(f"{con.name} Championship!!!")
                input(f"{team1.rank} {team1.name} ({team1.total_wins}-{team1.total_losses}) vs {team2.rank} {team2.name} ({team2.total_wins}-{team2.total_losses})")

            winner, loser = self.cfb_ranker.determine_winner(team1, team2)
            
            #print(f"0-{1+box} | {team1_wins}")
            scores = self.get_scores()

            if print_stuff:
                print(f"{winner.name} {scores[0]} - {scores[1]} {loser.name} | {winner.name} wins!!!")
            
            winner.total_wins += 1 
            winner.reg_wins += 1

            winner.is_con_champion = True
            winner.opponents.append(OpponentMatch(loser, True, scores[0]-scores[1], (winner.rank, loser.rank), conference_champ_game=True, has_game_happened=True))

            loser.total_losses += 1
            loser.reg_losses += 1
            loser.opponents.append(OpponentMatch(winner, False, scores[1]-scores[0], (loser.rank, winner.rank), conference_champ_game=True, has_game_happened=True))

            if print_stuff:
                input("\n")
        self.week += 1
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
            allow_gw_rr: bool = self.week <= CFBGlobalSettings.NumOfRegWeeks.value
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
                self.save_load_file.save_season()
                print("\n")
            if selection.lower() == "l" and allow_save_load:
                self.save_load_file.load_season()
                print("\n")
            if selection.lower() == "b":
                cfp = self.trad_12_playoff.get_cfp_12_teams(get_first_two_out=True)
                self.trad_12_playoff.view_bracket(cfp)
                print("\n")
            if selection.lower() == "st":
                self.print_top25()
                print("\n")
            if selection.lower()[:2] == "sc":
                sc_split = selection.split(' ')
                if len(sc_split) == 1:
                    self.print_standings()
                else:
                    for con_to_show in sc_split[1:]:
                        self.print_standings(one_conference=con_to_show.upper())
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

    
    def main_game_loop(self):
        self.random_ranker.rank_teams()
        self.team_scheduler.generate_schedules()
        self.menu_processor(retry_counter=1)
    
        self.print_top25()
        input("")
        self.print_standings()
        self.menu_processor()
    
        while self.week <= CFBGlobalSettings.NumOfRegWeeks.value:
            self.play_week()
            input("")
            self.menu_processor(retry_counter=1, allow_save_load=False)

            if not CFBGlobalSettings.UseRandomRanker.value:
                if self.week <= CFBGlobalSettings.WeekCFBStartsRanking.value:
                    self.ap_ranker.rank_teams()
                else:
                    self.cfb_ranker.rank_teams()
            else:
                self.random_ranker.rank_teams()

            self.print_top25()
            input("")
            self.print_standings()
            input("")
            self.menu_processor()

        if self.week == CFBGlobalSettings.NumOfRegWeeks.value + 1:
            self.conference_championships()
            self.menu_processor()

        if not self.PLAYOFF_REVEALED:
            self.cfb_ranker.rank_teams()
    
        if CFBGlobalSettings.isTwelveTeamPlayoff.value:
            if not self.PLAYOFF_REVEALED:
                self.trad_12_playoff.cfp_teams_reveal()
                self.print_top25()
                self.menu_processor()
                input("")
            self.trad_12_playoff.playoffs_twelve()
        else:
            self.print_top25()
            self.menu_processor(allow_save_load=False)
            self.playoffs_four()
            input("")
    
        self.menu_processor(allow_save_load=CFBGlobalSettings.isTwelveTeamPlayoff.value)
