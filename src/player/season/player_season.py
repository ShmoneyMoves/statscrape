from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options

import requests
import os, sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from validate_name import validate_name
from proxy import get_proxy

# Retrieves a player's statistics for every game of the given season.
def get_season_stats(player, season):
    validation = validate_name(player)
    if validation[0]:
        url = "https://www.basketball-reference.com/players/" + validation[1][:1].lower() + "/" + validation[1].lower() + "01/gamelog/" + season
        response = requests.get(url, proxies=get_proxy())
    
        soup = BeautifulSoup(response.text, 'html.parser')
        
        stats_table = soup.find('table', {'id': 'pgl_basic'})
        result = []
        if stats_table:
            headers = [th.getText() for th in stats_table.findAll('tr', limit=2)[0].findAll('th')]
            rows = stats_table.findAll('tr')[1:]
            results = [[td.getText() for td in rows[i].findAll('td')]
                            for i in range(len(rows))]
            result.append(headers)
            for entry in results:
                result.append(entry)
            return result
            
    else:
        return ["ERROR:", validation[1]]
    
# Retrieves a player's statistics for every game of the given season.
def get_season_stats_against_team(player, season, team):
    validation = validate_name(player)
    if validation[0]:
        url = "https://www.basketball-reference.com/players/" + validation[1][:1].lower() + "/" + validation[1].lower() + "01/gamelog/" + season
        response = requests.get(url, proxies=get_proxy())
    
        soup = BeautifulSoup(response.text, 'html.parser')
        
        stats_table = soup.find('table', {'id': 'pgl_basic'})
        result = []
        if stats_table:
            headers = [th.getText() for th in stats_table.findAll('tr', limit=2)[0].findAll('th')]
            rows = stats_table.findAll('tr')[1:]
            results = [[td.getText() for td in rows[i].findAll('td')]
                            for i in range(len(rows))]
            result.append(headers)
            for entry in results:
                if len(entry) >= 6 and entry[5] == team:
                    result.append(entry)
            return result
            
    else:
        return ["ERROR:", validation[1]]