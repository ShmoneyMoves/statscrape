from player.career.player_career import get_career_stats, get_career_playoff_stats
from player.season.player_season import get_season_stats, get_season_stats_against_team
from player.player_other import get_first_season, get_last_season
from team.team import get_team_schedule, get_boxscore_links
from season.season import load_season_stats


def get_player_career_stats(player):
    return get_career_stats(player)

def get_player_career_playoff_stats(player):
    return get_career_playoff_stats(player)

def get_player_season_stats(player, season):
    return get_season_stats(player, season)

def get_player_season_stats_against_team(player, season, team):
    return get_season_stats_against_team(player, season, team)

def get_player_first_season(player):
    return get_first_season(player)

def get_player_last_season(player):
    return get_last_season(player)

def get_team_schedule_by_year(team, year):
    return get_team_schedule(team, year)

def get_team_boxscore_links(team, year):
    return get_boxscore_links(team, year)

def ceate_season_stats_table(year, table):
    return load_season_stats(year, table)

def main():
    print("main")
if __name__ == '__main__':
    main()
