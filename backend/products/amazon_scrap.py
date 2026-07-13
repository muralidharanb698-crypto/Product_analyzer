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



def amazon_scrape(product, max_results=5):

    results = []

    query = urllib.parse.quote(product)


    with sync_playwright() as p:

        browser = p.chromium.launch(
            headless=True,
            args=[
                "--disable-blink-features=AutomationControlled"
            ]
        )


        context = browser.new_context(
            user_agent=
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 Chrome/120 Safari/537.36"
        )


        page = context.new_page()


        try:

            url = f"https://www.amazon.in/s?k={query}"

            print("Opening:", url)


            page.goto(
                url,
                wait_until="domcontentloaded",
                timeout=60000
                )
            page.wait_for_timeout(5000)
            # page.screenshot(path="amazon_debug.png", full_page=True)
            # print(page.title())



        except Exception as e:

            print("Navigation Error:", e)

            browser.close()

            return []



        # Amazon product cards

        cards = page.locator(
            "div.s-result-item[data-component-type='s-search-result']"
        )


        count = cards.count()


        print("Products found:", count)



        for i in range(min(count,max_results)):


            try:

                card = cards.nth(i)


                title = card.locator("h2").last.inner_text(timeout=3000).strip()


                if not title:
                    continue



                # price

                price = None

                try:

                    price = card.locator(
                        ".a-price-whole"
                    ).inner_text(timeout=2000)

                except:
                    pass



                # image

                image = None

                try:

                  image = card.locator("img").first.get_attribute("src")

                except:
                    pass



                # link

                link = None
                try:
                    link = card.locator("a.a-link-normal.s-line-clamp-2").first.get_attribute("href")
                    if not link:
                        link = card.locator("h2 a").first.get_attribute("href")
                    if link and link.startswith("/"):
                        link = "https://www.amazon.in" + link
                except:
                   link = None




                results.append({

                    "title": title.strip(),

                    "price": clean_price(price),

                    "rating":4.0,

                    "image":image,

                    "url":link,

                    "site":"amazon"

                })



            except Exception as e:

                print(
                    "Card error:",
                    e
                )
            



        browser.close()



    print(results)

    return results
if __name__ == "__main__":
    from pprint import pprint

    product = input("Enter product: ")
    pprint(amazon_scrape(product))