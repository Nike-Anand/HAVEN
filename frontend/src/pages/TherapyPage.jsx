import { Box, Card, CardContent, Stack, Typography } from "@mui/material";

import TherapyChat from "../components/TherapyChat.jsx";

export default function TherapyPage() {
  return (
    <Box sx={{ maxWidth: 1100, mx: "auto", py: 1 }}>
      <Stack spacing={2} sx={{ mb: 3 }}>
        <Typography variant="h4" sx={{ fontWeight: 800, color: "primary.main" }}>
          AI Therapy
        </Typography>
        <Typography variant="body1" sx={{ color: "text.secondary", maxWidth: 760 }}>
          Compassionate, judgment-free support designed to help you feel heard, grounded, and safer during stressful moments.
        </Typography>
      </Stack>

      <Card
        variant="outlined"
        sx={{
          borderRadius: 4,
          border: "1px solid rgba(124,58,237,0.14)",
          background: "linear-gradient(135deg, rgba(255,46,99,0.04), rgba(124,58,237,0.06), rgba(255,255,255,0.98))",
          boxShadow: "0 22px 50px rgba(124,58,237,0.08)",
        }}
      >
        <CardContent sx={{ p: { xs: 2, md: 3 } }}>
          <TherapyChat />
        </CardContent>
      </Card>
    </Box>
  );
}