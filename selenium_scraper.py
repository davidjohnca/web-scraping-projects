import pandas as pd
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from time import sleep
from webdriver_manager.chrome import ChromeDriverManager


options = Options()
options.add_argument('--headless')
options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36')
#options.add_experimental_option('detach', True)
service = Service(ChromeDriverManager().install())
driver = webdriver.Chrome(options=options, service=service)
scraped_quotes = []

for page in range(1, 11):
    driver.implicitly_wait(30)
    driver.get(f'https://quotes.toscrape.com/page/{page}/')
    quotes = driver.find_elements(By.XPATH, '//div[@class="quote"]')

    for quote in quotes:
        text = quote.find_element(By.XPATH('.//span[@class="text"]'))
        author = quote.find_element(By.XPATH('.//small[@class="author"]'))
        tags = [tag.text for tag in quote.find_elements(By.XPATH('.//a[@class="tag"]'))]
        print({'text': text.text, 'author': author.text, 'tags': tags})
        scraped_quotes.append({'text': text.text, 'author': author.text, 'tags': tags})
    
    driver.quit()
    sleep(2)

df = pd.DataFrame(scraped_quotes)
df.to_csv('scraped_quotes.csv')
