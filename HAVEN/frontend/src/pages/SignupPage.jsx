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
    <Box sx={{ minHeight: "100vh", bgcolor: "background.default", display: "grid", placeItems: "center" }}>
      <Card sx={{ px: 4, py: 3, maxWidth: 440, width: "100%" }}>
        <Typography variant="h4" sx={{ fontWeight: 700 }}>Create your HAVEN account</Typography>
        <Typography variant="body2" sx={{ color: "text.secondary", mb: 3 }}>
          Privacy-first onboarding. Add emergency contacts next.
        </Typography>

        {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

        <Stack component="form" onSubmit={handleSubmit} spacing={2}>
          <TextField label="Full name" fullWidth value={form.name} onChange={update("name")} />
          <TextField label="Email" type="email" required fullWidth value={form.email} onChange={update("email")} />
          <TextField label="Phone (hashed at rest)" fullWidth value={form.phone} onChange={update("phone")} />
          <TextField label="Password (min 8 chars)" type="password" required fullWidth value={form.password} onChange={update("password")} />
          <Button type="submit" variant="contained" fullWidth disabled={loading}>
            {loading ? <CircularProgress size={22} color="inherit" /> : "Create account"}
          </Button>
        </Stack>

        <Typography variant="body2" sx={{ mt: 2 }}>
          Already registered? <Link to="/login">Sign in</Link>
        </Typography>
      </Card>
    </Box>
  );
}