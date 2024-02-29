from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import warnings

from . import validate_team, get_abbreviation

def get_team_schedule(team, year):

    team_validation = validate_team.validate_name(team)
    if team_validation:
        url = "https://www.basketball-reference.com/teams/" + team.upper() + "/" + year +  "_games.html"
        response = requests.get(url)
    
        soup = BeautifulSoup(response.text, 'html.parser')
        
        stats_table = soup.find('table', {'id': 'games'})
        result = []
        if stats_table:
            headers = [th.getText() for th in stats_table.findAll('tr', limit=2).findAll('th')]
            rows = stats_table.findAll('tr')[1:]
            results = [[td.getText() for td in rows[i].findAll('td')]
                            for i in range(len(rows))]
            result.append(headers)
            for entry in results:
                result.append(entry)
            return result
    else:
        return "ERROR: Invalid input"

def get_boxscore_links(team, year):
    team_validation = validate_team.validate_name(team)
    if team_validation:
        url = "https://www.basketball-reference.com/teams/" + team.upper() + "/" + year +  "_games.html"
        response = requests.get(url)
    
        soup = BeautifulSoup(response.text, 'html.parser')
        
        stats_table = soup.find('table', {'id': 'games'})
        result = []
        if stats_table:
            rows = stats_table.find_all('tr')
            for row in rows[1:]:  # Skipping the header ro
                if row.find('td', {'data-stat': 'box_score_text'}):
                    box_score_link = row.find('td', {'data-stat': 'box_score_text'}).find('a')['href'] if row.find('td', {'data-stat': 'box_score_text'}).find('a') else None
                    result.append(box_score_link)
        return result

 
    else:
        return "ERROR: Invalid input"
    
def get_injury_report(team, year):
    warnings.filterwarnings("ignore")
    team_validation = validate_team.validate_name(team)
    if team_validation:
        url = "https://www.basketball-reference.com/teams/" + team.upper() + "/" + str(year) +  ".html#all_injuries"

        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Run in headless mode
        chrome_options.add_argument('--no-sandbox')  # Bypass OS security model
        chrome_options.add_argument('--disable-dev-shm-usage')  # Avoid /dev/shm usage
        chrome_options.add_argument("--log-level=3")

        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        content = driver.page_source.encode('utf-8').strip()

        soup = BeautifulSoup(content, 'html.parser')
        driver.quit()
        
        stats_table = soup.find('table', {'id': 'injuries'})
        result = []
        if stats_table:
            rows = stats_table.findAll('tr')[1:]
            results = [[td.getText() for td in rows[i].findAll(['td', 'th'])]
                            for i in range(len(rows))]
            for entry in results:
                result.append(entry)
            return result

    else:
        return "ERROR: Invalid input"
    
def get_stat_totals(team, year):
    team_validation = validate_team.validate_name(team)
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

def get_ortg_by_lineup_helper(team):
    team_id = {
        "ATL": "1610612737",
        "BOS": "1610612738",
        "BKN": "1610612751",
        "CHA": "1610612766",
        "CHI": "1610612741",
        "CLE": "1610612739",
        "DAL": "1610612742",
        "DEN": "1610612743",
        "DET": "1610612765",
        "GSW": "1610612744",
        "HOU": "1610612745",
        "IND": "1610612754",
        "LAC": "1610612746",
        "LAL": "1610612747",
        "MEM": "1610612763",
        "MIA": "1610612748",
        "MIL": "1610612749",
        "MIN": "1610612750",
        "NOP": "1610612740",
        "NYK": "1610612752",
        "OKC": "1610612760",
        "ORL": "1610612753",
        "PHI": "1610612755",
        "PHX": "1610612756",
        "POR": "1610612757",
        "SAC": "1610612758",
        "SAS": "1610612759",
        "TOR": "1610612761",
        "UTA": "1610612762",
        "WAS": "1610612764"
    }
    return team_id[team]

