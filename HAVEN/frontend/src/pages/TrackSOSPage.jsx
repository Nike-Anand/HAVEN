import { useEffect, useState } from "react";
import { useParams, useNavigate } from "react-router-dom";
import {
  Box,
  Button,
  Card,
  CardContent,
  Chip,
  CircularProgress,
  Container,
  Divider,
  Grid,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Paper,
  Stack,
  Typography,
} from "@mui/material";
import {
  Directions,
  DirectionsRun,
  LocationOn,
  Map as MapIcon,
  Shield,
  Warning,
} from "@mui/icons-material";
import axios from "axios";

export default function TrackSOSPage() {
  const { sosId } = useParams();
  const navigate = useNavigate();
  const [sosData, setSosData] = useState(null);
  const [routeData, setRouteData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [myPos, setMyPos] = useState({ lat: 12.9249, lng: 80.2000 });
  const [ackStatus, setAckStatus] = useState(null);

  useEffect(() => {
    if (navigator.geolocation) {
      navigator.geolocation.getCurrentPosition(
        (pos) => {
          setMyPos({ lat: pos.coords.latitude, lng: pos.coords.longitude });
        },
        () => {}
      );
    }
  }, []);

  const fetchSOS = async () => {
    try {
      const res = await axios.get(`/sos/${sosId}/track`);
      setSosData(res.data);
      if (res.data.latitude && res.data.longitude) {
        fetchRoute(res.data.latitude, res.data.longitude);
      }
    } catch (e) {
      console.error("Failed to load SOS track:", e);
    } finally {
      setLoading(false);
    }
  };

  const fetchRoute = async (destLat, destLng) => {
    try {
      const res = await axios.get(
        `/maps/directions?orig_lat=${myPos.lat}&orig_lng=${myPos.lng}&dest_lat=${destLat}&dest_lng=${destLng}`
      );
      setRouteData(res.data);
    } catch (e) {
      console.error("Failed to fetch directions:", e);
    }
  };

  useEffect(() => {
    fetchSOS();
    const interval = setInterval(fetchSOS, 4000);
    return () => clearInterval(interval);
  }, [sosId]);

  const handleAcknowledge = async (code) => {
    try {
      await axios.post(`/sos/${sosId}/respond?contact_id=contact_b&response=${code}`);
      setAckStatus(code);
    } catch (e) {
      console.error("Ack failed:", e);
    }
  };

  if (loading) {
    return (
      <Container sx={{ py: 8, textAlign: "center" }}>
        <CircularProgress color="error" />
        <Typography sx={{ mt: 2 }}>Loading live SOS telemetry...</Typography>
      </Container>
    );
  }

  if (!sosData) {
    return (
      <Container sx={{ py: 8, textAlign: "center" }}>
        <Typography variant="h5" color="error">
          SOS Alert Not Found or Expired
        </Typography>
        <Button sx={{ mt: 2 }} variant="outlined" onClick={() => navigate("/")}>
          Return Home
        </Button>
      </Container>
    );
  }

  const distanceKm = routeData?.distance ? (routeData.distance / 1000).toFixed(2) : "--";
  const durationMins = routeData?.duration ? Math.round(routeData.duration / 60) : "--";
  const mapsUrl = `https://www.google.com/maps/dir/?api=1&destination=${sosData.latitude},${sosData.longitude}`;

  return (
    <Container maxWidth="lg" sx={{ py: 4 }}>
      <Paper
        sx={{
          p: 3,
          mb: 3,
          bgcolor: "#b91c1c",
          color: "white",
          borderRadius: 3,
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          flexWrap: "wrap",
          gap: 2,
        }}
      >
        <Box display="flex" alignItems="center" gap={2}>
          <Warning sx={{ fontSize: 44, color: "#fef08a" }} />
          <Box>
            <Typography variant="h5" sx={{ fontWeight: "bold" }}>
              CRISIS SOS ACTIVE: {sosData.user_email}
            </Typography>
            <Typography variant="body2" sx={{ opacity: 0.9 }}>
              Triggered at {new Date(sosData.timestamp).toLocaleTimeString()} • Status:{" "}
              {sosData.status.toUpperCase()}
            </Typography>
          </Box>
        </Box>
        <Stack direction="row" spacing={1.5}>
          <Button
            variant="contained"
            color="success"
            startIcon={<DirectionsRun />}
            onClick={() => handleAcknowledge("ON_WAY")}
            disabled={ackStatus === "ON_WAY"}
            sx={{ fontWeight: "bold" }}
          >
            {ackStatus === "ON_WAY" ? "Status Sent: On My Way" : "I'm On My Way"}
          </Button>
          <Button
            variant="contained"
            color="info"
            startIcon={<MapIcon />}
            component="a"
            href={mapsUrl}
            target="_blank"
            rel="noopener noreferrer"
            sx={{ fontWeight: "bold" }}
          >
            Google Maps
          </Button>
        </Stack>
      </Paper>

      <Grid container spacing={3}>
        <Grid item xs={12} md={7}>
          <Card variant="outlined" sx={{ borderRadius: 3, height: "100%" }}>
            <CardContent>
              <Typography variant="h6" sx={{ fontWeight: "bold", mb: 2, display: "flex", alignItems: "center", gap: 1 }}>
                <LocationOn color="error" /> Live Telemetry & GPS Route
              </Typography>

              <Box
                sx={{
                  width: "100%",
                  height: 380,
                  borderRadius: 2,
                  overflow: "hidden",
                  bgcolor: "#1e293b",
                  border: "1px solid #334155",
                  position: "relative",
                }}
              >
                <iframe
                  title="SOS Location Map"
                  width="100%"
                  height="100%"
                  frameBorder="0"
                  scrolling="no"
                  marginHeight="0"
                  marginWidth="0"
                  src={`https://www.openstreetmap.org/export/embed.html?bbox=${sosData.longitude - 0.01}%2C${sosData.latitude - 0.01}%2C${sosData.longitude + 0.01}%2C${sosData.latitude + 0.01}&layer=mapnik&marker=${sosData.latitude}%2C${sosData.longitude}`}
                />
              </Box>

              <Stack direction="row" spacing={2} sx={{ mt: 2 }}>
                <Chip
                  icon={<LocationOn />}
                  label={`GPS: ${sosData.latitude.toFixed(4)}, ${sosData.longitude.toFixed(4)}`}
                  color="error"
                  variant="outlined"
                />
                <Chip
                  label={`Distance: ${distanceKm} km`}
                  color="primary"
                  variant="filled"
                />
                <Chip
                  label={`Est. Arrival: ${durationMins} mins`}
                  color="success"
                  variant="filled"
                />
              </Stack>
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={5}>
          <Stack spacing={3}>
            <Card variant="outlined" sx={{ borderRadius: 3 }}>
              <CardContent>
                <Typography variant="h6" sx={{ fontWeight: "bold", mb: 1, display: "flex", alignItems: "center", gap: 1 }}>
                  <Directions color="primary" /> Navigation Route Instructions
                </Typography>
                <Typography variant="body2" color="text.secondary" sx={{ mb: 2 }}>
                  Optimal path generated by OSRM routing engine:
                </Typography>

                <List sx={{ maxHeight: 260, overflowY: "auto" }} dense>
                  {routeData?.steps && routeData.steps.length > 0 ? (
                    routeData.steps.map((step, idx) => (
                      <ListItem key={idx} sx={{ bgcolor: "#f8fafc", mb: 1, borderRadius: 1.5, border: "1px solid #e2e8f0" }}>
                        <ListItemIcon sx={{ minWidth: 32 }}>
                          <Chip size="small" label={idx + 1} color="primary" sx={{ height: 22, width: 22, p: 0 }} />
                        </ListItemIcon>
                        <ListItemText
                          primary={step}
                          primaryTypographyProps={{ fontSize: 13, fontWeight: 500 }}
                        />
                      </ListItem>
                    ))
                  ) : (
                    <Typography variant="body2" color="text.secondary">
                      Calculating optimal road route to destination...
                    </Typography>
                  )}
                </List>
              </CardContent>
            </Card>

            <Card variant="outlined" sx={{ borderRadius: 3, bgcolor: "#fef2f2", borderColor: "#fecaca" }}>
              <CardContent>
                <Typography variant="subtitle1" sx={{ fontWeight: "bold", color: "#991b1b", mb: 1, display: "flex", alignItems: "center", gap: 1 }}>
                  <Shield /> Rapid Emergency Helplines
                </Typography>
                <Stack spacing={1}>
                  <Box display="flex" justifyContent="space-between">
                    <Typography variant="body2" fontWeight="bold">112</Typography>
                    <Typography variant="body2" color="text.secondary">All-India Emergency</Typography>
                  </Box>
                  <Divider />
                  <Box display="flex" justifyContent="space-between">
                    <Typography variant="body2" fontWeight="bold">1091</Typography>
                    <Typography variant="body2" color="text.secondary">Women in Distress Helpline</Typography>
                  </Box>
                  <Divider />
                  <Box display="flex" justifyContent="space-between">
                    <Typography variant="body2" fontWeight="bold">181</Typography>
                    <Typography variant="body2" color="text.secondary">Women Helpline (Domestic Violence)</Typography>
                  </Box>
                </Stack>
              </CardContent>
            </Card>
          </Stack>
        </Grid>
      </Grid>
    </Container>
  );
}
