import requests
from bs4 import BeautifulSoup
import random
import concurrent.futures

proxies = [
    {'https': '35.185.196.38:3128'}, 
    {'https': '167.114.107.37:80'}, 
    {'https': '1.0.209.176:8080'}, 
    {'https': '189.240.60.168:9090'}, 
    {'https': '124.156.219.100:80'}
]

proxies_to_add = []

def make_request_with_proxy(url, proxy):
    try:
        response = requests.get(url, proxies=proxy, timeout=5)
        if response.status_code == 200:
            return BeautifulSoup(response.text, 'html.parser')
    except requests.RequestException as e:
        print(f"Request failed with proxy {proxy} due to {e}")
        return None
    
def get_proxy():
    url = "http://ipinfo.io/json"
    for i in range(len(proxies)):
        index = random.randint(0, 9)
        soup = make_request_with_proxy(url, proxies[index])
        if soup:
            return proxies[index]
    return "No valid proxies!"

def test_working_proxies():
    with open('proxy_list.txt', 'r') as file:
        for proxy in file:
            test_proxy(proxy.split("'")[3])

def test_proxy(proxy):
    print("testing: ", proxy)
    try:
        response = requests.get("https://free-proxy-list.net/", proxies={"https": proxy}, timeout=10)
        if response.status_code == 200:
            if proxy not in proxies_to_add:
                proxies_to_add.append(proxy)
            print("SUCCCESS", proxy)
            return proxy, True
    except Exception as e:
        pass
    return proxy, False

def update_proxies():
    url = 'https://free-proxy-list.net/'
    header = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/601.3.9 (KHTML, like Gecko) Version/9.0.2 Safari/601.3.9'
    }

    response = requests.get(url, headers=header)
    soup = BeautifulSoup(response.text, 'html.parser')

    table = soup.find('table', class_='table table-striped table-bordered')
    if table:
        rows = table.find_all('tr')[1:]  # Find all table rows and skip the header row
        proxy_list = []
        with concurrent.futures.ThreadPoolExecutor(max_workers=300) as executor:
            futures = []
            for row in rows:
                cells = row.find_all(['th', 'td'])  # Find all table cells in the row (both headers and data cells)
                temp_proxy = str(cells[0].text.strip()) + ":" + str(cells[1].text.strip())
                futures.append(executor.submit(test_proxy, temp_proxy))
            for future, row in zip(futures, rows):
                if future.result():
                    proxy_list.append(str(row.find_all(['th', 'td'])[0].text.strip()) + ":" + str(row.find_all(['th', 'td'])[1].text.strip()))
        test_working_proxies()
        with open('proxy_list.txt', 'w') as file:
            for proxy in proxies_to_add:
                file.write("{ 'https': '" + proxy + "' }\n")


