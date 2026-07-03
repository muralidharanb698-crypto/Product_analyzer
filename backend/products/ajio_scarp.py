from playwright.sync_api import sync_playwright
from urllib.parse import quote
from pprint import pprint


def ajio_scrape(product):
    products = []

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

        page.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });
        """)

        url = f"https://www.ajio.com/search/?text={quote(product)}"

        page.goto(url, wait_until="domcontentloaded")

        page.wait_for_timeout(5000)

        print("URL :", page.url)
        print("TITLE :", page.title())

        page.screenshot(path="ajio.png")

        try:
            page.wait_for_selector("div.item", timeout=10000)
        except:
            print("No products found.")
            browser.close()
            return []

        cards = page.locator("div.item")
        for i in range(min(cards.count(), 1)):
            card = cards.nth(i)

            try:
                try:
                    brand = card.locator(".brand").text_content().strip()
                except:
                    brand = ""

                try:
                    name = card.locator(".nameCls").text_content().strip()
                except:
                    name = ""

                title = f"{brand} {name}".strip()

                try:
                    price = card.locator(".price strong").text_content()
                    price = price.replace("₹", "").replace(",", "").strip()
                except:
                    price = "Not Available"

                try:
                    image = card.locator("img").first.get_attribute("src")
                except:
                    image = None

                try:
                    href = card.locator("a").first.get_attribute("href")
                    if href:
                        if href.startswith("/"):
                            link = "https://www.ajio.com" + href
                        else:
                            link = href
                    else:
                        link = None
                except:
                    link = None
                
                try:
                  rating = card.locator("p._3I65V").first.text_content().strip()
                except:
                  rating = "No Rating"

                products.append({
                    "title": title,
                    "price": price,
                    "rating": rating,
                    "image": image,
                    "link": link,
                    "website": "Ajio"
                })

            except Exception as e:
                print(e)

        browser.close()

    return products


if __name__ == "__main__":
    product = input("Enter product: ")
    pprint(ajio_scrape(product))