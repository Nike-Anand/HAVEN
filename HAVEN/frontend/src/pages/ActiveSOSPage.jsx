import {
  Alert,
  Button,
  Card,
  CardContent,
  Chip,
  CircularProgress,
  List,
  ListItem,
  ListItemText,
  Stack,
  Typography,
} from "@mui/material";
import { useDispatch } from "react-redux";
import { useEffect, useState } from "react";
import { useNavigate, useParams } from "react-router-dom";

import { cancelSOS, fetchSOSStatus } from "../store/slices/sosSlice.js";
import TherapyChat from "../components/TherapyChat.jsx";

const RESPONSES = new Set(["ON_WAY", "EMS", "POLICE", "SAFE", "CALLING"]);

export default function ActiveSOSPage() {
  const { sosId } = useParams();
  const dispatch = useDispatch();
  const navigate = useNavigate();
  const [status, setStatus] = useState(null);
  const [elapsed, setElapsed] = useState(0);
  const [error, setError] = useState("");

  useEffect(() => {
    dispatch(fetchSOSStatus(sosId))
      .unwrap()
      .then(({ payload }) => {
        setStatus(payload);
        setElapsed(payload.duration_seconds);
      })
      .catch(() => setError("Could not load SOS status."));
    // eslint-disable-next-line
  }, [sosId]);

  // Local ticker for visual feedback.
  useEffect(() => {
    if (!status || status.status !== "active") return;
    const timer = setInterval(() => setElapsed((e) => e + 1), 1000);
    return () => clearInterval(timer);
    // eslint-disable-next-line
  }, [status]);

  async function handleCancel() {
    await dispatch(cancelSOS({ sosId, reason: "False alarm" })).unwrap();
    navigate("/dashboard");
  }

  return (
    <Stack spacing={2}>
      <Typography variant="h5" sx={{ color: "error.main", fontWeight: 700 }}>
        🆘 SOS ACTIVE
      </Typography>

      {error && <Alert severity="error">{error}</Alert>}
      {!status && !error && <CircularProgress />}

      {status && (
        <Card variant="outlined" sx={{ bgcolor: "error.light" }}>
          <CardContent>
            <Typography variant="h6">Elapsed: {elapsed}s</Typography>
            <Chip label={`Contacts notified: ${status.contacts_notified}`} sx={{ mt: 1 }} />
            <Chip label={`Severity: ${status.severity}`} sx={{ mt: 1, ml: 1 }} />
            {status.authorities_notified && <Chip label="Authorities alerted" sx={{ mt: 1, ml: 1 }} />}
          </CardContent>
        </Card>
      )}

      {status && status.contact_responses?.length > 0 && (
        <Card variant="outlined">
          <CardContent>
            <Typography variant="h6">Contact responses</Typography>
            <List dense>
              {status.contact_responses
                .filter((r) => RESPONSES.has(r.response))
                .map((r) => (
                  <ListItem key={r.contact_id}>
                    <ListItemText primary={`${r.response} — at ${r.responded_at}`} />
                  </ListItem>
                ))}
            </List>
          </CardContent>
        </Card>
      )}

      <TherapyChat sosId={sosId} height={320} />

      {status?.status === "active" && (
        <Button variant="outlined" color="secondary" onClick={handleCancel}>
          Cancel SOS (false alarm)
        </Button>
      )}
    </Stack>
  );
}