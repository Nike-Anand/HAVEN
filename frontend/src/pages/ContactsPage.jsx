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
import { addContact, deleteContact, fetchContacts } from "../store/slices/contactsSlice.js";

export default function ContactsPage() {
  const dispatch = useDispatch();
  const { list, status } = useSelector((s) => s.contacts);
  const [form, setForm] = useState({ name: "", phone: "", email: "", relationship: "Mother", priority: 3 });
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
      setForm({ name: "", phone: "", email: "", relationship: "Mother", priority: 3 });
      dispatch(fetchContacts());
    } catch (err) {
      setError(apiError(err));
    }
  }

  async function handleDelete(contact) {
    await dispatch(deleteContact(contact.contact_id)).unwrap();
  }

  return (
    <Stack spacing={2.5}>
      <Typography variant="h4" sx={{ fontWeight: 800 }}>Emergency Contacts</Typography>
      {error && <Alert severity="error">{error}</Alert>}

      <Card
        variant="outlined"
        sx={{
          borderRadius: 3,
          border: "1px solid rgba(124,58,237,0.12)",
          background: "linear-gradient(180deg, rgba(255,255,255,0.98), rgba(245,242,255,0.96))",
        }}
      >
        <CardContent>
          <Typography variant="h6" sx={{ fontWeight: 700, mb: 1.5 }}>Add a trusted contact</Typography>
          <Stack direction={{ xs: "column", md: "row" }} spacing={1.2} sx={{ alignItems: "stretch" }}>
            <TextField label="Name" size="small" value={form.name} onChange={update("name")} sx={{ flex: 1, bgcolor: "#fff" }} />
            <TextField label="Phone" size="small" value={form.phone} onChange={update("phone")} sx={{ flex: 1, bgcolor: "#fff" }} />
            <TextField label="Email" type="email" size="small" value={form.email} onChange={update("email")} sx={{ flex: 1, bgcolor: "#fff" }} />
            <TextField select label="Relationship" size="small" value={form.relationship} sx={{ minWidth: 180, bgcolor: "#fff" }}>
              {["Mother", "Father", "Sibling", "Spouse", "Friend", "Counselor", "Other"].map((r) => (
                <MenuItem key={r} value={r}>{r}</MenuItem>
              ))}
            </TextField>
            <Button
              variant="contained"
              onClick={handleAdd}
              disabled={!form.name || !form.phone}
              sx={{ minWidth: 120, borderRadius: 2, fontWeight: 700 }}
            >
              Add
            </Button>
          </Stack>
        </CardContent>
      </Card>

      {status === "loading" && <CircularProgress />}
      <List>
        {list.map((c) => (
          <ListItem key={c.contact_id} sx={{ borderRadius: 3, border: "1px solid rgba(0,0,0,0.05)", mb: 1, bgcolor: "#fff" }}>
            <ListItemText
              primary={`${c.name}  ·  ${c.relationship}`}
              secondary={`${c.phone}  ·  priority ${c.priority}`}
            />
            <ListItemSecondaryAction>
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