def get_rtg_by_lineup(team, lname1, lname2, lname3, lname4, lname5):
    team_validation = validate_team.validate_name(team)
    if team_validation:
        team_id = get_ortg_by_lineup_helper(team)
        url = f"https://www.nba.com/stats/lineups/advanced?slug=advanced&TeamID={team_id}"

        # Use Selenium to wait for the table to load
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')  # Bypass OS security model
        chrome_options.add_argument('--disable-dev-shm-usage')  # Avoid /dev/shm usage
        chrome_options.add_argument("--log-level=3")
        driver = webdriver.Chrome(options=chrome_options)
        
        driver.get(url)
        try:
            # Wait for the table to be present
            table = WebDriverWait(driver, 30).until(EC.presence_of_element_located((By.CLASS_NAME, "Crom_table__p1iZz")))
            
            # Now that the table is loaded, extract the HTML content
            soup = BeautifulSoup(driver.page_source.encode('utf-8').strip(), 'html.parser')
            stats_table = soup.find('table', class_='Crom_table__p1iZz')
            result = []
            if stats_table:
                rows = stats_table.findAll('tr')[1:]
                results = [[td.getText() for td in rows[i].findAll(['td', 'th'])]
                                for i in range(len(rows))]
                for entry in results:
                    if lname1 in entry[0] and lname2 in entry[0] and lname3 in entry[0] and lname4 in entry[0] and lname5 in entry[0]: 
                        result.append(entry)
                    
            return result
        finally:
            driver.quit()  # Close the WebDriver session

def get_starting_lineup(team):
    team_validation = validate_team.validate_name(team)
    if team_validation:
        url = f"https://www.nba.com/players/todays-lineups"

        # Use Selenium to wait for the table to load
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument('--no-sandbox')  # Bypass OS security model
        chrome_options.add_argument('--disable-dev-shm-usage')  # Avoid /dev/shm usage
        chrome_options.add_argument("--log-level=3")
        driver = webdriver.Chrome(options=chrome_options)
        
        driver.get(url)
        try:
            # Wait for the table to be present
            button = WebDriverWait(driver, 30).until(
                EC.presence_of_element_located((By.XPATH, f"//button[@type='button' and contains(@class, 'ButtonGroup_btn__r075w') and text()='{team}']"))
            )
            button.click()

            WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.TAG_NAME, "body")))

            content = driver.page_source.encode('utf-8').strip()
            
            # Now that the table is loaded, extract the HTML content
            soup = BeautifulSoup(content, 'html.parser')
            result = []
            block_divs = soup.find_all('div', class_='Block_blockContent__6iJ_n')

            lineup_div = "NONE"
            # Loop through each div
            for div in block_divs:
                # Check if the div contains a nested div with class Block_titleContainerBetween__0GYet
                title_container = div.find('div', class_='Block_titleContainerBetween__0GYet')
                if title_container:
                    # Check if the title_container contains an h1 element with the text "BOS vs NYK"
                    title_h1 = title_container.find('h1')
                    if title_h1 and team in title_h1.text.strip():
                        lineup_div = div
                        break
            if lineup_div != "NONE":
                players = lineup_div.find_all('span', class_='DailyLineup_dlName__UcFOL')
                for player in players:
                    result.append(str(player).split(">")[1].split("<")[0])
                return result
            else:
                return "ERROR couldnt find div"
        finally:
            driver.quit()  # Close the WebDriver session


# Returns [TEAM, PACE, eFG%, TOV%, ORB%, FT/FGA, ORtg]
#
def get_four_factors_by_game(suffix):
    url = "https://www.basketball-reference.com" + suffix

    chrome_options = Options()
    chrome_options.add_argument('--headless')  # Run in headless mode
    chrome_options.add_argument('--no-sandbox')  # Bypass OS security model
    chrome_options.add_argument('--disable-dev-shm-usage')  # Avoid /dev/shm usage
    chrome_options.add_argument("--log-level=3")

    driver = webdriver.Chrome(options=chrome_options)
    driver.get(url)
    content = driver.page_source.encode('utf-8').strip()

    soup = BeautifulSoup(content, 'html.parser')
    
    stats_table = soup.find('table', {'id': 'four_factors'})
    result = []
    if stats_table:
        rows = stats_table.find_all('tr')
        results = [[td.getText() for td in rows[i].findAll(['td', 'th'])]
                                for i in range(len(rows))]
        for row in results[2:]:
            result.append(row)
    return result

