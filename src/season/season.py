from bs4 import BeautifulSoup
import requests
import os
from datetime import datetime
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

def get_directory(year):
    return str(int(year) - 1) + "-" + str(int(year))[2:]


def load_season_stats(year, table):
    url = "https://www.basketball-reference.com/leagues/NBA_" + year + ".html"
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')
        
    stats_table = soup.find('table', {'id': table})
    result = []
    if stats_table:
        headers = [th.getText() for th in stats_table.findAll('tr')[0 if table == "per_game-team" else 1].findAll('th')]
        rows = stats_table.findAll('tr')
        results = [[td.getText() for td in rows[i].findAll('td')]
                        for i in range(len(rows))]
    
        result.append([element for element in headers if element != '\xa0'])
        for entry in results:
            result.append(entry)

        if not os.path.exists(f"csv/{get_directory(year)}"):
            os.makedirs(f"csv/{get_directory(year)}", exist_ok=True)

        with open(f"csv/{get_directory(year)}/{table}.txt", "w") as file:
            for entry in result:
                csv_entry = ""
                for data in entry:
                    if len(data) > 0:
                        csv_entry = csv_entry + data + ","
                if csv_entry != "":
                    file.write(csv_entry + "\n")

def fetch_season_boxscores(year):
    url_suffix = str(int(year) - 1) + "-" + str(year[2:])
    url = f"https://www.nba.com/stats/teams/boxscores?Season={url_suffix}&dir=A&sort=GDATE"

    chrome_options = Options()
    #chrome_options.add_argument('--headless')  # Run in headless mode
    chrome_options.add_argument('--no-sandbox')  # Bypass OS security model
    chrome_options.add_argument('--disable-dev-shm-usage')  # Avoid /dev/shm usage
    chrome_options.add_argument("--log-level=3")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    result = []

    for i in range(0,50):
        print(f"{i}th Page...")
        WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "Crom_table__p1iZz")))

        soup = BeautifulSoup(driver.page_source.encode('utf-8').strip(), 'html.parser')
        stats_table = soup.find('table', class_='Crom_table__p1iZz')
        
        if stats_table:
            rows = stats_table.findAll('tr')[1:]
            results = [[td.getText() for td in rows[i].findAll(['td', 'th'])]
                            for i in range(len(rows))]
            for entry in results:
                result.append(entry)

        button = driver.find_element("xpath", "//button[@class='Pagination_button__sqGoH' and @title='Next Page Button']")
        
        button.click()
        print(f"{i}th Button Clicked...")
    return result


# teamfga = 5205
    # teamfg = 2521
    # teamfta = 1260
    # teamorb = 612
    # teamdrb = 2118
    # teamtov = 725
    # oppdrb = 1875
    # oppfga = 5359
    # oppfg = 2399
    # oppfta = 1089
    # opporb = 653
    # opptov = 683
    # team_one_pts = 6999
    # team_two_pts = 6394
def get_ratings_from_stats(team_fga, team_fg, team_fta, team_orb, team_drb, team_tov, team_pts, opp_fga, opp_fg, opp_fta, opp_orb, opp_drb, opp_tov, opp_pts, num_games):

    # print("-------------------------------------")
    # print(f"Team FGA={team_fga}")
    # print(f"Team FGM={team_fg}")
    # print(f"Team FTA={team_fta}")
    # print(f"Team ORB={team_orb}")
    # print(f"Team DRB={team_drb}")
    # print(f"Team TOV={team_tov}")
    # print(f"Team PTS={team_pts}")
    # print(f"Opp FGA={opp_fga}")
    # print(f"Opp FGM={opp_fg}")
    # print(f"Opp FTA={opp_fta}")
    # print(f"Opp ORB={opp_orb}")
    # print(f"Opp DRB={opp_drb}")
    # print(f"Opp TOV={opp_tov}")
    # print(f"Opp PTS={opp_pts}")

    possessions = 0.5 *((team_fga + 0.4 * team_fta - 1.07 * (team_orb/(team_orb + opp_drb)) * (team_fga - team_fg) + team_tov) + (opp_fga + 0.4 * opp_fta - 1.07 * (opp_orb/(opp_orb + team_drb)) * (opp_fga - opp_fg) + opp_tov))

    ortg = round((team_pts/possessions)*100, 1)
    drtg = round((opp_pts/possessions)*100, 1)
    pace = round((possessions / num_games), 1)

    return [ortg, drtg, pace]

def calculate_team_ratings_progressively(box_score_file, team_abbreviation):
    response = []
    with open(box_score_file, "r") as file:
        for line in file:
            date_ratings = []
            data = line.split(',')
            if team_abbreviation == data[1]:
                ratings = get_ratings_from_stats(float(data[6]), float(data[5]), float(data[12]), float(data[14]), float(data[15]), float(data[20]), float(data[4]), float(data[28]), float(data[27]), float(data[34]), float(data[36]), float(data[37]), float(data[42]), float(data[26]))
                date_ratings.append(data[0])
                date_ratings.append(ratings[0])
                date_ratings.append(ratings[1])
                date_ratings.append(ratings[2])
                response.append(date_ratings)
            elif team_abbreviation == data[23]:
                ratings = get_ratings_from_stats(float(data[28]), float(data[27]), float(data[34]), float(data[36]), float(data[37]), float(data[42]), float(data[26]), float(data[6]), float(data[5]), float(data[12]), float(data[14]), float(data[15]), float(data[20]), float(data[4]))
                date_ratings.append(data[0])
                date_ratings.append(ratings[0])
                date_ratings.append(ratings[1])
                date_ratings.append(ratings[2])
                response.append(date_ratings)
        return response

