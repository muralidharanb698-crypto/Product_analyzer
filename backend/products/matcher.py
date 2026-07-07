from rapidfuzz import fuzz


def get_best_match(products, search_query, threshold=60):

    if not products:
        return None

    search_query = search_query.lower().strip()

    best_product = None
    best_score = 0

    accessories = [
        "bag", "cover", "case", "stand", "sleeve",
        "mouse", "keyboard", "charger", "adapter",
        "toy", "polish", "lace", "laces", "rack",
        "cleaner", "cream", "spray", "sock", "socks"
    ]

    for product in products:

        title = product["title"].lower()

        score = (
            fuzz.token_set_ratio(search_query, title) * 0.5 +
            fuzz.partial_ratio(search_query, title) * 0.3 +
            fuzz.token_sort_ratio(search_query, title) * 0.2
        )

        # Bonus if every search word exists
        if all(word in title for word in search_query.split()):
            score += 20

        # Penalize accessories
        if any(word in title for word in accessories):
            score -= 25

        # Bonus for real product keywords
        if any(word in title for word in [
            "shoe", "shoes", "sneaker", "running",
            "sports", "boot", "loafer", "slipper",
            "sandals", "heels"
        ]) and "shoe" in search_query:
            score += 15

        if any(word in title for word in [
            "laptop", "notebook", "macbook", "vivobook",
            "thinkpad", "vostro", "ideapad"
        ]) and "laptop" in search_query:
            score += 15

        if score > best_score:
            best_score = score
            best_product = product

    print(best_score)

    return best_product if best_score >= threshold else None