from app.services.indexer import INDEX, get_client


def search_properties(
    q: str | None = None,
    locality: str | None = None,
    bhk: int | None = None,
    min_price: int | None = None,
    max_price: int | None = None,
    parking: bool | None = None,
    possession: str | None = None,
    size: int = 20,
) -> dict:
    filters = []
    if locality:
        filters.append({"term": {"locality": locality}})
    if bhk:
        filters.append({"term": {"bhk": bhk}})
    if parking is not None:
        filters.append({"term": {"parking": parking}})
    if possession:
        filters.append({"term": {"possession": possession}})
    if min_price or max_price:
        rng = {}
        if min_price:
            rng["gte"] = min_price
        if max_price:
            rng["lte"] = max_price
        filters.append({"range": {"price": rng}})

    must = (
        [{"multi_match": {"query": q, "fields": ["title^2", "description", "amenities"]}}]
        if q
        else [{"match_all": {}}]
    )
    body = {"size": size, "query": {"bool": {"must": must, "filter": filters}}}

    res = get_client().search(index=INDEX, body=body)
    hits = [{**h["_source"], "score": h["_score"]} for h in res["hits"]["hits"]]
    return {"total": res["hits"]["total"]["value"], "results": hits}
