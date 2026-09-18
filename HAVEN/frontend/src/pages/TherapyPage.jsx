import { Typography } from "@mui/material";
import { Box } from "@mui/material";

import TherapyChat from "../components/TherapyChat.jsx";

export default function TherapyPage() {
  return (
    <Box>
      <Typography variant="h5" sx={{ fontWeight: 600 }}>AI Therapy</Typography>
      <Typography variant="body2" sx={{ color: "text.secondary", mb: 2 }}>
        Compassionate, judgment-free crisis support. Responsive even offline.
      </Typography>
      <TherapyChat />
    </Box>
  );
}