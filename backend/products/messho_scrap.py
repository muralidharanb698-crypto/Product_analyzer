from playwright.sync_api import sync_playwright
from urllib.parse import quote
from pprint import pprint


def safe_text(card, selector, timeout=2000):
    try:
        return card.locator(selector).first.text_content(timeout=timeout).strip()
    except Exception:
        return ""


def safe_attr(card, selector, attr, timeout=2000):
    try:
        return card.locator(selector).first.get_attribute(attr, timeout=timeout)
    except Exception:
        return None


def meesho_scrape(product, limit=1):
    products = []

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            channel="chrome",
            args=["--disable-blink-features=AutomationControlled"]
        )

        context = browser.new_context(
            viewport={"width": 1366, "height": 768},
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                        "AppleWebKit/537.36 (KHTML, like Gecko) "
                        "Chrome/137.0.0.0 Safari/537.36"
        )

        page = context.new_page()
        page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
        """)

        url = f"https://www.meesho.com/search?q={quote(product)}"
        page.goto(url, wait_until="domcontentloaded")
        page.wait_for_timeout(5000)

        print("URL   :", page.url)
        print("TITLE :", page.title())

        CARD_SELECTOR = 'a[href*="/p/"]'

        try:
            page.wait_for_selector(CARD_SELECTOR, timeout=3000)
        except Exception:
            print("No products found.")
            browser.close()
            return []

        cards = page.locator(CARD_SELECTOR)
        count = cards.count()
        print("Cards Found:", count)

        for i in range(min(count, limit)):
            card = cards.nth(i)

            title = safe_text(card, 'p[class*="StyledDesktopProductTitle"]') or "Not Available"

            price_raw = safe_text(card, 'div[class*="PriceRow"] h5')
            price = price_raw.replace("₹", "").replace(",", "").strip() or "Not Available"

            image = safe_attr(card, "img", "src")

            href = card.get_attribute("href", timeout=2000)
            link = f"https://www.meesho.com{href}" if href and href.startswith("/") else href

            rating = safe_text(card, 'div[class*="RatingSection"] span[label]') or "No Rating"
            review_count = safe_text(card, 'span[class*="RatingCount"]')

            products.append({
                "title": title,
                "price": price,
                "rating": rating,
                "review_count": review_count,
                "image": image,
                "link": link,
                "website": "Meesho"
            })

        browser.close()

    return products


if __name__ == "__main__":
    product = input("Enter product: ")
    pprint(meesho_scrape(product))