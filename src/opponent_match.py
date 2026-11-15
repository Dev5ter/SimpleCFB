from typing import Union, TYPE_CHECKING

if TYPE_CHECKING: 
    from src.team import Team


class OpponentMatch:
    def __init__(self, op, win=False, pd=0, rh=(0,0), cfb_p="AP", conference_champ_game=False, po_octo=False, po_quarter=False, po_semi=False, po_final=False, has_game_happened=False):
        self.opponent: Team = op
        self.win: bool = win
        self.point_diff: int = pd
        self.rank_history: tuple = rh
        self.cfb_points: Union[int, str] = cfb_p
        self.is_conference_title: bool = conference_champ_game
        self.is_playoff_octo: bool = po_octo
        self.is_playoff_quarter: bool = po_quarter
        self.is_playoff_semi: bool = po_semi
        self.is_playoff_final: bool = po_final
        self.has_game_happened: bool = has_game_happened