def calculate_daily_team_ratings(box_score_file, team_abbreviation):
    #    0          1       2         3         4           5       6         7       8       9        10       11        12        12
    # team_fga, team_fg, team_fta, team_orb, team_drb, team_tov, team_pts, opp_fga, opp_fg, opp_fta, opp_orb, opp_drb, opp_tov, opp_pts
    response = []
    data_totals = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    count = 1
    with open(box_score_file, "r") as file:
        for line in file:
            if team_abbreviation in line:
                data = line.split(',')
                if data[1] == team_abbreviation:
                    data_totals[0] = data_totals[0] + float(data[6])
                    data_totals[1] = data_totals[1] + float(data[5])
                    data_totals[2] = data_totals[2] + float(data[12])
                    data_totals[3] = data_totals[3] + float(data[14])
                    data_totals[4] = data_totals[4] + float(data[15])
                    data_totals[5] = data_totals[5] + float(data[20])
                    data_totals[6] = data_totals[6] + float(data[4])

                    data_totals[7] = data_totals[7] + float(data[28])
                    data_totals[8] = data_totals[8] + float(data[27])
                    data_totals[9] = data_totals[9] + float(data[34])
                    data_totals[10] = data_totals[10] + float(data[36])
                    data_totals[11] = data_totals[11] + float(data[37])
                    data_totals[12] = data_totals[12] + float(data[42])
                    data_totals[13] = data_totals[13] + float(data[26])
                elif data[23] == team_abbreviation:
                    data_totals[0] = data_totals[0] + float(data[28])
                    data_totals[1] = data_totals[1] + float(data[27])
                    data_totals[2] = data_totals[2] + float(data[34])
                    data_totals[3] = data_totals[3] + float(data[36])
                    data_totals[4] = data_totals[4] + float(data[37])
                    data_totals[5] = data_totals[5] + float(data[42])
                    data_totals[6] = data_totals[6] + float(data[26])

                    data_totals[7] = data_totals[7] + float(data[6])
                    data_totals[8] = data_totals[8] + float(data[5])
                    data_totals[9] = data_totals[9] + float(data[12])
                    data_totals[10] = data_totals[10] + float(data[14])
                    data_totals[11] = data_totals[11] + float(data[15])
                    data_totals[12] = data_totals[12] + float(data[20])
                    data_totals[13] = data_totals[13] + float(data[4])
                else:
                    if team_abbreviation == "MIN" and data[3] == team_abbreviation:
                        continue
                    else:
                        print(f"ERROR: Game {count}")


                ratings = get_ratings_from_stats(data_totals[0], data_totals[1], data_totals[2], data_totals[3], data_totals[4], data_totals[5], data_totals[6], data_totals[7], data_totals[8], data_totals[9], data_totals[10], data_totals[11], data_totals[12], data_totals[13], count)
                daily_ratings = [data[0], ratings[0], ratings[1], ratings[2], f"Game {count}"]
                response.append(daily_ratings)
                count = count + 1
        return response

def calculate_league_average(season):
    csv_path = f"season/csv/{season}/teams"
    teams = [
        "ATL", "BOS", "BKN", "CHA", "CHI", "CLE", "DAL", "DEN", "DET", "GSW", 
        "HOU", "IND", "LAC", "LAL", "MEM", "MIA", "MIL", "MIN", "NOP", "NYK", 
        "OKC", "ORL", "PHI", "PHX", "POR", "SAC", "SAS", "TOR"
    ]
    #              DATE, ORtg, DRtg, Pace
    average_list = []

    for index, team in enumerate(teams):
        with open(str(csv_path + "/" + team + ".txt"), "r") as file:
            for line in file:
                data = line.split(',')
                date = data[0]
                ortg = float(data[1])
                drtg = float(data[2])
                pace = float(data[3])

                flag = False
                for i, day in enumerate(average_list):
                    if date == day[0]:
                        flag = True
                        games_on_day = float(day[4])
                        
                        new_ortg = round(((float(day[1]) * games_on_day) + ortg) / (games_on_day + 1), 1)
                        new_drtg = round(((float(day[2]) * games_on_day) + drtg) / (games_on_day + 1), 1)
                        new_pace = round(((float(day[3]) * games_on_day) + pace) / (games_on_day + 1), 1)
                        new_game_count = games_on_day + 1
                        day = [date, new_ortg, new_drtg, new_pace, new_game_count]
                        average_list[i] = day
                        break
                if not flag:
                    day_info = [date, ortg, drtg, pace, 1]
                    average_list.append(day_info)
            def get_date(item):
                return datetime.strptime(item[0], "%m/%d/%Y")
            sorted_data = sorted(average_list, key=get_date)
    with open(f"season/csv/{season}/league_average.txt", "w") as file:
        for entry in sorted_data:
            entry = [str(i) for i in entry]
            csv_row = ','.join(entry)
            file.write(csv_row + "\n")
    for i, day in enumerate(sorted_data):
        print(f"{i} --- {day}")
    print(len(sorted_data)) 
            