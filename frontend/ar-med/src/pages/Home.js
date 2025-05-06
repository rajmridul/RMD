import React from 'react';
import { Link as RouterLink } from 'react-router-dom';
import {
  Box,
  Button,
  Card,
  CardContent,
  Container,
  Grid,
  Paper,
  Typography,
  useTheme,
  useMediaQuery,
  Stack,
  Divider,
  Avatar,
} from '@mui/material';
import AnalyticsIcon from '@mui/icons-material/Analytics';
import HealthAndSafetyIcon from '@mui/icons-material/HealthAndSafety';
import CloudUploadIcon from '@mui/icons-material/CloudUpload';
import DevicesIcon from '@mui/icons-material/Devices';
import AssessmentIcon from '@mui/icons-material/Assessment';
import MedicalInformationIcon from '@mui/icons-material/MedicalInformation';
import AutoAwesomeIcon from '@mui/icons-material/AutoAwesome';
import ArrowForwardIcon from '@mui/icons-material/ArrowForward';

// Hero section with improved styling for both light and dark modes
const Hero = () => {
  const theme = useTheme();
  const isMobile = useMediaQuery(theme.breakpoints.down('md'));
  const isDarkMode = theme.palette.mode === 'dark';

  return (
    <Box
      sx={{
        position: 'relative',
        backgroundImage: isDarkMode 
          ? 'linear-gradient(45deg, rgba(15, 23, 42, 0.95) 0%, rgba(15, 23, 42, 0.7) 100%)' 
          : 'linear-gradient(45deg, rgba(240, 249, 255, 0.9) 0%, rgba(224, 242, 254, 0.7) 100%)',
        pt: { xs: 6, md: 12 },
        pb: { xs: 10, md: 16 },
        overflow: 'hidden',
      }}
    >
      {/* Background decorative elements */}
      <Box 
        sx={{ 
          position: 'absolute',
          top: -100,
          right: -100,
          width: 300,
          height: 300,
          borderRadius: '50%',
          background: isDarkMode ? 'radial-gradient(circle, rgba(56, 189, 248, 0.1) 0%, rgba(2, 132, 199, 0.05) 70%, transparent 100%)' : 'radial-gradient(circle, rgba(191, 219, 254, 0.7) 0%, rgba(147, 197, 253, 0.2) 70%, transparent 100%)',
          filter: 'blur(40px)',
          zIndex: 0,
        }} 
      />
      <Box 
        sx={{ 
          position: 'absolute',
          bottom: -50,
          left: -50,
          width: 250,
          height: 250,
          borderRadius: '50%',
          background: isDarkMode ? 'radial-gradient(circle, rgba(79, 70, 229, 0.1) 0%, rgba(67, 56, 202, 0.05) 70%, transparent 100%)' : 'radial-gradient(circle, rgba(224, 231, 255, 0.7) 0%, rgba(199, 210, 254, 0.2) 70%, transparent 100%)',
          filter: 'blur(40px)',
          zIndex: 0,
        }} 
      />
      
      <Container maxWidth="lg" sx={{ position: 'relative', zIndex: 1 }}>
        <Grid container spacing={6} alignItems="center">
          <Grid item xs={12} md={6}>
            <Box className="slide-up" sx={{ animationDelay: '0.1s' }}>
              <Typography 
                variant="h2" 
                component="h1" 
                gutterBottom
                sx={{ 
                  fontWeight: 800,
                  fontSize: { xs: '2.5rem', md: '3.5rem' },
                  lineHeight: 1.2,
                  mb: 2,
                  background: isDarkMode ? 
                    'linear-gradient(to right, #60a5fa, #3b82f6)' : 
                    'linear-gradient(to right, #1e40af, #3b82f6)',
                  WebkitBackgroundClip: 'text',
                  WebkitTextFillColor: 'transparent',
                  letterSpacing: '-0.02em',
                }}
              >
                Advanced Posture Analysis Made Simple
              </Typography>
              <Typography 
                variant="h6" 
                color="text.secondary" 
                sx={{ 
                  mb: 4, 
                  fontWeight: 500,
                  maxWidth: 500,
                  lineHeight: 1.6,
                }}
              >
                AR-MED provides AI-powered posture analysis to help healthcare professionals 
                and individuals identify potential musculoskeletal issues.
              </Typography>
              <Stack direction={{ xs: 'column', sm: 'row' }} spacing={2}>
                <Button
                  variant="contained"
                  color="primary"
                  size="large"
                  component={RouterLink}
                  to="/analysis"
                  sx={{ 
                    px: 4, 
                    py: 1.5,
                    fontWeight: 600,
                    borderRadius: 2,
                    boxShadow: isDarkMode ? '0 0 20px rgba(59, 130, 246, 0.4)' : '0 4px 14px rgba(59, 130, 246, 0.25)',
                  }}
                  endIcon={<ArrowForwardIcon />}
                >
                  Try Analysis Tool
                </Button>
                <Button
                  variant="outlined"
                  color="primary"
                  size="large"
                  component={RouterLink}
                  to="/about"
                  sx={{ 
                    px: 4, 
                    py: 1.5,
                    fontWeight: 600,
                    borderRadius: 2,
                    borderWidth: 2,
                    '&:hover': {
                      borderWidth: 2,
                      backgroundColor: isDarkMode ? 'rgba(59, 130, 246, 0.08)' : 'rgba(59, 130, 246, 0.04)',
                    }
                  }}
                >
                  Learn More
                </Button>
              </Stack>
            </Box>
          </Grid>
          <Grid item xs={12} md={6} sx={{ display: 'flex', justifyContent: 'center' }}>
            <Box
              className="fade-in"
              component="img"
              src="/images/posture-analysis.svg"
              alt="AR-MED Posture Analysis"
              onError={(e) => {
                e.target.onerror = null; // Prevents infinite loop if fallback also fails
                e.target.src = "https://source.unsplash.com/random/800x600/?posture,health,medical"; 
              }}
              sx={{
                maxWidth: { xs: '100%', md: '90%' },
                height: 'auto',
                borderRadius: 4,
                boxShadow: isDarkMode ? 
                  '0 10px 40px -10px rgba(0, 0, 0, 0.5), 0 0 20px rgba(59, 130, 246, 0.3)' : 
                  '0 20px 40px -15px rgba(0, 24, 40, 0.18)',
                transform: 'perspective(1000px) rotateY(-5deg)',
                transition: 'all 0.5s ease',
                '&:hover': {
                  transform: 'perspective(1000px) rotateY(0deg)',
                },
                bgcolor: isDarkMode ? 'rgba(15, 23, 42, 0.2)' : 'rgba(255, 255, 255, 0.8)',
              }}
            />
          </Grid>
        </Grid>
      </Container>
    </Box>
  );
};

