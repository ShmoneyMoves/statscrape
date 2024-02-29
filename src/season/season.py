from bs4 import BeautifulSoup
import requests
import os
import time

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

