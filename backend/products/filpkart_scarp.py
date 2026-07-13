import re
import urllib.parse
from playwright.sync_api import sync_playwright


def clean_price(raw):
    if not raw:
        return None

    numbers = re.findall(r"\d+", raw.replace(",", ""))

    if numbers:
        return int(numbers[0])

    return None


def clean_rating(raw):
    if not raw:
        return 4.0

    match = re.search(r"\d+\.\d+", raw)

    if match:
        return float(match.group())

    return 4.0


def flipkart_scrape(product, max_results=5):

    results = []

    query = urllib.parse.quote(product)

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True,
            args=["--disable-blink-features=AutomationControlled"]
        )

        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
        )

        page = context.new_page()

        try:

            url = f"https://www.flipkart.com/search?q={query}"

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

        try:
            page.keyboard.press("Escape")
        except:
            pass

        cards = page.locator("div[data-id]")

        count = cards.count()

        print("Products found:", count)

        for i in range(min(count, max_results)):

            try:

                card = cards.nth(i)

                title = None

                selectors = [
                    "div.KzDlHZ",
                    "a.WKTcLC",
                    "a.IRpwTa",
                    "div.s1Q9rs"
                ]

                for selector in selectors:
                    try:
                        title = card.locator(selector).first.inner_text(timeout=2000)
                        if title:
                            break
                    except:
                        pass

                if not title:
                    continue

                price = None

                for selector in [
                    "div.Nx9bqj",
                    "div._30jeq3",
                    "div.hl05eU"
                ]:
                    try:
                        price = card.locator(selector).first.inner_text(timeout=2000)
                        if price:
                            break
                    except:
                        pass

                image = None

                try:
                    image = card.locator("img").first.get_attribute("src")
                except:
                    pass

                link = None

                try:
                    href = card.locator("a").first.get_attribute("href")

                    if href:
                        link = "https://www.flipkart.com" + href
                except:
                    pass

                results.append({
                    "title": title.strip(),
                    "price": clean_price(price),
                    "rating": 4.0,
                    "image": image,
                    "url": link,
                    "site": "flipkart"
                })

            except Exception as e:
                print("Card error:", e)

        browser.close()

    print(results)

    return results


if __name__ == "__main__":
    from pprint import pprint

    product = input("Enter product: ")

    pprint(flipkart_scrape(product))