// Benefits section with improved card design
const Benefits = () => {
  const theme = useTheme();
  const isDarkMode = theme.palette.mode === 'dark';
  
  const benefits = [
    {
      icon: <AnalyticsIcon />,
      title: 'Advanced Analysis',
      description: 'AI-powered posture assessment that analyzes key metrics to identify potential issues.',
    },
    {
      icon: <HealthAndSafetyIcon />,
      title: 'Health Insights',
      description: 'Get personalized insights about your posture and potential musculoskeletal concerns.',
    },
    {
      icon: <CloudUploadIcon />,
      title: 'Easy to Use',
      description: 'Simply upload a photo or video of yourself to receive an instant posture analysis.',
    },
    {
      icon: <DevicesIcon />,
      title: 'Cross-Platform',
      description: 'Access AR-MED from any device with a web browser for convenience.',
    },
    {
      icon: <AssessmentIcon />,
      title: 'Detailed Reports',
      description: 'Receive comprehensive PDF reports that you can share with healthcare providers.',
    },
    {
      icon: <MedicalInformationIcon />,
      title: 'For Professionals',
      description: 'Designed to assist healthcare professionals with preliminary posture assessments.',
    },
  ];

  return (
    <Box 
      component="section" 
      sx={{ 
        py: 10,
        background: isDarkMode ? 
          'linear-gradient(to bottom, rgba(15, 23, 42, 0.8), rgba(30, 41, 59, 0.8))' : 
          theme.palette.background.default,
      }}
    >
      <Container maxWidth="lg">
        <Box sx={{ textAlign: 'center', mb: 8 }}>
          <Typography 
            component="span" 
            variant="overline" 
            color="primary" 
            fontWeight={600}
            sx={{ 
              display: 'block', 
              mb: 1,
              textTransform: 'uppercase',
              letterSpacing: 1.2,
            }}
          >
            <AutoAwesomeIcon sx={{ fontSize: 16, mr: 0.5, verticalAlign: 'text-top' }} />
            Key Benefits
          </Typography>
          <Typography 
            variant="h3" 
            component="h2" 
            sx={{ 
              mb: 2, 
              fontWeight: 700,
              fontSize: { xs: '2rem', md: '2.5rem' },
              letterSpacing: '-0.02em',
            }}
          >
            Why Choose AR-MED?
          </Typography>
          <Typography 
            variant="h6" 
            color="text.secondary"
            sx={{ 
              maxWidth: 600, 
              mx: 'auto',
              fontWeight: 400,
              lineHeight: 1.6,
            }}
          >
            Our platform offers several advantages for both healthcare professionals 
            and individuals concerned about their posture.
          </Typography>
        </Box>

        <Grid container spacing={4}>
          {benefits.map((benefit, index) => (
            <Grid item xs={12} sm={6} md={4} key={index}>
              <Card 
                className="fade-in" 
                sx={{
                  height: '100%',
                  borderRadius: 4,
                  boxShadow: isDarkMode ? 
                    '0 4px 20px -5px rgba(0, 0, 0, 0.4)' : 
                    '0 10px 30px -15px rgba(0, 0, 0, 0.1)',
                  transition: 'all 0.3s ease',
                  overflow: 'hidden',
                  border: isDarkMode ? '1px solid rgba(255, 255, 255, 0.05)' : 'none',
                  background: isDarkMode ? 
                    'linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%)' : 
                    theme.palette.background.paper,
                  backdropFilter: 'blur(8px)',
                }}
                style={{ animationDelay: `${index * 0.1}s` }}
              >
                <CardContent sx={{ p: 4 }}>
                  <Avatar
                    sx={{ 
                      mb: 2,
                      width: 56, 
                      height: 56,
                      bgcolor: 'primary.main',
                      color: 'white',
                      boxShadow: isDarkMode ? '0 0 15px rgba(59, 130, 246, 0.4)' : 'none',
                    }}
                  >
                    {benefit.icon}
                  </Avatar>
                  <Typography 
                    variant="h5" 
                    component="h3" 
                    gutterBottom
                    sx={{ 
                      fontWeight: 600,
                      mb: 1.5,
                    }}
                  >
                    {benefit.title}
                  </Typography>
                  <Typography variant="body1" color="text.secondary">
                    {benefit.description}
                  </Typography>
                </CardContent>
              </Card>
            </Grid>
          ))}
        </Grid>
      </Container>
    </Box>
  );
};

