import {
  Card,
  CardContent,
  Chip,
  Grid,
  Stack,
  Typography,
} from "@mui/material";
import { ContactEmergency, Gavel, HealthAndSafety } from "@mui/icons-material";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";

import { triggerSOS } from "../store/slices/sosSlice.js";
import SOSButton from "../components/SOSButton.jsx";

const QUICK_ACTIONS = [
  { to: "/therapy", title: "AI Therapy", desc: "Talk to our crisis bot", icon: HealthAndSafety },
  { to: "/legal", title: "Legal Aid", desc: "Know your rights", icon: Gavel },
  { to: "/contacts", title: "Contacts", desc: "Manage your network", icon: ContactEmergency },
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
      /* apiError surfaces via the global 401 handler */
    }
  }

  return (
    <Stack spacing={3}>
      <Typography variant="h5" sx={{ fontWeight: 600 }}>
        Welcome, {name}
      </Typography>
      <Typography variant="body1" sx={{ color: "text.secondary" }}>
        One discreet press connects you to your network, a counselor, and the law.
      </Typography>

      <Card variant="outlined">
        <CardContent>
          <Typography variant="h6" sx={{ fontWeight: 700, color: "error.main" }}>
            Emergency
          </Typography>
          <SOSButton onActivated={handleSOS} />
          <Chip label="Discreet • location-shared • contacts alerted" sx={{ mt: 1 }} />
        </CardContent>
      </Card>

      <Grid container spacing={2}>
        {QUICK_ACTIONS.map(({ to, title, desc, icon: Icon }) => (
          <Grid item xs={12} sm={4} key={to}>
            <Card variant="outlined" sx={{ cursor: "pointer" }} onClick={() => navigate(to)}>
              <CardContent>
                <Icon sx={{ fontSize: 40, color: "primary.main" }} />
                <Typography variant="h6">{title}</Typography>
                <Typography variant="body2" sx={{ color: "text.secondary" }}>{desc}</Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>
    </Stack>
  );
}