import React from 'react';
import { Link as RouterLink } from 'react-router-dom';
import {
  Box,
  Container,
  Divider,
  Grid,
  IconButton,
  Link,
  Stack,
  Typography,
  useTheme,
} from '@mui/material';
import HealthAndSafetyIcon from '@mui/icons-material/HealthAndSafety';
import GitHubIcon from '@mui/icons-material/GitHub';
import LinkedInIcon from '@mui/icons-material/LinkedIn';
import ArticleIcon from '@mui/icons-material/Article';

const FooterLink = ({ to, children, ...props }) => {
  const theme = useTheme();
  const isDarkMode = theme.palette.mode === 'dark';
  
  return (
    <Link
      component={RouterLink}
      to={to}
      sx={{
        color: 'text.secondary',
        textDecoration: 'none',
        fontWeight: 500,
        transition: 'color 0.2s',
        '&:hover': {
          color: 'primary.main',
          textDecoration: 'none',
        },
        display: 'block',
        mb: 1.5,
        fontSize: '0.9rem',
      }}
      {...props}
    >
      {children}
    </Link>
  );
};

const Footer = () => {
  const theme = useTheme();
  const isDarkMode = theme.palette.mode === 'dark';
  const currentYear = new Date().getFullYear();
  
  return (
    <Box 
      component="footer" 
      sx={{
        py: 6,
        mt: 'auto',
        borderTop: 1,
        borderColor: 'divider',
        background: isDarkMode 
          ? 'linear-gradient(to bottom, rgba(10, 15, 30, 0.2) 0%, rgba(10, 15, 30, 0.6) 100%)' 
          : 'linear-gradient(to bottom, rgba(245, 249, 255, 0.7) 0%, rgba(235, 240, 250, 0.9) 100%)',
        backdropFilter: 'blur(8px)',
      }}
    >
      <Container maxWidth="lg">
        <Grid container spacing={4}>
          <Grid item xs={12} sm={6} md={4}>
            <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
              <HealthAndSafetyIcon 
                sx={{ 
                  fontSize: 28, 
                  color: 'primary.main',
                  mr: 1,
                  filter: isDarkMode ? 'drop-shadow(0 0 5px rgba(59, 130, 246, 0.5))' : 'none',
                }} 
              />
              <Typography variant="h6" color="primary" fontWeight={700}>
                AR-MED
              </Typography>
            </Box>
            <Typography variant="body2" color="text.secondary" sx={{ mb: 3, maxWidth: 300 }}>
              Advanced posture analysis tool for healthcare professionals and individuals 
              concerned about their posture and musculoskeletal health.
            </Typography>
            <Stack direction="row" spacing={1}>
              <IconButton 
                aria-label="GitHub" 
                size="small"
                sx={{ 
                  color: 'text.secondary',
                  border: '1px solid',
                  borderColor: 'divider',
                  '&:hover': {
                    color: 'primary.main',
                    borderColor: 'primary.main',
                  }
                }}
              >
                <GitHubIcon fontSize="small" />
              </IconButton>
              <IconButton 
                aria-label="LinkedIn" 
                size="small"
                sx={{ 
                  color: 'text.secondary',
                  border: '1px solid',
                  borderColor: 'divider',
                  '&:hover': {
                    color: 'primary.main',
                    borderColor: 'primary.main',
                  }
                }}
              >
                <LinkedInIcon fontSize="small" />
              </IconButton>
              <IconButton 
                aria-label="Documentation" 
                size="small"
                sx={{ 
                  color: 'text.secondary',
                  border: '1px solid',
                  borderColor: 'divider',
                  '&:hover': {
                    color: 'primary.main',
                    borderColor: 'primary.main',
                  }
                }}
              >
                <ArticleIcon fontSize="small" />
              </IconButton>
            </Stack>
          </Grid>
          
          <Grid item xs={12} sm={6} md={2}>
            <Typography variant="subtitle1" fontWeight={600} gutterBottom>
              Quick Links
            </Typography>
            <FooterLink to="/">Home</FooterLink>
            <FooterLink to="/analysis">Analysis Tool</FooterLink>
            <FooterLink to="/about">About</FooterLink>
          </Grid>
          
          <Grid item xs={12} sm={6} md={3}>
            <Typography variant="subtitle1" fontWeight={600} gutterBottom>
              Resources
            </Typography>
            <FooterLink to="#">Documentation</FooterLink>
            <FooterLink to="#">FAQ</FooterLink>
            <FooterLink to="#">Privacy Policy</FooterLink>
            <FooterLink to="#">Terms of Service</FooterLink>
          </Grid>
          
          <Grid item xs={12} sm={6} md={3}>
            <Typography variant="subtitle1" fontWeight={600} gutterBottom>
              Disclaimer
            </Typography>
            <Typography variant="body2" color="text.secondary" sx={{ fontSize: '0.9rem' }}>
              The posture analysis provided by AR-MED is meant for informational purposes only and 
              should not be considered as medical advice. Please consult with a healthcare professional 
              for proper medical assessment and treatment.
            </Typography>
          </Grid>
        </Grid>
        
        <Divider sx={{ my: 4 }} />
        
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', flexWrap: 'wrap' }}>
          <Typography variant="body2" color="text.secondary" sx={{ fontSize: '0.85rem' }}>
            © {currentYear} AR-MED. All rights reserved.
          </Typography>
          <Typography variant="body2" color="text.secondary" sx={{ fontSize: '0.85rem' }}>
            Made with ❤️ for better posture
          </Typography>
        </Box>
      </Container>
    </Box>
  );
};

export default Footer; 