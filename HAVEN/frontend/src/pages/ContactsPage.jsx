import {
  Alert,
  Button,
  Card,
  CardContent,
  Chip,
  CircularProgress,
  IconButton,
  List,
  ListItem,
  ListItemSecondaryAction,
  ListItemText,
  MenuItem,
  Stack,
  TextField,
  Typography,
} from "@mui/material";
import { Delete } from "@mui/icons-material";
import { useDispatch, useSelector } from "react-redux";
import { useEffect, useState } from "react";

import { apiError } from "../api/client.js";
import {
  addContact, deleteContact, fetchContacts, verifyContact,
} from "../store/slices/contactsSlice.js";

export default function ContactsPage() {
  const dispatch = useDispatch();
  const { list, status } = useSelector((s) => s.contacts);
  const [form, setForm] = useState({ name: "", phone: "", relationship: "family", priority: 3 });
  const [error, setError] = useState("");

  useEffect(() => {
    dispatch(fetchContacts());
    // eslint-disable-next-line
  }, []);

  function update(key) {
    return (e) => setForm({ ...form, [key]: e.target.value });
  }

  async function handleAdd() {
    setError("");
    try {
      await dispatch(addContact(form)).unwrap();
      setForm({ name: "", phone: "", relationship: "family", priority: 3 });
      dispatch(fetchContacts());
    } catch (err) {
      setError(apiError(err));
    }
  }

  async function handleVerify(contact) {
    await dispatch(verifyContact({ contactId: contact.contact_id, verificationCode: "000000" })).unwrap();
    dispatch(fetchContacts());
  }

  async function handleDelete(contact) {
    await dispatch(deleteContact(contact.contact_id)).unwrap();
  }

  return (
    <Stack spacing={2}>
      <Typography variant="h5" sx={{ fontWeight: 600 }}>Emergency Contacts</Typography>
      {error && <Alert severity="error">{error}</Alert>}

      <Card variant="outlined">
        <CardContent>
          <Typography variant="h6">Add a trusted contact</Typography>
          <Stack direction="row" spacing={1} sx={{ alignItems: "center" }}>
            <TextField label="Name" size="small" value={form.name} onChange={update("name")} />
            <TextField label="Phone" size="small" value={form.phone} onChange={update("phone")} />
            <TextField select label="Relationship" size="small" value={form.relationship} sx={{ minWidth: 140 }}>
              {["family", "friend", "counselor", "police"].map((r) => (
                <MenuItem key={r} value={r}>{r}</MenuItem>
              ))}
            </TextField>
            <Button variant="contained" onClick={handleAdd} disabled={!form.name || !form.phone}>
              Add
            </Button>
          </Stack>
          <Typography variant="caption" sx={{ color: "text.secondary", display: "block", mt: 1 }}>
            A verification code is sent to the contact before they can receive alerts (demo: any code verifies).
          </Typography>
        </CardContent>
      </Card>

      {status === "loading" && <CircularProgress />}
      <List>
        {list.map((c) => (
          <ListItem key={c.contact_id}>
            <ListItemText
              primary={`${c.name}  ·  ${c.relationship}`}
              secondary={`${c.phone}  ·  priority ${c.priority}`}
            />
            <ListItemSecondaryAction>
              <Chip
                size="small"
                color={c.status === "verified" ? "success" : "warning"}
                label={c.status}
              />
              {c.status !== "verified" && (
                <Button size="small" onClick={() => handleVerify(c)}>Verify</Button>
              )}
              <IconButton edge="end" aria-label="delete" onClick={() => handleDelete(c)}>
                <Delete color="error" />
              </IconButton>
            </ListItemSecondaryAction>
          </ListItem>
        ))}
        {list.length === 0 && <ListItem><ListItemText primary="No contacts yet — add your trusted network above." /></ListItem>}
      </List>
    </Stack>
  );
}