import requests
import bs4

ip_response = bs4.BeautifulSoup(requests.get('https://2ip.ua/ru/').text, "html.parser")
IP = ip_response.select(" .ipblockgradient .ip")[0].getText().split()[0]

def get_my_ip():
    return IP

def get_my_city():
    return requests.get(f'https://ipapi.co/{IP}/json/').json().get("city")

def get_my_country():
    return requests.get(f'https://ipapi.co/{IP}/json/').json().get("country")