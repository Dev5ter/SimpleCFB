from cfb import Team

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