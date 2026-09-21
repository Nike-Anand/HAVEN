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
  IconButton,
  Stack,
  TextField,
  Typography,
} from "@mui/material";
import {
  ArrowBack,
  Backspace,
  PhoneInTalk,
  Security,
} from "@mui/icons-material";
import { useMemo, useState } from "react";
import { useNavigate } from "react-router-dom";

import client, { apiError } from "../api/client.js";

const KEYS = [
  "C", "⌫", "(", ")",
  "7", "8", "9", "/",
  "4", "5", "6", "*",
  "1", "2", "3", "-",
  "0", ".", "=", "+",
];

function safeEvaluate(expression) {
  const sanitized = expression.replace(/[^0-9+\-*/().%\s]/g, "");
  if (!sanitized || sanitized === ".") return "0";

  const tokens = sanitized.match(/[0-9]+(?:\.[0-9]+)?|[()+\-*/.%]/g) || [];
  if (tokens.length === 0) return "0";

  const numbers = [];
  const operators = [];
  const precedence = { "+": 1, "-": 1, "*": 2, "/": 2, "%": 2 };

  const applyOperator = () => {
    const op = operators.pop();
    const right = numbers.pop();
    const left = numbers.pop();
    if (left === undefined || right === undefined || !op) return;
    switch (op) {
      case "+": numbers.push(left + right); break;
      case "-": numbers.push(left - right); break;
      case "*": numbers.push(left * right); break;
      case "/": numbers.push(right === 0 ? Number.NaN : left / right); break;
      case "%": numbers.push(right === 0 ? Number.NaN : left % right); break;
      default: break;
    }
  };

  for (const token of tokens) {
    if (/^\d+(?:\.\d+)?$/.test(token)) {
      numbers.push(Number(token));
      continue;
    }

    if (token === "(") {
      operators.push(token);
      continue;
    }

    if (token === ")") {
      while (operators.length && operators[operators.length - 1] !== "(") applyOperator();
      operators.pop();
      continue;
    }

    while (
      operators.length &&
      operators[operators.length - 1] !== "(" &&
      precedence[operators[operators.length - 1]] >= precedence[token]
    ) {
      applyOperator();
    }
    operators.push(token);
  }

  while (operators.length) applyOperator();

  const result = numbers[0];
  if (!Number.isFinite(result)) return "Error";
  return String(result);
}

export default function CalculatorPage() {
  const navigate = useNavigate();
  const [display, setDisplay] = useState("0");
  const [pressedEquals, setPressedEquals] = useState(0);
  const [unlockOpen, setUnlockOpen] = useState(false);
  const [unlocked, setUnlocked] = useState(false);
  const [pin, setPin] = useState("");
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  const displayText = useMemo(() => (unlocked ? "🛡 SAFE MODE" : display), [display, unlocked]);

  function press(k) {
    setError("");

    if (k === "C") {
      setDisplay("0");
      setPressedEquals(0);
      return;
    }

    if (k === "⌫") {
      setDisplay((d) => (d.length <= 1 ? "0" : d.slice(0, -1)));
      return;
    }

    if (k === "=") {
      const next = pressedEquals + 1;
      setPressedEquals(next);
      if (next >= 5) {
        setPressedEquals(0);
        setUnlockOpen(true);
        return;
      }

      const computed = safeEvaluate(display);
      setDisplay(computed === "Error" ? "Error" : computed);
      return;
    }

    setPressedEquals(0);
    setDisplay((d) => {
      const nextValue = d === "0" ? k : `${d}${k}`;
      return nextValue.slice(0, 24);
    });
  }

  async function verify() {
    setError("");
    if (!/^\d{4,6}$/.test(pin)) {
      setError("Enter your 4–6 digit safety PIN.");
      return;
    }

    setBusy(true);
    try {
      await client.post("/auth/verify-pin", { pin });
      setUnlocked(true);
      setPin("");
      setUnlockOpen(false);
    } catch (err) {
      setError(apiError(err));
    } finally {
      setBusy(false);
    }
  }

  function triggerSOS() {
    navigate("/dashboard");
  }

  return (
    <Stack spacing={2} sx={{ maxWidth: 420, mx: "auto", width: "100%" }}>
      <Stack direction="row" alignItems="center" spacing={1}>
        <IconButton onClick={() => navigate("/dashboard")} aria-label="back"><ArrowBack /></IconButton>
        <Typography variant="h5" sx={{ fontWeight: 700 }}>Calculator</Typography>
      </Stack>

      {!unlocked && (
        <Alert severity="info" sx={{ borderRadius: 3 }}>
          A safe-looking calculator. Your personal data stays off this screen.
        </Alert>
      )}

      <Card variant="outlined" sx={{ borderRadius: 4, boxShadow: "0 18px 40px rgba(255,46,99,0.12)", overflow: "hidden" }}>
        <CardContent sx={{ p: 2.5 }}>
          <Box
            sx={{
              background: "linear-gradient(135deg,#1f2438,#3a2f55)",
              color: "#fff",
              borderRadius: 3,
              px: 2,
              py: 3,
              textAlign: "right",
              mb: 2,
              minHeight: 86,
              display: "flex",
              flexDirection: "column",
              justifyContent: "flex-end",
            }}
          >
            <Typography variant="h4" sx={{ fontFamily: "monospace", fontWeight: 600, wordBreak: "break-all" }}>
              {displayText}
            </Typography>
            <Typography variant="caption" sx={{ color: "#9fb0ff", mt: 0.5 }}>
              Standard HAVEN device
            </Typography>
          </Box>

          <Box sx={{ display: "grid", gridTemplateColumns: "repeat(4, minmax(0, 1fr))", gap: 1 }}>
            {KEYS.map((k) => (
              <Button
                key={k}
                variant={k === "=" ? "contained" : "outlined"}
                color={k === "=" ? "primary" : k === "C" ? "error" : "inherit"}
                onClick={() => press(k)}
                sx={{
                  py: 1.8,
                  minHeight: 56,
                  fontSize: 20,
                  fontWeight: 700,
                  borderRadius: 2.5,
                  color: k === "C" ? undefined : "#24304f",
                  borderColor: "#e6eaf5",
                }}
              >
                {k === "⌫" ? <Backspace /> : k}
              </Button>
            ))}
          </Box>
        </CardContent>
      </Card>

      <Dialog open={unlockOpen} onClose={() => setUnlockOpen(false)} fullWidth maxWidth="xs">
        <DialogTitle sx={{ fontWeight: 700 }}>🔒 Safety unlock</DialogTitle>
        <DialogContent>
          <Stack spacing={2} sx={{ pt: 1 }}>
            <Typography variant="body2" color="text.secondary">
              Enter your 4–6 digit safety PIN to reveal discreet emergency actions.
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

      {unlocked && (
        <Card variant="outlined" sx={{ borderRadius: 4, background: "#fff9fb" }}>
          <CardContent>
            <Stack direction={{ xs: "column", sm: "row" }} spacing={1.5}>
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