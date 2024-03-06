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

# Retrieves a player's statistics for every game of the given season.
def get_season_stats(player, season):
    validation = validate_name(player)
    if validation[0]:
        url = "https://www.basketball-reference.com/players/" + validation[1][:1].lower() + "/" + validation[1].lower() + "01/gamelog/" + season
        response = requests.get(url)
    
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
    
def get_season_stat_average(player, season, stat):
    validation = validate_name(player)
    if validation[0]:
        url = "https://www.basketball-reference.com/players/" + validation[1][:1].lower() + "/" + validation[1].lower() + "01.html" 
        response = requests.get(url)
    
        soup = BeautifulSoup(response.text, 'html.parser')
        
        stats_table = soup.find('table', {'id': 'per_game'})
        result = 0
        if stats_table:
            rows = stats_table.findAll('tr')[1:]
            results = [[td.getText() for td in rows[i].findAll(['td', 'th'])]
                            for i in range(len(rows))]
            for entry in results:
                entry[0][5:]
                if season[2:] == entry[0][5:]:
                    if stat == "pts":
                        result = entry[len(entry) - 2]
                    elif stat == 'pf':
                        result = entry[len(entry) - 3]
                    elif stat == 'tov':
                        result = entry[len(entry) - 4]
                    elif stat == "blk":
                        result = entry[len(entry) - 5]
                    elif stat == "stl":
                        result = entry[len(entry) - 6]
                    elif stat == "ast":
                        result = entry[len(entry) - 7]
                    elif stat == "trb":
                        result = entry[len(entry) - 8]
                    elif stat == "drb":
                        result = entry[len(entry) - 9]
                    elif stat == "orb":
                        result = entry[len(entry) - 10]
            return result
            
    else:
        return ["ERROR:", validation[1]]
    
def get_season_stat_total(player, season, stat):
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
        result = 0
        if stats_table:
            rows = stats_table.findAll('tr')[1:]
            results = [[td.getText() for td in rows[i].findAll(['td', 'th'])]
                            for i in range(len(rows))]
            for entry in results:
                if season[2:] == entry[0][5:]:
                    if stat == "pts":
                        result = entry[len(entry) - 3]
                    elif stat == 'pf':
                        result = entry[len(entry) - 4]
                    elif stat == 'tov':
                        result = entry[len(entry) - 5]
                    elif stat == "blk":
                        result = entry[len(entry) - 6]
                    elif stat == "stl":
                        result = entry[len(entry) - 7]
                    elif stat == "ast":
                        result = entry[len(entry) - 8]
                    elif stat == "trb":
                        result = entry[len(entry) - 9]
                    elif stat == "drb":
                        result = entry[len(entry) - 10]
                    elif stat == "orb":
                        result = entry[len(entry) - 11]
            return result
            
    else:
        return ["ERROR:", validation[1]]
