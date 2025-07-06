import React, { useState, useEffect, useRef } from 'react';
import { Typography, Button, Stack, Snackbar, Alert, Paper, CircularProgress, Box, TextField, IconButton, List, ListItem, ListItemText, AppBar, Toolbar, Avatar, Menu, MenuItem } from '@mui/material';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import AssessmentIcon from '@mui/icons-material/Assessment';

import LogoutIcon from '@mui/icons-material/Logout';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import ErrorIcon from '@mui/icons-material/Error';
import axios from 'axios';

import { AuthProvider, useAuth } from './contexts/AuthContext';
import LoginForm from './components/LoginForm';
import RegisterForm from './components/RegisterForm';
import UserReports from './components/UserReports';

function capitalizeWords(str) {
  return str.replace(/\w\S*/g, w => w.charAt(0).toUpperCase() + w.slice(1).toLowerCase());
}

function AppContent() {
  const [loading, setLoading] = useState('');
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'info' });

  const [sources, setSources] = useState([]);
  const [selectedSources, setSelectedSources] = useState([]);
  const [keyword, setKeyword] = useState('');
  const [scrapedJobs, setScrapedJobs] = useState([]);
  const [scraping, setScraping] = useState(false);
  const [showAuth, setShowAuth] = useState('login'); // 'login', 'register', or null
  const [anchorEl, setAnchorEl] = useState(null);
  const [emailVerification, setEmailVerification] = useState(null); // 'verifying', 'success', 'error', or null

  const { user, isAuthenticated, logout, loading: authLoading } = useAuth();
  const userReportsRef = useRef();

  // Check for email verification on mount
  useEffect(() => {
    // Check for hash fragment (Supabase format)
    const hash = window.location.hash.substring(1);
    const hashParams = new URLSearchParams(hash);
    const accessToken = hashParams.get('access_token');
    const type = hashParams.get('type');

    // Also check for query parameters (fallback)
    const urlParams = new URLSearchParams(window.location.search);
    const token = urlParams.get('token');
    const queryType = urlParams.get('type');

    if ((accessToken && type === 'signup') || (token && queryType === 'signup')) {
      setEmailVerification('verifying');
      // Handle email verification
      setTimeout(() => {
        setEmailVerification('success');
        // Clear URL parameters and hash
        window.history.replaceState({}, document.title, window.location.pathname);
      }, 2000);
    }
  }, []);



  // Fetch sources on mount
  useEffect(() => {
    if (isAuthenticated) {
      axios.get('/api/sources').then(res => setSources(res.data)).catch(() => setSources([]));
    }
  }, [isAuthenticated]);



  const handleSaveReport = async () => {
    if (scrapedJobs.length === 0) {
      setSnackbar({ open: true, message: 'No jobs to save. Please scrape some jobs first.', severity: 'warning' });
      return;
    }
    
    setLoading('save');
    setSnackbar({ open: true, message: 'Saving report...', severity: 'info' });
    try {
      const reportData = {
        title: `Job Search: ${keyword}`,
        description: `Jobs scraped for keyword "${keyword}" from ${selectedSources.length} sources`,
        jobs_data: JSON.stringify(scrapedJobs),
        keyword: keyword,
        sources_used: JSON.stringify(selectedSources),
        job_count: scrapedJobs.length
      };
      
      await axios.post('/api/supabase-auth/reports', reportData);
      setSnackbar({ open: true, message: 'Report saved successfully!', severity: 'success' });
      // Refresh the reports list
      if (userReportsRef.current && userReportsRef.current.loadReports) {
        userReportsRef.current.loadReports();
      }
    } catch (err) {
      setSnackbar({ open: true, message: `Error saving report: ${err.response?.data?.detail || err.message}`, severity: 'error' });
    } finally {
      setLoading('');
    }
  };



  const handleSourceToggle = (id) => {
    setSelectedSources(prev => prev.includes(id) ? prev.filter(s => s !== id) : [...prev, id]);
  };

  const handleScrapeJobs = async () => {
    if (!keyword || selectedSources.length === 0) {
      setSnackbar({ open: true, message: 'Please enter a keyword and select at least one source.', severity: 'warning' });
      return;
    }
    setScraping(true);
    setScrapedJobs([]);
    try {
      const res = await axios.post('/api/scrape/jobs', { keyword, sources: selectedSources });
      setScrapedJobs(res.data.jobs || []);
      setSnackbar({ open: true, message: `Scraped ${res.data.jobs?.length || 0} jobs.`, severity: 'success' });
    } catch (err) {
      setSnackbar({ open: true, message: `Scrape failed: ${err.response?.data?.error || err.message}`, severity: 'error' });
    } finally {
      setScraping(false);
    }
  };

  const handleLogout = () => {
    logout();
    setAnchorEl(null);
    setSnackbar({ open: true, message: 'Logged out successfully', severity: 'info' });
  };

  const handleUserMenuOpen = (event) => {
    setAnchorEl(event.currentTarget);
  };

  const handleUserMenuClose = () => {
    setAnchorEl(null);
  };

  // Show email verification if needed
  if (emailVerification) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh', bgcolor: '#181c24' }}>
        <Paper sx={{ p: 4, textAlign: 'center', maxWidth: 400, bgcolor: '#232936', color: '#fff' }}>
          <Typography variant="h5" gutterBottom sx={{ color: '#fff' }}>
            Email Verification
          </Typography>
          {emailVerification === 'verifying' && (
            <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 2 }}>
              <CircularProgress />
              <Typography sx={{ color: '#ccc' }}>
                Verifying your email...
              </Typography>
            </Box>
          )}
          {emailVerification === 'success' && (
            <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 2 }}>
              <CheckCircleIcon sx={{ fontSize: 60, color: 'success.main' }} />
              <Typography sx={{ color: '#ccc' }}>
                Email verified successfully! You can now log in.
              </Typography>
              <Button 
                variant="contained" 
                onClick={() => setEmailVerification(null)}
                sx={{ mt: 2 }}
              >
                Continue to Login
              </Button>
            </Box>
          )}
          {emailVerification === 'error' && (
            <Box sx={{ display: 'flex', flexDirection: 'column', alignItems: 'center', gap: 2 }}>
              <ErrorIcon sx={{ fontSize: 60, color: 'error.main' }} />
              <Typography sx={{ color: '#ccc' }}>
                Email verification failed. Please try again.
              </Typography>
              <Button 
                variant="contained" 
                onClick={() => setEmailVerification(null)}
                sx={{ mt: 2 }}
              >
                Continue to Login
              </Button>
            </Box>
          )}
        </Paper>
      </Box>
    );
  }

  // Show authentication forms if not authenticated
  if (!isAuthenticated) {
    if (authLoading) {
      return (
        <Box sx={{ display: 'flex', justifyContent: 'center', alignItems: 'center', minHeight: '100vh', bgcolor: '#181c24' }}>
          <CircularProgress />
        </Box>
      );
    }

    if (showAuth === 'login') {
      return <LoginForm onSwitchToRegister={() => setShowAuth('register')} />;
    } else if (showAuth === 'register') {
      return <RegisterForm onSwitchToLogin={() => setShowAuth('login')} />;
    }
  }

  // Actions for job scraping and saving
  const actions = [
    { key: 'scrape', label: 'Scrape Jobs', icon: <PlayArrowIcon fontSize="large" />, onClick: handleScrapeJobs },
    { key: 'save', label: 'Save Report', icon: <AssessmentIcon fontSize="large" />, onClick: handleSaveReport },
  ];

  return (
    <Box sx={{ minHeight: '100vh', width: '98vw', bgcolor: '#181c24', display: 'flex', flexDirection: 'column' }}>
      {/* App Bar */}
      <AppBar position="static" sx={{ bgcolor: '#232936' }}>
        <Toolbar>
          <Typography variant="h6" component="div" sx={{ flexGrow: 1, color: '#fff' }}>
            TalentTrek
          </Typography>
          <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
            <Typography variant="body2" color="#ccc">
              Welcome, {user?.username}!
            </Typography>
            <IconButton
              onClick={handleUserMenuOpen}
              sx={{ color: '#fff' }}
            >
              <Avatar sx={{ width: 32, height: 32, bgcolor: '#1976d2' }}>
                {user?.username?.charAt(0).toUpperCase()}
              </Avatar>
            </IconButton>
            <Menu
              anchorEl={anchorEl}
              open={Boolean(anchorEl)}
              onClose={handleUserMenuClose}
              sx={{
                '& .MuiPaper-root': {
                  bgcolor: '#232936',
                  color: '#fff',
                }
              }}
            >
              <MenuItem onClick={handleLogout}>
                <LogoutIcon sx={{ mr: 1 }} />
                Logout
              </MenuItem>
            </Menu>
          </Box>
        </Toolbar>
      </AppBar>

      {/* Main Content */}
      <Box sx={{ display: 'flex', flex: 1 }}>
        {/* Sidebar */}
        <Box sx={{ width: 450, minWidth: 300, maxWidth: 500, height: '90vh', bgcolor: '#232936', color: '#fff', display: 'flex', flexDirection: 'column', borderRadius: 3, m: 3, boxShadow: 4, position: 'sticky', top: 24 }}>
          {/* Centered content */}
          <Box sx={{ flex: 1, width: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center' }}>
            {/* Keyword and Source Selection */}
            <Box sx={{ mb: 4, width: '100%', display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
              <Typography variant="h6" color="#fff" gutterBottom>Scrape Jobs by Keyword & Source</Typography>
              <TextField
                label="Keyword"
                variant="outlined"
                size="small"
                value={keyword}
                onChange={e => setKeyword(e.target.value)}
                sx={{ bgcolor: '#fff', borderRadius: 1, width: { xs: '97%', sm: '90%', md: 375 }, mb: 2 }}
              />
              <Stack direction="column" spacing={1} alignItems="center" sx={{ width: { xs: '97%', sm: '90%', md: 375 } }}>
                {sources.map(src => (
                  <Button
                    key={src.id}
                    variant={selectedSources.includes(src.id) ? 'contained' : 'outlined'}
                    color={selectedSources.includes(src.id) ? 'secondary' : 'primary'}
                    onClick={() => handleSourceToggle(src.id)}
                    sx={{ fontWeight: 600, justifyContent: 'center' }}
                    fullWidth
                  >
                    {src.name}
                  </Button>
                ))}
              </Stack>
            </Box>
            {/* Action Buttons */}
            <Stack direction="column" spacing={2} alignItems="center" justifyContent="center" sx={{ width: '100%' }}>
              {actions.map(({ key, label, icon, onClick }) => (
                <Button
                  key={key}
                  variant="contained"
                  startIcon={icon}
                  onClick={onClick}
                  disabled={!!loading || (key === 'scrape' && (scraping || !keyword || selectedSources.length === 0)) || (key === 'save' && scrapedJobs.length === 0)}
                  color={key === loading ? 'secondary' : 'primary'}
                  size="large"
                  sx={{ width: { xs: '97%', sm: '90%', md: 375 }, justifyContent: 'center', fontWeight: 600, fontSize: 18, alignSelf: 'center' }}
                >
                  {key === loading || (key === 'scrape' && scraping) ? <CircularProgress size={24} color="inherit" /> : label}
                </Button>
              ))}
            </Stack>
          </Box>
        </Box>

        {/* Main Content Area */}
        <Box sx={{ flex: 1, p: 4, display: 'flex', flexDirection: 'column', minHeight: '100vh', overflowY: 'auto', overflowX: 'hidden', width: '97%' }}>
          {/* User Reports Section */}
          <Paper elevation={2} sx={{ p: 3, mb: 3, bgcolor: '#232936', color: '#fff', width: '97%', maxWidth: '97%' }}>
            <UserReports 
              ref={userReportsRef}
              onSaveSuccess={() => setSnackbar({ open: true, message: 'Report saved successfully!', severity: 'success' })}
            />
          </Paper>

          {/* Scraped Jobs Display */}
          {scrapedJobs.length > 0 && (
            <Paper elevation={2} sx={{ p: 3, bgcolor: '#232936', color: '#fff', width: '97%', maxWidth: '97%' }}>
              <Typography variant="h5" gutterBottom color="#fff">
                Scraped Jobs ({scrapedJobs.length})
              </Typography>
              <List>
                {scrapedJobs.map((job, index) => (
                  <ListItem key={index} sx={{ bgcolor: '#2d3341', mb: 1, borderRadius: 1 }}>
                    <ListItemText
                      primary={
                        <Typography variant="h6" color="#fff">
                          {job.title || 'No title'}
                        </Typography>
                      }
                      secondary={
                        <Box>
                          <Typography variant="body2" color="#ccc">
                            <strong>Company:</strong> {job.company || 'N/A'}
                          </Typography>
                          <Typography variant="body2" color="#ccc">
                            <strong>Location:</strong> {job.location || 'N/A'}
                          </Typography>
                          <Typography variant="body2" color="#ccc">
                            <strong>Source:</strong> {job.source || 'N/A'}
                          </Typography>
                          {job.salary && (
                            <Typography variant="body2" color="#ccc">
                              <strong>Salary:</strong> {job.salary}
                            </Typography>
                          )}
                          {job.date_posted && (
                            <Typography variant="body2" color="#ccc">
                              <strong>Posted:</strong> {job.date_posted}
                            </Typography>
                          )}
                          {job.url && (
                            <Typography variant="body2" color="#ccc">
                              <strong>URL:</strong> <a href={job.url} target="_blank" rel="noopener noreferrer" style={{ color: '#1976d2' }}>{job.url}</a>
                            </Typography>
                          )}
                        </Box>
                      }
                    />
                  </ListItem>
                ))}
              </List>
            </Paper>
          )}
        </Box>
      </Box>

      {/* Snackbar for notifications */}
      <Snackbar
        open={snackbar.open}
        autoHideDuration={6000}
        onClose={() => setSnackbar({ ...snackbar, open: false })}
      >
        <Alert
          onClose={() => setSnackbar({ ...snackbar, open: false })}
          severity={snackbar.severity}
          sx={{ width: '100%' }}
        >
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Box>
  );
}

export default function App() {
  return (
    <AuthProvider>
      <AppContent />
    </AuthProvider>
  );
}
