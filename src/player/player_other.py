from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from validate_name import validate_name

def get_first_season(player):
    validation = validate_name(player)
    if validation[0]:

        url = "https://www.basketball-reference.com/players/" + validation[1][:1].lower() + "/" + validation[1].lower() + "01.html"
        response = requests.get(url)
    
        soup = BeautifulSoup(response.text, 'html.parser')
        stats_table = soup.find('table', {'id': 'per_game'})
        if stats_table:
            rows = stats_table.findAll(['tr'])
            first_row = [cell.getText() for cell in rows[1].find_all(['th', 'td'])]
            first_season = first_row[0][:2] + first_row[0][5:]
            return first_season
            
    else:
        return ["ERROR:", validation[1]]
    
def get_last_season(player):
    validation = validate_name(player)
    if validation[0]:
        url = "https://www.basketball-reference.com/players/" + validation[1][:1].lower() + "/" + validation[1].lower() + "01.html"
        response = requests.get(url)
    
        soup = BeautifulSoup(response.text, 'html.parser')
        
        stats_table = soup.find('table', {'id': 'per_game'})
        season_years = [1]
        if stats_table:
            rows = stats_table.findAll(['tr'])
            for row in rows:
                cells = row.find_all(['td', 'th'])
                season_cell = cells[0].getText().strip()
                if '-' in season_cell and len(cells) > 4:
                    season_years.append(int(season_cell[:2] + season_cell[5:]))
            return max(season_years)
    else:
        return ["ERROR:", validation[1]]
    
def scrape_ortg(player, year):
    validation = validate_name(player)
    if validation[0]:
        url = "https://www.basketball-reference.com/players/" + validation[1][:1].lower() + "/" + validation[1].lower() + "01.html" 
        pageCount = 1
        while True:
            if pageCount == 10:
                return "Player not found after 10 requests."
            response = requests.get(url)
            soup = BeautifulSoup(response.text, 'html.parser')
            soup = BeautifulSoup(response.text, 'html.parser')
            li_element = soup.find('li', class_='current index')
            if li_element:
                a_element = li_element.find('a')
                if a_element:
                    if player in a_element.text.strip():  
                        break
                    else:
                        pageCount = pageCount + 1
                        url = "https://www.basketball-reference.com/players/" + validation[1][:1].lower() + "/" + validation[1].lower() + f"0{pageCount}.html" 
                else:
                    return "Player not found"
            else:
                return "Player not found"
        
        stats_table = soup.find('table', {'id': 'totals'})
        
        stats = []
        if stats_table:
            rows = stats_table.findAll('tr')[1:]
            results = [[td.getText() for td in rows[i].findAll(['td', 'th'])]
                            for i in range(len(rows))]
            for entry in results:
                if (str(year - 1) + "-" + str(year)[2:]) == entry[0]:
                    stats.append(int(entry[29]))
                    stats.append(int(entry[24]))
                    stats.append(int(entry[21]))
                    stats.append(int(entry[9]))
                    stats.append(int(entry[8]))
                    stats.append(int(entry[19]))
                    stats.append(int(entry[18]))
                    stats.append(int(entry[7]))
                    stats.append(int(entry[27]))
                    stats.append(int(entry[11])) 
                    break
            return stats
    else:
        return ["ERROR:", validation[1]]

def get_team_stat_totals(team, year):
    team_validation = True
    if team_validation:
        url = "https://www.basketball-reference.com/teams/" + team.upper() + "/" + str(year) +  ".html"
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Run in headless mode
        chrome_options.add_argument('--no-sandbox')  # Bypass OS security model
        chrome_options.add_argument('--disable-dev-shm-usage')  # Avoid /dev/shm usage
        chrome_options.add_argument("--log-level=3")

        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        content = driver.page_source.encode('utf-8').strip()

        soup = BeautifulSoup(content, 'html.parser')
        
        stats_table = soup.find('table', {'id': 'team_and_opponent'})
        print(url)
        stats = []
        if stats_table:
            rows = stats_table.findAll('tr')[1:]
            results = [[td.getText() for td in rows[i].findAll(['td', 'th'])]
                            for i in range(len(rows))]
            for entry in results:
                if entry[0] == 'Team':
                    stats.append(int(entry[23]))
                    stats.append(int(entry[18]))
                    stats.append(int(entry[4]))
                    stats.append(int(entry[3]))
                    stats.append(int(entry[13]))
                    stats.append(int(entry[12]))
                    stats.append(int(entry[15]))
                    stats.append(int(entry[21]))
                    stats.append(int(entry[2]))
                    stats.append(int(entry[6]))
                elif entry[0] == 'Opponent':
                    stats.append(int(entry[17]))
                    stats.append(int(entry[15]))
                    break
            return stats
    else:
        return "ERROR: Invalid input"

