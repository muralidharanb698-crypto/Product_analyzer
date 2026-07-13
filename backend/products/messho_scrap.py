import re
from urllib.parse import quote
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


def meesho_scrape(product, max_results=5):

    results = []

    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled"
            ]
        )

        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/120 Safari/537.36"
        )

        page = context.new_page()

        try:

            url = f"https://www.meesho.com/search?q={quote(product)}"

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

        cards = page.locator('a[href*="/p/"]')

        count = cards.count()

        print("Products found:", count)

        for i in range(min(count, max_results)):

            try:

                card = cards.nth(i)

                title = None

                selectors = [
                    "p",
                    "h3",
                    "div[title]"
                ]

                for selector in selectors:
                    try:
                        title = card.locator(selector).first.inner_text(timeout=2000)
                        if title and len(title) > 5:
                            break
                    except:
                        pass

                if not title:
                    continue

                price = None

                try:
                    text = card.inner_text(timeout=2000)
                    match = re.search(r"₹\s?[\d,]+", text)

                    if match:
                        price = match.group()
                except:
                    pass

                image = None

                try:
                    image = card.locator("img").first.get_attribute("src")
                except:
                    pass

                link = None

                try:
                    href = card.get_attribute("href")

                    if href:
                        if href.startswith("/"):
                            link = "https://www.meesho.com" + href
                        else:
                            link = href
                except:
                    pass

                results.append({
                    "title": title.strip(),
                    "price": clean_price(price),
                    "rating": 4.0,
                    "image": image,
                    "url": link,
                    "site": "meesho"
                })

            except Exception as e:

                print("Card error:", e)

        browser.close()

    print(results)

    return results


if __name__ == "__main__":
    from pprint import pprint

    product = input("Enter product: ")

    pprint(meesho_scrape(product))