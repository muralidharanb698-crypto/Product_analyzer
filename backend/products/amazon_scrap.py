from playwright.sync_api import sync_playwright
from pprint import pprint
from urllib.parse import urlparse, parse_qs, unquote


from urllib.parse import quote
from playwright.sync_api import sync_playwright
from pprint import pprint


from playwright.sync_api import sync_playwright
from pprint import pprint


def amazon_scrape(product):
    products = []

    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=True,
            channel="chrome"
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

        page.goto(
            "https://www.amazon.in/",
            wait_until="domcontentloaded",
            timeout=10000
        )

        page.wait_for_selector("#twotabsearchtextbox", timeout=10000)
        page.fill("#twotabsearchtextbox", product)
        page.click("#nav-search-submit-button")

        CARD_SELECTOR = "div[data-component-type='s-search-result']"

        try:
            page.wait_for_selector(CARD_SELECTOR, timeout=10000)
        except:
            browser.close()
            return []

        cards = page.locator(CARD_SELECTOR)

        if cards.count() == 0:
            browser.close()
            return []

        card = cards.first
        img = card.locator("img").first

        print("src:", img.get_attribute("src"))

        try:
            title = card.locator("h2 span").first.text_content().strip()
        except:
            title = "Not Available"

        try:
            price = card.locator(".a-price-whole").first.text_content().strip()
        except:
            price = "Not Available"

        try:
            rating = card.locator(".a-icon-alt").first.text_content().strip()
        except:
            rating = "No Rating"

        try:
            image = card.locator("img.s-image").first.get_attribute("src")
        except:
            image = None

        try:
            href = card.locator("h2 a").first.get_attribute("href")
            if href:
                link = "https://www.amazon.in" + href
            else:
                link = None
        except:
            link = None

        products.append({
            "title": title,
            "price": price,
            "rating": rating,
            "image": image,
            "link": link,
            "website": "Amazon"
        })

        context.close()
        browser.close()

    return products


if __name__ == "__main__":
    product = input("Enter product: ")
    pprint(amazon_scrape(product))