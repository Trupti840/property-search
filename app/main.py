from fastapi import Depends, FastAPI, HTTPException, Query
from sqlalchemy import select
from sqlalchemy.orm import Session
from app.db.models import Property
from app.db.session import get_db
from app.api.search import router as search_router
from app.api.search import router as search_router

app = FastAPI(title="Property Search")
app.include_router(search_router)
app.include_router(search_router)

POSSESSION = {0: "ready_to_move", 1: "under_construction"}

def to_dict(p: Property) -> dict:
    return {
        "id": p.id, "title": p.title, "locality": p.locality, "bhk": p.bhk,
        "price": p.price, "area_sqft": p.area_sqft, "parking": p.parking,
        "possession": POSSESSION.get(p.possession_status), "amenities": p.amenities,
    }

@app.get("/health")
def health():
    return {"status": "ok"}

@app.get("/properties/{property_id}")
def get_property(property_id: int, db: Session = Depends(get_db)):
    p = db.get(Property, property_id)
    if not p:
        raise HTTPException(404, "Property not found")
    return to_dict(p)

@app.get("/properties")
def list_properties(
    locality: str | None = None, bhk: int | None = None,
    max_price: int | None = None, parking: bool | None = None,
    limit: int = Query(20, le=100), db: Session = Depends(get_db),
):
    q = select(Property)
    if locality: q = q.where(Property.locality.ilike(locality))
    if bhk: q = q.where(Property.bhk == bhk)
    if max_price: q = q.where(Property.price <= max_price)
    if parking is not None: q = q.where(Property.parking == parking)
    return [to_dict(p) for p in db.scalars(q.limit(limit))]
