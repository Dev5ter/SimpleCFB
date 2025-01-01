from cfb import *

def main():
    ncaa = CFB()
    ncaa.make_ap_top25()
    ncaa.menu_processor()
    ncaa.print_top25()
    input("")
    ncaa.print_standings()
    ncaa.menu_processor()

    while ncaa.week <= 12:
        ncaa.play_week(print_stuff=True)
        input("")
        if ncaa.week <= 6:
            ncaa.make_ap_top25()
        else:
            ncaa.make_cfb_top_25()
        ncaa.print_top25()
        input("")
        ncaa.print_standings()
        input("")
        ncaa.week += 1
        ncaa.menu_processor()

    ncaa.conference_championships()
    ncaa.menu_processor(allow_save_load=False)
    
    ncaa.make_cfb_top_25()
    ncaa.cfp_teams_reveal()
    ncaa.print_top25()
    ncaa.menu_processor(allow_save_load=False)
    input("")

    # ncaa.playoffs_four()
    ncaa.playoffs_twelve()
    input("")
    ncaa.menu_processor(allow_save_load=False)
   


if __name__ == "__main__":
    main()
