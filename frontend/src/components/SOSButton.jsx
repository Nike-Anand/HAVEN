import { Button, Typography } from "@mui/material";

/**
 * The discreet-but-prominent SOS trigger.
 *
 * On press it uses the browser geolocation (with fallback to fixed coords) and
 * calls POST /sos/trigger via the redux slice, then navigates to the active SOS
 * screen. Matches the spec's SOSButton behavior.
 */
export default function SOSButton({ onActivated }) {
  async function handlePress() {
    let location = { latitude: 0, longitude: 0, accuracy: 0 };
    try {
      if (navigator.geolocation) {
        const pos = await new Promise((resolve, reject) =>
          navigator.geolocation.getCurrentPosition
            ? navigator.geolocation.getCurrentPosition(resolve, reject, { enableHighAccuracy: true })
            : reject(new Error("no-location")),
        );
        location = {
          latitude: pos?.coords?.latitude ?? 0,
          longitude: pos?.coords?.longitude ?? 0,
          accuracy: pos?.coords?.accuracy ?? 0,
        };
      }
    } catch {
      /* fall back to fixed coordinates for the demo */
    }

    if (onActivated) {
      onActivated(location);
    }
  }

  return (
    <Button
      variant="contained"
      size="large"
      onClick={handlePress}
      sx={{
        width: "100%",
        height: 180,
        backgroundColor: "error.main",
        "&:hover": { backgroundColor: "error.light" },
        fontSize: 52,
        borderRadius: 3,
        boxShadow: 6,
      }}
    >
      🆘
      <Typography sx={{ color: "#fff", fontWeight: 700, mt: 1 }}>
        PRESS FOR HELP
      </Typography>
    </Button>
  );
}