// How it works section with modern styling
const HowItWorks = () => {
  const theme = useTheme();
  const isDarkMode = theme.palette.mode === 'dark';
  
  const steps = [
    {
      number: '1',
      title: 'Upload Media',
      description: 'Upload a photo or video of yourself in the required poses.',
    },
    {
      number: '2',
      title: 'AI Analysis',
      description: 'Our AI system analyzes your posture using advanced computer vision.',
    },
    {
      number: '3',
      title: 'Review Results',
      description: 'Get instant results with visual guides and detailed explanation.',
    },
    {
      number: '4',
      title: 'Download Report',
      description: 'Download the analysis report as a PDF to share with healthcare providers.',
    },
  ];

  return (
    <Box 
      component="section" 
      sx={{ 
        py: 10,
        background: isDarkMode ? 
          theme.palette.background.default : 
          'linear-gradient(to bottom, #f0f9ff, #e0f2fe)',
        position: 'relative',
        overflow: 'hidden',
      }}
    >
      {/* Decorative background elements */}
      <Box 
        sx={{
          position: 'absolute',
          top: '20%',
          right: '5%',
          width: 300,
          height: 300,
          borderRadius: '50%',
          background: isDarkMode ? 
            'radial-gradient(circle, rgba(59, 130, 246, 0.05) 0%, rgba(30, 64, 175, 0.03) 70%, transparent 100%)' : 
            'radial-gradient(circle, rgba(191, 219, 254, 0.7) 0%, rgba(147, 197, 253, 0.2) 70%, transparent 100%)',
          filter: 'blur(50px)',
          zIndex: 0,
        }}
      />
      
      <Container maxWidth="lg" sx={{ position: 'relative', zIndex: 1 }}>
        <Box sx={{ textAlign: 'center', mb: 8 }}>
          <Typography 
            component="span" 
            variant="overline" 
            color="primary" 
            fontWeight={600}
            sx={{ 
              display: 'block', 
              mb: 1,
              textTransform: 'uppercase',
              letterSpacing: 1.2,
            }}
          >
            <AutoAwesomeIcon sx={{ fontSize: 16, mr: 0.5, verticalAlign: 'text-top' }} />
            Process
          </Typography>
          <Typography 
            variant="h3" 
            component="h2" 
            sx={{ 
              mb: 2, 
              fontWeight: 700,
              fontSize: { xs: '2rem', md: '2.5rem' },
              letterSpacing: '-0.02em',
            }}
          >
            How It Works
          </Typography>
          <Typography 
            variant="h6" 
            color="text.secondary"
            sx={{ 
              maxWidth: 600, 
              mx: 'auto',
              fontWeight: 400,
              lineHeight: 1.6,
            }}
          >
            Our posture analysis process is simple, fast, and provides valuable insights 
            in just a few steps.
          </Typography>
        </Box>

        <Box
          sx={{
            display: 'flex',
            flexDirection: 'column',
            position: 'relative',
            mt: 2,
          }}
        >
          {/* Central connecting line */}
          <Box
            sx={{
              position: 'absolute',
              left: '50%',
              top: 40,
              bottom: 0,
              width: 2,
              bgcolor: isDarkMode ? 'rgba(59, 130, 246, 0.3)' : 'rgba(59, 130, 246, 0.2)',
              transform: 'translateX(-50%)',
              display: { xs: 'none', md: 'block' },
            }}
          />

          {steps.map((step, index) => (
            <Box
              key={index}
              className="fade-in"
              sx={{
                display: 'flex',
                flexDirection: { xs: 'column', md: index % 2 === 0 ? 'row' : 'row-reverse' },
                mb: 8,
                alignItems: 'center',
                justifyContent: 'center',
              }}
              style={{ animationDelay: `${index * 0.15}s` }}
            >
              <Box
                sx={{
                  flex: 1,
                  display: 'flex',
                  justifyContent: { xs: 'center', md: index % 2 === 0 ? 'flex-end' : 'flex-start' },
                  pr: { md: index % 2 === 0 ? 6 : 0 },
                  pl: { md: index % 2 === 0 ? 0 : 6 },
                  position: 'relative',
                  zIndex: 1,
                }}
              >
                <Paper
                  elevation={0}
                  sx={{
                    p: 4,
                    borderRadius: 4,
                    width: { xs: '100%', md: '80%' },
                    maxWidth: 400,
                    boxShadow: isDarkMode ? 
                      '0 8px 25px -5px rgba(0, 0, 0, 0.4)' : 
                      '0 15px 30px -10px rgba(0, 0, 0, 0.1)',
                    border: isDarkMode ? '1px solid rgba(255, 255, 255, 0.05)' : 'none',
                    background: isDarkMode ? 
                      'linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%)' : 
                      theme.palette.background.paper,
                    backdropFilter: 'blur(8px)',
                  }}
                >
                  <Typography
                    variant="h5"
                    component="h3"
                    gutterBottom
                    sx={{ fontWeight: 700, display: 'flex', alignItems: 'center' }}
                  >
                    <Avatar
                      sx={{
                        bgcolor: 'primary.main',
                        color: 'white',
                        width: 36,
                        height: 36,
                        mr: 1.5,
                        fontWeight: 700,
                        boxShadow: isDarkMode ? '0 0 10px rgba(59, 130, 246, 0.5)' : 'none',
                      }}
                    >
                      {step.number}
                    </Avatar>
                    {step.title}
                  </Typography>
                  <Typography variant="body1" color="text.secondary" sx={{ mt: 1 }}>
                    {step.description}
                  </Typography>
                </Paper>
              </Box>

              {/* Circle for timeline on medium and larger screens */}
              <Box
                sx={{
                  width: 20,
                  height: 20,
                  borderRadius: '50%',
                  bgcolor: 'primary.main',
                  boxShadow: isDarkMode ? '0 0 15px rgba(59, 130, 246, 0.5)' : '0 0 10px rgba(59, 130, 246, 0.3)',
                  position: 'relative',
                  zIndex: 2,
                  display: { xs: 'none', md: 'block' },
                }}
              />

              <Box sx={{ flex: 1 }} /> {/* Spacer for layout */}
            </Box>
          ))}
        </Box>

        <Box sx={{ textAlign: 'center', mt: 4 }}>
          <Button
            variant="contained"
            color="primary"
            size="large"
            component={RouterLink}
            to="/analysis"
            sx={{ 
              px: 4, 
              py: 1.5,
              fontWeight: 600,
              borderRadius: 2,
              boxShadow: isDarkMode ? '0 0 20px rgba(59, 130, 246, 0.4)' : '0 4px 14px rgba(59, 130, 246, 0.25)',
            }}
            endIcon={<ArrowForwardIcon />}
          >
            Try Analysis Now
          </Button>
        </Box>
      </Container>
    </Box>
  );
};

// Main Home component
const Home = () => {
  return (
    <Box sx={{ minHeight: '100vh' }}>
      <Hero />
      <Benefits />
      <HowItWorks />
    </Box>
  );
};

export default Home; 