def calculate_ortg(player, team, year):
    print(player, team, year)
    player_stats = scrape_ortg(player, year)
    points = player_stats[0]
    assists = player_stats[1]
    offensive_rebounds = player_stats[2]
    field_goals_attempted = player_stats[3]
    field_goals_made = player_stats[4]
    free_throws_attempted = player_stats[5]
    free_throws_made = player_stats[6]
    minutes_played = player_stats[7]
    turnovers = player_stats[8]
    three_pointers_made = player_stats[9]

    # print([points, assists, offensive_rebounds, field_goals_attempted, field_goals_made, free_throws_attempted, free_throws_made, minutes_played, turnovers, three_pointers_made])

    team_stats = get_team_stat_totals(team, year)
    team_points = team_stats[0]
    team_assists = team_stats[1]
    team_fga = team_stats[2]
    team_fgm = team_stats[3]
    team_fta = team_stats[4]
    team_ftm = team_stats[5]
    team_orb = team_stats[6]
    team_tov = team_stats[7]
    team_minutes = team_stats[8]
    team_threes_made = team_stats[9]
    
    opponent_trb = team_stats[10]
    opponent_orb = team_stats[11]

    # print([team_points, team_assists, team_fga, team_fgm, team_fta, team_ftm, team_orb, team_tov, team_minutes, team_threes_made, opponent_trb, opponent_orb])

    # Team_Scoring_Poss = Team_FGM + (1 - (1 - (Team_FTM / Team_FTA))^2) * Team_FTA * 0.4
    team_scoring_possessions = team_fgm + (1.0 - (1.0 -(team_ftm / team_fta))**2.0) * team_fta * 0.4

    # Team_Play% = Team_Scoring_Poss / (Team_FGA + Team_FTA * 0.4 + Team_TOV)
    team_play_percentage = team_scoring_possessions / (team_fga + team_fta * 0.4 + team_tov)

    # Team_ORB% = Team_ORB / (Team_ORB + (Opponent_TRB - Opponent_ORB))
    team_orb_percentage = team_orb / (team_orb + (opponent_trb - opponent_orb))

    # Team_ORB_Weight = ((1 - Team_ORB%) * Team_Play%) / ((1 - Team_ORB%) * Team_Play% + Team_ORB% * (1 - Team_Play%))
    team_orb_weight = ((1.0 - team_orb_percentage) * team_play_percentage) / ((1.0 - team_orb_percentage) * team_play_percentage + team_orb_percentage * (1.0 - team_play_percentage))

    # ORB_Part = ORB * Team_ORB_Weight * Team_Play%
    orb_part = offensive_rebounds * team_orb_weight * team_play_percentage

    # FT_Part = (1-(1-(FTM/FTA))^2)*0.4*FTA
    free_throw_part = (1.0 - (1.0 - (free_throws_made / free_throws_attempted))**2.0) * 0.4 * free_throws_attempted

    # AST_Part = 0.5 * (((Team_PTS - Team_FTM) - (PTS - FTM)) / (2 * (Team_FGA - FGA))) * AST
    assist_part = 0.5 * (((team_points - team_ftm) - (points - free_throws_made)) / (2.0 * (team_fga - field_goals_attempted))) * assists

    # qAST = ((MP / (Team_MP / 5)) * (1.14 * ((Team_AST - AST) / Team_FGM))) + ((((Team_AST / Team_MP) * MP * 5 - AST) / ((Team_FGM / Team_MP) * MP * 5 - FGM)) * (1 - (MP / (Team_MP / 5))))
    q_assist = ((minutes_played / (team_minutes / 5)) * (1.14 * ((team_assists - assists) / team_fgm))) + ((((team_assists / team_minutes) * minutes_played * 5 - assists) / ((team_fgm / team_minutes) * minutes_played * 5.0 - field_goals_made)) * (1.0 - (minutes_played / (team_minutes / 5.0))))

    # FG_Part = FGM * (1 - 0.5 * ((PTS - FTM) / (2 * FGA)) * qAST)
    field_goal_part = field_goals_made * (1.0 - 0.5 * ((points - free_throws_made) / (2.0 * field_goals_attempted)) * q_assist)

    # ScPoss = (FG_Part + AST_Part + FT_Part) * (1 - (Team_ORB / Team_Scoring_Poss) * Team_ORB_Weight * Team_Play%) + ORB_Part
    scoring_possesions = (field_goal_part + assist_part + free_throw_part) * (1.0 - (team_orb / team_scoring_possessions) * team_orb_weight * team_play_percentage) + orb_part


    # FGxPoss = (FGA - FGM) * (1 - 1.07 * Team_ORB%)
    field_goals_missed = (field_goals_attempted - field_goals_made) * (1.0 - 1.07 * team_orb_percentage)

    # FTxPoss = ((1 - (FTM / FTA))^2) * 0.4 * FTA
    free_throws_missed = ((1.0 - (free_throws_made / free_throws_attempted))**2.0) * 0.4 * free_throws_attempted

    # TotPoss = ScPoss + FGxPoss + FTxPoss + TOV
    total_possesions = scoring_possesions + field_goals_missed + free_throws_missed + turnovers
    print([total_possesions, scoring_possesions])


    # PProd_FG_Part = 2 * (FGM + 0.5 * 3PM) * (1 - 0.5 * ((PTS - FTM) / (2 * FGA)) * qAST)
    pprod_field_goals = 2.0 * (field_goals_made + 0.5 * three_pointers_made) * (1.0 - 0.5 * ((points - free_throws_made) / (2.0 * field_goals_attempted)) * q_assist)
    
    # PProd_AST_Part = 2 * ((Team_FGM - FGM + 0.5 * (Team_3PM - 3PM)) / (Team_FGM - FGM)) * 0.5 * (((Team_PTS - Team_FTM) - (PTS - FTM)) / (2 * (Team_FGA - FGA))) * AST
    pprod_assists = 2.0 * ((team_fgm - field_goals_made + 0.5 * (team_threes_made - three_pointers_made)) / (team_fgm - field_goals_made)) * 0.5 * (((team_points - team_ftm) - (points - free_throws_made)) / (2.0 * (team_fga - field_goals_attempted))) * assists

    # PProd_ORB_Part = ORB * Team_ORB_Weight * Team_Play% * (Team_PTS / (Team_FGM + (1 - (1 - (Team_FTM / Team_FTA))^2) * 0.4 * Team_FTA))
    pprod_offensive_rebounds = offensive_rebounds * team_orb_weight * team_play_percentage * (team_points / (team_fgm + (1.0 - (1.0 - (team_ftm / team_fta))**2.0) * 0.4 * team_fta))

    # PProd = (PProd_FG_Part + PProd_AST_Part + FTM) * (1 - (Team_ORB / Team_Scoring_Poss) * Team_ORB_Weight * Team_Play%) + PProd_ORB_Part
    points_produced = (pprod_field_goals + pprod_assists + free_throws_made) * (1.0 -(team_orb / team_scoring_possessions) * team_orb_weight * team_play_percentage) + pprod_offensive_rebounds

    
    # ORtg = 100 * (PProd / TotPoss)
    offensive_rating = 100 * (points_produced / total_possesions)

    # Floor% = ScPoss / TotPoss
    floor_percentage = scoring_possesions / total_possesions

    return [round(offensive_rating), round((floor_percentage*100), 3)]