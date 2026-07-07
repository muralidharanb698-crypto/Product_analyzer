import re
import urllib.parse
from playwright.sync_api import sync_playwright
from pprint import pprint


def clean_price(raw):
    if not raw:
        return None
    digits = re.sub(r"[^\d]", "", raw)
    return int(digits) if digits else None


def clean_rating(raw):
    if not raw:
        return 4.0
    match = re.search(r"(\d+(\.\d+)?)", raw)
    return float(match.group(1)) if match else 4.0


def flipkart_scrape(product, max_results=5):
    products = []
    query = urllib.parse.quote(product)

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
        page.set_default_timeout(5000)
        page.set_default_navigation_timeout(5000)

        page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
        """)

        try:
            # go straight to search results, skip homepage + typing
            page.goto(
                f"https://www.flipkart.com/search?q={query}",
                wait_until="domcontentloaded",
                timeout=15000
            )
        except Exception as e:
            print("Flipkart navigation error:", e)
            browser.close()
            return []

        # close login popup if it appears
        try:
            page.locator("button:has-text('✕')").click(timeout=2000)
        except:
            pass

        try:
            page.wait_for_selector("div[data-id]", timeout=10000)
        except:
            browser.close()
            return []

        cards = page.locator("div[data-id]")
        count = min(cards.count(), max_results)

        for i in range(count):
            card = cards.nth(i)

            try:
                title = card.locator("a[title]").first.get_attribute("title")
                if not title:
                    title = card.locator("a").nth(1).text_content().strip()
                if not title:
                    continue
            except:
                continue  

            price_raw = None
            for selector in ["div.hZ3P6w", "div.Nx9bqj", "div._30jeq3", "div.cN1yYO"]:
                try:
                    text = card.locator(selector).first.text_content(timeout=1500).strip()
                    if text:
                        price_raw = text
                        break
                except:
                    pass

            try:
                rating_raw = card.locator("div.XQDdHH").first.text_content(timeout=1500).strip()
            except:
                rating_raw = None

            try:
                image = card.locator("img").first.get_attribute("src")
            except:
                image = None

            try:
                href = card.locator("a[href]").first.get_attribute("href")
                link = "https://www.flipkart.com" + href if href else None
            except:
                link = None

            products.append({
                "title": title,
                "price": clean_price(price_raw),
                "rating": clean_rating(rating_raw),
                "image": image,
                "url": link,
                "site": "flipkart"
            })

        context.close()
        browser.close()

    return products


if __name__ == "__main__":
    product = input("Enter product: ")
    pprint(flipkart_scrape(product))