def get_all_games_four_factors(team, year):
    team_validation = validate_team.validate_name(team)
    if team_validation:
        url = "https://www.basketball-reference.com/teams/" + team.upper() + "/" + str(year) +  "_games.html"
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')  # Bypass OS security model
        chrome_options.add_argument('--disable-dev-shm-usage')  # Avoid /dev/shm usage
        chrome_options.add_argument("--log-level=3")

        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        
        stats_table_function = lambda: driver.find_element(By.ID, 'games')
        stats_table = stats_table_function()
        table_body = stats_table.find_element(By.TAG_NAME, 'tbody')
        rows = table_body.find_elements(By.TAG_NAME,'tr')
        rows = [row for row in rows if "thead" not in row.get_attribute('class')]
        size = len(rows)
        result = []
        if stats_table:
            for i in range(3, size):
                
                row = rows[i]
                print(f"Game: {i} | {row.find_elements(By.TAG_NAME, 'a')[1]}")
                try:
                    box_score_link = row.find_elements(By.TAG_NAME, 'a')[1]
                    
                    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "games")))
                    #box_score_link = row.find_element(By.XPATH, "//td[@data-stat='box_score_text']/a[contains(text(), 'Box Score')]")
                    driver.execute_script("arguments[0].scrollIntoView();", box_score_link)
                    driver.execute_script("arguments[0].click();", box_score_link)

                    WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.ID, "four_factors")))
                    content = driver.page_source.encode('utf-8').strip()

                    soup = BeautifulSoup(content, 'html.parser')
                    
                    factor_table = soup.find('table', {'id': 'four_factors'})
                    game_factors = []
                    if factor_table:
                        rows = factor_table.find_all('tr')
                        results = [[td.getText() for td in rows[i].findAll(['td', 'th'])]
                                                for i in range(len(rows))]
                        for row in results[2:]:
                            game_factors.append(row)
                        result.append(game_factors)
                    with open("2024_Hawks_FourFactors.txt", "a") as file:
                        lastElement = False
                        for team_index, team in enumerate(game_factors):
                            if team_index == len(game_factors) - 1:
                                lastElement = True
                            for index, stat in enumerate(team): 
                                if lastElement:
                                    if index != len(team) - 1:
                                        file.write(stat + ",")
                                    else:
                                        file.write(stat)
                                else:          
                                    file.write(stat + ",")
                        file.write('\n')
                    print(game_factors)
                    driver.back()
                    rows = stats_table_function().find_elements(By.TAG_NAME,'tr')
                except Exception as e:
                    return f"Error: {e}"
            driver.quit()       
            return result
    else:
        return "ERROR: Invalid input"
    
def get_games_on_date(date):
    if len(date) == 10:
        url = f"https://www.nba.com/games?date={date}"
        chrome_options = Options()
        chrome_options.add_argument('--headless')  # Run in headless mode
        chrome_options.add_argument('--no-sandbox')  # Bypass OS security model
        chrome_options.add_argument('--disable-dev-shm-usage')  # Avoid /dev/shm usage
        chrome_options.add_argument("--log-level=3")

        driver = webdriver.Chrome(options=chrome_options)
        driver.get(url)
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, "GameCard_gc__UCI46.GameCardsMapper_gamecard__pz1rg")))
        gameCards = driver.find_elements(By.CLASS_NAME, "GameCard_gc__UCI46.GameCardsMapper_gamecard__pz1rg")

        matchups = []
        
        for game in gameCards:
            teams = game.find_elements(By.CLASS_NAME, "MatchupCardTeamName_teamName__9YaBA")
            away_team = teams[0].get_attribute('outerHTML').split('>')[1].split('<')[0]
            home_team = teams[1].get_attribute('outerHTML').split('>')[1].split('<')[0]
            matchups.append([get_abbreviation.get_full_name(away_team), get_abbreviation.get_full_name(home_team)])
    
        return matchups
        
    else:
        return "ERROR: Invalid input"
    
        