import re
from urllib.parse import quote
from pprint import pprint
from playwright.sync_api import sync_playwright



def clean_price(raw):

    if not raw:
        return None

    numbers = re.findall(
        r"\d+",
        raw.replace(",", "")
    )

    return int(numbers[0]) if numbers else None



def clean_rating(raw):

    if not raw:
        return 4.0

    match = re.search(
        r"\d+\.\d+",
        raw
    )

    if match:
        return float(match.group())

    return 4.0



def safe_text(locator):

    try:

        text = locator.inner_text(
            timeout=1500
        )

        return text.strip()

    except:

        return ""




def meesho_scrape(product, max_results=5):

    products = []

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
                f"https://www.meesho.com/search?q={quote(product)}"
            )


            print("Opening:",url)


            page.goto(

                url,

                wait_until="networkidle",

                timeout=30000

            )


            page.wait_for_timeout(4000)



        except Exception as e:

            print(
                "Meesho navigation error:",
                e
            )

            browser.close()

            return []




        print(
            "URL:",
            page.url
        )


        print(
            "TITLE:",
            page.title()
        )




        # Product links

        cards = page.locator(
            'a[href*="/p/"]'
        )


        count = cards.count()


        print(
            "Meesho products found:",
            count
        )



        for i in range(
            min(count,max_results)
        ):


            try:


                card = cards.nth(i)



                # Title

                title=""



                possible_titles=[

                    "p",

                    "h3",

                    "div[title]",

                ]



                for selector in possible_titles:

                    try:

                        value = safe_text(
                            card.locator(selector).first
                        )

                        if len(value)>5:

                            title=value

                            break

                    except:

                        pass




                if not title:

                    continue




                # Price

                price=""



                try:

                    text = card.inner_text()

                    match = re.search(

                        r"₹\s?[\d,]+",

                        text

                    )

                    if match:

                        price=match.group()


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

                    href = card.get_attribute(
                        "href"
                    )


                    if href and href.startswith("/"):

                        link = (
                            "https://www.meesho.com"
                            + href
                        )

                    else:

                        link=href


                except:

                    link=None





                products.append({

                    "title":title,

                    "price":clean_price(price),

                    "rating":4.0,

                    "image":image,

                    "url":link,

                    "site":"meesho"

                })



            except Exception as e:

                print(
                    "Meesho card error:",
                    e
                )



        browser.close()



    pprint(products)

    return products





if __name__=="__main__":

    product=input(
        "Enter product: "
    )


    pprint(
        meesho_scrape(product)
    )