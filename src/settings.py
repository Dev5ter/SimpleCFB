from enum import Enum


class CFBGlobalSettings(Enum):
    # These Aren't Dynamic. TPD can't be changed as of V8
    NumOfConferences: int = 6
    TeamsPerDivision: int = 7

    # General League Settings
    NumOfTeamsRanked: int = 25
    NumOfRegWeeks: int = 12
    WeekCFBStartsRanking: int = 7
    UseRandomRanker: bool = False

    # Conference Match-up Settings
    isConferenceOppOn: bool = True
    NonConfWeeksHaveUniqueConf: bool = True

    # Playoff Settings
    isTwelveTeamPlayoff: bool = True
    AllConfChampInPlayoff: bool = True
    NumOfConfChampInPlayoff: int = 6
