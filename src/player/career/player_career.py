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

from player.player_other import get_first_season, get_last_season
from player.season.player_season import get_season_stats_against_team
from proxy import get_proxy

# Retrieves a player's per game statistics for every season of their career.
def get_career_stats(player):
    validation = validate_name(player)
    if validation[0]:
        url = "https://www.basketball-reference.com/players/" + validation[1][:1].lower() + "/" + validation[1].lower() + "01.html"
        response = requests.get(url, proxies=get_proxy())
    
        soup = BeautifulSoup(response.text, 'html.parser')
        
        stats_table = soup.find('table', {'id': 'per_game'})
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

# Returns given player's career playoff stats from each season.
def get_career_playoff_stats(player):
    validation = validate_name(player)
    if validation[0]:
        chrome_options = Options()
        chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
        chrome_options.add_argument("--headless")  # Run in headless mode
        driver = webdriver.Chrome(options=chrome_options)

        url = "https://www.basketball-reference.com/players/" + validation[1][:1].lower() + "/" + validation[1].lower() + "01.html"

        driver.get(url)
        button_xpath = "//a[@class='sr_preset' and contains(text(), 'Playoffs')]"
        button = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable((By.XPATH, button_xpath))
        )

        # Click the button
        button.click()
        content = driver.page_source.encode('utf-8').strip()

        soup = BeautifulSoup(content, 'html.parser')
        
        stats_table = soup.find('table', {'id': 'playoffs_per_game'})
        result = []
        if stats_table:
            headers = [th.getText() for th in stats_table.findAll('tr', limit=2)[0].findAll('th')]
            rows = stats_table.findAll('tr')[1:]
            results = [[td.getText() for td in rows[i].findAll('td')]
                            for i in range(len(rows))]
            result.append(headers)
            for entry in results:
                result.append(entry)
            driver.quit()
            return result
            
    else:
        return ["ERROR:", validation[1]]
