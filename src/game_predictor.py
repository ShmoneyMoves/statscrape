from bs4 import BeautifulSoup
import requests


def get_offensive_defenseive_pace(team):
    url ="https://www.basketball-reference.com/leagues/NBA_2024.html#all_per_game_team-opponent"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
        
    stats_table = soup.find('table', {'id': 'advanced-team'})
    result = []
    if stats_table:
            rows = stats_table.findAll('tr')[1:]
            results = [[td.getText() for td in rows[i].findAll('td')]
                            for i in range(len(rows))]
            for entry in results[1:]:
                if len(entry) >= 11 and entry[0] == team:
                    result.append(entry[9])
                    result.append(entry[10])
                    result.append(entry[12])
            return result

def adjust_offensive_rating(offensive_rating, is_home):
    if is_home:
        return offensive_rating + offensive_rating * 0.014
    else:
        return offensive_rating - offensive_rating *0.014
    
def adjust_defensive_rating(defensive_rating, is_home):
    if is_home:
        return defensive_rating - defensive_rating * 0.014
    else:
        return defensive_rating + defensive_rating *0.014
    

def get_league_offensive_defenseive_pace():
    url ="https://www.basketball-reference.com/leagues/NBA_2024.html#all_per_game_team-opponent"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
        
    stats_table = soup.find('table', {'id': 'advanced-team'})
    result = []
    if stats_table:
        if stats_table:
            rows = stats_table.findAll('tr')[1:]
            results = [[td.getText() for td in rows[i].findAll('td')]
                            for i in range(len(rows))]
            for entry in results:
                if len(entry) >= 11 and entry[0] == "League Average":
                    result.append(entry[9])
                    result.append(entry[10])
                    result.append(entry[12])
            return result
    return result


def predict_final_score(team_aoppp, predicted_pace):
    # 1. Return (team_aopp * predicted_pace) / 100
    print("final score")

# Home team is team one
# Away team is team two
def predict_manually(team_one, team_one_ortg, team_one_drtg, team_one_pace, team_two, team_two_ortg, team_two_drtg, team_two_pace, league_pace, league_ortg):
    team_one_adrtg = 1.014 * team_one_drtg
    team_one_aortg = 0.986 * team_one_ortg
    team_two_adrtg = 0.986 * team_two_drtg
    team_two_aortg = 1.014 * team_two_ortg

    game_pace = (team_one_pace * team_two_pace) / league_pace

    team_one_ppp = (team_one_aortg * team_two_adrtg) / league_ortg
    team_two_ppp = (team_two_aortg * team_one_adrtg) / league_ortg

    team_one_final_score = (team_one_ppp * game_pace) / 100
    team_two_final_score = (team_two_ppp * game_pace) / 100

    print("+---------- Final Score Prediction ----------+")
    print(team_one + ": " + str(round(team_one_final_score, 1)))
    print(team_two + ": " + str(round(team_two_final_score, 1)))
    print("+--------------------------------------------+")

def predict_game_v1(away_team, home_team):
    # predict_manually("Pelicans", 117.9, 113.6, 98.6, "Kings", 117.2, 116.7, 100.1, 99.1, 115.9)
    # exit(0)
    #  100 x Pts / 0.5 * ((Tm FGA + 0.4 * Tm FTA - 1.07 * (Tm ORB / (Tm ORB + Opp DRB)) * (Tm FGA - Tm FG) + Tm TOV) + (Opp FGA + 0.4 * Opp FTA - 1.07 * (Opp ORB / (Opp ORB + Tm DRB)) * (Opp FGA - Opp FG) + Opp TOV))
   
    team_one = away_team
    team_two = home_team
    print_statistics = True

    league_rtgs = get_league_offensive_defenseive_pace()
    if print_statistics:
        print("League Ratings:", league_rtgs)

    team_one_rtgs = get_offensive_defenseive_pace(team_one)
    team_one_offensive_rating = float(team_one_rtgs[0])
    team_one_defensive_rating = float(team_one_rtgs[1])
    if print_statistics:
        print("Team One's ORTG:", team_one_offensive_rating)
        print("Team One's DRTG:", team_one_defensive_rating)

    team_two_rtgs = get_offensive_defenseive_pace(team_two)
    team_two_offensive_rating = float(team_two_rtgs[0])
    team_two_defensive_rating = float(team_two_rtgs[1])
    if print_statistics:
        print("Team Two's ORTG:", team_two_offensive_rating)
        print("Team Two's DRTG:", team_two_defensive_rating)
        print()

    team_one_offensive_rating_adjusted = adjust_offensive_rating(team_one_offensive_rating, True if home_team == team_one else False)
    team_one_defensive_rating_adjusted = adjust_defensive_rating(team_one_defensive_rating, True if home_team == team_one else False)
    if print_statistics:
        print("T1 AORtg:", team_one_offensive_rating_adjusted)
        print("T1 ADRtg:", team_one_defensive_rating_adjusted)

    team_two_offensive_rating_adjusted = adjust_offensive_rating(team_two_offensive_rating, True if home_team == team_two else False)
    team_two_defensive_rating_adjusted = adjust_defensive_rating(team_two_defensive_rating, True if home_team == team_two else False)
    if print_statistics:
        print("T2 AORtg:", team_two_offensive_rating_adjusted)
        print("T2 ADRtg:", team_two_defensive_rating_adjusted)
        print()

    team_one_pace = float(team_one_rtgs[2])
    team_two_pace = float(team_two_rtgs[2])
    league_pace = float(league_rtgs[2])
    adjusted_game_pace = (team_one_pace * team_two_pace) / league_pace
    if print_statistics:
        print("T1 Pace:", team_one_pace)
        print("T2 Pace:", team_two_pace)
        print("Game Pace:", adjusted_game_pace)
        print()

    team_one_adjusted_ppp = (team_one_offensive_rating_adjusted * team_two_defensive_rating_adjusted) / float(league_rtgs[0])
    team_two_adjusted_ppp = (team_two_offensive_rating_adjusted * team_one_defensive_rating_adjusted) / float(league_rtgs[0])
    if print_statistics:
        print("T1 Adjusted PPP:", team_one_adjusted_ppp)
        print("T2 Adjusted PPP:", team_two_adjusted_ppp)
        print()

    team_one_final_score = (team_one_adjusted_ppp * adjusted_game_pace) / 100
    team_two_final_score = (team_two_adjusted_ppp * adjusted_game_pace) / 100

    return [f"{team_one}: {round(team_one_final_score, 1)}", f"{team_two}: {round(team_two_final_score, 1)}"]

    print("+---------- Final Score Prediction ----------+")
    print(team_one + ": " + str(round(team_one_final_score, 1)))
    print(team_two + ": " + str(round(team_two_final_score, 1)))
    print("+--------------------------------------------+")


