import pandas as pd
from playwright.sync_api import sync_playwright


scraped_quotes = []

for next_page in range(1, 11):
    
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True, timeout=30000)
        context = browser.new_context()
        page = context.new_page()
        page.goto(f'https://quotes.toscrape.com/page/{next_page}/')
        quotes = page.query_selector_all('div.quote')

        for quote in quotes:
            text = quote.query_selector('span.text').inner_text()
            author = quote.query_selector('small.author').inner_text()
            tags = [tag.inner_text() for tag in quote.query_selector_all('a.tag')]
            print({'text': text, 'author': author, 'tags': tags})
            scraped_quotes.append({'text': text, 'author': author, 'tags': tags})
        
        context.close()
        browser.close()

df = pd.DataFrame(scraped_quotes)
df.to_csv('scraped_quotes.csv')
