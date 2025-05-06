import React, { useState, useContext } from 'react';
import { Link as RouterLink, useLocation } from 'react-router-dom';
import {
  AppBar,
  Box,
  Button,
  Container,
  Drawer,
  IconButton,
  Link,
  List,
  ListItem,
  ListItemText,
  Toolbar,
  Typography,
  useMediaQuery,
  useTheme,
  Avatar,
  Tooltip,
  Fade,
} from '@mui/material';
import MenuIcon from '@mui/icons-material/Menu';
import HealthAndSafetyIcon from '@mui/icons-material/HealthAndSafety';
import Brightness4Icon from '@mui/icons-material/Brightness4';
import Brightness7Icon from '@mui/icons-material/Brightness7';
import { ColorModeContext } from '../App';

const navItems = [
  { text: 'Home', path: '/' },
  { text: 'Analysis Tool', path: '/analysis' },
  { text: 'About', path: '/about' },
];

const Header = () => {
  const theme = useTheme();
  const location = useLocation();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const [drawerOpen, setDrawerOpen] = useState(false);
  const colorMode = useContext(ColorModeContext);
  const isDarkMode = theme.palette.mode === 'dark';

  const handleDrawerToggle = () => {
    setDrawerOpen(!drawerOpen);
  };

  const isActive = (path) => {
    return location.pathname === path;
  };

  const drawer = (
    <Box 
      onClick={handleDrawerToggle} 
      sx={{ 
        textAlign: 'center', 
        p: 3,
        height: '100%', 
        display: 'flex', 
        flexDirection: 'column',
        background: theme.palette.background.paper,
      }}
    >
      <Box sx={{ display: 'flex', alignItems: 'center', justifyContent: 'center', mb: 4 }}>
        <Avatar 
          sx={{ 
            mr: 1.5, 
            bgcolor: 'primary.main',
            width: 40,
            height: 40,
          }}
        >
          <HealthAndSafetyIcon />
        </Avatar>
        <Typography variant="h5" component="div" color="primary" fontWeight={700}>
          AR-MED
        </Typography>
      </Box>
      <List sx={{ flexGrow: 1 }}>
        {navItems.map((item) => (
          <ListItem 
            key={item.text} 
            component={RouterLink} 
            to={item.path}
            sx={{
              my: 1,
              borderRadius: 2,
              color: isActive(item.path) ? 'primary.main' : 'text.primary',
              fontWeight: isActive(item.path) ? 700 : 500,
              bgcolor: isActive(item.path) ? (isDarkMode ? 'rgba(59, 130, 246, 0.08)' : 'rgba(59, 130, 246, 0.04)') : 'transparent',
              '&:hover': {
                bgcolor: isDarkMode ? 'rgba(59, 130, 246, 0.12)' : 'rgba(59, 130, 246, 0.08)',
              },
            }}
          >
            <ListItemText 
              primary={item.text} 
              primaryTypographyProps={{ 
                fontWeight: 'inherit', 
                fontSize: '1rem',
              }} 
            />
          </ListItem>
        ))}
      </List>
      <Box sx={{ mt: 4 }}>
        <Tooltip title={isDarkMode ? "Switch to light mode" : "Switch to dark mode"}>
          <IconButton 
            onClick={(e) => {
              e.stopPropagation();
              colorMode.toggleColorMode();
            }} 
            color="primary"
            sx={{ 
              p: 1.5, 
              border: '2px solid',
              borderColor: 'primary.main',
              borderRadius: 2,
            }}
          >
            {isDarkMode ? <Brightness7Icon /> : <Brightness4Icon />}
          </IconButton>
        </Tooltip>
      </Box>
    </Box>
  );

  return (
    <AppBar 
      position="sticky" 
      color="default" 
      elevation={0} 
      sx={{ 
        borderBottom: 1, 
        borderColor: 'divider', 
      }}
    >
      <Container maxWidth="lg">
        <Toolbar disableGutters sx={{ justifyContent: 'space-between', py: 1.5 }}>
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <Avatar 
              sx={{ 
                mr: 1.5, 
                bgcolor: 'primary.main',
                width: 40,
                height: 40,
                boxShadow: isDarkMode ? '0 0 10px rgba(59, 130, 246, 0.5)' : 'none',
              }}
            >
              <HealthAndSafetyIcon />
            </Avatar>
            <Typography
              variant="h5"
              component={RouterLink}
              to="/"
              sx={{
                fontWeight: 700,
                color: 'primary.main',
                textDecoration: 'none',
                display: 'flex',
                alignItems: 'center',
                letterSpacing: '-0.02em',
              }}
            >
              AR-MED
            </Typography>
          </Box>

          {isMobile ? (
            <>
              <Box sx={{ display: 'flex', alignItems: 'center' }}>
                <Tooltip title={isDarkMode ? "Switch to light mode" : "Switch to dark mode"}>
                  <IconButton 
                    onClick={colorMode.toggleColorMode} 
                    color="primary"
                    sx={{ mr: 1 }}
                  >
                    {isDarkMode ? <Brightness7Icon /> : <Brightness4Icon />}
                  </IconButton>
                </Tooltip>
                <IconButton
                  aria-label="open drawer"
                  edge="end"
                  onClick={handleDrawerToggle}
                  sx={{
                    borderRadius: 2,
                    p: 1,
                    border: '2px solid',
                    borderColor: 'primary.main',
                    color: 'primary.main',
                  }}
                >
                  <MenuIcon />
                </IconButton>
              </Box>
              <Drawer
                anchor="right"
                open={drawerOpen}
                onClose={handleDrawerToggle}
                PaperProps={{
                  sx: {
                    width: '280px',
                    borderTopLeftRadius: 16,
                    borderBottomLeftRadius: 16,
                  }
                }}
              >
                {drawer}
              </Drawer>
            </>
          ) : (
            <Box sx={{ display: 'flex', alignItems: 'center' }}>
              {navItems.map((item) => (
                <Button
                  key={item.text}
                  component={RouterLink}
                  to={item.path}
                  sx={{
                    mx: 1,
                    px: 2,
                    py: 1,
                    color: isActive(item.path) ? 'primary.main' : 'text.primary',
                    fontWeight: isActive(item.path) ? 700 : 500,
                    position: 'relative',
                    overflow: 'hidden',
                    '&:hover': {
                      backgroundColor: isDarkMode ? 'rgba(59, 130, 246, 0.08)' : 'rgba(59, 130, 246, 0.04)',
                    },
                    '&::after': isActive(item.path) ? {
                      content: '""',
                      position: 'absolute',
                      bottom: 0,
                      left: '20%',
                      width: '60%',
                      height: '3px',
                      bgcolor: 'primary.main',
                      borderRadius: '3px 3px 0 0',
                    } : {},
                  }}
                >
                  {item.text}
                </Button>
              ))}
              <Tooltip 
                title={isDarkMode ? "Switch to light mode" : "Switch to dark mode"}
                TransitionComponent={Fade}
                TransitionProps={{ timeout: 600 }}
              >
                <IconButton 
                  onClick={colorMode.toggleColorMode} 
                  color="primary"
                  sx={{ 
                    ml: 2,
                    mr: 2,
                    border: '2px solid',
                    borderColor: 'primary.main',
                    borderRadius: 2,
                  }}
                >
                  {isDarkMode ? <Brightness7Icon /> : <Brightness4Icon />}
                </IconButton>
              </Tooltip>
              <Button
                variant="contained"
                color="primary"
                component={RouterLink}
                to="/analysis"
                sx={{ 
                  ml: 1,
                  px: 2.5,
                  py: 1,
                  borderRadius: 2,
                  fontWeight: 600,
                  boxShadow: isDarkMode ? '0 0 15px rgba(59, 130, 246, 0.3)' : 'none',
                }}
              >
                Try Analysis
              </Button>
            </Box>
          )}
        </Toolbar>
      </Container>
    </AppBar>
  );
};

export default Header; 