import requests
from django.conf import settings

API_KEY = settings.SERPAPI_KEY


def serpapi_fallback(query, site):
    url = "https://serpapi.com/search"

    params = {
        "engine": "google_shopping",
        "q": query,
        "gl": "in",
        "hl": "en",
        "api_key": API_KEY,
    }

    try:
        response = requests.get(url, params=params, timeout=10)
        data = response.json()

        products = []

        for item in data.get("shopping_results", []):

            source = item.get("source", "").lower()

            if site.lower() not in source:
                continue

            products.append({
                "title": item.get("title"),
                "price": item.get("extracted_price"),
                "rating": item.get("rating"),
                "image": item.get("thumbnail"),
                "url": item.get("product_link"),
                "site": site,
            })

        return products

    except Exception as e:
        print(e)
        return []