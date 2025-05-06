import React, { useState, useMemo } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';
import { IconButton, Box, useMediaQuery } from '@mui/material';
import Brightness4Icon from '@mui/icons-material/Brightness4';
import Brightness7Icon from '@mui/icons-material/Brightness7';

// Components
import Header from './components/Header';
import Footer from './components/Footer';

// Pages
import Home from './pages/Home';
import AnalysisTool from './pages/AnalysisTool';
import About from './pages/About';

// Create ThemeContext to manage theme state across components
export const ColorModeContext = React.createContext({ 
  toggleColorMode: () => {},
  mode: 'dark'
});

function App() {
  // Use system preference as initial mode
  const prefersDarkMode = useMediaQuery('(prefers-color-scheme: dark)');
  const [mode, setMode] = useState(prefersDarkMode ? 'dark' : 'dark'); // Default to dark theme

  // Color mode toggle context
  const colorMode = useMemo(
    () => ({
      toggleColorMode: () => {
        setMode((prevMode) => (prevMode === 'light' ? 'dark' : 'light'));
      },
      mode,
    }),
    [mode],
  );

  // Create dynamic theme based on mode
  const theme = useMemo(
    () =>
      createTheme({
        palette: {
          mode,
          ...(mode === 'light'
            ? {
                // Light mode
                primary: {
                  main: '#2563eb', // Blue 600
                  light: '#60a5fa', // Blue 400
                  dark: '#1d4ed8', // Blue 700
                  contrastText: '#ffffff',
                },
                secondary: {
                  main: '#8b5cf6', // Violet 500
                  light: '#a78bfa', // Violet 400
                  dark: '#7c3aed', // Violet 600
                },
                background: {
                  default: '#f8fafc', // Slate 50
                  paper: '#ffffff',
                },
                text: {
                  primary: '#0f172a', // Slate 900
                  secondary: '#64748b', // Slate 500
                },
                divider: '#e2e8f0', // Slate 200
              }
            : {
                // Dark mode
                primary: {
                  main: '#3b82f6', // Blue 500
                  light: '#60a5fa', // Blue 400
                  dark: '#2563eb', // Blue 600
                  contrastText: '#ffffff',
                },
                secondary: {
                  main: '#8b5cf6', // Violet 500
                  light: '#a78bfa', // Violet 400
                  dark: '#7c3aed', // Violet 600
                },
                background: {
                  default: '#0f172a', // Slate 900
                  paper: '#1e293b', // Slate 800
                },
                text: {
                  primary: '#f8fafc', // Slate 50
                  secondary: '#cbd5e1', // Slate 300
                },
                divider: '#334155', // Slate 700
              }),
        },
        typography: {
          fontFamily: "'Inter', 'Poppins', sans-serif",
          h1: {
            fontFamily: "'Plus Jakarta Sans', 'Raleway', sans-serif",
            fontWeight: 800,
            letterSpacing: '-0.015em',
          },
          h2: {
            fontFamily: "'Plus Jakarta Sans', 'Raleway', sans-serif",
            fontWeight: 700,
            letterSpacing: '-0.01em',
          },
          h3: {
            fontFamily: "'Plus Jakarta Sans', 'Raleway', sans-serif",
            fontWeight: 700,
            letterSpacing: '-0.01em',
          },
          h4: {
            fontFamily: "'Plus Jakarta Sans', 'Raleway', sans-serif",
            fontWeight: 600,
          },
          h5: {
            fontFamily: "'Plus Jakarta Sans', 'Raleway', sans-serif",
            fontWeight: 600,
          },
          h6: {
            fontFamily: "'Plus Jakarta Sans', 'Raleway', sans-serif",
            fontWeight: 600,
          },
          button: {
            textTransform: 'none',
            fontWeight: 600,
          },
          body1: {
            lineHeight: 1.7,
          },
        },
        shape: {
          borderRadius: 12,
        },
        components: {
          MuiAppBar: {
            styleOverrides: {
              root: {
                background: mode === 'dark' ? '#1e293b' : '#ffffff',
                boxShadow: mode === 'dark' 
                  ? '0 1px 3px 0 rgba(0, 0, 0, 0.4), 0 1px 2px 0 rgba(0, 0, 0, 0.24)'
                  : '0 1px 3px 0 rgba(0, 0, 0, 0.1), 0 1px 2px 0 rgba(0, 0, 0, 0.06)',
              },
            },
          },
          MuiButton: {
            styleOverrides: {
              root: {
                borderRadius: 8,
                padding: '10px 20px',
                fontWeight: 600,
                boxShadow: 'none',
                textTransform: 'none',
                '&:hover': {
                  boxShadow: mode === 'dark' 
                    ? '0 4px 12px rgba(59, 130, 246, 0.5)'
                    : '0 4px 12px rgba(59, 130, 246, 0.3)',
                  transform: 'translateY(-2px)',
                },
                transition: 'all 0.2s ease-in-out',
              },
              contained: {
                '&.MuiButton-containedPrimary': {
                  background: mode === 'dark' 
                    ? 'linear-gradient(90deg, #3b82f6 0%, #60a5fa 100%)' 
                    : 'linear-gradient(90deg, #2563eb 0%, #3b82f6 100%)',
                },
                '&.MuiButton-containedSecondary': {
                  background: 'linear-gradient(90deg, #8b5cf6 0%, #a78bfa 100%)',
                },
              },
              outlined: {
                borderWidth: 2,
                '&:hover': {
                  borderWidth: 2,
                },
              },
            },
          },
          MuiCard: {
            styleOverrides: {
              root: {
                borderRadius: 16,
                boxShadow: mode === 'dark' 
                  ? '0 4px 20px rgba(0, 0, 0, 0.25)'
                  : '0 4px 20px rgba(0, 0, 0, 0.08)',
                transition: 'transform 0.3s ease, box-shadow 0.3s ease',
                '&:hover': {
                  transform: 'translateY(-5px)',
                  boxShadow: mode === 'dark' 
                    ? '0 10px 30px rgba(0, 0, 0, 0.35)'
                    : '0 10px 30px rgba(0, 0, 0, 0.12)',
                },
                ...(mode === 'dark' && {
                  background: 'linear-gradient(145deg, #1e293b 0%, #0f172a 100%)',
                  border: '1px solid #334155',
                }),
              },
            },
          },
          MuiIconButton: {
            styleOverrides: {
              root: {
                '&:hover': {
                  background: mode === 'dark' 
                    ? 'rgba(255, 255, 255, 0.08)' 
                    : 'rgba(0, 0, 0, 0.04)',
                },
              },
            },
          },
          MuiCssBaseline: {
            styleOverrides: {
              body: {
                scrollbarWidth: 'thin',
                '&::-webkit-scrollbar': {
                  width: '8px',
                },
                '&::-webkit-scrollbar-track': {
                  background: mode === 'dark' ? '#0f172a' : '#f1f5f9',
                },
                '&::-webkit-scrollbar-thumb': {
                  background: mode === 'dark' ? '#334155' : '#cbd5e1',
                  borderRadius: '4px',
                },
                '&::-webkit-scrollbar-thumb:hover': {
                  background: mode === 'dark' ? '#475569' : '#94a3b8',
                },
              },
            },
          },
          MuiListItem: {
            styleOverrides: {
              root: {
                borderRadius: 8,
                '&:hover': {
                  backgroundColor: mode === 'dark' 
                    ? 'rgba(59, 130, 246, 0.08)' 
                    : 'rgba(59, 130, 246, 0.04)',
                },
              },
            },
          },
          MuiInputBase: {
            styleOverrides: {
              root: {
                borderRadius: 8,
              },
            },
          },
          MuiOutlinedInput: {
            styleOverrides: {
              root: {
                borderRadius: 8,
                ...(mode === 'dark' && {
                  '& .MuiOutlinedInput-notchedOutline': {
                    borderColor: '#334155',
                  },
                  '&:hover .MuiOutlinedInput-notchedOutline': {
                    borderColor: '#475569',
                  },
                  '&.Mui-focused .MuiOutlinedInput-notchedOutline': {
                    borderColor: '#3b82f6',
                  },
                }),
              },
            },
          },
        },
      }),
    [mode],
  );

  return (
    <ColorModeContext.Provider value={colorMode}>
      <ThemeProvider theme={theme}>
        <CssBaseline />
        <Router>
          <div className="App">
            <Header />
            <main>
              <Routes>
                <Route path="/" element={<Home />} />
                <Route path="/analysis" element={<AnalysisTool />} />
                <Route path="/about" element={<About />} />
              </Routes>
            </main>
            <Footer />
          </div>
        </Router>
      </ThemeProvider>
    </ColorModeContext.Provider>
  );
}

export default App; 