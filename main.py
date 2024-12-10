from cfb import *

def main():
    ncaa = CFB()
    ncaa.get_scores()
    ncaa.make_ap_top25(0)
    ncaa.print_top25()
    input("")
    ncaa.print_standings()

    for week in range(12):
        ncaa.menu_processor()
        ncaa.play_week(week+1, print_stuff=True)
        input("")
        if week <= 5:
            ncaa.make_ap_top25(week+1)
        else:
            ncaa.make_cfb_top_25()
        ncaa.print_top25()
        input("")
        ncaa.print_standings()
        input("")
    ncaa.menu_processor()

    ncaa.conference_championships()
    ncaa.make_cfb_top_25()
    ncaa.print_top25()
    ncaa.menu_processor()
    input("")

    # ncaa.playoffs_four()
    ncaa.playoffs_twelve()
    input("")
    ncaa.menu_processor()
   


if __name__ == "__main__":
    main()
