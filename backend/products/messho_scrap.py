import re
from playwright.sync_api import sync_playwright
from urllib.parse import quote
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


def safe_text(card, selector, timeout=1500):
    try:
        return card.locator(selector).first.text_content(timeout=timeout).strip()
    except Exception:
        return ""


def safe_attr(card, selector, attr, timeout=1500):
    try:
        return card.locator(selector).first.get_attribute(attr, timeout=timeout)
    except Exception:
        return None


def meesho_scrape(product, max_results=5):
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
        page.set_default_timeout(5000)
        page.set_default_navigation_timeout(5000)

        page.add_init_script("""
            Object.defineProperty(navigator, 'webdriver', { get: () => undefined });
        """)

        url = f"https://www.meesho.com/search?q={quote(product)}"

        try:
            page.goto(url, wait_until="domcontentloaded", timeout=15000)
        except Exception as e:
            print("Meesho navigation error:", e)
            browser.close()
            return []

        page.wait_for_timeout(2500)

        CARD_SELECTOR = 'a[href*="/p/"]'

        try:
            page.wait_for_selector(CARD_SELECTOR, timeout=8000)
        except Exception:
            browser.close()
            return []

        cards = page.locator(CARD_SELECTOR)
        count = min(cards.count(), max_results)

        for i in range(count):
            card = cards.nth(i)

            title = safe_text(card, 'p[class*="StyledDesktopProductTitle"]')
            if not title:
                continue  # skip cards with no usable title

            price_raw = safe_text(card, 'div[class*="PriceRow"] h5')
            rating_raw = safe_text(card, 'div[class*="RatingSection"] span[label]')
            review_count_raw = safe_text(card, 'span[class*="RatingCount"]')

            image = safe_attr(card, "img", "src")

            try:
                href = card.get_attribute("href", timeout=1500)
                link = f"https://www.meesho.com{href}" if href and href.startswith("/") else href
            except:
                link = None

            products.append({
                "title": title,
                "price": clean_price(price_raw),
                "rating": clean_rating(rating_raw),
                "review_count": review_count_raw or None,
                "image": image,
                "url": link,
                "site": "meesho"
            })

        context.close()
        browser.close()

    return products


if __name__ == "__main__":
    product = input("Enter product: ")
    pprint(meesho_scrape(product))