from bs4 import BeautifulSoup
import pandas as pd
import requests


scraped_quotes = []

for page in range(1, 11):
    response = requests.get(f'https://quotes.toscrape.com/page/{page}/')
    soup = BeautifulSoup(response.content, 'html.parser')
    quotes = soup.find_all('div', class_='quote')
    
    for quote in quotes:
        text = quote.find('span', class_='text')
        author = quote.find('small', class_='author')
        tags = [tag.text for tag in quote.find_all('a', class_='tag')]
        print({'text': text.text, 'author': author.text, 'tags': tags})
        scraped_quotes.append({'text': text.text, 'author': author.text, 'tags': tags})

df = pd.DataFrame(scraped_quotes)
df.to_csv('scraped_quotes.csv')
