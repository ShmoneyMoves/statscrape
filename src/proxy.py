import requests
from bs4 import BeautifulSoup
import random

proxies = [
    {
        'https:': '23.19.244.109:109'
    },
    {
        'https:': "183.100.14.134:8000"
    },
    {
        'https:':  "202.61.204.51:80"
    },
    {
        'https:':  "13.81.217.201:80"
    },
    {
        'https:':  "167.71.5.83:3128"
    },
    {
        'https:': "8.213.129.15:443"
    },
    {
        'https:':  "198.199.86.11:8080"
    },
    {
        'https:': "162.240.75.37:80"
    },
    {
        'https:': "20.210.113.32:80"
    },
    {
        'https:': "18.206.243.225:4920"
    }
]

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
        soup = make_request_with_proxy(url, proxies[random.randint(0, 9)])
        if soup:
            return proxies[random.randint(0, 9)]
    return "No valid proxies!"

# # Example usage
# url = "https://www.basketball-reference.com/players/t/tatumja01.html"
# for proxy in proxies:
#     soup = make_request_with_proxy(url, proxy)
#     if soup:
#         # Process your BeautifulSoup object as needed
#         print("Request successful", proxy)