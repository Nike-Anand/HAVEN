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
    token = os.environ.get("MAPBOX_TOKEN") or getattr(config, "MAPBOX_TOKEN", None)
    
    # 1. Try Mapbox if token is provided
    if token:
        try:
            url = (
                f"https://api.mapbox.com/directions/v5/mapbox/driving/"
                f"{orig_lng},{orig_lat};{dest_lng},{dest_lat}"
            )
            params = {
                "geometries": "geojson",
                "overview": "full",
                "steps": "true",
                "access_token": token,
            }
            async with httpx.AsyncClient(timeout=8) as client:
                r = await client.get(url, params=params)
            if r.status_code == 200:
                data = r.json()
                if data.get("routes"):
                    route = data["routes"][0]
                    return {
                        "geometry": route.get("geometry", {}),
                        "distance": route.get("distance", 0),
                        "duration": route.get("duration", 0),
                        "steps": [
                            step.get("maneuver", {}).get("instruction", "")
                            for leg in route.get("legs", [])
                            for step in leg.get("steps", [])
                            if step.get("maneuver", {}).get("instruction")
                        ],
                        "source": "mapbox"
                    }
        except Exception:
            pass

    # 2. Try Open Source Routing Machine (OSRM) - free public routing engine
    try:
        osrm_url = (
            f"https://router.project-osrm.org/route/v1/driving/"
            f"{orig_lng},{orig_lat};{dest_lng},{dest_lat}?overview=full&geometries=geojson&steps=true"
        )
        async with httpx.AsyncClient(timeout=8) as client:
            r = await client.get(osrm_url)
        if r.status_code == 200:
            data = r.json()
            if data.get("routes"):
                route = data["routes"][0]
                steps = []
                for leg in route.get("legs", []):
                    for step in leg.get("steps", []):
                        maneuver = step.get("maneuver", {})
                        instruction = f"{maneuver.get('type', 'proceed')} on {step.get('name') or 'road'}"
                        steps.append(instruction)
                return {
                    "geometry": route.get("geometry", {}),
                    "distance": route.get("distance", 0),
                    "duration": route.get("duration", 0),
                    "steps": steps,
                    "source": "osrm"
                }
    except Exception:
        pass

    # 3. Fallback direct interpolated route (straight line with intermediate points)
    num_pts = 10
    coords = []
    for i in range(num_pts + 1):
        frac = i / float(num_pts)
        lng = orig_lng + (dest_lng - orig_lng) * frac
        lat = orig_lat + (dest_lat - orig_lat) * frac
        coords.append([lng, lat])

    # Approximate distance using Haversine formula
    import math
    dlat = math.radians(dest_lat - orig_lat)
    dlng = math.radians(dest_lng - orig_lng)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(orig_lat)) * math.cos(math.radians(dest_lat)) * math.sin(dlng/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    dist_meters = 6371000 * c

    return {
        "geometry": {
            "type": "LineString",
            "coordinates": coords
        },
        "distance": round(dist_meters, 1),
        "duration": round(dist_meters / 8.33, 1), # ~30 km/h driving speed
        "steps": [
            f"Head towards destination ({round(dist_meters / 1000, 2)} km)",
            "Follow active tracking coordinates until arrival"
        ],
        "source": "fallback"
    }

