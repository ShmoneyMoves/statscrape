from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

from . import validate_team, get_abbreviation
from proxy import get_proxy

def get_team_schedule(team, year):

    team_validation = validate_team.validate_name(team)
    if team_validation:
        url = "https://www.basketball-reference.com/teams/" + team.upper() + "/" + year +  "_games.html"
        response = requests.get(url, proxies=get_proxy())
    
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
        response = requests.get(url, proxies=get_proxy())
    
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