import {
  Alert,
  Button,
  Card,
  CardContent,
  CircularProgress,
  Divider,
  FormControlLabel,
  MenuItem,
  Stack,
  Switch,
  TextField,
  Typography,
} from "@mui/material";
import { useEffect, useState } from "react";

import client, { apiError } from "../api/client.js";
import { fetchProfile } from "../store/slices/authSlice.js";

const LANGUAGES = [
  ["en", "English"],
  ["hi", "हिंदी"],
  ["ta", "தமிழ்"],
  ["te", "తెలుగు"],
  ["kn", "ಕನ್ನಡ"],
  ["ml", "മലയാളം"],
  ["bn", "বাংলা"],
];

export default function ProfilePage() {
  const [profile, setProfile] = useState(null);
  const [name, setName] = useState("");
  const [language, setLanguage] = useState("en");
  const [notifyAuthorities, setNotifyAuthorities] = useState(false);
  const [pwd, setPwd] = useState({ current: "", next: "" });
  const [error, setError] = useState("");
  const [ok, setOk] = useState("");

  useEffect(() => {
    client.get("/auth/profile").then(({ data }) => {
      setProfile(data);
      setName(data.name || "");
      setLanguage(data.language || "en");
      setNotifyAuthorities(data.notify_authorities || false);
    });
    // eslint-disable-next-line
  }, []);

  async function saveProfile() {
    setError(""); setOk("");
    try {
      await client.put("/auth/profile", { name, language, notify_authorities: notifyAuthorities });
      setOk("Profile updated.");
    } catch (err) { setError(apiError(err)); }
  }

  async function changePassword() {
    setError(""); setOk("");
    try {
      await client.post("/auth/change-password", {
        current_password: pwd.current,
        new_password: pwd.next,
      });
      setPwd({ current: "", next: "" });
      setOk("Password changed.");
    } catch (err) { setError(apiError(err)); }
  }

  if (!profile) return <CircularProgress />;

  return (
    <Stack spacing={2}>
      <Typography variant="h5" sx={{ fontWeight: 600 }}>Profile & Safety</Typography>
      {error && <Alert severity="error">{error}</Alert>}
      {ok && <Alert severity="success">{ok}</Alert>}

      <Card variant="outlined">
        <CardContent>
          <Typography variant="h6">Details</Typography>
          <Typography variant="body2" sx={{ mb: 1 }}>Email: {profile.email}</Typography>
          <Stack direction="row" spacing={1} sx={{ alignItems: "center" }}>
            <TextField label="Full name" size="small" value={name} onChange={(e) => setName(e.target.value)} />
            <TextField select label="Language" size="small" value={language} sx={{ minWidth: 140 }}>
              {LANGUAGES.map(([code, label]) => <MenuItem key={code} value={code}>{label}</MenuItem>)}
            </TextField>
            <Button variant="contained" onClick={saveProfile}>Save</Button>
          </Stack>
          <FormControlLabel
            sx={{ mt: 2, display: "flex" }}
            control={<Switch checked={notifyAuthorities} onChange={(e) => setNotifyAuthorities(e.target.checked)} />}
            label={notifyAuthorities
              ? "Notify authorities automatically when SOS is pressed"
              : "Notify authorities on SOS (recommended for your safety)"}
          />
        </CardContent>
      </Card>

      <Divider />

      <Card variant="outlined">
        <CardContent>
          <Typography variant="h6">Change password</Typography>
          <Stack spacing={1} direction="row" sx={{ alignItems: "center" }}>
            <TextField label="Current password" type="password" size="small" value={pwd.current}
              onChange={(e) => setPwd({ ...pwd, current: e.target.value })} />
            <TextField label="New password" type="password" size="small" value={pwd.next}
              onChange={(e) => setPwd({ ...pwd, next: e.target.value })} />
            <Button variant="contained" onClick={changePassword} disabled={!pwd.current || pwd.next.length < 8}>
              Update
            </Button>
          </Stack>
        </CardContent>
      </Card>
    </Stack>
  );
}