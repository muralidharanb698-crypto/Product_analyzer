import re
import urllib.parse
from playwright.sync_api import sync_playwright
from pprint import pprint


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

    products = []

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

            url = (
                f"https://www.flipkart.com/search?q={query}"
            )

            print("Opening:",url)


            page.goto(
                url,
                wait_until="networkidle",
                timeout=30000
            )


            page.wait_for_timeout(3000)



        except Exception as e:

            print(
                "Flipkart navigation error:",
                e
            )

            browser.close()

            return []



        # close login popup

        try:

            page.keyboard.press("Escape")

        except:

            pass



        # Product containers

        cards = page.locator(
            "div[data-id]"
        )


        count = cards.count()


        print(
            "Flipkart products found:",
            count
        )



        for i in range(
            min(count,max_results)
        ):


            try:

                card = cards.nth(i)



                # Title

                title = None


                selectors = [

                    "div.KzDlHZ",

                    "a.WKTcLC",

                    "a.IRpwTa",

                    "div.s1Q9rs",

                    "a"

                ]



                for selector in selectors:

                    try:

                        text = card.locator(
                            selector
                        ).first.inner_text(
                            timeout=1000
                        )

                        if text and len(text)>5:

                            title=text.strip()

                            break


                    except:

                        pass



                if not title:

                    continue




                # Price

                price = None


                price_selectors=[

                    "div.Nx9bqj",

                    "div._30jeq3",

                    "div.hl05eU"

                ]


                for selector in price_selectors:

                    try:

                        price = card.locator(
                            selector
                        ).first.inner_text(
                            timeout=1000
                        )

                        if price:

                            break


                    except:

                        pass




                # Image

                try:

                    image = card.locator(
                        "img"
                    ).first.get_attribute(
                        "src"
                    )

                except:

                    image=None




                # Link

                try:

                    href = card.locator(
                        "a"
                    ).first.get_attribute(
                        "href"
                    )


                    link = (
                        "https://www.flipkart.com"
                        + href
                        if href else None
                    )

                except:

                    link=None




                products.append({

                    "title":title,

                    "price":clean_price(price),

                    "rating":4.0,

                    "image":image,

                    "url":link,

                    "site":"flipkart"

                })



            except Exception as e:

                print(
                    "Card error:",
                    e
                )




        browser.close()



    pprint(products)

    return products