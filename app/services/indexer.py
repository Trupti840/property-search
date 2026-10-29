from opensearchpy import OpenSearch, helpers
from sqlalchemy import select
from app.core.config import settings
from app.db.models import Property
from app.db.session import SessionLocal

INDEX = "properties"
POSSESSION = {0: "ready_to_move", 1: "under_construction"}

MAPPING = {
    "settings": {
        "index": {"number_of_shards": 1, "number_of_replicas": 0},
        "analysis": {
            "normalizer": {"lc": {"type": "custom", "filter": ["lowercase"]}}
        },
    },
    "mappings": {
        "properties": {
            "id": {"type": "long"},
            "title": {"type": "text"},
            "description": {"type": "text"},
            "locality": {"type": "keyword", "normalizer": "lc"},
            "city": {"type": "keyword", "normalizer": "lc"},
            "bhk": {"type": "integer"},
            "price": {"type": "long"},
            "area_sqft": {"type": "integer"},
            "parking": {"type": "boolean"},
            "possession": {"type": "keyword"},
            "amenities": {"type": "keyword", "normalizer": "lc"},
        }
    },
}


def get_client() -> OpenSearch:
    return OpenSearch(hosts=[settings.opensearch_url])


def _docs():
    with SessionLocal() as db:
        for p in db.scalars(select(Property).execution_options(yield_per=500)):
            yield {
                "_index": INDEX,
                "_id": p.id,
                "_source": {
                    "id": p.id,
                    "title": p.title,
                    "description": p.description,
                    "locality": p.locality,
                    "city": p.city,
                    "bhk": p.bhk,
                    "price": p.price,
                    "area_sqft": p.area_sqft,
                    "parking": p.parking,
                    "possession": POSSESSION.get(p.possession_status),
                    "amenities": p.amenities,
                },
            }


def reindex() -> int:
    client = get_client()
    if client.indices.exists(index=INDEX):
        client.indices.delete(index=INDEX)
    client.indices.create(index=INDEX, body=MAPPING)
    ok, _ = helpers.bulk(client, _docs())
    client.indices.refresh(index=INDEX)
    return ok


if __name__ == "__main__":
    print("Indexed", reindex(), "documents")
