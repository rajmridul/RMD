import React from 'react';
import { Link as RouterLink } from 'react-router-dom';
import {
  Box,
  Button,
  Card,
  CardContent,
  Container,
  Divider,
  Grid,
  List,
  ListItem,
  ListItemIcon,
  ListItemText,
  Paper,
  Typography,
  Avatar,
  useTheme,
  alpha,
  Stack,
} from '@mui/material';
import CheckCircleOutlineIcon from '@mui/icons-material/CheckCircleOutline';
import ComputerIcon from '@mui/icons-material/Computer';
import HealthAndSafetyIcon from '@mui/icons-material/HealthAndSafety';
import BiotechIcon from '@mui/icons-material/Biotech';
import SchoolIcon from '@mui/icons-material/School';
import WarningIcon from '@mui/icons-material/Warning';
import AutoAwesomeIcon from '@mui/icons-material/AutoAwesome';
import ArrowForwardIcon from '@mui/icons-material/ArrowForward';
import WorkIcon from '@mui/icons-material/Work';

const About = () => {
  const theme = useTheme();
  const isDarkMode = theme.palette.mode === 'dark';

  return (
    <Box
      sx={{
        minHeight: '100vh',
        pt: 6,
        pb: 12,
        position: 'relative',
        overflow: 'hidden',
        background: isDarkMode ? 
          'linear-gradient(to bottom, rgba(15, 23, 42, 0.95), rgba(15, 23, 42, 0.8))' : 
          'linear-gradient(to bottom, #f8fafc, #f1f5f9)',
      }}
    >
      {/* Background decorative elements */}
      <Box 
        sx={{ 
          position: 'absolute',
          top: '10%',
          right: '5%',
          width: 400,
          height: 400,
          borderRadius: '50%',
          background: isDarkMode ? 
            'radial-gradient(circle, rgba(56, 189, 248, 0.05) 0%, rgba(2, 132, 199, 0.02) 70%, transparent 100%)' : 
            'radial-gradient(circle, rgba(186, 230, 253, 0.6) 0%, rgba(125, 211, 252, 0.15) 70%, transparent 100%)',
          filter: 'blur(60px)',
          zIndex: 0,
        }} 
      />
      <Box 
        sx={{ 
          position: 'absolute',
          bottom: '10%',
          left: '5%',
          width: 350,
          height: 350,
          borderRadius: '50%',
          background: isDarkMode ? 
            'radial-gradient(circle, rgba(79, 70, 229, 0.05) 0%, rgba(67, 56, 202, 0.02) 70%, transparent 100%)' : 
            'radial-gradient(circle, rgba(224, 231, 255, 0.6) 0%, rgba(199, 210, 254, 0.15) 70%, transparent 100%)',
          filter: 'blur(60px)',
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
            Our Story
          </Typography>
          <Typography
            variant="h2"
            component="h1"
            gutterBottom
            sx={{ 
              fontWeight: 800,
              fontSize: { xs: '2.5rem', md: '3.5rem' },
              mb: 3,
              background: isDarkMode ? 
                'linear-gradient(to right, #60a5fa, #3b82f6)' : 
                'linear-gradient(to right, #1e40af, #3b82f6)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent',
              letterSpacing: '-0.02em',
            }}
          >
            About AR-MED
          </Typography>
          <Typography
            variant="h5"
            color="text.secondary"
            gutterBottom
            sx={{ 
              mb: 6, 
              maxWidth: 800, 
              mx: 'auto',
              fontWeight: 400,
              lineHeight: 1.6,
            }}
          >
            Advancing preventive healthcare through AI-powered posture analysis
          </Typography>

          <Grid container spacing={6} alignItems="stretch">
            <Grid item xs={12} md={6}>
              <Box 
                className="slide-up"
                sx={{ 
                  height: '100%',
                  animationDelay: '0.1s',
                }}
              >
                <Typography 
                  variant="h3" 
                  gutterBottom 
                  color="primary"
                  sx={{ 
                    fontWeight: 700,
                    mb: 3,
                    fontSize: { xs: '1.75rem', md: '2.25rem' },
                  }}
                >
                  Our Mission
                </Typography>
                <Typography 
                  variant="body1" 
                  paragraph
                  sx={{ 
                    fontSize: '1.05rem',
                    lineHeight: 1.7,
                    mb: 3,
                  }}
                >
                  AR-MED was developed with a clear mission: to make professional-grade
                  posture analysis accessible to everyone. By leveraging cutting-edge
                  artificial intelligence and computer vision technology, we've created
                  a tool that can detect potential alignment issues early, before they
                  develop into more serious conditions.
                </Typography>
                <Typography 
                  variant="body1" 
                  paragraph
                  sx={{ 
                    fontSize: '1.05rem',
                    lineHeight: 1.7,
                    mb: 3,
                  }}
                >
                  Poor posture and body alignment are often overlooked but can lead to
                  chronic pain, reduced mobility, and decreased quality of life. Our
                  goal is to help users identify these issues early and provide
                  guidance for improvement.
                </Typography>
                <Typography 
                  variant="body1"
                  sx={{ 
                    fontSize: '1.05rem',
                    lineHeight: 1.7,
                  }}
                >
                  While AR-MED is not a substitute for professional medical care, it
                  serves as a valuable preliminary assessment tool that can help users
                  decide when to seek professional advice and track their progress over
                  time.
                </Typography>
              </Box>
            </Grid>

            <Grid item xs={12} md={6}>
              <Paper
                elevation={0}
                className="fade-in"
                sx={{
                  p: 4,
                  height: '100%',
                  borderRadius: 4,
                  border: 1,
                  borderColor: isDarkMode ? alpha(theme.palette.primary.main, 0.1) : 'divider',
                  background: isDarkMode ? 
                    'linear-gradient(135deg, rgba(30, 41, 59, 0.8) 0%, rgba(15, 23, 42, 0.9) 100%)' : 
                    theme.palette.background.paper,
                  backdropFilter: 'blur(8px)',
                  boxShadow: isDarkMode ? 
                    '0 8px 32px -5px rgba(0, 0, 0, 0.3)' : 
                    '0 20px 50px -15px rgba(0, 0, 0, 0.1)',
                }}
              >
                <Typography 
                  variant="h4" 
                  gutterBottom 
                  color="primary"
                  sx={{ 
                    fontWeight: 700,
                    mb: 3,
                    fontSize: { xs: '1.5rem', md: '1.75rem' },
                    display: 'flex',
                    alignItems: 'center',
                  }}
                >
                  <WorkIcon sx={{ mr: 1.5, fontSize: 28 }} />
                  The Technology Behind AR-MED
                </Typography>
                <List>
                  {[
                    {
                      icon: <ComputerIcon />,
                      title: "Computer Vision",
                      description: "Uses advanced pose estimation models to accurately identify 33 body landmarks from simple 2D images."
                    },
                    {
                      icon: <BiotechIcon />,
                      title: "Biomechanical Analysis",
                      description: "Applies clinical biomechanical principles to analyze posture and alignment issues."
                    },
                    {
                      icon: <HealthAndSafetyIcon />,
                      title: "Comprehensive Assessment",
                      description: "Evaluates knee alignment, shoulder balance, hip alignment, and overall posture."
                    },
                    {
                      icon: <SchoolIcon />,
                      title: "Evidence-Based Recommendations",
                      description: "Provides personalized suggestions based on established clinical guidelines."
                    }
                  ].map((item, index) => (
                    <ListItem 
                      key={index} 
                      sx={{ 
                        px: 0, 
                        py: 1.5,
                        transition: 'all 0.2s ease',
                        '&:hover': {
                          transform: 'translateX(4px)',
                        }
                      }}
                    >
                      <ListItemIcon>
                        <Avatar 
                          sx={{ 
                            bgcolor: alpha(theme.palette.primary.main, isDarkMode ? 0.2 : 0.1),
                            color: 'primary.main',
                            width: 44,
                            height: 44,
                          }}
                        >
                          {item.icon}
                        </Avatar>
                      </ListItemIcon>
                      <ListItemText
                        primary={item.title}
                        secondary={item.description}
                        primaryTypographyProps={{ 
                          fontWeight: 600,
                          mb: 0.5, 
                        }}
                        secondaryTypographyProps={{ 
                          color: 'text.secondary',
                          lineHeight: 1.6,
                        }}
                      />
                    </ListItem>
                  ))}
                </List>
              </Paper>
            </Grid>

            <Grid item xs={12}>
              <Divider sx={{ my: 6 }} />
            </Grid>

            <Grid item xs={12} md={6}>
              <Box className="fade-in" sx={{ animationDelay: '0.2s' }}>
                <Typography 
                  variant="h3" 
                  gutterBottom 
                  color="primary"
                  sx={{ 
                    fontWeight: 700,
                    mb: 3,
                    fontSize: { xs: '1.75rem', md: '2.25rem' },
                  }}
                >
                  Benefits and Advantages
                </Typography>
                <List>
                  {[
                    {
                      text: 'Early Detection of Alignment Issues',
                      description:
                        'Identify potential posture and alignment problems before they progress to more serious conditions or injuries.',
                    },
                    {
                      text: 'Comprehensive Analysis',
                      description:
                        'Detailed assessment of multiple body regions including knees, shoulders, hips, and overall posture.',
                    },
                    {
                      text: 'Accessibility',
                      description:
                        'Professional-level posture analysis accessible anytime, anywhere, without expensive equipment or appointments.',
                    },
                    {
                      text: 'Educational Value',
                      description:
                        'Learn about your body mechanics and how alignment affects your health and physical performance.',
                    },
                    {
                      text: 'Progress Tracking',
                      description:
                        'Monitor improvements in your posture over time with consistent, objective measurements.',
                    },
                    {
                      text: 'Preventative Health',
                      description:
                        'Take proactive steps to prevent potential musculoskeletal issues before they develop.',
                    },
                  ].map((item, index) => (
                    <ListItem 
                      key={index} 
                      sx={{ 
                        px: 0, 
                        py: 1.5,
                        transition: 'all 0.2s ease',
                        '&:hover': {
                          transform: 'translateX(4px)',
                        }
                      }}
                    >
                      <ListItemIcon>
                        <Avatar 
                          sx={{ 
                            bgcolor: isDarkMode ? alpha(theme.palette.primary.main, 0.2) : alpha(theme.palette.success.light, 0.15),
                            color: isDarkMode ? 'primary.main' : 'success.main',
                            width: 44,
                            height: 44,
                          }}
                        >
                          <CheckCircleOutlineIcon />
                        </Avatar>
                      </ListItemIcon>
                      <ListItemText
                        primary={item.text}
                        secondary={item.description}
                        primaryTypographyProps={{ 
                          fontWeight: 600,
                          mb: 0.5,
                        }}
                        secondaryTypographyProps={{ 
                          color: 'text.secondary',
                          lineHeight: 1.6,
                        }}
                      />
                    </ListItem>
                  ))}
                </List>
              </Box>
            </Grid>

            <Grid item xs={12} md={6}>
              <Card 
                className="fade-in"
                sx={{ 
                  height: '100%', 
                  borderRadius: 4,
                  background: isDarkMode ? 
                    `linear-gradient(135deg, ${alpha(theme.palette.warning.dark, 0.12)} 0%, ${alpha(theme.palette.warning.dark, 0.05)} 100%)` : 
                    `linear-gradient(135deg, ${alpha(theme.palette.warning.light, 0.15)} 0%, ${alpha(theme.palette.warning.light, 0.05)} 100%)`,
                  backdropFilter: 'blur(8px)',
                  border: 1,
                  borderColor: isDarkMode ? alpha(theme.palette.warning.main, 0.2) : alpha(theme.palette.warning.light, 0.3),
                  boxShadow: isDarkMode ? 
                    '0 8px 32px -5px rgba(0, 0, 0, 0.3)' : 
                    '0 20px 50px -15px rgba(0, 0, 0, 0.1)',
                  animationDelay: '0.3s',
                }}
              >
                <CardContent sx={{ p: 4 }}>
                  <Box sx={{ 
                    display: 'flex', 
                    alignItems: 'center', 
                    mb: 3,
                    pb: 2,
                    borderBottom: 1,
                    borderColor: isDarkMode ? alpha(theme.palette.warning.main, 0.2) : alpha(theme.palette.warning.light, 0.3),
                  }}>
                    <Avatar 
                      sx={{ 
                        bgcolor: isDarkMode ? alpha(theme.palette.warning.main, 0.2) : alpha(theme.palette.warning.light, 0.2),
                        color: 'warning.main',
                        width: 48,
                        height: 48,
                        mr: 2,
                      }}
                    >
                      <WarningIcon />
                    </Avatar>
                    <Typography 
                      variant="h4" 
                      color={isDarkMode ? 'warning.light' : 'warning.dark'} 
                      sx={{ 
                        fontWeight: 700,
                        fontSize: { xs: '1.5rem', md: '1.75rem' },
                      }}
                    >
                      Important Disclaimer
                    </Typography>
                  </Box>
                  <Typography 
                    variant="body1" 
                    paragraph
                    sx={{ 
                      mb: 3,
                      lineHeight: 1.7,
                    }}
                  >
                    <strong>AR-MED is a preliminary assessment tool only.</strong> The
                    posture analysis provided is intended for informational and
                    educational purposes only and is not meant to be a substitute for
                    professional medical advice, diagnosis, or treatment.
                  </Typography>
                  <Typography 
                    variant="body1" 
                    paragraph
                    sx={{ 
                      mb: 2,
                      fontWeight: 600,
                    }}
                  >
                    Limitations of our analysis include:
                  </Typography>
                  <Box sx={{ 
                    mb: 3,
                    p: 2,
                    borderRadius: 2,
                    bgcolor: isDarkMode ? alpha(theme.palette.background.paper, 0.1) : alpha(theme.palette.background.paper, 0.5),
                  }}>
                    <List disablePadding dense>
                      {[
                        "2D image analysis cannot capture all aspects of 3D posture",
                        "Analysis quality depends on image clarity and positioning",
                        "Cannot diagnose medical conditions or provide treatment",
                        "Not a replacement for in-person clinical assessment"
                      ].map((text, index) => (
                        <ListItem key={index} sx={{ py: 0.5 }}>
                          <ListItemIcon sx={{ minWidth: 28 }}>
                            <Box 
                              component="span" 
                              sx={{ 
                                width: 6, 
                                height: 6, 
                                borderRadius: '50%', 
                                bgcolor: 'warning.main',
                                display: 'inline-block',
                              }} 
                            />
                          </ListItemIcon>
                          <ListItemText 
                            primary={text} 
                            primaryTypographyProps={{ fontSize: '0.95rem' }}
                          />
                        </ListItem>
                      ))}
                    </List>
                  </Box>
                  <Typography 
                    variant="body1" 
                    paragraph 
                    sx={{ 
                      mt: 2,
                      lineHeight: 1.7,
                    }}
                  >
                    <strong>Always consult with qualified healthcare providers</strong> such
                    as physicians, physical therapists, or chiropractors for proper
                    diagnosis and treatment of any posture-related issues or medical
                    conditions.
                  </Typography>
                  <Box sx={{ mt: 4 }}>
                    <Button
                      variant="contained"
                      component={RouterLink}
                      to="/analysis"
                      size="large"
                      endIcon={<ArrowForwardIcon />}
                      fullWidth
                      sx={{ 
                        py: 1.5, 
                        borderRadius: 2, 
                        fontWeight: 600,
                        boxShadow: isDarkMode ? '0 0 20px rgba(59, 130, 246, 0.4)' : '0 4px 14px rgba(59, 130, 246, 0.25)',
                      }}
                    >
                      Try the Analysis Tool
                    </Button>
                  </Box>
                </CardContent>
              </Card>
            </Grid>
          </Grid>
        </Box>
      </Container>
    </Box>
  );
};

export default About; 