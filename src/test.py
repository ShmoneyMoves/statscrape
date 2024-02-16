from player.career.player_career import get_career_stats, get_career_playoff_stats, get_career_stats_against_team
from player.season.player_season import get_season_stats, get_season_stats_against_team
from player.player_other import get_first_season, get_last_season
from proxy import get_proxy

def main():
    response = get_career_stats_against_team("Jayson Tatum", "LAL")
    if response[0] != "ERROR:":
        for entry in response:
            print(entry[:18])
            
    else:
        print("ERROR:", response[1])
if __name__ == '__main__':
    main()
