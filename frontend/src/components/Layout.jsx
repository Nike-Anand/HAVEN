import {
  AccountCircle,
  Chat,
  ContactEmergency,
  Dashboard,
  Gavel,
  Logout,
  Menu,
} from "@mui/icons-material";
import {
  AppBar,
  Box,
  Chip,
  Drawer,
  IconButton,
  List,
  ListItemIcon,
  Toolbar,
  Typography,
  useMediaQuery,
  useTheme,
} from "@mui/material";
import { Navigate, NavLink, Outlet, useNavigate } from "react-router-dom";
import { useSelector } from "react-redux";
import { useState } from "react";

const NAV_ITEMS = [
  { to: "/dashboard", label: "Dashboard", icon: Dashboard },
  { to: "/therapy", label: "Therapy", icon: Chat },
  { to: "/legal", label: "Legal Aid", icon: Gavel },
  { to: "/contacts", label: "Emergency Contacts", icon: ContactEmergency },
  { to: "/profile", label: "Profile & Safety", icon: AccountCircle },
];

function NavButton({ to, label, icon: Icon }) {
  return (
    <Box
      component={NavLink}
      to={to}
      end
      sx={{
        display: "flex",
        alignItems: "center",
        width: "100%",
        px: 2,
        py: 1.3,
        borderRadius: 3,
        color: "text.primary",
        textDecoration: "none",
        cursor: "pointer",
        transition: "all 0.2s ease",
        "&[aria-current=page]": {
          background: "linear-gradient(90deg,#ff2e63,#ff6b81)",
          color: "#fff",
          boxShadow: "0 8px 16px rgba(255,46,99,0.22)",
        },
        "&:hover": {
          background: "#fff0f5",
          color: "#c2185b",
        },
      }}
    >
      <ListItemIcon sx={{ color: "inherit", minWidth: 34 }}><Icon /></ListItemIcon>
      <Typography variant="body2" sx={{ fontWeight: 700, flex: 1 }}>
        {label}
      </Typography>
    </Box>
  );
}

export default function Layout() {
  const token = useSelector((s) => s.auth.token) || localStorage.getItem("haven_token");
  const navigate = useNavigate();
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down("md"));
  const [drawerOpen, setDrawerOpen] = useState(false);

  if (!token) {
    return <Navigate to="/login" replace />;
  }

  const drawerContent = (
    <Box sx={{ width: 256, pt: 2, px: 1 }}>
      <Typography variant="overline" sx={{ display: "block", px: 2.5, pb: 1, color: "text.secondary" }}>
        Menu
      </Typography>
      <Box sx={{ display: "flex", flexDirection: "column", gap: 0.5 }}>
        {NAV_ITEMS.map((item) => (
          <NavButton key={item.to} {...item} />
        ))}
        <Box
          onClick={() => {
            localStorage.removeItem("haven_token");
            navigate("/login");
            setDrawerOpen(false);
          }}
          sx={{
            display: "flex",
            alignItems: "center",
            px: 2,
            py: 1.25,
            borderRadius: 3,
            color: "text.secondary",
            cursor: "pointer",
            "&:hover": { background: "#fff0f5", color: "#c2185b" },
          }}
        >
          <ListItemIcon sx={{ color: "inherit", minWidth: 34 }}><Logout /></ListItemIcon>
          <Typography variant="body2" sx={{ fontWeight: 700, flex: 1 }}>Logout</Typography>
        </Box>
      </Box>
    </Box>
  );

  return (
    <Box sx={{ display: "flex", minHeight: "100vh", background: "#f7f2ff" }}>
      <AppBar
        position="fixed"
        sx={{
          zIndex: 1400,
          background: "linear-gradient(90deg,#ff2e63,#c2185b 52%,#7c3aed)",
          boxShadow: "0 12px 28px rgba(255,46,99,0.18)",
        }}
      >
        <Toolbar sx={{ minHeight: 68 }}>
          {isMobile && (
            <IconButton
              edge="start"
              color="inherit"
              aria-label="open menu"
              onClick={() => setDrawerOpen(true)}
              sx={{ mr: 1.5 }}
            >
              <Menu />
            </IconButton>
          )}
          <Box sx={{ display: "flex", alignItems: "center", mr: 1.5 }}>
            <Box
              sx={{
                width: 38,
                height: 38,
                borderRadius: "50%",
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
                bgcolor: "common.white",
                fontSize: 22,
              }}
            >
              🛡️
            </Box>
          </Box>
          <Typography variant="h6" sx={{ fontWeight: 800, letterSpacing: 1, color: "#fff" }}>
            HAVEN
          </Typography>
          <Typography variant="body2" sx={{ ml: 1.5, color: "rgba(255,255,255,0.88)", display: { xs: "none", sm: "block" } }}>
            AI Women&apos;s Safety Platform
          </Typography>
        </Toolbar>
      </AppBar>

      {!isMobile ? (
        <Box
          component="aside"
          sx={{
            width: 260,
            minWidth: 260,
            borderRight: "1px solid rgba(124,58,237,0.12)",
            bgcolor: "#ffffff",
            pt: 10,
            pb: 2,
            px: 1,
            position: "sticky",
            top: 0,
            height: "100vh",
          }}
        >
          {drawerContent}
        </Box>
      ) : (
        <Drawer
          anchor="left"
          open={drawerOpen}
          onClose={() => setDrawerOpen(false)}
          ModalProps={{ keepMounted: true }}
          PaperProps={{ sx: { bgcolor: "#ffffff", borderRight: "1px solid rgba(124,58,237,0.12)" } }}
        >
          {drawerContent}
        </Drawer>
      )}

      <Box component="main" sx={{ flexGrow: 1, mt: 9, px: { xs: 2, md: 3 }, pb: 4, width: "100%" }}>
        <Outlet />
      </Box>
    </Box>
  );
}