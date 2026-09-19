import {
  Alert,
  Box,
  Button,
  CircularProgress,
  Paper,
  Stack,
  TextField,
  Typography,
} from "@mui/material";
import { useState } from "react";

import client, { apiError } from "../api/client.js";
import ChatBubble from "../components/ChatBubble.jsx";

export default function LegalPage() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  async function ask() {
    const text = input.trim();
    if (!text || loading) return;
    setMessages([...messages, { role: "user", content: text, timestamp: new Date().toISOString() }]);
    setInput("");
    setLoading(true);
    setError("");
    try {
      const { data } = await client.post("/legal/ask", { query: text, language: "en" });
      const reply = data.reply || data.response || "";
      const disclaimer = data.disclaimer ? `\n\n_Disclaimer: ${data.disclaimer}_` : "";
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: `${reply}${disclaimer}`,
          timestamp: new Date().toISOString(),
        },
      ]);
    } catch (err) {
      setError(apiError(err));
    } finally {
      setLoading(false);
    }
  }

  return (
    <Stack spacing={2}>
      <Typography variant="h5" sx={{ fontWeight: 600 }}>Legal Guidance</Typography>
      <Typography variant="body2" sx={{ color: "text.secondary" }}>
        Indian women's rights: DV Act 2005, Dowry Act 1961, POSH Act 2013, IPC, FIR steps.
      </Typography>

      {error && <Alert severity="error">{error}</Alert>}
      <Paper variant="outlined" sx={{ p: 2 }}>
        <Box sx={{ height: 400, overflowY: "auto", bgcolor: "grey.100", borderRadius: 1 }}>
          {messages.length === 0 && (
            <Typography variant="body2" sx={{ color: "text.secondary", py: 2 }}>
              Ask for example: "What can I do about domestic violence?" or "How do I file an FIR?"
            </Typography>
          )}
          {messages.map((m, i) => <ChatBubble key={i} message={m} />)}
        </Box>
        <Stack direction="row" spacing={1} sx={{ alignItems: "center" }}>
          <TextField fullWidth size="small" multiline placeholder="Ask about your rights…"
            value={input} onChange={(e) => setInput(e.target.value)} disabled={loading}
            onKeyDown={(e) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); ask(); } }} />
          <Button variant="contained" onClick={ask} disabled={loading || !input.trim()} sx={{ height: 48 }}>
            {loading ? <CircularProgress size={20} color="inherit" /> : "Ask"}
          </Button>
        </Stack>
      </Paper>
    </Stack>
  );
}