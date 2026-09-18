import { Box, Paper, Typography } from "@mui/material";

/** Renders a single chat message bubble (user = right/blue, bot = left/grey). */
export default function ChatBubble({ message }) {
  const isUser = message.role === "user";
  const content = String(message.content ?? message.response ?? "");

  return (
    <Box
      sx={{
        display: "flex",
        justifyContent: isUser ? "flex-end" : "flex-start",
        mb: 1,
      }}
    >
      <Paper
        variant="outlined"
        sx={{
          maxWidth: "78%",
          px: 1.5,
          py: 1,
          bgcolor: isUser ? "primary.main" : "grey.100",
          color: isUser ? "#fff" : "text.primary",
          borderRadius: 2,
          whiteSpace: "pre-wrap",
        }}
      >
        <Typography variant="body1" sx={{ fontSize: 14 }}>
          {content}
        </Typography>
        <Typography variant="caption" sx={{ color: "text.secondary", display: "block" }}>
          {message.timestamp ? new Date(message.timestamp).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" }) : ""}
        </Typography>
      </Paper>
    </Box>
  );
}