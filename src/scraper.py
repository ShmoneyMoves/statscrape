from bs4 import BeautifulSoup
from selenium import webdriver
import requests

def scrape_player_stats(url):
    # Send a GET request to the URL
    response = requests.get(url)
    
    # Parse the HTML content of the page with Beautiful Soup
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Find the stats table by ID
    stats_table = soup.find('table', {'id': 'schedule'})
    
    # Extract and print the header row and each row of data from the table
    if stats_table:
        headers = [th.getText() for th in stats_table.findAll('tr', limit=2)[0].findAll('th')]
        rows = stats_table.findAll('tr')[1:]
        results = [[td.getText() for td in rows[i].findAll('td')]
                        for i in range(len(rows))]
        for entry in results:
            print(entry)
        # Print headers
        print(headers)
       
    else:
        print("Stats table not found.")

def parse_schedule(url):
    print(url)
    response = requests.get(url)

    soup = BeautifulSoup(response.text, 'html.parser')
    # Find the stats table by ID
    schedule_table = soup.find('table', {'id': 'schedule'})
    print(schedule_table)
    if schedule_table:
        rows = schedule_table.find_all('tr')
        for row in rows[1:]:  # Skipping the header row
            columns = row.find_all(['th', 'td'])
            
            date = columns[0].text.strip()
            start_time = columns[1].text.strip()
            visitor_team = columns[2].text.strip()
            visitor_pts = columns[3].text.strip()
            home_team = columns[4].text.strip()
            home_pts = columns[5].text.strip()
            box_score_link = row.find('td', {'data-stat': 'box_score_text'}).find('a')['href'] if row.find('td', {'data-stat': 'box_score_text'}).find('a') else None
            attendance = columns[7].text.strip()
            arena = columns[8].text.strip()
            
            print("Date:", date)
            print("Start Time:", start_time)
            print("Visitor/Neutral:", visitor_team)
            print("PTS:", visitor_pts)
            print("Home/Neutral:", home_team)
            print("PTS:", home_pts)
            print("Box Score:", box_score_link)
            print("Attend:", attendance)
            print("Arena:", arena)
            # parse_box_score('https://www.basketball-reference.com' + box_score_link, get_team_abbreviation(visitor_team), get_team_abbreviation(home_team))
            print()

def parse_box_score(url, team_one, team_two):
    print(url)

    driver = webdriver.Chrome()
    driver.maximize_window()
    driver.get(url)
    content = driver.page_source.encode('utf-8').strip()

    soup = BeautifulSoup(content, 'html.parser')

    # Basic Stats
    print(" |--------------- BASIC ---------------| ")
    tableOneId = 'box-' + team_one
    tabelTwoId = 'box-' + team_two
    print(tableOneId)

    basic_stats_table_1 = soup.find('table', attrs={'id': tableOneId  + "-game-basic"})
    if basic_stats_table_1:
        rows = basic_stats_table_1.find_all('tr')
        for row in rows[1:]:
            columns = row.find_all(['th', 'td'])
            stats = [column.text.strip() for column in columns]
            # Assuming the first column is always the player's name
            print(stats)
    basic_stats_table_2 = soup.find('table', attrs={'id': tabelTwoId  + "-game-basic"})
    if basic_stats_table_2:
        rows = basic_stats_table_2.find_all('tr')
        for row in rows[1:]:
            columns = row.find_all(['th', 'td'])
            stats = [column.text.strip() for column in columns]
            # Assuming the first column is always the player's name
            print(stats)

    # Advancted Stast
    print(" |--------------- ADVANCED ---------------| ")
    advanted_stats_table_1 = soup.find('table', attrs={'id': tableOneId  + "-game-advanced"})
    if advanted_stats_table_1:
        rows = advanted_stats_table_1.find_all('tr')
        for row in rows[1:]:
            columns = row.find_all(['th', 'td'])
            stats = [column.text.strip() for column in columns]
            # Assuming the first column is always the player's name
            print(stats)
    advanted_stats_table_2 = soup.find('table', attrs={'id': tabelTwoId  + "-game-advanced"})
    if advanted_stats_table_2:
        rows = advanted_stats_table_2.find_all('tr')
        for row in rows[1:]:
            columns = row.find_all(['th', 'td'])
            stats = [column.text.strip() for column in columns]
            # Assuming the first column is always the player's name
            print(stats)

def get_team_abbreviation(team_name):
    team_abbreviations = {
        "Atlanta Hawks": "ATL",
        "Boston Celtics": "BOS",
        "Brooklyn Nets": "BKN",
        "Charlotte Hornets": "CHA",
        "Chicago Bulls": "CHI",
        "Cleveland Cavaliers": "CLE",
        "Dallas Mavericks": "DAL",
        "Denver Nuggets": "DEN",
        "Detroit Pistons": "DET",
        "Golden State Warriors": "GSW",
        "Houston Rockets": "HOU",
        "Indiana Pacers": "IND",
        "Los Angeles Clippers": "LAC",
        "Los Angeles Lakers": "LAL",
        "Memphis Grizzlies": "MEM",
        "Miami Heat": "MIA",
        "Milwaukee Bucks": "MIL",
        "Minnesota Timberwolves": "MIN",
        "New Orleans Pelicans": "NOP",
        "New York Knicks": "NYK",
        "Oklahoma City Thunder": "OKC",
        "Orlando Magic": "ORL",
        "Philadelphia 76ers": "PHI",
        "Phoenix Suns": "PHX",
        "Portland Trail Blazers": "POR",
        "Sacramento Kings": "SAC",
        "San Antonio Spurs": "SAS",
        "Toronto Raptors": "TOR",
        "Utah Jazz": "UTA",
        "Washington Wizards": "WAS"
    }
    
    return team_abbreviations.get(team_name, "Unknown")
def main():
    # parse_schedule('https://www.basketball-reference.com/leagues/NBA_2023_games.html')
    # scrape_player_stats('https://www.basketball-reference.com/players/j/jamesle01.html')
    parse_box_score('https://www.basketball-reference.com/boxscores/202210180BOS.html', "BOS", "PHI")
if __name__ == '__main__':
    main()

