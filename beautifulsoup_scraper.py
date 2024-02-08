from bs4 import BeautifulSoup
import pandas as pd
import requests
from time import sleep


scraped_quotes = []
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
}

for page in range(1, 11):
    response = requests.get(f'https://quotes.toscrape.com/page/{page}/', headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    quotes = soup.find_all('div', class_='quote')
    
    for quote in quotes:
        text = quote.find('span', class_='text')
        author = quote.find('small', class_='author')
        tags = [tag.text for tag in quote.find_all('a', class_='tag')]
        print({'text': text.text, 'author': author.text, 'tags': tags})
        scraped_quotes.append({'text': text.text, 'author': author.text, 'tags': tags})

    sleep(2)

df = pd.DataFrame(scraped_quotes)
df.to_csv('scraped_quotes.csv')