def predict_game_v2(away_team, away_ortg, away_drtg, away_pace, home_team, home_ortg, home_drtg, home_pace):

    team_one = away_team
    team_two = home_team
    home_team = team_two
    print_statistics = False

    league_rtgs = get_league_offensive_defenseive_pace()
    if print_statistics:
        print("League Ratings:", league_rtgs)

    team_one_offensive_rating = float(away_ortg)
    team_one_defensive_rating = float(away_drtg)
    if print_statistics:
        print("Team One's ORTG:", team_one_offensive_rating)
        print("Team One's DRTG:", team_one_defensive_rating)

    team_two_offensive_rating = float(home_ortg)
    team_two_defensive_rating = float(home_drtg)
    if print_statistics:
        print("Team Two's ORTG:", team_two_offensive_rating)
        print("Team Two's DRTG:", team_two_defensive_rating)
        print()

    team_one_offensive_rating_adjusted = adjust_offensive_rating(team_one_offensive_rating, True if home_team == team_one else False)
    team_one_defensive_rating_adjusted = adjust_defensive_rating(team_one_defensive_rating, True if home_team == team_one else False)
    if print_statistics:
        print("T1 AORtg:", team_one_offensive_rating_adjusted)
        print("T1 ADRtg:", team_one_defensive_rating_adjusted)

    team_two_offensive_rating_adjusted = adjust_offensive_rating(team_two_offensive_rating, True if home_team == team_two else False)
    team_two_defensive_rating_adjusted = adjust_defensive_rating(team_two_defensive_rating, True if home_team == team_two else False)
    if print_statistics:
        print("T2 AORtg:", team_two_offensive_rating_adjusted)
        print("T2 ADRtg:", team_two_defensive_rating_adjusted)
        print()

    team_one_pace = float(away_pace)
    team_two_pace = float(home_pace)
    league_pace = float(league_rtgs[2])
    adjusted_game_pace = (team_one_pace * team_two_pace) / league_pace
    if print_statistics:
        print("T1 Pace:", team_one_pace)
        print("T2 Pace:", team_two_pace)
        print("Game Pace:", adjusted_game_pace)
        print()

    team_one_adjusted_ppp = (team_one_offensive_rating_adjusted * team_two_defensive_rating_adjusted) / float(league_rtgs[0])
    team_two_adjusted_ppp = (team_two_offensive_rating_adjusted * team_one_defensive_rating_adjusted) / float(league_rtgs[0])
    if print_statistics:
        print("T1 Adjusted PPP:", team_one_adjusted_ppp)
        print("T2 Adjusted PPP:", team_two_adjusted_ppp)
        print()

    team_one_final_score = (team_one_adjusted_ppp * adjusted_game_pace) / 100
    team_two_final_score = (team_two_adjusted_ppp * adjusted_game_pace) / 100

    return [f"{team_one}: {round(team_one_final_score, 1)}", f"{team_two}: {round(team_two_final_score, 1)}"]


def relative_prediction():
    # 1. Get pace and pts scored for game
    # 2. Normalize to 100 possessions
    # 3. Add all normalized ORTGs 
    # 4. Average ORTG over games played
    with open("2024_Celtics_FourFactors.txt") as file:
        game_count = 0
        total_pace = 0
        total_ortg = 0
        total_drtg = 0
        for line_number, line  in enumerate(file):
            if line_number < 2:
                continue
            else:
                game_count = game_count + 1
                if line.split(',')[0] == 'BOS':
                    ortg = float(line.split(',')[6])
                    drtg = float(line.split(',')[13])
                    pace = float(line.split(',')[1])
                else:
                    ortg = float(line.split(',')[13])
                    drtg = float(line.split(',')[6])
                    pace = float(line.split(',')[1])
                total_ortg = total_ortg + round((ortg * (100/pace)), 1)
                total_drtg = total_drtg + round((drtg  * (100/pace)), 1)
                total_pace = total_pace + pace
                print([ round((ortg * (100/pace)), 1), round((drtg  * (100/pace)), 1), pace])
        print('---------------------------')
        print(game_count)
        print(total_pace/game_count)
        print(f"ORtg: {round((total_ortg/game_count)*((total_pace/game_count)/100), 1)}")
        print(f"DRtg: {round((total_drtg/game_count)*((total_pace/game_count)/100), 1)}")