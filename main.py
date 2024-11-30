from cfb import *

def main():
    ncaa = CFB()
    ncaa.get_scores()
    ncaa.make_top25(0)
    input("")
    ncaa.print_standings()

    for week in range(12):
        ncaa.menu_processor()
        ncaa.play_week(print_stuff=True)
        input("")
        ncaa.make_top25(week+1)
        input("")
        ncaa.print_standings()
        input("")
    ncaa.menu_processor()
    ncaa.conference_championships()
    input("")

    # ncaa.playoffs_four()
    ncaa.playoffs_twelve()
    input("")
    ncaa.print_full_rankings()
   


if __name__ == "__main__":
    main()
