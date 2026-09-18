import {
  AccountCircle,
  Chat,
  ContactEmergency,
  Dashboard,
  Gavel,
  Logout,
} from "@mui/icons-material";
import {
  AppBar,
  Box,
  Drawer,
  List,
  ListItem,
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
  { to: "/therapy", label: "Therapy", icon: Chat },
  { to: "/legal", label: "Legal Aid", icon: Gavel },
  { to: "/contacts", label: "Emergency Contacts", icon: ContactEmergency },
  { to: "/profile", label: "Profile & Safety", icon: AccountCircle },
];

export default function Layout() {
  const token = useSelector((s) => s.auth.token) || localStorage.getItem("haven_token");
  const navigate = useNavigate();

  if (!token) {
    return <Navigate to="/login" replace />;
  }

  return (
    <Box sx={{ display: "flex", minHeight: "100vh" }}>
      <AppBar position="fixed" sx={{ zIndex: 20, height: 64 }}>
        <Toolbar>
          <Typography variant="h6" sx={{ fontWeight: 700, letterSpacing: 1 }}>
            🛡️ HAVEN
          </Typography>
          <Typography variant="body2" sx={{ ml: 1, color: "#9aa7b8" }}>
            Safety Platform
          </Typography>
        </Toolbar>
      </AppBar>

      <Drawer
        variant="permanent"
        sx={{
          width: 240,
          top: 64,
          height: "calc(100vh - 64px)",
          boxSizing: "border-box",
        }}
      >
        <Box sx={{ px: 2, py: 2 }}>
          <Typography variant="body2" sx={{ fontWeight: 600 }}>
            Menu
          </Typography>
        </Box>
        <List>
          {NAV_ITEMS.map(({ to, label, icon: Icon }) => (
            <ListItemButton key={to} component={NavLink} to={to}>
              <ListItemIcon sx={{ color: "primary.main" }}>
                <Icon />
              </ListItemIcon>
              <ListItemText primary={label} />
            </ListItemButton>
          ))}
          <ListItemButton onClick={() => { localStorage.removeItem("haven_token"); navigate("/login"); }}>
            <ListItemIcon><Logout /></ListItemIcon>
            <ListItemText primary="Logout" />
          </ListItemButton>
        </List>
      </Drawer>

      <Box component="main" sx={{ flexGrow: 1, mt: 8, px: 3 }}>
        <Outlet />
      </Box>
    </Box>
  );
}