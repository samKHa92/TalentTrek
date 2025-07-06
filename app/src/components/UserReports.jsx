import React, { useState, useEffect, forwardRef, useImperativeHandle } from 'react';
import {
  Box,
  Typography,
  Paper,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  IconButton,
  Chip,
  Alert,
  CircularProgress,
  Snackbar
} from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import VisibilityIcon from '@mui/icons-material/Visibility';
import { useAuth } from '../contexts/AuthContext';

const UserReports = forwardRef(({ onSaveSuccess }, ref) => {
  const [reports, setReports] = useState([]);
  const [sources, setSources] = useState([]);
  const [loading, setLoading] = useState(false);
  const [viewJobsDialogOpen, setViewJobsDialogOpen] = useState(false);
  const [deleteConfirmDialogOpen, setDeleteConfirmDialogOpen] = useState(false);
  const [selectedReport, setSelectedReport] = useState(null);
  const [reportToDelete, setReportToDelete] = useState(null);
  const [error, setError] = useState('');
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'info' });
  const { getUserReports, deleteReport } = useAuth();

  // Expose loadReports method to parent component
  useImperativeHandle(ref, () => ({
    loadReports
  }));

  useEffect(() => {
    loadReports();
    loadSources();
  }, []);

  const loadReports = async () => {
    setLoading(true);
    const result = await getUserReports();
    if (result.success) {
      setReports(result.reports);
    } else {
      setError(result.error);
    }
    setLoading(false);
  };

  const loadSources = async () => {
    try {
      const response = await fetch('/api/sources');
      const sourcesData = await response.json();
      setSources(sourcesData);
    } catch (error) {
      console.error('Failed to load sources:', error);
    }
  };

  const handleViewJobs = (report) => {
    setSelectedReport(report);
    setViewJobsDialogOpen(true);
  };

  const parseReportData = (reportData) => {
    try {
      return JSON.parse(reportData);
    } catch (e) {
      return [];
    }
  };

  const handleDeleteReport = (report) => {
    setReportToDelete(report);
    setDeleteConfirmDialogOpen(true);
  };

  const confirmDelete = async () => {
    if (!reportToDelete) return;
    
    const result = await deleteReport(reportToDelete.id);
    if (result.success) {
      loadReports();
      setSnackbar({ open: true, message: 'Report deleted successfully!', severity: 'success' });
    } else {
      setError(result.error);
    }
    setDeleteConfirmDialogOpen(false);
    setReportToDelete(null);
  };

  const cancelDelete = () => {
    setDeleteConfirmDialogOpen(false);
    setReportToDelete(null);
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString() + ' ' + new Date(dateString).toLocaleTimeString();
  };

  const getSourceNames = (sourcesUsed) => {
    if (!sourcesUsed) return [];
    try {
      const sourceIds = JSON.parse(sourcesUsed);
      return sourceIds.map(id => {
        const source = sources.find(s => s.id === id);
        return source ? source.name : id;
      });
    } catch (e) {
      return [];
    }
  };



  return (
    <Box sx={{ width: '100%' }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
        <Typography variant="h6" color="#fff">
          My Saved Reports
        </Typography>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      {loading ? (
        <Box sx={{ display: 'flex', justifyContent: 'center', p: 3 }}>
          <CircularProgress />
        </Box>
      ) : reports.length === 0 ? (
        <Paper sx={{ p: 3, bgcolor: '#2d3341', color: '#fff', textAlign: 'center' }}>
          <Typography variant="body1" color="#ccc">
            No saved reports yet. Scrape some jobs and save them to see them here.
          </Typography>
        </Paper>
      ) : (
        <List>
          {reports.map((report) => (
            <React.Fragment key={report.id}>
              <ListItem sx={{ bgcolor: '#2d3341', mb: 1, borderRadius: 1 }}>
                <ListItemText
                  primary={
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1, flexWrap: 'wrap' }}>
                      <Typography variant="h6" color="#fff">
                        {report.title}
                      </Typography>
                      {getSourceNames(report.sources_used).map((sourceName, index) => (
                        <Chip
                          key={index}
                          label={sourceName}
                          color="primary"
                          size="small"
                        />
                      ))}
                      <Chip
                        label={`${report.job_count || parseReportData(report.jobs_data).length} jobs`}
                        color="info"
                        size="small"
                        variant="outlined"
                      />
                    </Box>
                  }
                  secondary={
                    <Box>
                      {report.description && (
                        <Typography variant="body2" color="#ccc" sx={{ mb: 1 }}>
                          {report.description}
                        </Typography>
                      )}
                      <Typography variant="caption" color="#999">
                        Created: {formatDate(report.created_at)}
                      </Typography>
                    </Box>
                  }
                />
                <ListItemSecondaryAction>
                  <IconButton
                    edge="end"
                    onClick={() => handleViewJobs(report)}
                    sx={{ color: '#1976d2', mr: 1 }}
                  >
                    <VisibilityIcon />
                  </IconButton>
                  <IconButton
                    edge="end"
                    onClick={() => handleDeleteReport(report)}
                    sx={{ color: '#ff6b6b' }}
                  >
                    <DeleteIcon />
                  </IconButton>
                </ListItemSecondaryAction>
              </ListItem>
            </React.Fragment>
          ))}
        </List>
      )}

      {/* View Jobs Dialog */}
      <Dialog open={viewJobsDialogOpen} onClose={() => setViewJobsDialogOpen(false)} maxWidth="md" fullWidth>
        <DialogTitle sx={{ bgcolor: '#232936', color: '#fff' }}>
          {selectedReport?.title} - Jobs
        </DialogTitle>
        <DialogContent sx={{ bgcolor: '#232936', color: '#fff', maxHeight: '70vh' }}>
          {selectedReport && (
            <List>
              {parseReportData(selectedReport.jobs_data).map((job, index) => (
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
          )}
        </DialogContent>
        <DialogActions sx={{ bgcolor: '#232936' }}>
          <Button onClick={() => setViewJobsDialogOpen(false)} sx={{ color: '#ccc' }}>
            Close
          </Button>
        </DialogActions>
      </Dialog>

      {/* Delete Confirmation Dialog */}
      <Dialog open={deleteConfirmDialogOpen} onClose={cancelDelete} maxWidth="sm" fullWidth>
        <DialogTitle sx={{ bgcolor: '#232936', color: '#fff' }}>
          Confirm Delete
        </DialogTitle>
        <DialogContent sx={{ bgcolor: '#232936', color: '#fff' }}>
          <Typography variant="body1" color="#ccc">
            Are you sure you want to delete the report "{reportToDelete?.title}"?
          </Typography>
          <Typography variant="body2" color="#999" sx={{ mt: 1 }}>
            This action cannot be undone.
          </Typography>
        </DialogContent>
        <DialogActions sx={{ bgcolor: '#232936' }}>
          <Button onClick={cancelDelete} sx={{ color: '#ccc' }}>
            Cancel
          </Button>
          <Button onClick={confirmDelete} sx={{ bgcolor: '#ff6b6b', color: '#fff', '&:hover': { bgcolor: '#d32f2f' } }} variant="contained">
            Delete
          </Button>
        </DialogActions>
      </Dialog>

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
});

export default UserReports; 