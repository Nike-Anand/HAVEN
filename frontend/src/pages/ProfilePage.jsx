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

const NOTIF_DEFAULTS = {
  email_alerts: true,
  push_notifications: true,
  vibration: true,
  sound_enabled: false,
};

const PRIVACY_DEFAULTS = {
  share_location_with_contacts: true,
  allow_data_sharing: false,
  data_retention_days: 90,
};

function NotificationSettings() {
  const [notif, setNotif] = useState(NOTIF_DEFAULTS);
  const [privacy, setPrivacy] = useState(PRIVACY_DEFAULTS);
  const [msg, setMsg] = useState({ error: "", ok: "" });

  useEffect(() => {
    setMsg({ error: "", ok: "" });
    client
      .get("/settings")
      .then(({ data }) => {
        setNotif({ ...NOTIF_DEFAULTS, ...data.notification_preferences });
        setPrivacy({ ...PRIVACY_DEFAULTS, ...data.privacy });
      })
      .catch(() => {
        // Keep defaults if the server has no saved settings yet.
      });
    // eslint-disable-next-line
  }, []);

  async function save() {
    setMsg({ error: "", ok: "" });
    try {
      await client.put("/settings/notification-preferences", notif);
      await client.put("/settings/privacy", privacy);
      setMsg({ ok: "Settings saved." });
    } catch (err) {
      setMsg({ error: apiError(err) });
    }
  }

  const toggle = (key) => (e) => setNotif({ ...notif, [key]: e.target.checked });
  const togglePrivacy = (key) => (e) => setPrivacy({ ...privacy, [key]: e.target.checked });

  return (
    <Stack>
      {msg.error && <Alert severity="error">{msg.error}</Alert>}
      {msg.ok && <Alert severity="success">{msg.ok}</Alert>}
      <Typography variant="subtitle2" sx={{ mt: 1 }}>Alerts</Typography>
      {Object.entries({
        email_alerts: "Email notifications",
        push_notifications: "Push notifications",
        vibration: "Vibration on SOS",
        sound_enabled: "Sound on SOS",
      }).map(([key, label]) => (
        <FormControlLabel
          key={key}
          control={<Switch checked={!!notif[key]} onChange={toggle(key)} />}
          label={label}
        />
      ))}
      <Typography variant="subtitle2" sx={{ mt: 1 }}>Privacy</Typography>
      <FormControlLabel
        control={<Switch checked={!!privacy.share_location_with_contacts} onChange={togglePrivacy("share_location_with_contacts")} />}
        label="Share my live location with trusted contacts"
      />
      <FormControlLabel
        control={<Switch checked={!!privacy.allow_data_sharing} onChange={togglePrivacy("allow_data_sharing")} />}
        label="Allow de-identified data sharing for safety research"
      />
      <Stack direction="row" spacing={1} sx={{ alignItems: "center", mt: 1 }}>
        <TextField
          label="Data retention (days)"
          type="number"
          size="small"
          value={privacy.data_retention_days}
          onChange={(e) => setPrivacy({ ...privacy, data_retention_days: Number(e.target.value) || 90 })}
        />
        <Button variant="contained" onClick={save}>Save settings</Button>
      </Stack>
    </Stack>
  );
}

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

  // ---- Discreet calculator safety PIN ------------------------------>
  const [pin, setPin] = useState({ password: "", newPin: "" });
  const [pinMsg, setPinMsg] = useState({ error: "", ok: "" });

  async function changePin() {
    setPinMsg({ error: "", ok: "" });
    if (!/^\d{4,6}$/.test(pin.newPin)) {
      setPinMsg({ error: "PIN must be 4–6 digits." });
      return;
    }
    try {
      await client.post("/auth/change-pin", {
        current_password: pin.password,
        new_pin: pin.newPin,
      });
      setPin({ password: "", newPin: "" });
      setPinMsg({ ok: "Safety PIN updated. Use it to unlock the Calculator disguise." });
    } catch (err) { setPinMsg({ error: apiError(err) }); }
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
          <Typography variant="h6">Notifications & Privacy</Typography>
          <NotificationSettings />
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