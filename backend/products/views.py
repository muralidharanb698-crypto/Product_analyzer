from concurrent.futures import ThreadPoolExecutor
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .amazon_scrap import amazon_scrape
from .filpkart_scarp import flipkart_scrape
from .messho_scrap import meesho_scrape
from .ajio_scarp import ajio_scrape

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
        result = scraper(product)
        update_site(search_id, site, result)
        print(f"{site} completed")
    except Exception as e:
        update_error(search_id, site, str(e))
        print(f"{site} error:", e)


@api_view(["GET"])
def start_search(request):
    product = request.query_params.get("q")

    if not product:
        return Response({"error": "Missing query parameter 'q'"}, status=400)

    search_id = create_search()

    executor = ThreadPoolExecutor(max_workers=len(SCRAPERS))

    for site, scraper in SCRAPERS.items():
        executor.submit(run_scraper, search_id, site, scraper, product)

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

    return Response(result)