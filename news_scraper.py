import requests
from bs4 import BeautifulSoup

def scrape_news_headlines(url):
    """Fetches news headlines from the given URL and organizes them by category."""

    response = requests.get(url)
    response.raise_for_status()  # Raise an exception for error status codes

    soup = BeautifulSoup(response.content, 'html.parser')

    headlines_by_category = {}

    # Find elements containing headlines and categories (adapt selectors for the target website):
    for headline_element, category_element in zip(soup.find_all("h2", class_="headline"), soup.find_all("span", class_="category")):
        headline = headline_element.text.strip()
        category = category_element.text.strip()

        headlines_by_category.setdefault(category, []).append(headline)

    return headlines_by_category

# Example usage:
target_url = "https://www.example.com/news"  # Replace with the actual news website URL
headlines = scrape_news_headlines(target_url)

# Display headlines in a user-friendly format:
for category, category_headlines in headlines.items():
    print(f"\n**{category}**")
    for headline in category_headlines:
        print(headline)
