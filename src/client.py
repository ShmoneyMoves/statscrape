import csv
from player.career.player_career import get_career_stats, get_career_playoff_stats
from player.season.player_season import get_season_stats, get_season_stats_against_team, get_season_stat_average, get_season_stat_total
from player.player_other import get_first_season, get_last_season, calculate_ortg, scrape_ortg
from team.team import get_team_schedule, get_boxscore_links, get_injury_report, get_stat_totals, get_rtg_by_lineup, get_starting_lineup, get_four_factors_by_game, get_all_games_four_factors, get_games_on_date, calculate_team_ortg
from season.season import load_season_stats, fetch_season_boxscores, calculate_league_average, calculate_team_ratings_progressively, calculate_daily_team_ratings, get_team_boxscore_on_date
from game_predictor import predict_manually, predict_game_v1, predict_game_v2, relative_prediction, predict_season

def get_team_stat_totals(team, year):
    return get_stat_totals(team, year)

def get_player_scrape_ortg(player, year):
    return scrape_ortg(player, year)

def get_player_offensive_rating(player, team, year):
    return calculate_ortg(player, team, year)

def get_player_season_stat_total(player, season, stat):
    return get_season_stat_total(player, season, stat)

def get_player_season_stat_average(player, season, stat):
    return get_season_stat_average(player, season, stat)

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

def get_team_injury_report(team, year):
    return get_injury_report(team, year)

def get_team_lineup_ortg(team, lname1, lname2, lname3, lname4, lname5):
    response = get_rtg_by_lineup(team, lname1, lname2, lname3, lname4, lname5)
    print(response)
    return [response[0][4], response[0][5], response[0][16]]

def get_team_starting_lineup(team):
    return get_starting_lineup(team)

def get_team_four_factors_by_game(suffix):
    return get_four_factors_by_game(suffix)

def get_team_all_games_four_factors(team, year):
    return get_all_games_four_factors(team, year),

def get_team_box_score_on_date(box_score_link, team, date):
    return get_team_boxscore_on_date(box_score_link, team, date)

def get_games_by_date(date):
    return get_games_on_date(date)

def create_season_stats_table(year, table):
    return load_season_stats(year, table)

def get_season_boxscores(year):
    return fetch_season_boxscores(year)

def get_season_league_averages(season):
    return calculate_league_average(season)

def get_season_team_ratings_progressively(box_score_file, team_abbreivation):
    return calculate_team_ratings_progressively(box_score_file, team_abbreivation)

def get_daily_team_ratings(box_score_file, team_abbreviation):
    return calculate_daily_team_ratings(box_score_file, team_abbreviation)

def predict_manual(team_one, team_one_ortg, team_one_drtg, team_one_pace, team_two, team_two_ortg, team_two_drtg, team_two_pace, league_pace, league_ortg):
    return predict_manually(team_one, team_one_ortg, team_one_drtg, team_one_pace, team_two, team_two_ortg, team_two_drtg, team_two_pace, league_pace, league_ortg)

def predict_v1(away_team, home_team):
    return predict_game_v1(away_team, home_team)

def predict_v2(away_team, home_team):
    away_lineup = get_team_starting_lineup(away_team)
    print(f"Away Starters: {away_lineup}")
    away_rtgs = get_team_lineup_ortg(away_team, away_lineup[0].split(' ')[1], away_lineup[1].split(' ')[1], away_lineup[2].split(' ')[1], away_lineup[3].split(' ')[1], away_lineup[4].split(' ')[1])
    away_ortg = away_rtgs[0]
    away_drtg = away_rtgs[1]
    away_pace = away_rtgs[2]

    home_lineup = get_team_starting_lineup(home_team)
    print(f"Home Starts: {home_lineup}")
    home_rtgs = get_team_lineup_ortg(home_team, home_lineup[0].split(' ')[1], home_lineup[1].split(' ')[1], home_lineup[2].split(' ')[1], home_lineup[3].split(' ')[1], home_lineup[4].split(' ')[1])
    home_ortg = home_rtgs[0]
    home_drtg = home_rtgs[1]
    home_pace = home_rtgs[2]

    return predict_game_v2(away_team, away_ortg, away_drtg, away_pace, home_team, home_ortg, home_drtg, home_pace)

def predict_games_on(date):
    matchups = get_games_by_date(date)
    for game in matchups:
        response = predict_v1(game[0], game[1])
        print(response)

def predict_year(season):
    return predict_season(season)

def get_relative_prediction():
    return relative_prediction()

def get_team_ortg(team, year):
    return calculate_team_ortg(team, year)

def predict_season_from_scratch(year):
    response = get_season_boxscores(year)

    game_csv = ""
    for game in response:
        for index, data_point in enumerate(game):
            if index == 0:
                continue
            else:
                game_csv = game_csv + data_point + ","
        with open(f"season/csv/{str(int(year) - 1)}-{year[2:]}/box_score.txt", "a") as file:
            file.write(game_csv + "\n")
        game_csv = ""

    # Load the team stats from each game

    teams = [
        "ATL", "BOS", "BKN", "CHA", "CHI", "CLE", "DAL", "DEN", "DET", "GSW", 
        "HOU", "IND", "LAC", "LAL", "MEM", "MIA", "MIL", "MIN", "NOP", "NYK", 
        "OKC", "ORL", "PHI", "PHX", "POR", "SAC", "SAS", "TOR", "UTA", "WAS"
    ]
    for team in teams:
        file = f"season/csv/{str(int(year) - 1)}-{year[2:]}/teams/{team}.txt"
        response = get_daily_team_ratings(f"season/csv/{str(int(year) - 1)}-{year[2:]}/box_score.txt", team)
        with open(file, "w") as file:
            for entry in response:
                entry = [str(i) for i in entry]
                csv_row = ','.join(entry)
                file.write(csv_row + "\n")
        print(len(response))

    # Calculate the season average per day

    get_season_league_averages(f"{str(int(year) - 1)}-{year[2:]}")

    # Predict season

    response = predict_year(f"{str(int(year) - 1)}-{year[2:]}")

    with open(f"season/csv/{str(int(year) - 1)}-{year[2:]}/prediction.txt", "w") as file:
        for line in response:
            file.write("%s\n" % line)

    for entry in response:
        print(entry)
def main():

    response = predict_v1("Phoenix Suns", "Boston Celtics")
    print(response)
    
if __name__ == '__main__':
    main()
