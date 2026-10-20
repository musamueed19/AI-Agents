import requests
from bs4 import BeautifulSoup

main_url = "toscrape.com"
sub_domain = "https://books." + main_url

response = requests.get(sub_domain)

# print(response.status_code)

page_html = response.text

soup = BeautifulSoup(page_html, 'html.parser')

print(soup.prettify())