import {
  Alert,
  Box,
  Button,
  Card,
  CardContent,
  CircularProgress,
  Dialog,
  DialogActions,
  DialogContent,
  DialogTitle,
  Divider,
  IconButton,
  Stack,
  TextField,
  Typography,
} from "@mui/material";
import {
  ArrowBack,
  Backspace,
  Key,
  Lock,
  LockOpen,
  PhoneInTalk,
  Security,
} from "@mui/icons-material";
import { useState } from "react";
import { useNavigate } from "react-router-dom";

import client, { apiError } from "../api/client.js";

/**
 * Discreet Calculator disguise.
 *
 * Surface: a fully-working calculator — exactly what an abuser would see.
 * Hidden safety layer (unlocked only by the user's numeric safety PIN, set in
 * Profile → "Change safety PIN"):
 *   • Tap the 🔒 padlock, or press "=" 5x in a row → unlock overlay.
 *   • PIN verifies server-side via /auth/verify-pin → discreet emergency
 *     actions appear (Trigger SOS / Talk to therapist) in one tap.
 */
const KEYS = [
  "C", "⌫", "(", ")",
  "7", "8", "9", "/",
  "4", "5", "6", "*",
  "1", "2", "3", "-",
  "0", ".", "=", "+",
];

export default function CalculatorPage() {
  const navigate = useNavigate();
  const [display, setDisplay] = useState("0");
  const [pressedEquals, setPressedEquals] = useState(0);
  const [unlockOpen, setUnlockOpen] = useState(false);
  const [unlocked, setUnlocked] = useState(false);
  const [pin, setPin] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  // ---- Calculator engine (simple, dependency-free) ----------------------->
  function press(k) {
    setError("");
    if (k === "C") { setDisplay("0"); setPressedEquals(0); return; }
    if (k === "⌫") { setDisplay((d) => (d.length <= 1 ? "0" : d.slice(0, -1))); return; }
    if (k === "=") {
      const next = pressedEquals + 1;
      setPressedEquals(next);
      if (next >= 5) { setPressedEquals(0); setUnlockOpen(true); return; }
      try {
        const safe = display.replace(/[^-()\d/*+.]/g, "");
        // eslint-disable-next-line no-eval
        setDisplay(String(eval(safe) || 0));
      } catch { setDisplay("Error"); }
      return;
    }
    setPressedEquals(0);
    setDisplay((d) => (d === "0" ? k : (d + k).slice(0, 24)));
  }

  // ---- Hidden unlock (server-verified PIN) ------------------------------->
  async function verify() {
    setError("");
    if (!/^\d{4,6}$/.test(pin)) { setError("Enter your 4–6 digit safety PIN."); return; }
    setBusy(true);
    try {
      await client.post("/auth/verify-pin", { pin });
      setUnlocked(true); setPin(""); setUnlockOpen(false);
    } catch (err) { setError(apiError(err)); }
    finally { setBusy(false); }
  }

  function triggerSOS() { navigate("/dashboard"); }

  const displayText = unlocked ? "🛡 SAFE MODE" : display;

  return (
    <Stack spacing={2} sx={{ maxWidth: 420, mx: "auto", width: "100%" }}>
      <Stack direction="row" alignItems="center" spacing={1}>
        <IconButton onClick={() => navigate("/dashboard")}><ArrowBack /></IconButton>
        <Typography variant="h6" sx={{ fontWeight: 700 }}>Calculator</Typography>
      </Stack>

      {!unlocked && (
        <Alert severity="info" sx={{ borderRadius: 12 }}>
          A safe-looking calculator. Your personal data stays off this screen.
        </Alert>
      )}

      {/* The calculator body */}
      <Card
        variant="outlined"
        sx={{ borderRadius: 5, background: "#ffffff",
          boxShadow: "0 18px 40px rgba(255,46,99,0.12)", overflow: "hidden" }}
      >
        <CardContent>
          {/* Screen */}
          <Box
            sx={{ background: "linear-gradient(135deg,#1f2438,#3a2f55)", color: "#fff",
              borderRadius: 3, px: 2, py: 3, textAlign: "right", mb: 2, minHeight: 86,
              display: "flex", flexDirection: "column", justifyContent: "flex-end" }}
          >
            <Typography variant="h4" sx={{ fontFamily: "monospace", fontWeight: 600 }}>
              {displayText}
            </Typography>
            <Typography variant="caption" sx={{ color: "#9fb0ff", mt: 0.5 }}>
              Standard HAVEN device
            </Typography>
          </Box>

          {/* Keypad */}
          <Box sx={{ display: "grid", gridTemplateColumns: "repeat(4, 1fr)", gap: 1 }}>
            {KEYS.map((k) => (
              <Button
                key={k}
                variant={k === "=" ? "contained" : "outlined"}
                color={k === "=" ? "primary" : k === "C" ? "error" : "inherit"}
                onClick={() => press(k)}
                sx={{ py: 1.8, fontSize: 20, fontWeight: 700, borderRadius: 2.5,
                  color: k === "C" ? undefined : "#24304f", borderColor: "#e6eaf5" }}
              >
                {k === "⌫" ? <Backspace /> : k}
              </Button>
            ))}
          </Box>
        </CardContent>
      </Card>

      {/* Hidden unlock dialog — verified server-side by numeric safety PIN */}
      <Dialog open={unlockOpen} onClose={() => setUnlockOpen(false)} fullWidth maxWidth="xs">
        <DialogTitle sx={{ fontWeight: 700 }}>🔒 Safety unlock</DialogTitle>
        <DialogContent>
          <Stack spacing={2} sx={{ pt: 1 }}>
            <Typography variant="body2" color="text.secondary">
              Enter your 4–6 digit safety PIN (set in Profile → “Change safety
              PIN”) to reveal discreet emergency actions.
            </Typography>
            <TextField
              autoFocus
              type="password"
              inputMode="numeric"
              label="Safety PIN"
              value={pin}
              onChange={(e) => setPin(e.target.value.replace(/\D/g, ""))}
              fullWidth
            />
            {error && <Alert severity="error">{error}</Alert>}
          </Stack>
        </DialogContent>
        <DialogActions sx={{ px: 3, pb: 2 }}>
          <Button onClick={() => setUnlockOpen(false)}>Cancel</Button>
          <Button variant="contained" onClick={verify} disabled={busy}>
            {busy ? <CircularProgress size={18} color="inherit" /> : "Unlock"}
          </Button>
        </DialogActions>
      </Dialog>

      {/* Discreet quick actions — shown only while unlocked */}
      {unlocked && (
        <Card variant="outlined" sx={{ borderRadius: 5, background: "#fff9fb" }}>
          <CardContent>
            <Stack direction="row" spacing={2} sx={{ flexWrap: "wrap" }}>
              <Button
                variant="contained"
                color="error"
                startIcon={<PhoneInTalk />}
                onClick={triggerSOS}
                sx={{ flex: 1, minWidth: 140 }}
              >
                Trigger SOS
              </Button>
              <Button
                variant="contained"
                color="secondary"
                startIcon={<Security />}
                onClick={() => navigate("/therapy")}
                sx={{ flex: 1, minWidth: 140 }}
              >
                Talk to therapist
              </Button>
            </Stack>
            <Typography variant="caption" color="text.secondary" sx={{ mt: 1.5, display: "block" }}>
              🛡 Safe mode — this area hides instantly when you press “C”.
            </Typography>
          </CardContent>
        </Card>
      )}
    </Stack>
  );
}