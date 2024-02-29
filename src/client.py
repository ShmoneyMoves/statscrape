from player.career.player_career import get_career_stats, get_career_playoff_stats
from player.season.player_season import get_season_stats, get_season_stats_against_team, get_season_stat_average, get_season_stat_total
from player.player_other import get_first_season, get_last_season, calculate_ortg, scrape_ortg
from team.team import get_team_schedule, get_boxscore_links, get_injury_report, get_stat_totals, get_rtg_by_lineup, get_starting_lineup, get_four_factors_by_game, get_all_games_four_factors, get_games_on_date
from season.season import load_season_stats
from game_predictor import predict_manually, predict_game_v1, predict_game_v2, relative_prediction

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
    return get_all_games_four_factors(team, year)

def get_games_by_date(date):
    return get_games_on_date(date)

def create_season_stats_table(year, table):
    return load_season_stats(year, table)

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

def get_relative_prediction():
    return relative_prediction()

def main():
    # response = predict_game_v1("Dallas Mavericks", "Toronto Raptors")
    # print(response)
    # with open("2024_Celtics_FourFactors.txt", "r") as file:
    #     ortg = 0
    #     drtg = 0
    #     pace_total = 0
    #     count = 0
    #     for line_number, line  in enumerate(file):
    #         if line_number < 2:
    #             continue
    #         else:
    #             count = count + 1
    #             pace_total = pace_total + (float(line.split(",")[1])/100)
    #             adjusted_pace = 1
    #             if line.split(',')[0] == "BOS":
    #                 ortg = (ortg + (float(line.split(',')[6]))*adjusted_pace)
    #                 drtg = (drtg + (float(line.split(',')[13]))*adjusted_pace)
    #             else:
    #                 ortg = ortg + (float(line.split(',')[13]))*adjusted_pace
    #                 drtg = drtg + (float(line.split(',')[6]))*adjusted_pace

    #     print(count)
    #     print(pace_total/count)
    #     print(round((ortg/count), 1), round((drtg/count), 1))
    # exit(0)

    teamfga = 5205
    teamfg = 2521
    teamfta = 1260
    teamorb = 612
    teamdrb = 2118
    teamtov = 725
    oppdrb = 1875
    oppfga = 5359
    oppfg = 2399
    oppfta = 1089
    opporb = 653
    opptov = 683

    #           0.5 * ((Tm FGA + 0.4 * Tm FTA – 1.07 * (Tm ORB / (Tm ORB + Opp DRB)) * (Tm FGA – Tm FG) + Tm TOV) + (Opp FGA + 0.4 * Opp FTA – 1.07 * (Opp ORB / (Opp ORB + Tm DRB)) * (Opp FGA – Opp FG) + Opp TOV)
    possesions = 0.5 *((teamfga + 0.4 * teamfta - 1.07 * (teamorb/(teamorb + oppdrb)) * (teamfga - teamfg) + teamtov) + (oppfga + 0.4 * oppfta - 1.07 * (opporb/(opporb + teamdrb)) * (oppfga - oppfg) + opptov))
    print(possesions/58)

    team_one_pts = 6999
    team_two_pts = 6394

    print(f"Team 1 ORtg: {round((team_one_pts/possesions)*100, 1)}")

    print(f"Team 1 ORtg: {round((team_two_pts/possesions)*100, 1)}")

    # 97.9 posessions     points scored
    # 48 minutes           100 possesions

    #       pace = possesions/game 
    #       120.7pts/game
    #       97.9 possesions/game
    #       ortg = pts/100 possesions
    #
    #       100/97.9 = 1.0288
    #       120.7 * 1.0288 = 123.289


    # response = relative_prediction()
    # print(response)

    # # FGA - ORB + TO + (0.44 * FTA)
    # offensive_possesions = 102 - 15 + 17 + 0.475*7
    # offensive_points = 126
    # ortg = round(((offensive_points/offensive_possesions)*100), 1)

    # defensive_possesions = 87 - 11 + 15 + 0.475*26
    # defensive_points = 107
    # drtg = round(((defensive_points/defensive_possesions)*100), 1)
    # print(ortg, drtg)
    
if __name__ == '__main__':
    main()


