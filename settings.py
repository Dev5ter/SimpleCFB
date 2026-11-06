from enum import Enum


class CFBGlobalSettings(Enum):
    NumOfConferences: int = 6
    TeamsPerDivision: int = 7
    NumOfTeamsRanked: int = 25
    NumOfRegWeeks: int = 12
    WeekCFBStartsRanking: int = 7

    isConferenceOppOn: bool = True
    isTwelveTeamPlayoff: bool = True

    NonConfWeeksHaveUniqueConf: bool = True

    AllConfChampInPlayoff: bool = True
    NumOfConfChampInPlayoff: int = 6