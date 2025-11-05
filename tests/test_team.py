import pytest

from cfb import Team, OpponentMatch

def test_team_constructor():
    TEAM_NAME = "Tennessee"
    vols = Team(TEAM_NAME)

    assert vols.name == TEAM_NAME
    assert vols.reg_wins == 0
    assert vols.total_wins == 0
    assert vols.reg_losses == 0
    assert vols.total_losses == 0
    assert vols.point_diff == 0


def test_team_handle_win():
    TEAM_NAME = "Tennessee"
    POINTS = 23
    vols = Team(TEAM_NAME)

    vols.handle_win(23)

    assert vols.reg_wins == 1
    assert vols.total_wins == 1
    assert vols.reg_losses == 0
    assert vols.total_losses == 0
    assert vols.point_diff == POINTS



def test_team_handle_loss():
    TEAM_NAME = "Tennessee"
    POINTS = 23
    vols = Team(TEAM_NAME)

    vols.handle_loss(POINTS)

    assert vols.reg_wins == 0
    assert vols.total_wins == 0
    assert vols.reg_losses == 1
    assert vols.total_losses == 1
    assert vols.point_diff == -POINTS


@pytest.mark.parametrize("rank, prev_rank, correct_diff", [
    ("UR", "UR", "THIS SHOULD NOT HAPPEN"),
    ("UR", "23", "THIS SHOULD NOT HAPPEN"),
    ("5", "5", "~ "),
    ("24", "UR", "UR"),
    ("6", "19", "+13"),
    ("13", "4", "-9")
])
def test_team_get_rank_difference(rank, prev_rank, correct_diff):
    vols = Team("Tennessee")
    vols.prev_rank = prev_rank
    vols.rank = rank

    assert vols.get_rank_difference() == correct_diff


def test_team_get_ranked_and_unranked_records():
    vols = Team("Tennessee")
    vols.rank = '3'
    clemson = Team("Clemson")
    unc = Team("North Carolina")
    unc.rank = '12'

    vols_p2 = OpponentMatch(unc, True, 21)
    vols_p = OpponentMatch(clemson, True, 14)
    clem_p = OpponentMatch(vols, False, -14)

    vols.opponents.append(vols_p)
    vols.opponents.append(vols_p2)
    clemson.opponents.append(clem_p)

    assert vols.get_ranked_and_unranked_records() == (1, 0, 1, 0)
    assert clemson.get_ranked_and_unranked_records() == (0, 1, 0, 0)