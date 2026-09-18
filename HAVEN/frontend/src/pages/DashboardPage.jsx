import { useState } from "react";
import {
  Box,
  Button,
  Card,
  CardContent,
  Chip,
  Dialog,
  Divider,
  Grid,
  Paper,
  Stack,
  Typography,
} from "@mui/material";
import {
  Calculate,
  ContactEmergency,
  Gavel,
  HealthAndSafety,
  Map,
  Shield,
  Timer,
} from "@mui/icons-material";
import { useDispatch, useSelector } from "react-redux";
import { useNavigate } from "react-router-dom";

import { triggerSOS } from "../store/slices/sosSlice.js";
import SOSButton from "../components/SOSButton.jsx";

const QUICK_ACTIONS = [
  { to: "/therapy", title: "AI Therapy Companion", desc: "Trauma-informed 24/7 crisis support & grounding", icon: HealthAndSafety, color: "#10b981" },
  { to: "/legal", title: "Legal Rights Guide", desc: "Indian laws, PWDVA 2005, 498A, and protection orders", icon: Gavel, color: "#3b82f6" },
  { to: "/contacts", title: "Emergency Network", desc: "Manage trusted contacts and immediate responders", icon: ContactEmergency, color: "#8b5cf6" },
];

export default function DashboardPage() {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const user = useSelector((s) => s.auth.user);
  const name = user?.name || "Friend";
  const [decoyOpen, setDecoyOpen] = useState(false);
  const [calcDisplay, setCalcDisplay] = useState("0");

  async function handleSOS(location) {
    try {
      const { payload } = await dispatch(triggerSOS(location));
      navigate(`/sos/${payload.sos_id}`);
    } catch {
      /* apiError surfaces via the global 401 handler */
    }
  }

  const handleCalcPress = (btn) => {
    if (btn === "C") setCalcDisplay("0");
    else if (btn === "=") {
      if (calcDisplay === "8080") {
        setDecoyOpen(false);
        setCalcDisplay("0");
      } else {
        try {
          const sanitized = calcDisplay.replace(/[^0-9+\-*/.]/g, "");
          // Safe evaluation using Function
          // eslint-disable-next-line no-new-func
          const result = Function(`'use strict'; return (${sanitized})`)();
          setCalcDisplay(String(result));
        } catch {
          setCalcDisplay("Error");
        }
      }
    } else {
      setCalcDisplay((prev) => (prev === "0" || prev === "Error" ? btn : prev + btn));
    }
  };

  return (
    <Stack spacing={3}>
      <Box display="flex" justifyContent="space-between" alignItems="center" flexWrap="wrap" gap={1}>
        <Box>
          <Typography variant="h5" sx={{ fontWeight: 700 }}>
            Welcome back, {name}
          </Typography>
          <Typography variant="body2" sx={{ color: "text.secondary" }}>
            SafeHaven is active. Discreet crisis support, legal guidance, and rapid coordination ready.
          </Typography>
        </Box>
        <Button
          variant="outlined"
          color="inherit"
          startIcon={<Calculate />}
          onClick={() => setDecoyOpen(true)}
          sx={{ borderRadius: 2, textTransform: "none" }}
        >
          Quick Decoy Mode
        </Button>
      </Box>

      {/* Main Crisis SOS Action Card */}
      <Card
        variant="outlined"
        sx={{
          borderRadius: 3,
          p: 2,
          bgcolor: "#0f172a",
          color: "white",
          border: "1px solid #dc2626",
          boxShadow: "0 4px 20px rgba(220, 38, 38, 0.15)",
        }}
      >
        <CardContent sx={{ textAlign: "center", py: 4 }}>
          <Typography variant="h5" sx={{ fontWeight: 800, color: "#f87171", mb: 1 }}>
            ONE-TOUCH DISCREET SOS
          </Typography>
          <Typography variant="body2" sx={{ color: "#94a3b8", mb: 3 }}>
            Pressing SOS captures your GPS coordinates, sends emergency dispatch alerts to your network, and starts an instant AI crisis therapy session.
          </Typography>
          <Box display="flex" justifyContent="center" my={2}>
            <SOSButton onActivated={handleSOS} />
          </Box>
          <Stack direction="row" spacing={1} justifyContent="center" sx={{ mt: 2 }} flexWrap="wrap" gap={1}>
            <Chip size="small" label="Live GPS Stream" color="error" variant="outlined" />
            <Chip size="small" label="Encrypted at Rest" color="info" variant="outlined" />
            <Chip size="small" label="Auto-Therapy Ready" color="success" variant="outlined" />
          </Stack>
        </CardContent>
      </Card>

      {/* Quick Core Services Grid */}
      <Grid container spacing={2}>
        {QUICK_ACTIONS.map(({ to, title, desc, icon: Icon, color }) => (
          <Grid item xs={12} sm={4} key={to}>
            <Card
              variant="outlined"
              sx={{
                borderRadius: 3,
                cursor: "pointer",
                height: "100%",
                transition: "all 0.2s ease-in-out",
                "&:hover": { borderColor: color, transform: "translateY(-3px)", boxShadow: 3 },
              }}
              onClick={() => navigate(to)}
            >
              <CardContent>
                <Box
                  sx={{
                    width: 50,
                    height: 50,
                    borderRadius: 2,
                    bgcolor: `${color}15`,
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    mb: 2,
                  }}
                >
                  <Icon sx={{ fontSize: 28, color: color }} />
                </Box>
                <Typography variant="h6" sx={{ fontWeight: 700, mb: 0.5 }}>
                  {title}
                </Typography>
                <Typography variant="body2" sx={{ color: "text.secondary" }}>
                  {desc}
                </Typography>
              </CardContent>
            </Card>
          </Grid>
        ))}
      </Grid>

      {/* Emergency Hotlines Banner */}
      <Paper
        variant="outlined"
        sx={{
          p: 2.5,
          borderRadius: 3,
          bgcolor: "#fff1f2",
          borderColor: "#fecdd3",
        }}
      >
        <Typography variant="subtitle1" sx={{ fontWeight: 700, color: "#9f1239", mb: 1, display: "flex", alignItems: "center", gap: 1 }}>
          <Shield /> Immediate Indian Legal & Crisis Helplines (24/7 Free)
        </Typography>
        <Grid container spacing={2}>
          <Grid item xs={12} sm={4}>
            <Typography variant="body2" fontWeight="bold">112</Typography>
            <Typography variant="caption" color="text.secondary">National Emergency (Police, Medical, Fire)</Typography>
          </Grid>
          <Grid item xs={12} sm={4}>
            <Typography variant="body2" fontWeight="bold">1091</Typography>
            <Typography variant="caption" color="text.secondary">National Commission for Women Helpline</Typography>
          </Grid>
          <Grid item xs={12} sm={4}>
            <Typography variant="body2" fontWeight="bold">181</Typography>
            <Typography variant="caption" color="text.secondary">Women in Distress / Domestic Violence</Typography>
          </Grid>
        </Grid>
      </Paper>

      {/* Decoy Calculator Modal */}
      <Dialog fullScreen open={decoyOpen} onClose={() => setDecoyOpen(false)}>
        <Box sx={{ bgcolor: "#111827", height: "100vh", p: 3, display: "flex", flexDirection: "column", justifyContent: "center", alignItems: "center" }}>
          <Box sx={{ width: 320, bgcolor: "#1f2937", p: 3, borderRadius: 4, boxShadow: 6 }}>
            <Box sx={{ height: 80, bgcolor: "#111827", borderRadius: 2, p: 2, mb: 2, display: "flex", alignItems: "flex-end", justifyContent: "flex-end" }}>
              <Typography variant="h4" sx={{ color: "white", fontFamily: "monospace" }}>{calcDisplay}</Typography>
            </Box>
            <Grid container spacing={1}>
              {["C", "/", "*", "-", "7", "8", "9", "+", "4", "5", "6", "=", "1", "2", "3", "0"].map((btn) => (
                <Grid item xs={3} key={btn}>
                  <Button
                    fullWidth
                    variant="contained"
                    sx={{
                      height: 54,
                      bgcolor: ["/", "*", "-", "+", "="].includes(btn) ? "#ef4444" : "#374151",
                      fontSize: 18,
                      fontWeight: "bold",
                    }}
                    onClick={() => handleCalcPress(btn)}
                  >
                    {btn}
                  </Button>
                </Grid>
              ))}
            </Grid>
            <Typography variant="caption" sx={{ color: "#6b7280", display: "block", textAlign: "center", mt: 2 }}>
              Decoy Calculator Active. Enter 8080= to unlock.
            </Typography>
          </Box>
        </Box>
      </Dialog>
    </Stack>
  );
}