from fastapi import APIRouter, Query
from app.services.indexer import reindex
from app.services.search import search_properties

router = APIRouter()


@router.get("/search")
def search(
    q: str | None = None,
    locality: str | None = None,
    bhk: int | None = None,
    min_price: int | None = None,
    max_price: int | None = None,
    parking: bool | None = None,
    possession: str | None = None,
    size: int = Query(20, le=100),
):
    return search_properties(q, locality, bhk, min_price, max_price, parking, possession, size)


@router.post("/admin/reindex")
def admin_reindex():
    return {"indexed": reindex()}
