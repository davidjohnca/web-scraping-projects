from playwright.async_api import async_playwright
import time

# Function to extract product price from a page
async def extract_product_price(page):
    """Extracts the product price from the current page."""

    # Find the element containing the price (adapt selector for the target website):
    price_element = await page.query_selector("#product-price")  # Example selector
    price_text = await page.inner_text(price_element)

    # Parse and return the price as a float (adapt parsing logic if needed):
    return float(price_text.strip("$"))  # Example parsing

# Function to handle notifications
async def send_notification(message):
    """Sends a notification to the user (implement your preferred notification method)"""

    # ... (Implement notification logic, e.g., using email, SMS, or desktop notifications)

async def track_price(product_url, target_price_range):
    """Tracks the product price and sends notifications when it drops within the target range."""

    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page()

        while True:
            try:
                await page.goto(product_url)

                current_price = await extract_product_price(page)

                if current_price <= target_price_range[1]:
                    await send_notification(f"Price dropped to {current_price}! Check the link: {product_url}")
                    break  # Stop tracking if price reaches the target

            except Exception as e:
                print(f"Error during price tracking: {e}")

            await page.close()
            await browser.new_page()  # Create a new page for the next check

            time.sleep(3600)  # Check every hour (adjust interval as needed)

# Main script
product_url = input("Enter the product URL: ")
target_price_range = input("Enter the desired price range (e.g., 50-75): ").split("-")

async_playwright().start(track_price(product_url, [float(x) for x in target_price_range]))
