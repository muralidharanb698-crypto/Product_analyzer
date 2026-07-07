import re
import urllib.parse
from playwright.sync_api import sync_playwright


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

def amazon_scrape(product, max_results=5):
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
        page.set_default_timeout(10000)
        page.set_default_navigation_timeout(10000)

        page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', {
                get: () => undefined
            });
        """)

        try:
            page.goto(
                f"https://www.amazon.in/s?k={query}",
                wait_until="domcontentloaded",
                timeout=15000
            )
        except Exception as e:
            print("Amazon navigation error:", e)
            browser.close()
            return []

        CARD_SELECTOR = "div[data-component-type='s-search-result']"

        try:
            page.wait_for_selector(CARD_SELECTOR, timeout=10000)
        except:
            browser.close()
            return []

        cards = page.locator(CARD_SELECTOR)
        count = min(cards.count(), max_results)

        for i in range(count):
            card = cards.nth(i)

            try:
                if card.locator("text=Sponsored").count() > 0:
                    continue
            except:
                pass

            title = None

            selectors = [
                "h2 a span",
                "h2 span",
                "a h2 span",
                "h2"
            ]

            for selector in selectors:
                try:
                    text = card.locator(selector).first.text_content(timeout=1000)
                    if text and len(text.strip()) > 3:
                        title = text.strip()
                        break
                except:
                    pass

            if not title:
                continue

            price_raw = None
            try:
                price_raw = card.locator(".a-price-whole").first.text_content().strip()
            except:
                pass

            rating_raw = None
            try:
                rating_raw = card.locator(".a-icon-alt").first.text_content().strip()
            except:
                pass

            image = None
            try:
                image = card.locator("img.s-image").first.get_attribute("src")
            except:
                pass

            try:
                link = card.locator("a.a-link-normal.s-line-clamp-2").first.get_attribute("href")
                if not link:
                    link = card.locator("h2 a").first.get_attribute("href")

                if link:
                    if link.startswith("/"):
                        link = "https://www.amazon.in" + link
            except Exception:
                link = None

            products.append({
                "title": title,
                "price": clean_price(price_raw),
                "rating": clean_rating(rating_raw),
                "image": image,
                "url": link,
                "site": "amazon"
            })

        context.close()
        browser.close()

    return products


if __name__ == "__main__":
    from pprint import pprint

    product = input("Enter product: ")
    pprint(amazon_scrape(product))