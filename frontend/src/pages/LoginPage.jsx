import { Alert, Box, Button, Card, CircularProgress, Stack, TextField, Typography } from "@mui/material";
import { useDispatch } from "react-redux";
import { Link, useNavigate } from "react-router-dom";
import { useState } from "react";

import { apiError } from "../api/client.js";
import { fetchProfile, loginUser } from "../store/slices/authSlice.js";

export default function LoginPage() {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function handleSubmit(event) {
    event.preventDefault();
    setLoading(true);
    setError("");
    try {
      await dispatch(loginUser({ email, password })).unwrap();
      await dispatch(fetchProfile()).unwrap();
      navigate("/dashboard");
    } catch (err) {
      setError(apiError(err));
    } finally {
      setLoading(false);
    }
  }

  return (
    <Box
      sx={{
        minHeight: "100vh",
        background: "radial-gradient(circle at top, #fff3f7 0%, #ffeaf3 25%, #f3f4ff 55%, #eef6ff 100%)",
        display: "grid",
        placeItems: "center",
        px: 2,
      }}
    >
      <Card
        sx={{
          px: { xs: 2.5, sm: 4 },
          py: 3,
          maxWidth: 440,
          width: "100%",
          borderRadius: 4,
          border: "1px solid rgba(255,46,99,0.12)",
          boxShadow: "0 25px 60px rgba(131, 93, 165, 0.16)",
        }}
      >
        <Box sx={{ display: "flex", alignItems: "center", mb: 1.5 }}>
          <Box
            sx={{
              width: 46,
              height: 46,
              borderRadius: "50%",
              display: "grid",
              placeItems: "center",
              fontSize: 24,
              background: "linear-gradient(135deg, #ff2e63 0%, #7c3aed 100%)",
              mr: 1.5,
            }}
          >
            🛡️
          </Box>
          <Typography variant="h4" sx={{ fontWeight: 800, letterSpacing: 0.5 }}>
            HAVEN
          </Typography>
        </Box>

        <Typography variant="body1" sx={{ color: "text.secondary", mb: 3 }}>
          Your trusted safety companion. Sign in to continue.
        </Typography>

        {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

        <Stack component="form" onSubmit={handleSubmit} spacing={2.5}>
          <TextField
            label="Email"
            type="email"
            required
            fullWidth
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            sx={{ bgcolor: "#fff" }}
          />
          <TextField
            label="Password"
            type="password"
            required
            fullWidth
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            sx={{ bgcolor: "#fff" }}
          />
          <Button
            type="submit"
            variant="contained"
            fullWidth
            disabled={loading}
            sx={{
              py: 1.4,
              borderRadius: 2,
              background: "linear-gradient(90deg, #ff2e63 0%, #7c3aed 100%)",
              fontWeight: 700,
            }}
          >
            {loading ? <CircularProgress size={22} color="inherit" /> : "Sign in"}
          </Button>
        </Stack>

        <Typography variant="body2" sx={{ mt: 2.5, color: "text.secondary" }}>
          New here? <Link to="/signup">Create an account</Link>
        </Typography>
      </Card>
    </Box>
  );
}