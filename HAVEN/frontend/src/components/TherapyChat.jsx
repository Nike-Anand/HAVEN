import { Alert, Box, Button, CircularProgress, Paper, Stack, TextField, Typography } from "@mui/material";
import { useState } from "react";

import client, { apiError } from "../api/client.js";
import ChatBubble from "./ChatBubble.jsx";

/**
 * Reusable therapy chat.
 *
 * When `sosId` is provided the session is tied to an active SOS (spec:
 * TherapyDuringCrisis). Otherwise it starts a standalone session.
 */
export default function TherapyChat({ sosId = null, language = "en", height = 420 }) {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [sessionId, setSessionId] = useState(null);

  async function sendMessage() {
    const text = input.trim();
    if (!text || loading) return;
    setMessages([...messages, { role: "user", content: text, timestamp: new Date().toISOString() }]);
    setInput("");
    setLoading(true);
    setError("");
    try {
      const payload = { message: text, language, ...(sosId ? { sos_id: sosId } : {}) };
      const { data } = await client.post("/therapy/send-message", payload);
      setSessionId(data.session_id);
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: data.response, timestamp: new Date().toISOString() },
      ]);
      if (data.needs_human_support) {
        setError("A supporter has been flagged for human follow-up. You are not alone.");
      }
    } catch (err) {
      setError(apiError(err));
    } finally {
      setLoading(false);
    }
  }

  return (
    <Paper variant="outlined" sx={{ p: 2 }}>
      <Stack spacing={1}>
        {error && <Alert severity="warning">{error}</Alert>}
        <Box sx={{ height, overflowY: "auto", bgcolor: "grey.50", borderRadius: 1 }}>
          {messages.length === 0 && (
            <Typography variant="body2" sx={{ color: "text.secondary", py: 2 }}>
              {sosId
                ? "You're safe with me. Tell me how you're feeling — I'll stay with you."
                : "Hi, I'm HAVEN. Whatever you're carrying, share it here. It stays between us."}
            </Typography>
          )}
          {messages.map((m, i) => <ChatBubble key={i} message={m} />)}
        </Box>
        <Stack direction="row" spacing={1} sx={{ alignItems: "center" }}>
          <TextField
            fullWidth size="small" multiline minRows={1} maxRows={3}
            placeholder="How are you feeling?"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={loading}
            onKeyDown={(e) => { if (e.key === "Enter" && !e.shiftKey) { e.preventDefault(); sendMessage(); } }}
          />
          <Button variant="contained" onClick={sendMessage} disabled={loading || !input.trim()} sx={{ height: 48 }}>
            {loading ? <CircularProgress size={20} color="inherit" /> : "Send"}
          </Button>
        </Stack>
      </Stack>
    </Paper>
  );
}