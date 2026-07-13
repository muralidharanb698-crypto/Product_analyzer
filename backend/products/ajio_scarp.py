import re
from urllib.parse import quote
from playwright.sync_api import sync_playwright


def clean_price(raw):
    if not raw:
        return None

    digits = re.findall(r"\d+", raw.replace(",", ""))

    if digits:
        return int(digits[0])

    return None


def ajio_scrape(product, max_results=5):

    results = []

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled"]
        )

        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36",
            viewport={"width": 1366, "height": 768}
        )

        page = context.new_page()

        page.set_default_timeout(10000)

        try:

            url = f"https://www.ajio.com/search/?text={quote(product)}"

            print("Opening:", url)

            page.goto(
                url,
                wait_until="domcontentloaded",
                timeout=60000
            )

            page.wait_for_timeout(5000)

        except Exception as e:

            print("Navigation Error:", e)

            browser.close()

            return []

        CARD_SELECTOR = "div.item"

        try:
            page.wait_for_selector(CARD_SELECTOR, timeout=15000)
        except:
            print("No products found")
            browser.close()
            return []

        cards = page.locator(CARD_SELECTOR)

        count = min(cards.count(), max_results)

        print("Products found:", count)

        for i in range(count):

            card = cards.nth(i)

            try:

                brand = ""

                try:
                    brand = card.locator(".brand").first.inner_text()
                except:
                    pass

                name = ""

                try:
                    name = card.locator(".nameCls").first.inner_text()
                except:
                    pass

                title = (brand + " " + name).strip()

                if not title:
                    continue

                try:
                    price = card.locator(".price strong").first.inner_text()
                except:
                    price = None

                try:
                    image = card.locator("img").first.get_attribute("src")
                except:
                    image = None

                try:
                    link = card.locator("a").first.get_attribute("href")

                    if link and link.startswith("/"):
                        link = "https://www.ajio.com" + link

                except:
                    link = None

                results.append({
                    "title": title,
                    "price": clean_price(price),
                    "rating": 4.0,
                    "image": image,
                    "url": link,
                    "site": "ajio"
                })

            except Exception as e:
                print("Card Error:", e)

        browser.close()

    print(results)

    return results


if __name__ == "__main__":

    product = input("Enter product: ")

    from pprint import pprint

    pprint(ajio_scrape(product))