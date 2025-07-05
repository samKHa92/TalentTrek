import React, { useState, useEffect } from 'react';
import { Typography, Button, Stack, Snackbar, Alert, Paper, CircularProgress, Box, TextField, Divider, IconButton, List, ListItem, ListItemText, ListItemSecondaryAction, AppBar, Toolbar, Avatar, Menu, MenuItem } from '@mui/material';
import PlayArrowIcon from '@mui/icons-material/PlayArrow';
import AssessmentIcon from '@mui/icons-material/Assessment';
import BarChartIcon from '@mui/icons-material/BarChart';
import ScienceIcon from '@mui/icons-material/Science';
import DeleteIcon from '@mui/icons-material/Delete';
import AccountCircleIcon from '@mui/icons-material/AccountCircle';
import LogoutIcon from '@mui/icons-material/Logout';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import ErrorIcon from '@mui/icons-material/Error';
import axios from 'axios';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend } from 'recharts';
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
  const [report, setReport] = useState(null);
  const [urls, setUrls] = useState({ static_urls: [], dynamic_urls: [] });
  const [newStaticUrl, setNewStaticUrl] = useState('');
  const [newDynamicUrl, setNewDynamicUrl] = useState('');
  const [sources, setSources] = useState([]);
  const [selectedSources, setSelectedSources] = useState([]);
  const [keyword, setKeyword] = useState('');
  const [scrapedJobs, setScrapedJobs] = useState([]);
  const [scraping, setScraping] = useState(false);
  const [showAuth, setShowAuth] = useState('login'); // 'login', 'register', or null
  const [anchorEl, setAnchorEl] = useState(null);
  const [emailVerification, setEmailVerification] = useState(null); // 'verifying', 'success', 'error', or null

  const { user, isAuthenticated, logout, loading: authLoading } = useAuth();

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

  // Fetch URLs on mount
  useEffect(() => {
    if (isAuthenticated) {
      fetchUrls();
    }
  }, [isAuthenticated]);

  // Fetch sources on mount
  useEffect(() => {
    if (isAuthenticated) {
      axios.get('/api/sources').then(res => setSources(res.data)).catch(() => setSources([]));
    }
  }, [isAuthenticated]);

  const fetchUrls = async () => {
    try {
      const res = await axios.get('/api/urls');
      setUrls(res.data);
    } catch (err) {
      setSnackbar({ open: true, message: 'Failed to fetch URLs', severity: 'error' });
    }
  };

  const handleAction = async (action) => {
    setLoading(action);
    setSnackbar({ open: true, message: `Running ${action}...`, severity: 'info' });
    try {
      const res = await axios.post('/api/' + action);
      setSnackbar({ open: true, message: `${action} complete!`, severity: 'success' });
      if (action === 'report') {
        setReport(res.data);
      }
    } catch (err) {
      setSnackbar({ open: true, message: `Error: ${err.response?.data || err.message}`, severity: 'error' });
    } finally {
      setLoading('');
    }
  };

  const handleAddUrl = async (type) => {
    const url = type === 'static' ? newStaticUrl : newDynamicUrl;
    if (!url) return;
    try {
      await axios.post('/api/urls/' + (type === 'static' ? 'static' : 'dynamic'), { url });
      setSnackbar({ open: true, message: `Added ${type} URL!`, severity: 'success' });
      fetchUrls();
      if (type === 'static') setNewStaticUrl('');
      else setNewDynamicUrl('');
    } catch (err) {
      setSnackbar({ open: true, message: `Error: ${err.response?.data?.detail || err.message}`, severity: 'error' });
    }
  };

  const handleRemoveUrl = async (type, url) => {
    try {
      await axios.delete('/api/urls/' + (type === 'static' ? 'static' : 'dynamic'), { data: { url } });
      setSnackbar({ open: true, message: `Removed ${type} URL!`, severity: 'success' });
      fetchUrls();
    } catch (err) {
      setSnackbar({ open: true, message: `Error: ${err.response?.data?.detail || err.message}`, severity: 'error' });
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

  // Move actions array here so it can use handleScrapeJobs
  const actions = [
    { key: 'scrape', label: 'Scrape Jobs', icon: <PlayArrowIcon fontSize="large" />, onClick: handleScrapeJobs },
    { key: 'analyze', label: 'Analyze Data', icon: <ScienceIcon fontSize="large" /> },
    { key: 'report', label: 'Generate Report', icon: <AssessmentIcon fontSize="large" /> },
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
                  onClick={onClick || (() => handleAction(key))}
                  disabled={!!loading || (key === 'scrape' && (scraping || !keyword || selectedSources.length === 0))}
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

        {/* Main Report Area */}
        <Box sx={{ flex: 1, p: 4, display: 'flex', flexDirection: 'column', minHeight: '100vh', overflowY: 'auto', overflowX: 'hidden', width: '97%' }}>
          {/* User Reports Section */}
          <Paper elevation={2} sx={{ p: 3, mb: 3, bgcolor: '#232936', color: '#fff', width: '97%', maxWidth: '97%' }}>
            <UserReports 
              reportData={report} 
              onSaveSuccess={() => setSnackbar({ open: true, message: 'Report saved successfully!', severity: 'success' })}
            />
          </Paper>

          {/* Report Visualization */}
          <Paper elevation={2} sx={{ p: 3, mb: 3, bgcolor: '#232936', color: '#fff', width: '97%', maxWidth: '97%' }}>
            <Typography variant="h5" gutterBottom color="#fff">
              Report Visualization
            </Typography>
            {report ? (
              <Box>
                <Button
                  variant="outlined"
                  sx={{ mb: 2 }}
                  onClick={() => window.open('/api/report/html', '_blank')}
                >
                  Open Full HTML Report
                </Button>
                {/* Statistics */}
                <Typography variant="h6" color="#fff" gutterBottom>Key Statistics</Typography>
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 2, mb: 3 }}>
                  {report.stats && Object.entries(report.stats).map(([key, value]) => (
                    <Paper key={key} sx={{ p: 2, minWidth: 180, bgcolor: '#2d3341', color: '#fff' }}>
                      <Typography variant="subtitle2" color="#b0b3b8">{key.replace(/_/g, ' ').replace(/\b\w/g, l => l.toUpperCase())}</Typography>
                      {typeof value === 'object' && value !== null ? (
                        <ul style={{ margin: 0, paddingLeft: 16 }}>
                          {Object.entries(value).map(([k, v]) => (
                            <li key={k}><b>{k}</b>: {v}</li>
                          ))}
                        </ul>
                      ) : (
                        <Typography variant="h6" color="#fff">{value}</Typography>
                      )}
                    </Paper>
                  ))}
                </Box>

                {/* Trends Chart */}
                {report.trends && report.trends.length > 0 && (
                  <Box sx={{ mb: 3 }}>
                    <Typography variant="h6" color="#fff" gutterBottom>Trends Over Time</Typography>
                    <ResponsiveContainer width="100%" height={300}>
                      <LineChart data={report.trends}>
                        <CartesianGrid strokeDasharray="3 3" stroke="#444" />
                        <XAxis dataKey="date" stroke="#fff" />
                        <YAxis stroke="#fff" />
                        <Tooltip 
                          contentStyle={{ 
                            backgroundColor: '#2d3341', 
                            border: '1px solid #444',
                            color: '#fff'
                          }}
                        />
                        <Legend />
                        <Line type="monotone" dataKey="count" stroke="#1976d2" strokeWidth={2} />
                      </LineChart>
                    </ResponsiveContainer>
                  </Box>
                )}

                {/* Sample Jobs */}
                {report.sample_jobs && report.sample_jobs.length > 0 && (
                  <Box>
                    <Typography variant="h6" color="#fff" gutterBottom>Sample Job Postings</Typography>
                    <List>
                      {report.sample_jobs.map((job, index) => (
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
                              </Box>
                            }
                          />
                        </ListItem>
                      ))}
                    </List>
                  </Box>
                )}
              </Box>
            ) : (
              <Typography variant="body1" color="#ccc">
                Generate a report to see visualizations here.
              </Typography>
            )}
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
