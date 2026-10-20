import requests
from bs4 import BeautifulSoup

main_url = "toscrape.com"
sub_domain = "https://quotes." + main_url

response = requests.get(sub_domain)

# print(response.status_code)

page_html = response.text

soup = BeautifulSoup(page_html, 'html.parser')

first_quote = soup.find('div', class_='quote')
quote_text = first_quote.find('span', attrs={'itemprop': 'text'})
print(quote_text.text)