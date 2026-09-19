import {
  AccountCircle,
  Calculate,
  Chat,
  ContactEmergency,
  Dashboard,
  Gavel,
  Logout,
} from "@mui/icons-material";
import {
  AppBar,
  Box,
  Chip,
  Drawer,
  List,
  ListItemButton,
  ListItemIcon,
  ListItemText,
  Toolbar,
  Typography,
} from "@mui/material";
import { Navigate, NavLink, Outlet, useNavigate } from "react-router-dom";
import { useSelector } from "react-redux";

const NAV_ITEMS = [
  { to: "/dashboard", label: "Dashboard", icon: Dashboard },
  { to: "/calculator", label: "Calculator", icon: Calculate },
  { to: "/therapy", label: "Therapy", icon: Chat },
  { to: "/legal", label: "Legal Aid", icon: Gavel },
  { to: "/contacts", label: "Emergency Contacts", icon: ContactEmergency },
  { to: "/profile", label: "Profile & Safety", icon: AccountCircle },
];

/** Bright, pill-highlighted nav button (active link gets the gradient). */
function NavButton({ to, label, icon: Icon }) {
  return (
    <Box
      component={NavLink}
      to={to}
      end
      sx={(theme) => ({
        display: "flex",
        alignItems: "center",
        width: "100%",
        px: 2,
        py: 1.2,
        borderRadius: 3,
        color: "text.primary",
        textDecoration: "none",
        cursor: "pointer",
        "&[aria-current=page]": {
          background: "linear-gradient(90deg,#ff2e63,#ff6b81)",
          color: "#fff",
          boxShadow: "0 6px 14px rgba(255,46,99,0.25)",
        },
        "&:hover": {
          background: "#ffeaf2",
          color: "#c2185b",
        },
      })}
    >
      <ListItemIcon sx={{ color: "inherit", minWidth: 34 }}><Icon /></ListItemIcon>
      <Typography variant="body2" sx={{ fontWeight: 600, flex: 1 }}>
        {label}
      </Typography>
      {to === "/calculator" && (
        <Chip size="small" label="Discreet" sx={{ height: 20, fontSize: 10 }} />
      )}
    </Box>
  );
}

export default function Layout() {
  const token = useSelector((s) => s.auth.token) || localStorage.getItem("haven_token");
  const navigate = useNavigate();

  if (!token) {
    return <Navigate to="/login" replace />;
  }

  return (
    <Box sx={{ display: "flex", minHeight: "100vh", background: "#f7f2ff" }}>
      <AppBar
        position="fixed"
        sx={{
          zIndex: 20,
          height: 64,
          background: "linear-gradient(90deg,#ff2e63,#c2185b 55%,#7c3aed)",
          boxShadow: "0 8px 24px rgba(255,46,99,0.18)",
        }}
      >
        <Toolbar>
          <Box
            sx={{
              width: 38,
              height: 38,
              borderRadius: "50%",
              bgcolor: "common.white",
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
              mr: 1,
            }}
          >
            <Typography variant="h6" sx={{ lineHeight: 1 }}>🛡️</Typography>
          </Box>
          <Typography variant="h6" sx={{ fontWeight: 800, letterSpacing: 1, color: "#fff" }}>
            HAVEN
          </Typography>
          <Typography variant="body2" sx={{ ml: 1.5, color: "rgba(255,255,255,0.85)" }}>
            AI Women's Safety Platform
          </Typography>
        </Toolbar>
      </AppBar>

      <Drawer
        variant="permanent"
        sx={{
          width: 248,
          top: 64,
          height: "calc(100vh - 64px)",
          boxSizing: "border-box",
          bgcolor: "#ffffff",
          borderRight: "1px solid #e6eaf5",
          py: 2,
        }}
      >
        <Typography variant="overline" sx={{ display: "block", px: 2.5, pt: 1.5, color: "text.secondary" }}>
          Menu
        </Typography>
        <List sx={{ px: 1, "& .MuiListItem-root": { p: 0 } }}>
          {NAV_ITEMS.map((item) => <NavButton key={item.to} {...item} />)}
          <Box
            onClick={() => {
              localStorage.removeItem("haven_token");
              navigate("/login");
            }}
            sx={{
              display: "flex",
              alignItems: "center",
              px: 2,
              py: 1.2,
              borderRadius: 3,
              color: "text.secondary",
              cursor: "pointer",
              "&:hover": { background: "#fff0f5", color: "#c2185b" },
            }}
          >
            <ListItemIcon sx={{ color: "inherit", minWidth: 34 }}><Logout /></ListItemIcon>
            <Typography variant="body2" sx={{ fontWeight: 600, flex: 1 }}>Logout</Typography>
          </Box>
        </List>
      </Drawer>

      <Box component="main" sx={{ flexGrow: 1, mt: 9, px: 3, pb: 4 }}>
        <Outlet />
      </Box>
    </Box>
  );
}