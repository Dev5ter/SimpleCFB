from __future__ import annotations
from typing import TYPE_CHECKING

from src.opponent_match import OpponentMatch
from src.settings import CFBGlobalSettings

if TYPE_CHECKING:
    from src.cfb import CFB
    from src.team import Team


class TradTwelvePlayoff:
    def __init__(self, cfb: CFB):
        self.cfb = cfb
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

    def get_cfp_12_teams(self, get_first_two_out:bool = False) -> list[Team]:
        # Clear Previous Seeding
        all_teams = self.cfb.get_all_teams()
        for team in all_teams:
            team.cfp_seed = "OUT"

        cfp_teams = []
        limit = 14 if get_first_two_out else 12

        if self.cfb.is_after_conference_championship:
            if CFBGlobalSettings.AllConfChampInPlayoff.value:
                self.cfb.team_ranks.sort(key=lambda x: (not x.is_con_champion, int(x.full_rank)))
                cfp_teams = self.cfb.team_ranks[:limit]
            else:
                self.cfb.team_ranks.sort(key=lambda x: (not x.is_con_champion, int(x.full_rank)))
                cfp_teams = self.cfb.team_ranks[:CFBGlobalSettings.NumOfConfChampInPlayoff.value]
                self.cfb.team_ranks.sort(key=lambda x: int(x.full_rank))
                index = 0
                while len(cfp_teams) < limit:
                    if self.cfb.team_ranks[index] not in cfp_teams:
                        cfp_teams.append(self.cfb.team_ranks[index])
    
                    index += 1
            
        else:
            for con in self.cfb.conferences:
                teams = []
                for d1 in con.div1:
                    teams.append(d1)
                for d2 in con.div2:
                    teams.append(d2)

                teams.sort(key=lambda x: int(x.full_rank))
                cfp_teams.append(teams[0])
            index = 0
            while len(cfp_teams) < limit:
                if self.cfb.team_ranks[index] not in cfp_teams:
                    cfp_teams.append(self.cfb.team_ranks[index])

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


    def _print_reveal(self, teams: list[Team], other_made_it, outs):
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


    def cfp_teams_reveal(self):
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
        self._print_reveal(revealed_teams, made_it, out)
        input("\n")
        for i in range(12):
            revealed_teams.append(made_it.pop(0))
            self._print_reveal(revealed_teams, made_it, out)

            if i == 10:
                input("")
                comb = made_it + out 
                comb.sort(key = lambda x: x.name)
                for team in comb:
                    print("\n")
                    team.print_team_details(show_cfp_points=False)
                    print("\n")
                
                input("")
                self._print_reveal(revealed_teams, made_it, out)
                print("\n")

            input("")

        self.cfb.PLAYOFF_REVEALED = True
            
    
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

        WINNER = self.cfb.winner
        

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


    def playoffs_twelve(self):
        teams = self.get_cfp_12_teams()

        # Octo Matches
        for i in range(4):
            if teams[self.octo[i][0]].has_had_playoff_win(octo=True) or teams[self.octo[i][1]].has_had_playoff_win(octo=True):
                continue

            input(f"CFB Championship Octo Round {i+1}: {teams[self.octo[i][0]].rank} {teams[self.octo[i][0]].name} ({teams[self.octo[i][0]].total_wins}-{teams[self.octo[i][0]].total_losses}) vs {teams[self.octo[i][1]].rank} {teams[self.octo[i][1]].name} ({teams[self.octo[i][1]].total_wins}-{teams[self.octo[i][1]].total_losses})")

            winner, loser = self.cfb.cfb_ranker.determine_winner(teams[self.octo[i][1]], teams[self.octo[i][0]])

            winner = int(winner == teams[self.octo[i][1]])
            loser = int(not bool(winner))

            scores = self.cfb.get_scores()
            self.quarter[i].append(self.octo[i][winner])
            teams[self.octo[i][winner]].total_wins += 1
            teams[self.octo[i][winner]].opponents.append(OpponentMatch(teams[self.octo[i][loser]], True, scores[0]-scores[1], (teams[self.octo[i][winner]].rank, teams[self.octo[i][loser]].rank), po_octo=True, has_game_happened=True))
            teams[self.octo[i][loser]].total_losses += 1
            teams[self.octo[i][loser]].opponents.append(OpponentMatch(teams[self.octo[i][winner]], False, scores[1]-scores[0], (teams[self.octo[i][loser]].rank, teams[self.octo[i][winner]].rank), po_octo=True, has_game_happened=True))
            print(f"{teams[self.octo[i][winner]].name} {scores[0]} - {scores[1]} {teams[self.octo[i][loser]].name} | {teams[self.octo[i][winner]].name} wins!!!\n")

            self.cfb.HAVE_PLAYOFFS_STARTED = True

            self.cfb.menu_processor(retry_counter=1)

        # Quarter Matches
        for i in range(4):
            if teams[self.quarter[i][0]].has_had_playoff_win(quarter=True) or teams[self.quarter[i][1]].has_had_playoff_win(quarter=True):
                continue

            input(f"CFB Championship Quarter Round {i+1}: {teams[self.quarter[i][0]].rank} {teams[self.quarter[i][0]].name} ({teams[self.quarter[i][0]].total_wins}-{teams[self.quarter[i][0]].total_losses}) vs {teams[self.quarter[i][1]].rank} {teams[self.quarter[i][1]].name} ({teams[self.quarter[i][1]].total_wins}-{teams[self.quarter[i][1]].total_losses})")

            winner, loser = self.cfb.cfb_ranker.determine_winner(teams[self.quarter[i][0]], teams[self.quarter[i][1]])
            
            winner = int(winner == teams[self.quarter[i][1]])
            loser = int(not bool(winner))

            scores = self.cfb.get_scores()
            self.semi[i//2].append(self.quarter[i][winner])
            teams[self.quarter[i][winner]].total_wins += 1
            teams[self.quarter[i][winner]].opponents.append(OpponentMatch(teams[self.quarter[i][loser]], True, scores[0]-scores[1], (teams[self.quarter[i][winner]].rank, teams[self.quarter[i][loser]].rank), po_quarter=True, has_game_happened=True))
            teams[self.quarter[i][loser]].total_losses += 1
            teams[self.quarter[i][loser]].opponents.append(OpponentMatch(teams[self.quarter[i][winner]], False, scores[1]-scores[0], (teams[self.quarter[i][loser]].rank, teams[self.quarter[i][winner]].rank), po_quarter=True, has_game_happened=True))

            print(f"{teams[self.quarter[i][winner]].name} {scores[0]} - {scores[1]} {teams[self.quarter[i][loser]].name} | {teams[self.quarter[i][winner]].name} wins!!!\n")

            self.cfb.menu_processor(retry_counter=1)

        # Semi Matches
        for i in range(2):
            if teams[self.semi[i][0]].has_had_playoff_win(semi=True) or teams[self.semi[i][1]].has_had_playoff_win(semi=True):
                continue

            input(f"CFB Championship Semi Round {i+1}: {teams[self.semi[i][0]].rank} {teams[self.semi[i][0]].name} ({teams[self.semi[i][0]].total_wins}-{teams[self.semi[i][0]].total_losses}) vs {teams[self.semi[i][1]].rank} {teams[self.semi[i][1]].name} ({teams[self.semi[i][1]].total_wins}-{teams[self.semi[i][1]].total_losses})")

            winner, loser = self.cfb.cfb_ranker.determine_winner(teams[self.semi[i][1]], teams[self.semi[i][0]])

            winner = int(winner == teams[self.semi[i][1]])
            loser = int(not bool(winner))

            #print(f"0-{1+box} | {winner}")
            scores = self.cfb.get_scores()
            self.final.append(self.semi[i][winner])

            teams[self.semi[i][winner]].total_wins += 1
            teams[self.semi[i][winner]].opponents.append(OpponentMatch(teams[self.semi[i][loser]], True, scores[0]-scores[1], (teams[self.semi[i][winner]].rank, teams[self.semi[i][loser]].rank), po_semi=True, has_game_happened=True))
            teams[self.semi[i][loser]].total_losses += 1
            teams[self.semi[i][loser]].opponents.append(OpponentMatch(teams[self.semi[i][winner]], False, scores[1]-scores[0], (teams[self.semi[i][loser]].rank, teams[self.semi[i][winner]].rank), po_semi=True, has_game_happened=True))

            print(f"{teams[self.semi[i][winner]].name} {scores[0]} - {scores[1]} {teams[self.semi[i][loser]].name} | {teams[self.semi[i][winner]].name} wins!!!\n")

            self.cfb.menu_processor(retry_counter=1)

        if self.cfb.winner is not None:
            return

        # The Championship
        input(f"CFB Championship!!! {teams[self.final[0]].rank} {teams[self.final[0]].name} ({teams[self.final[0]].total_wins}-{teams[self.final[0]].total_losses}) vs {teams[self.final[1]].rank} {teams[self.final[1]].name} ({teams[self.final[1]].total_wins}-{teams[self.final[1]].total_losses})")

        winner, loser = self.cfb.cfb_ranker.determine_winner(teams[self.final[1]], teams[self.final[0]])
        self.cfb.winner = winner

        winner = int(winner == teams[self.final[1]])
        loser = int(not bool(winner))

        scores = self.cfb.get_scores()
        teams[self.final[winner]].total_wins += 1
        teams[self.final[winner]].opponents.append(OpponentMatch(teams[self.final[loser]], True, scores[0]-scores[1], (teams[self.final[winner]].rank, teams[self.final[loser]].rank), (winner), po_final=True, has_game_happened=True))
        teams[self.final[int(not winner)]].total_losses += 1
        teams[self.final[loser]].opponents.append(OpponentMatch(teams[self.final[winner]], False, scores[1]-scores[0], (teams[self.final[loser]].rank, teams[self.final[winner]].rank), po_final=True, has_game_happened=True))

        print(f"{teams[self.final[winner]].name} {scores[0]} - {scores[1]} {teams[self.final[loser]].name} | {teams[self.final[winner]].name} wins!!!\n")
        print(f"{teams[self.final[winner]].name} are your CFB CHAMPIONS!!!!")
        print(f"Ranked: {teams[self.final[winner]].rank} | ({teams[self.final[winner]].total_wins}-{teams[self.final[winner]].total_losses})")
        input("")


    def load_playoff_lists_after_save(self):
        playoff_teams = [
            x
            for x
            in self.cfb.get_all_teams()
            if x.cfp_seed != "OUT"
        ]

        octo_winners = [x for x in playoff_teams if x.has_had_playoff_win(octo=True)]
        for octo_winner in octo_winners:
            for octo_set in range(len(self.octo)):
                if octo_winner.cfp_seed-1 in self.octo[octo_set]:
                    self.quarter[octo_set].append(octo_winner.cfp_seed-1)

        quarter_winners = [x for x in playoff_teams if x.has_had_playoff_win(quarter=True)]
        quarter_winners.sort(key = lambda x: (x.cfp_seed in [1,8,9], x.cfp_seed in [4,5,12], x.cfp_seed in [2,7,10], x.cfp_seed in [3,6,11]), reverse=True)
        for quarter_winner in quarter_winners:
            for quarter_set in range(len(self.quarter)):
                if quarter_winner.cfp_seed-1 in self.quarter[quarter_set]:
                    self.semi[quarter_set//2].append(quarter_winner.cfp_seed-1)

        semi_winners = [x for x in playoff_teams if x.has_had_playoff_win(semi=True)]
        semi_winners.sort(key = lambda x: (x.cfp_seed in [1,8,9,4,5,12], x.cfp_seed in [2,7,10,3,6,11]), reverse=True)
        for semi_winner in semi_winners:
            self.final.append(semi_winner.cfp_seed-1)

        final_winner = [x for x in playoff_teams if x.has_had_playoff_win(final=True)]
        if final_winner:
            self.cfb.winner = final_winner[0]

