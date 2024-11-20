from cfb import *

def main():
    ncaa = cfb()
    ncaa.get_scores()
    ncaa.make_top25(0)
    input("")
    ncaa.print_standings()

    for week in range(12):
        ncaa.play_week(print_stuff=True)
        input("")
        ncaa.make_top25(week+1)
        input("")
        ncaa.print_standings()
        input("")
    ncaa.print_full_rankings()
    print("")
    input("")
    ncaa.conference_championships()
    input("")

    # ncaa.playoffs_four()
    ncaa.playoffs_twelve()
    input("")
    ncaa.print_full_rankings()
   


if __name__ == "__main__":
    main()
