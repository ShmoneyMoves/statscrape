from bs4 import BeautifulSoup
import requests
from season.season import get_team_boxscore_on_date 

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
        return offensive_rating + offensive_rating * 0.021523
    else:
        return offensive_rating - offensive_rating * 0.000855
    
def adjust_defensive_rating(defensive_rating, is_home):
    if is_home:
        return defensive_rating - defensive_rating * 0.021523
    else:
        return defensive_rating + defensive_rating * 0.000855
    

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

def get_team_rating_on_day(season, team, date):
    with open(f"season/csv/{season}/teams/{team}.txt", "r") as file:
        for line in file:
            data = line.split(',')
            game_date = data[0]
            if date == game_date:
                #        ortg     drtg     pace  home_factor  away_factor
                return [data[2], data[3], data[4], data[5], data[7]]

def get_league_average_on_day(season, date):
    with open(f"season/csv/{season}/league_average.txt", "r") as file:
        for line in file:
            data = line.split(',')
            game_date = data[0]
            if date == game_date:
                return [data[1], data[2], data[3]]

def predict_season(season):
    #       corrent, incorrect
    moneyline_talley = [0, 0]
    #                                   1  2  3  4  5  6  7  8  9  10 
    outright_by_differential_correct = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    outright_by_differential_incorrect = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    spread_talley = [0, 0]
    seen_matchups = []
    with open(f"season/csv/{season}/box_score.txt") as file:
        for i, game in enumerate(file):
            if i == 0:
                continue
            data = game.split(',')
            date = data[1]

            matchup = data[0].split(' ')
            home_team = ""
            away_team = ""
            if matchup[1] == "vs.":
                home_team = matchup[0]
                away_team = matchup[2]
            else:       
                home_team = matchup[2]
                away_team = matchup[0]
            matchup = home_team + "," + away_team + "," + date

            if matchup not in seen_matchups:
                seen_matchups.append(matchup)
                home_box_score = get_team_boxscore_on_date(f"season/csv/{season}/box_score.txt", home_team, date)
                away_box_score = get_team_boxscore_on_date(f"season/csv/{season}/box_score.txt", away_team, date)
                home_score = float(home_box_score[6])
                away_score = float(away_box_score[6])

                winner = "tie"
                spread = home_score - away_score
                if home_score > away_score:
                    winner = home_team
                else:
                    winner = away_team
                home_ratings = get_team_rating_on_day(season, home_team, date)
                away_ratings = get_team_rating_on_day(season, away_team, date)
                average_ratings = get_league_average_on_day(season, date)

                prediction = predict_manually(home_team, float(home_ratings[0]), float(home_ratings[1]), float(home_ratings[2]), away_team, float(away_ratings[0]), float(away_ratings[1]), float(away_ratings[2]), float(average_ratings[2]), float(average_ratings[0]), float(home_ratings[3]), float(away_ratings[4]))

                predicted_spread = abs(prediction[0] - prediction[1])

                predicted_winner = "tie"
                if prediction[0] > prediction[1]:
                    predicted_winner = home_team
                else:
                    predicted_winner = away_team

                if round(predicted_spread) == 1 or round(predicted_spread) == 0:
                    if predicted_winner == winner:
                        outright_by_differential_correct[0] = outright_by_differential_correct[0] + 1
                    else:
                        outright_by_differential_incorrect[0] = outright_by_differential_incorrect[0] + 1
                elif round(predicted_spread) == 2:
                    if predicted_winner == winner:
                        outright_by_differential_correct[1] = outright_by_differential_correct[1] + 1
                    else:
                        outright_by_differential_incorrect[1] = outright_by_differential_incorrect[1] + 1
                elif round(predicted_spread) == 3:
                    if predicted_winner == winner:
                        outright_by_differential_correct[2] = outright_by_differential_correct[2] + 1
                    else:
                        outright_by_differential_incorrect[2] = outright_by_differential_incorrect[2] + 1
                elif round(predicted_spread) == 4:
                    if predicted_winner == winner:
                        outright_by_differential_correct[3] = outright_by_differential_correct[3] + 1
                    else:
                        outright_by_differential_incorrect[3] = outright_by_differential_incorrect[3] + 1
                elif round(predicted_spread) == 5:
                    if predicted_winner == winner:
                        outright_by_differential_correct[4] = outright_by_differential_correct[4] + 1
                    else:
                        outright_by_differential_incorrect[4] = outright_by_differential_incorrect[4] + 1
                elif round(predicted_spread) == 6:
                    if predicted_winner == winner:
                        outright_by_differential_correct[5] = outright_by_differential_correct[5] + 1
                    else:
                        outright_by_differential_incorrect[5] = outright_by_differential_incorrect[5] + 1
                elif round(predicted_spread) == 7:
                    if predicted_winner == winner:
                        outright_by_differential_correct[6] = outright_by_differential_correct[6] + 1
                    else:
                        outright_by_differential_incorrect[6] = outright_by_differential_incorrect[6] + 1
                elif round(predicted_spread) == 8:
                    if predicted_winner == winner:
                        outright_by_differential_correct[7] = outright_by_differential_correct[7] + 1
                    else:
                        outright_by_differential_incorrect[7] = outright_by_differential_incorrect[7] + 1
                elif round(predicted_spread) == 9:
                    if predicted_winner == winner:
                        outright_by_differential_correct[8] = outright_by_differential_correct[8] + 1
                    else:
                        outright_by_differential_incorrect[8] = outright_by_differential_incorrect[8] + 1
                elif round(predicted_spread) >= 10:
                    if predicted_winner == winner:
                        outright_by_differential_correct[9] = outright_by_differential_correct[9] + 1
                    else:
                        outright_by_differential_incorrect[9] = outright_by_differential_incorrect[9] + 1
                else:
                    print(f"SPREAD={predicted_spread}")
                    
                if predicted_spread <= spread:
                    spread_talley[0] = spread_talley[0] + 1
                else:
                    spread_talley[1] = spread_talley[1] + 1

                if predicted_winner == winner:
                    moneyline_talley[0] = moneyline_talley[0] + 1
                else:
                    moneyline_talley[1] = moneyline_talley[1] + 1

        differential_total = []
        for i in range(0, 10):
            differential_total.append(outright_by_differential_correct[i] + outright_by_differential_incorrect[i])

        outright_correct_as_percentage = [0] * 10
        outright_incorrect_as_percentage = [0] * 10
        for i in range(0, 10):
            outright_correct_as_percentage[i] = str(round((outright_by_differential_correct[i] / differential_total[i])*100, 1)) + "%"
            outright_incorrect_as_percentage[i] = str(round((outright_by_differential_incorrect[i] / differential_total[i])*100, 1)) + "%"
            
    response = [
        f"Correct Moneyline: {moneyline_talley[0]}", 
        f"Correct Moneyline Percentage: {round((moneyline_talley[0]/(moneyline_talley[0] + moneyline_talley[1]))*100, 1)}%", 
        f"Incorrect Moneyline: {moneyline_talley[1]}", 
        f"Incorrect Percentage Moneyline: {round((moneyline_talley[1]/(moneyline_talley[0] + moneyline_talley[1]))*100, 1)}%",
        f"Correct Spread: {spread_talley[0]}", 
        f"Correct Spread Percentage: {round((spread_talley[0]/(spread_talley[0] + spread_talley[1]))*100, 1)}%", 
        f"Incorrect Spread: {spread_talley[1]}", 
        f"Incorrect Percentage Spread: {round((spread_talley[1]/(spread_talley[0] + spread_talley[1]))*100, 1)}%\n",
        f"Correct by Differential: {outright_by_differential_correct}",
        f"Correct by Differential Percentage: {outright_correct_as_percentage}\n",
        f"Incorrect by Differential: {outright_by_differential_incorrect}",
        f"Incorrect by Differential Percentage: {outright_incorrect_as_percentage}"
    ]
    return response

