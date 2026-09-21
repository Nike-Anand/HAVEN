import { Alert, Box, Button, Card, CircularProgress, Stack, TextField, Typography } from "@mui/material";
import { useDispatch } from "react-redux";
import { Link, useNavigate } from "react-router-dom";
import { useState } from "react";

import { apiError } from "../api/client.js";
import { fetchProfile, signupUser } from "../store/slices/authSlice.js";

export default function SignupPage() {
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const [form, setForm] = useState({ email: "", password: "", name: "", phone: "" });
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  function update(key) {
    return (e) => setForm({ ...form, [key]: e.target.value });
  }

  async function handleSubmit(event) {
    event.preventDefault();
    setLoading(true);
    setError("");
    try {
      await dispatch(signupUser(form)).unwrap();
      await dispatch(fetchProfile()).unwrap();
      navigate("/contacts");
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
        background: "radial-gradient(circle at top, #fff6ec 0%, #fff0f5 28%, #f3f4ff 65%, #edf7ff 100%)",
        display: "grid",
        placeItems: "center",
        px: 2,
      }}
    >
      <Card
        sx={{
          px: { xs: 2.5, sm: 4 },
          py: 3,
          maxWidth: 460,
          width: "100%",
          borderRadius: 4,
          border: "1px solid rgba(124,58,237,0.12)",
          boxShadow: "0 25px 60px rgba(124, 58, 237, 0.1)",
        }}
      >
        <Typography variant="h4" sx={{ fontWeight: 800, mb: 1 }}>
          Create your HAVEN account
        </Typography>
        <Typography variant="body2" sx={{ color: "text.secondary", mb: 3 }}>
          Privacy-first onboarding. Add emergency contacts next.
        </Typography>

        {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

        <Stack component="form" onSubmit={handleSubmit} spacing={2.3}>
          <TextField label="Full name" fullWidth value={form.name} onChange={update("name")} sx={{ bgcolor: "#fff" }} />
          <TextField label="Email" type="email" required fullWidth value={form.email} onChange={update("email")} sx={{ bgcolor: "#fff" }} />
          <TextField label="Phone (hashed at rest)" fullWidth value={form.phone} onChange={update("phone")} sx={{ bgcolor: "#fff" }} />
          <TextField label="Password (min 8 chars)" type="password" required fullWidth value={form.password} onChange={update("password")} sx={{ bgcolor: "#fff" }} />
          <Button
            type="submit"
            variant="contained"
            fullWidth
            disabled={loading}
            sx={{
              py: 1.5,
              borderRadius: 2,
              background: "linear-gradient(90deg, #ff2e63 0%, #ff9f43 100%)",
              fontWeight: 700,
            }}
          >
            {loading ? <CircularProgress size={22} color="inherit" /> : "Create account"}
          </Button>
        </Stack>

        <Typography variant="body2" sx={{ mt: 2.5, color: "text.secondary" }}>
          Already registered? <Link to="/login">Sign in</Link>
        </Typography>
      </Card>
    </Box>
  );
}