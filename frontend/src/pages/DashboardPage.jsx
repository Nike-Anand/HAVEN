import {
  Card,
  CardContent,
  Chip,
  Grid,
  Stack,
  Typography,
} from "@mui/material";
import { ContactEmergency, Gavel, HealthAndSafety, LockReset } from "@mui/icons-material";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";

import { triggerSOS } from "../store/slices/sosSlice.js";
import SOSButton from "../components/SOSButton.jsx";

const QUICK_ACTIONS = [
  { to: "/therapy", title: "AI Therapy", desc: "Talk to our crisis bot", icon: HealthAndSafety },
  { to: "/legal", title: "Legal Aid", desc: "Know your rights", icon: Gavel },
  { to: "/contacts", title: "Contacts", desc: "Manage your network", icon: ContactEmergency },
  { to: "/profile", title: "Profile & Safety", desc: "Update your safety settings", icon: LockReset },
];

export default function DashboardPage() {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const user = useSelector((s) => s.auth.user);
  const name = user?.name || "friend";

  async function handleSOS(location) {
    try {
      const { payload } = await dispatch(triggerSOS(location));
      navigate(`/sos/${payload.sos_id}`);
    } catch {
      // API errors are handled globally.
    }
  }

  return (
    <Stack spacing={3} sx={{ maxWidth: 1200, mx: "auto" }}>
      <Stack spacing={0.5}>
        <Typography variant="h4" sx={{ fontWeight: 800 }}>
          Welcome, {name}
        </Typography>
        <Typography variant="body1" sx={{ color: "text.secondary" }}>
          One discreet press connects you to your network, a counselor, and the law.
        </Typography>
      </Stack>

      <Card
        variant="outlined"
        sx={{
          background: "linear-gradient(135deg, rgba(255,46,99,0.08), rgba(124,58,237,0.08))",
          border: "1px solid rgba(255,46,99,0.15)",
          borderRadius: 4,
          overflow: "hidden",
        }}
      >
        <CardContent sx={{ p: { xs: 2, sm: 3 } }}>
          <Typography variant="h6" sx={{ fontWeight: 800, color: "error.main", mb: 2 }}>
            Emergency
          </Typography>
          <SOSButton onActivated={handleSOS} />
          <Chip
            label="Discreet • location-shared • contacts alerted"
            sx={{ mt: 2, background: "rgba(255,46,99,0.08)", color: "#8c153f" }}
          />
        </CardContent>
      </Card>

      <Grid container spacing={2}>
        {QUICK_ACTIONS.map(({ to, title, desc, icon: Icon }) => (
          <Grid key={to} item xs={12} sm={6} md={4}>
            <Card
              variant="outlined"
              sx={{
                cursor: "pointer",
                height: "100%",
                borderRadius: 3,
                background: "linear-gradient(180deg, rgba(255,255,255,0.96), rgba(246,245,255,0.96))",
                transition: "transform 0.2s ease, box-shadow 0.2s ease",
                "&:hover": { transform: "translateY(-2px)", boxShadow: "0 12px 28px rgba(124,58,237,0.12)" },
              }}
              onClick={() => navigate(to)}
            >
              <CardContent sx={{ p: 2.5 }}>
                <Icon sx={{ fontSize: 38, color: "primary.main", mb: 1.5 }} />
                <Typography variant="h6" sx={{ fontWeight: 700 }}>{title}</Typography>
                <Typography variant="body2" sx={{ color: "text.secondary", mt: 0.5 }}>{desc}</Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Stack>
  );
}