from __future__ import annotations
from typing import TYPE_CHECKING

from src.opponent_match import OpponentMatch
from src.settings import CFBGlobalSettings

if TYPE_CHECKING:
    from src.cfb import CFB
    from src.conference import Conference
    from src.team import Team


class SaveLoadFile:
    def __init__(self, cfb: CFB):
        self.cfb = cfb


    def save_season(self):
        file_name = input("Enter name of save file: ")
        filepath = f"{self.cfb.SEASON_FOLDER}/{file_name}.cfb"

        file = open(file=filepath, mode='w')
        
        file.write(f"{self.cfb.week},{self.cfb.rank_sig},{self.cfb.PLAYOFF_REVEALED},{self.cfb.HAVE_PLAYOFFS_STARTED},\n")

        for conf in self.cfb.conferences:
            conf: Conference
            file.write(f"{conf.name}\n{conf.div1_name}\n")
            for team in conf.div1:
                team: Team
                file.write(f"{team.name},{team.reg_wins},{team.reg_losses},{team.total_wins},{team.total_losses},{team.rank},{team.prev_rank},{team.full_rank},{team.point_diff},{team.cfb_points},{team.is_con_champion},{team.cfp_seed},\n")
                for op in team.opponents:
                    op: OpponentMatch
                    file.write(f"{op.opponent.name},{op.win},{op.point_diff},{op.rank_history[0]},{op.rank_history[1]},{op.cfb_points},{op.is_conference_title},{op.is_playoff_octo},{op.is_playoff_quarter},{op.is_playoff_semi},{op.is_playoff_final},{op.has_game_happened},\n")
                file.write("---,\n")
            file.write(f"{conf.div2_name}\n")
            for team in conf.div2:
                team: Team
                file.write(f"{team.name},{team.reg_wins},{team.reg_losses},{team.total_wins},{team.total_losses},{team.rank},{team.prev_rank},{team.full_rank},{team.point_diff},{team.cfb_points},{team.is_con_champion},{team.cfp_seed},\n")
                for op in team.opponents:
                    op: OpponentMatch
                    file.write(f"{op.opponent.name},{op.win},{op.point_diff},{op.rank_history[0]},{op.rank_history[1]},{op.cfb_points},{op.is_conference_title},{op.is_playoff_octo},{op.is_playoff_quarter},{op.is_playoff_semi},{op.is_playoff_final},{op.has_game_happened},\n")
                file.write("---,\n")

        file.close()
        print(f"Saved season to {filepath}")


    def load_season(self):
        file_name = input("Enter name of load file: ")
        filepath = f"{self.cfb.SEASON_FOLDER}/{file_name}.cfb"

        file = open(file=filepath, mode='r')
        
        conf_data = file.readline().split(',')[:-1]
        self.cfb.week = int(conf_data[0])
        self.cfb.rank_sig = conf_data[1]
        self.cfb.PLAYOFF_REVEALED = conf_data[2] == 'True'
        self.cfb.HAVE_PLAYOFFS_STARTED = conf_data[3] == 'True'

        for con in range(CFBGlobalSettings.NumOfConferences.value):
            self.cfb.conferences[con].name = file.readline()[:-1]
            self.cfb.conferences[con].div1_name = file.readline()[:-1]
            for div_team in range(CFBGlobalSettings.TeamsPerDivision.value):
                team_data = file.readline().split(',')[:-1]
                self.cfb.conferences[con].div1[div_team].name = team_data[0]
                self.cfb.conferences[con].div1[div_team].reg_wins = int(team_data[1])
                self.cfb.conferences[con].div1[div_team].reg_losses = int(team_data[2])
                self.cfb.conferences[con].div1[div_team].total_wins = int(team_data[3])
                self.cfb.conferences[con].div1[div_team].total_losses = int(team_data[4])
                self.cfb.conferences[con].div1[div_team].rank = team_data[5]
                self.cfb.conferences[con].div1[div_team].prev_rank = team_data[6]
                self.cfb.conferences[con].div1[div_team].full_rank = team_data[7]
                self.cfb.conferences[con].div1[div_team].point_diff = int(team_data[8])
                self.cfb.conferences[con].div1[div_team].cfb_points = int(team_data[9])
                self.cfb.conferences[con].div1[div_team].is_con_champion = team_data[10] == "True"
                self.cfb.conferences[con].div1[div_team].cfp_seed = (
                    int(team_data[11]) 
                    if team_data[11].isdigit() 
                    else team_data[11]
                )

                opponents = []
                while True:
                    op_data = file.readline().split(',')[:-1]
                    if op_data[0] == '---':
                        break
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
                self.cfb.conferences[con].div1[div_team].opponents = opponents

            self.cfb.conferences[con].div2_name = file.readline()[:-1]
            for div_team in range(CFBGlobalSettings.TeamsPerDivision.value):
                team_data = file.readline().split(',')[:-1]
                self.cfb.conferences[con].div2[div_team].name = team_data[0]
                self.cfb.conferences[con].div2[div_team].reg_wins = int(team_data[1])
                self.cfb.conferences[con].div2[div_team].reg_losses = int(team_data[2])
                self.cfb.conferences[con].div2[div_team].total_wins = int(team_data[3])
                self.cfb.conferences[con].div2[div_team].total_losses = int(team_data[4])
                self.cfb.conferences[con].div2[div_team].rank = team_data[5]
                self.cfb.conferences[con].div2[div_team].prev_rank = team_data[6]
                self.cfb.conferences[con].div2[div_team].full_rank = team_data[7]
                self.cfb.conferences[con].div2[div_team].point_diff = int(team_data[8])
                self.cfb.conferences[con].div2[div_team].cfb_points = int(team_data[9])
                self.cfb.conferences[con].div2[div_team].is_con_champion = team_data[10] == "True"
                self.cfb.conferences[con].div2[div_team].cfp_seed = (
                    int(team_data[11]) 
                    if team_data[11].isdigit() 
                    else team_data[11]
                )

                opponents = []
                while True:
                    op_data = file.readline().split(',')[:-1]
                    if op_data[0] == '---':
                        break
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
                self.cfb.conferences[con].div2[div_team].opponents = opponents

        file.close()

        # Look up teams names from loading process
        for conf in self.cfb.conferences:
            for d1 in conf.div1:
                for to in d1.opponents:
                    to.opponent = self._return_team_by_name(to.opponent)
            for d2 in conf.div2:
                for to in d2.opponents:
                    to.opponent = self._return_team_by_name(to.opponent)

        # re rank to match saved status
        self.cfb.team_ranks.sort(key=lambda x: int(x.full_rank))

        if self.cfb.HAVE_PLAYOFFS_STARTED and CFBGlobalSettings.isTwelveTeamPlayoff.value:
            self.cfb.trad_12_playoff.load_playoff_lists_after_save()

        print("Loading Successful!\n")


    def _return_team_by_name(self, name: str) -> Team:
        teams = [x for x in self.cfb.team_ranks if x.name == name]
        if teams == []:
            print("ERROR NO TEAM FOUND: ", name)
        else:
            return teams[0]

