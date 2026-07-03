from playwright.sync_api import sync_playwright
from pprint import pprint


def flipkart_scrape(product):
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            channel="chrome",
            args=["--disable-blink-features=AutomationControlled"]
        )

        context = browser.new_context(
            viewport={"width": 1366, "height": 768},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/137.0.0.0 Safari/537.36"
        )

        page = context.new_page()

        page.goto(
            "https://www.flipkart.com",
            wait_until="domcontentloaded",
            timeout=50000
        )
        # Close login popup
        try:
            page.locator("button:has-text('✕')").click(timeout=3000)
        except:
            pass

        page.fill("input[name='q']", product)
        page.keyboard.press("Enter")

        page.wait_for_selector("div[data-id]", timeout=30000)

        card = page.locator("div[data-id]").first
        img = card.locator("img").first

        print("src:", img.get_attribute("src"))
        try:
            title = card.locator("a[title]").first.get_attribute("title")
            if not title:
                title = card.locator("a").nth(1).text_content().strip()
        except:
            title = "Not Available"

        price = "Not Available"

        for selector in [
                    "div.hZ3P6w",
                    "div.Nx9bqj",
                    "div._30jeq3",
                    "div.cN1yYO"]:
            try:
                price = card.locator(selector).first.text_content().strip()
                price = price.replace("₹", "").replace(",", "")
                if price:
                    break
            except:
                pass

        try:
            rating = card.locator("div.XQDdHH").first.text_content().strip()
        except:
            rating = "No Rating"

        try:
            image = card.locator("img").first.get_attribute("src")
        except:
            image = None

        try:
            href = card.locator("a[href]").first.get_attribute("href")
            link = "https://www.flipkart.com" + href if href else None
        except:
            link = None

        browser.close()

        return [{
            "title": title,
            "price": price,
            "rating": rating,
            "image": image,
            "link": link,
            "website": "Flipkart"
        }]


if __name__ == "__main__":
    product = input("Enter product: ")
    pprint(flipkart_scrape(product))