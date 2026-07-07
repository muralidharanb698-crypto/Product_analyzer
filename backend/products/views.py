from concurrent.futures import ThreadPoolExecutor
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .amazon_scrap import amazon_scrape
from .filpkart_scarp import flipkart_scrape
from .messho_scrap import meesho_scrape
from .ajio_scarp import ajio_scrape
from .seri_api import serpapi_fallback

from .matcher import get_best_match

from .search_manager import (
    create_search,
    update_site,
    update_error,
    get_search
)

SCRAPERS = {
    "amazon": amazon_scrape,
    "flipkart": flipkart_scrape,
    "meesho": meesho_scrape,
    "ajio": ajio_scrape,
}


def run_scraper(search_id, site, scraper, product):
    try:
        print(f"Starting {site} scraper...")

        result = scraper(product)

        # Scraper returned no products
        if not result:
            print(f"{site} returned no results. Using SerpApi...")
            result = serpapi_fallback(product, site)

        if result:
            update_site(search_id, site, result)
            print(f"{site} completed")
        else:
            update_error(search_id, site, "No products found")
            print(f"{site} no products found")

    except Exception as e:
        print(f"{site} scraper failed: {e}")
        print(f"Trying SerpApi for {site}...")

        try:
            result = serpapi_fallback(product, site)

            if result:
                update_site(search_id, site, result)
                print(f"{site} completed using SerpApi")
            else:
                update_error(search_id, site, "No products found")
                print(f"{site} no products found even with SerpApi")

        except Exception as serp_error:
            update_error(search_id, site, str(serp_error))
            print(f"{site} SerpApi failed:", serp_error)


@api_view(["GET"])
def start_search(request):
    product = request.query_params.get("q")

    if not product:
        return Response(
            {"error": "Missing query parameter 'q'"},
            status=400
        )

    search_id = create_search(product)

    executor = ThreadPoolExecutor(max_workers=len(SCRAPERS))

    for site, scraper in SCRAPERS.items():
        executor.submit(
            run_scraper,
            search_id,
            site,
            scraper,
            product
        )

    return Response({
        "search_id": search_id
    })


@api_view(["GET"])
def search_status(request, search_id):

    result = get_search(search_id)

    if result is None:
        return Response(
            {"error": "Invalid search id"},
            status=404
        )

    completed = all(
        result[site]["status"] in ["done", "error"]
        for site in ["amazon", "flipkart", "ajio", "meesho"]
    )

  
    response = result.copy()

    if completed:

        comparison = []

        search_query = result["query"]

        for site in ["amazon", "flipkart", "ajio", "meesho"]:

            if result[site]["status"] != "done":
                continue

            products = result[site]["data"]

            if not products:
                continue

            best = get_best_match(products, search_query)

            if best:
                comparison.append(best)

        response["comparison"] = comparison

    return Response(response)