def predict_final_score(team_aoppp, predicted_pace):
    # 1. Return (team_aopp * predicted_pace) / 100
    print("final score")

# Home team is team one
# Away team is team two
def predict_manually(team_one, team_one_ortg, team_one_drtg, team_one_pace, team_two, team_two_ortg, team_two_drtg, team_two_pace, league_pace, league_ortg, home_factor, away_factor):
    team_one_adrtg = away_factor * team_one_drtg
    team_one_aortg = home_factor * team_one_ortg
    team_two_adrtg = home_factor * team_two_drtg
    team_two_aortg = away_factor * team_two_ortg

    game_pace = (team_one_pace * team_two_pace) / league_pace

    team_one_ppp = (team_one_aortg * team_two_adrtg) / league_ortg
    team_two_ppp = (team_two_aortg * team_one_adrtg) / league_ortg

    team_one_final_score = (team_one_ppp * game_pace) / 100
    team_two_final_score = (team_two_ppp * game_pace) / 100

    return [team_one_final_score, team_two_final_score]

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
    print_statistics = False

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




















        # 110 = A*injuries() + B*travel() + C*previous_performances() + D*home_court() + E*fatigue() + F*refs() + G*time_of_day() + predict_score()
        # 115


        # (percentage of minutes played) * (usage rate) * (ORtg per 100 possessions) = ORtg contribution by player
        # Jayson Tatum 
        # ( 35.7 / 48 ) * ( 0.30 ) = 0.223%
        # Jaylen Brown
        # ( 33.3 / 48 ) * ( 0.281 ) = 0.195%
        # Jrue Holiday
        # ( 33.1 / 48 ) * ( 0.165 ) = 0.114%
        # Derrick White
        # ( 32.1 / 48 ) * ( 0.188 ) = 0.126%
        # Kristaps Porzingis
        # ( 29.7 / 48 ) * ( 0.248 ) = 0.153%

        # 0.811

        # Al Horford
        # ( 26.7/48 ) * ( 0.114 ) = 0.063
        # Payton Pritchard
        # ( 20.4/48 ) * ( 0.161 ) = 0.068
        # Sam Hauser 
        # ( 21 / 48 ) * ( 0.138 ) = 0.06%