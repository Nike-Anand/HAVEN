"""Map-related helper endpoints (Directions proxy to Mapbox)."""
import os
from fastapi import APIRouter, HTTPException, Query
import httpx

from .. import config

router = APIRouter(prefix="/maps", tags=["maps"])


@router.get("/directions")
async def directions(orig_lat: float = Query(...), orig_lng: float = Query(...), dest_lat: float = Query(...), dest_lng: float = Query(...)):
    """Proxy to Mapbox Directions API and return GeoJSON coordinates.

    Expects server env var `MAPBOX_TOKEN` to be set.
    """
    token = os.environ.get("MAPBOX_TOKEN") or config.MAPBOX_TOKEN
    if not token:
        raise HTTPException(status_code=503, detail="Mapbox token not configured")

    url = (
        f"https://api.mapbox.com/directions/v5/mapbox/driving/"
        f"{orig_lng},{orig_lat};{dest_lng},{dest_lat}"
    )
    params = {
        "geometries": "geojson",
        "overview": "full",
        "access_token": token,
    }

    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(url, params=params)
    if r.status_code != 200:
        raise HTTPException(status_code=502, detail="Mapbox error")
    data = r.json()
    if not data.get("routes"):
        raise HTTPException(status_code=404, detail="No route found")
    geometry = data["routes"][0]["geometry"]
    return {"geometry": geometry}
