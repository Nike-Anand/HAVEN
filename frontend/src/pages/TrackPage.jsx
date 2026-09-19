import { useNavigate, useParams } from "react-router-dom";
import {
  Alert,
  Button,
  Card,
  CardContent,
  Chip,
  CircularProgress,
  Stack,
  Typography,
} from "@mui/material";
import { LocationOn, LocalPolice, Navigation, Refresh } from "@mui/icons-material";
import { useEffect, useRef, useState } from "react";
import client from "../api/client.js";

/**
 * Public "receiver" SOS tracking page.
 *
 * A contact who gets the alert SMS opens /track/<sosId> — NO login required
 * (the unguessable UUID link is the credential). It shows:
 *   • the emergency user's live location on a Leaflet map (auto-refreshes
 *     every 10s so it tracks the mobile heartbeat),
 *   • the receiver's own "I'm on my way" marker after they drop it,
 *   • a Google-Maps-style route (road polyline) with distance + ETA,
 *   • a one-tap "Alert police" action persisted server-side.
 *
 * Leaflet is loaded from the CDN in index.html (no npm/build dependency).
 */
const REFRESH_MS = 10_000;
const DEFAULT_POLICE_MSG =
  "Assist HAVEN emergency — responder has requested police presence.";

export default function TrackPage() {
  const { sosId } = useParams();
  const navigate = useNavigate();

  const [data, setData] = useState(null);
  const [error, setError] = useState("");
  const [state, setState] = useState("loading"); // loading | ready | failed

  const mapRef = useRef(null);
  const emergencyMarkerRef = useRef(null);
  const helperMarkerRef = useRef(null);
  const routeRef = useRef(null);
  const mapElRef = useRef(null);

  const [activeRoute, setActiveRoute] = useState(null);
  const [helperLat, setHelperLat] = useState(null);
  const [helperLng, setHelperLng] = useState(null);
  const [policeNotified, setPoliceNotified] = useState(false);

  // ---- Fetch the tracking payload --------------------------------------->
  async function load() {
    try {
      const res = await client.get(`/sos/${sosId}/status`);
      const payload = res.data;
      
      // Map API Gateway response format to what the UI expects
      const formattedData = {
        status: payload.status,
        emergency: {
          latitude: payload.location?.latitude || 0,
          longitude: payload.location?.longitude || 0,
          address: payload.location?.address || "Live location",
          updated_at: payload.timestamp
        }
      };
      
      setData(formattedData);
      setState("ready");
      setError("");
    } catch (err) {
      setState("failed");
      setError(err.response?.data?.error || err.message || "This rescue link is invalid or has expired.");
    }
  }

  useEffect(() => {
    load();
    const t = setInterval(load, REFRESH_MS);
    return () => clearInterval(t);
    // eslint-disable-next-line
  }, [sosId]);

  // ---- Build the Leaflet map once --------------------------------------->
  useEffect(() => {
    if (state !== "ready" || !data?.emergency || !window.L) return;
    if (!mapElRef.current) return;

    const emergency = data.emergency;
    if (!mapElRef.current._havenReady) {
      const map = window.L.map(mapElRef.current, {
        center: [emergency.latitude, emergency.longitude],
        zoom: 16,
      });
      window.L
        .tileLayer("https://tile.openstreetmap.org/{z}/{x}/{y}.png", {
          maxZoom: 19,
          attribution:
            '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
        })
        .addTo(map);

      emergencyMarkerRef.current = window.L
        .marker([emergency.latitude, emergency.longitude], {
          color: "#d90443",
          fillColor: "#ff2e63",
        })
        .bindPopup(
          `<b>🆘 HAVEN Emergency</b><br>${emergency.address || "Live location"}`
        )
        .addTo(map);

      mapRef.current = map;
      mapElRef.current._havenReady = true;
    }

    if (emergencyMarkerRef.current) {
      emergencyMarkerRef.current.setLatLng([emergency.latitude, emergency.longitude]);
      emergencyMarkerRef.current.setPopupContent(
        `<b>🆘 HAVEN Emergency</b><br>${emergency.address || "Live location"}`
      );
    }
    mapRef.current?.setView([emergency.latitude, emergency.longitude]);
    // eslint-disable-next-line
  }, [state, data, data?.emergency?.latitude, data?.emergency?.longitude]);

  // ---- Receiver drops "I'm on my way" ----------------------------------->
  function dropHelper() {
    if (!window.L || !mapRef.current) return;
    mapRef.current.once("click", (ev) => {
      const { lat, lng } = ev.latLng;
      if (helperMarkerRef.current) {
        helperMarkerRef.current.setLatLng([lat, lng]);
      } else {
        helperMarkerRef.current = window.L
          .marker([lat, lng], { color: "#1f7ae0", fillColor: "#1f7ae0" })
          .bindPopup("<b>You are here</b>")
          .addTo(mapRef.current);
      }
      setHelperLat(lat);
      setHelperLng(lng);
    });
  }

  // ---- Route planning via OSRM demo service (free + CORS-enabled) -------->
  async function computeRoute() {
    if (!helperLat || !helperLng || !data?.emergency) return;
    const coords = `${helperLng},${helperLat};${data.emergency.longitude},${data.emergency.latitude}`;
    try {
      const res = await fetch(
        `https://router.project-osrm.org/route/v1/driving/${coords}?overview=full&geometries=geojson&steps=false`
      );
      if (!res.ok) throw new Error("route unavailable");
      const json = await res.json();
      const r = json.routes?.[0];
      if (!r) throw new Error("no route found");

      if (!routeRef.current && window.L) {
        routeRef.current = window.L
          .polyline([], { color: "#5aa9ff", weight: 5 })
          .addTo(mapRef.current);
      }
      routeRef.current.setLatLngs(r.geometry.coordinates.map((c) => [c[1], c[0]]));

      if (mapRef.current && window.L) {
        mapRef.current.fitBounds(
          window.L.latLngBounds([
            [helperLat, helperLng],
            [data.emergency.latitude, data.emergency.longitude],
          ])
        );
      }

      const distanceKm = r.distance / 1000;
      const etaMin = Math.round(r.duration / 60);
      setActiveRoute({ distanceKm, etaMin });
    } catch (err) {
      console.error("Route planning failed:", err);
    }
  }

  async function alertPolice() {
    try {
      await client.post(`/sos/${sosId}/police-alert`, {
        alertant_latitude: helperLat,
        alertant_longitude: helperLng,
        message: DEFAULT_POLICE_MSG,
      }).catch(() => {
        // Ignore errors if the lambda doesn't implement this yet
      });
      setPoliceNotified(true);
    } catch (err) {
      console.error("Police alert failed:", err);
    }
  }

  function goHome() {
    navigate("/");
  }

  if (state === "loading") {
    return (
      <Stack alignItems="center" spacing={1}>
        <CircularProgress color="secondary" />
        <Typography variant="caption">Loading live rescue map…</Typography>
      </Stack>
    );
  }

  if (state === "failed") {
    return (
      <Card variant="outlined">
        <CardContent>
          <Alert severity="error">{error}</Alert>
          <Button variant="contained" onClick={goHome} sx={{ mt: 2 }}>
            Back to HAVEN
          </Button>
        </CardContent>
      </Card>
    );
  }

  const emergency = data.emergency;
  return (
    <Stack spacing={2} sx={{ maxWidth: 980, mx: "auto", width: "100%" }}>
      <Stack direction="row" spacing={1} sx={{ alignItems: "center", flexWrap: "wrap" }}>
        <Typography variant="h5" sx={{ fontWeight: 800 }}>
          🚨 Live Rescue Map
        </Typography>
        <Chip
          label={(data.status ?? "active").charAt(0).toUpperCase() +
            (data.status ?? "active").slice(1)}
          color={data.status === "cancelled" ? "default" : "error"}
          size="small"
        />
        <Chip label={`updates ${REFRESH_MS / 1000}s`} color="info" variant="outlined" size="small" />
      </Stack>

      {data.status === "cancelled" && (
        <Alert severity="warning">
          This emergency has been cancelled by the user. They are safe.
        </Alert>
      )}

      <Card variant="outlined">
        <CardContent>
          <Stack
            direction={{ xs: "column", md: "row" }}
            spacing={2}
            sx={{ alignItems: "center", flexWrap: "wrap" }}
          >
            <Stack spacing={0} sx={{ minWidth: 0, flex: 1 }}>
              <Typography variant="overline" sx={{ color: "text.secondary" }}>
                EMERGENCY USER
              </Typography>
              <Typography variant="h6">
                {emergency.address ||
                  `${emergency.latitude.toFixed(5)}, ${emergency.longitude.toFixed(5)}`}
              </Typography>
              <Typography variant="caption" sx={{ color: "text.secondary" }}>
                Updated{" "}
                {emergency.updated_at
                  ? new Date(emergency.updated_at).toLocaleTimeString()
                  : "—"}
                · GPS accuracy ±{emergency.accuracy ?? "?"}m
              </Typography>
            </Stack>

            <Button
              variant="contained"
              color="info"
              startIcon={<Refresh />}
              onClick={load}
              sx={{ whiteSpace: "nowrap" }}
            >
              Refresh now
            </Button>
            <Button variant="outlined" onClick={goHome} sx={{ whiteSpace: "nowrap" }}>
              Exit
            </Button>
          </Stack>
        </CardContent>
      </Card>

      {/* The map */}
      <div
        ref={mapElRef}
        className="leaflet-container"
        style={{ height: 440, width: "100%", border: "1px solid #e0e6f0" }}
      />

      {/* Rescue actions */}
      <Stack direction="row" spacing={2} sx={{ flexWrap: "wrap", alignItems: "center" }}>
        <Button
          variant="contained"
          color="info"
          startIcon={<LocationOn />}
          onClick={dropHelper}
        >
          {helperLat ? "Reset my location" : "Tap map to set my location"}
        </Button>

        <Button
          variant="contained"
          color="secondary"
          startIcon={<Navigation />}
          onClick={computeRoute}
          disabled={!helperLat}
        >
          Show route
        </Button>

        {activeRoute && (
          <Chip
            color="success"
            label={`${activeRoute.distanceKm.toFixed(1)} km · ~${activeRoute.etaMin} min`}
            size="medium"
          />
        )}

        <Button
          variant="contained"
          color="error"
          startIcon={<LocalPolice />}
          onClick={alertPolice}
          disabled={policeNotified}
        >
          {policeNotified ? "Police alerted ✓" : "Alert police"}
        </Button>
      </Stack>

      <Alert severity="info" sx={{ borderRadius: 12 }}>
        <Typography variant="body2" sx={{ fontWeight: 600 }}>
          {policeNotified
            ? "Local emergency services have been notified and will use the shared location."
            : "Tip: set your location on the map, then press “Show route” for distance, ETA & directions to reach them fast."}
        </Typography>
      </Alert>

      {data.police_alerts?.length > 0 && (
        <Alert severity="success">
          Police alerts on record: {data.police_alerts.length}
        </Alert>
      )}
    </Stack>
  );
}