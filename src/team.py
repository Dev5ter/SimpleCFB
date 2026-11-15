from typing import TYPE_CHECKING
from src.settings import CFBGlobalSettings

if TYPE_CHECKING:
    from src.opponent_match import OpponentMatch


class Team:
    def __init__(self, team_name) -> None:
        self.name = team_name
        self.conference: str = "Unknown"
        self.division: str = "Unknown"
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

    def handle_win(self, points, week, rank_history) -> None:
        self.reg_wins += 1
        self.total_wins += 1
        self.point_diff += points
        self.update_opponent_match(week, True, points, rank_history)

    def handle_loss(self, points, week, rank_history) -> None:
        self.reg_losses += 1
        self.total_losses += 1
        self.point_diff -= points
        self.update_opponent_match(week, False, -points, rank_history)
    
    def update_opponent_match(self, week, win, pd, rh):
        op_match = self.opponents[week]
        op_match.win = win
        op_match.point_diff = pd
        op_match.rank_history = rh
        op_match.has_game_happened = True
    
    def get_rank_difference(self) -> str:
        """
        This is currently only called by Top 25 teams, hence the message below
        """
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
            if op.has_game_happened:
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
        print(f"{self.prev_rank if not show_cfp_points else self.full_rank} {self.name} ({self.total_wins}-{self.total_losses}) CFP: {self.cfb_points if show_cfp_points else '???'} PD: {self.point_diff} RR: ({rw}-{rl}) URR: ({urw}-{url}) Conf: {self.conference}-{self.division}")

        if self.opponents == []:
            return

        print("Schedule: ")
        week_counter = 1
        name_length = max([len(x.opponent.name) for x in self.opponents]) + 1
        for op_match in self.opponents:
            op = op_match.opponent

            if op_match.is_conference_title:
                print("\n---------------- Conference Championship -----------------------")
                week_counter = CFBGlobalSettings.NumOfRegWeeks.value + 1
            if op_match.is_playoff_octo:
                print("\n------------------ Playoff Octo Round --------------------------")
                week_counter = CFBGlobalSettings.NumOfRegWeeks.value + 2
            if op_match.is_playoff_quarter:
                print("\n---------------- Playoff Quarter Round -------------------------")
                week_counter = CFBGlobalSettings.NumOfRegWeeks.value + 3
            if op_match.is_playoff_semi:
                print("\n----------------- Playoff Semi Round ---------------------------")
                week_counter = CFBGlobalSettings.NumOfRegWeeks.value + 4
            if op_match.is_playoff_final:
                print("\n---------------- Playoff Championship --------------------------")
                week_counter = CFBGlobalSettings.NumOfRegWeeks.value + 5

            if op_match.has_game_happened:
                print(f" {week_counter:>3}) {'W' if op_match.win else 'L'} ({op.rank:>2}) {op.name:<{name_length}} {f'({op.total_wins}-{op.total_losses})':<6} Conf: {op.conference:^3}  PD: {op_match.point_diff:>3}  RH: ( {op_match.rank_history[0]:>2} - {op_match.rank_history[1]:>2} ) CFB_P: {(op_match.cfb_points if show_cfp_points else '???'):>3}")
            else:
                print(f" {week_counter:>3}) ? ({op.rank:>2}) {op.name:<{name_length}} {f'({op.total_wins}-{op.total_losses})':<6} Conf: {op.conference:^3}  PD:  ??  RH: {'???':^11} CFB_P: {(op_match.cfb_points if show_cfp_points else '???'):>3}")
            
            week_counter += 1
    
    def calc_cfb_points(self):
        points = 0

        for op_match in self.opponents:
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

        self.cfb_points = points + 100
        return points

    def get_all_cur_reg_season_opp(self):
        return [x.opponent.name for x in self.opponents]
