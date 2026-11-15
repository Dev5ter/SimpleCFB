from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.team import Team


class Conference:
    def __init__(self, n, t1, t2, dn1, dn2):
        self.name: str = n
        self.div1: list[Team] = t1
        self.div2: list[Team] = t2
        self.div1_name: str = dn1
        self.div2_name: str = dn2

        for t in t1:
            t: Team
            t.conference = n
            t.division = dn1

        for t in t2:
            t: Team
            t.conference = n
            t.division = dn2
