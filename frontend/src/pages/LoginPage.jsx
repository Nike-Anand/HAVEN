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
    <Box sx={{ minHeight: "100vh", bgcolor: "background.default", display: "grid", placeItems: "center" }}>
      <Card sx={{ px: 4, py: 3, maxWidth: 420, width: "100%" }}>
        <Typography variant="h4" sx={{ fontWeight: 700 }}>🛡️ HAVEN</Typography>
        <Typography variant="body1" sx={{ color: "text.secondary", mb: 3 }}>
          Your trusted safety companion. Sign in to continue.
        </Typography>

        {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

        <Stack component="form" onSubmit={handleSubmit} spacing={2}>
          <TextField label="Email" type="email" required fullWidth value={email} onChange={(e) => setEmail(e.target.value)} />
          <TextField label="Password" type="password" required fullWidth value={password} onChange={(e) => setPassword(e.target.value)} />
          <Button type="submit" variant="contained" fullWidth disabled={loading}>
            {loading ? <CircularProgress size={22} color="inherit" /> : "Sign in"}
          </Button>
        </Stack>

        <Typography variant="body2" sx={{ mt: 2 }}>
          New here? <Link to="/signup">Create an account</Link>
        </Typography>
      </Card>
    </Box>
  );
}