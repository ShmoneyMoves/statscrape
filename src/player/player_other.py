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
from proxy import get_proxy

def get_first_season(player):
    validation = validate_name(player)
    if validation[0]:

        url = "https://www.basketball-reference.com/players/" + validation[1][:1].lower() + "/" + validation[1].lower() + "01.html"
        response = requests.get(url, get_proxy())
    
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
        response = requests.get(url, get_proxy())
    
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