from playwright.sync_api import sync_playwright
from urllib.parse import quote
from pprint import pprint
import re



def clean_price(raw):

    if not raw:
        return None

    numbers = re.findall(
        r"\d+",
        raw.replace(",", "")
    )

    return int(numbers[0]) if numbers else None




def ajio_scrape(product, max_results=5):

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
                f"https://www.ajio.com/search/?text={quote(product)}"
            )


            print("Opening:",url)


            page.goto(
                url,
                wait_until="networkidle",
                timeout=30000
            )


            page.wait_for_timeout(5000)



        except Exception as e:

            print(
                "Ajio navigation error:",
                e
            )

            browser.close()

            return []




        print("URL:",page.url)

        print("TITLE:",page.title())




        # Product cards

        selectors = [

            "div.item",

            "div.rilrtl-products-list",

            "div.product-card",

            "div[class*='item']"

        ]



        cards=None



        for selector in selectors:

            try:

                page.wait_for_selector(
                    selector,
                    timeout=5000
                )

                cards = page.locator(selector)

                if cards.count()>0:

                    break


            except:

                pass




        if not cards:


            print(
                "No Ajio products found"
            )

            browser.close()

            return []




        count = cards.count()


        print(
            "Ajio products found:",
            count
        )




        for i in range(
            min(count,max_results)
        ):


            try:


                card = cards.nth(i)



                # Title

                title = None



                try:

                    title = card.locator(
                        "div.brand"
                    ).inner_text(timeout=1000)


                except:

                    pass



                try:

                    name = card.locator(
                        "div.nameCls"
                    ).inner_text(timeout=1000)


                    if name:

                        title = (
                            title + " " + name
                            if title else name
                        )


                except:

                    pass




                if not title:


                    try:

                        title = card.inner_text(
                            timeout=1000
                        )

                    except:

                        continue




                # Price


                price=None


                try:

                    price = card.locator(
                        "div.price"
                    ).inner_text(timeout=1000)


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


                    if href and href.startswith("/"):

                        link = (
                            "https://www.ajio.com"
                            + href
                        )

                    else:

                        link=href


                except:

                    link=None





                products.append({

                    "title":title.strip(),

                    "price":clean_price(price),

                    "rating":4.0,

                    "image":image,

                    "url":link,

                    "site":"ajio"

                })



            except Exception as e:

                print(
                    "Ajio card error:",
                    e
                )



        browser.close()



    pprint(products)

    return products




if __name__ == "__main__":


    product=input(
        "Enter product: "
    )


    pprint(
        ajio_scrape(product)
    )