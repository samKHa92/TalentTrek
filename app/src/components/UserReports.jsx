import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Paper,
  Button,
  TextField,
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
  Divider
} from '@mui/material';
import DeleteIcon from '@mui/icons-material/Delete';
import SaveIcon from '@mui/icons-material/Save';
import { useAuth } from '../contexts/AuthContext';

const UserReports = ({ reportData, onSaveSuccess }) => {
  const [reports, setReports] = useState([]);
  const [loading, setLoading] = useState(false);
  const [saveDialogOpen, setSaveDialogOpen] = useState(false);
  const [saveTitle, setSaveTitle] = useState('');
  const [saveDescription, setSaveDescription] = useState('');
  const [saveType, setSaveType] = useState('analysis');
  const [error, setError] = useState('');
  const { saveReport, getUserReports, deleteReport } = useAuth();

  useEffect(() => {
    loadReports();
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

  const handleSaveReport = async () => {
    if (!saveTitle.trim()) {
      setError('Please enter a title for the report');
      return;
    }

    setLoading(true);
    const result = await saveReport(saveTitle, saveDescription, saveType, reportData);
    if (result.success) {
      setSaveDialogOpen(false);
      setSaveTitle('');
      setSaveDescription('');
      setSaveType('analysis');
      setError('');
      loadReports();
      if (onSaveSuccess) onSaveSuccess();
    } else {
      setError(result.error);
    }
    setLoading(false);
  };

  const handleDeleteReport = async (reportId) => {
    const result = await deleteReport(reportId);
    if (result.success) {
      loadReports();
    } else {
      setError(result.error);
    }
  };

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString() + ' ' + new Date(dateString).toLocaleTimeString();
  };

  const getReportTypeColor = (type) => {
    switch (type) {
      case 'scrape': return 'primary';
      case 'analysis': return 'secondary';
      case 'trends': return 'success';
      default: return 'default';
    }
  };

  return (
    <Box sx={{ width: '100%' }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
        <Typography variant="h6" color="#fff">
          My Saved Reports
        </Typography>
        <Button
          variant="contained"
          startIcon={<SaveIcon />}
          onClick={() => setSaveDialogOpen(true)}
          disabled={!reportData}
        >
          Save Current Report
        </Button>
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
            No saved reports yet. Generate a report and save it to see it here.
          </Typography>
        </Paper>
      ) : (
        <List>
          {reports.map((report) => (
            <React.Fragment key={report.id}>
              <ListItem sx={{ bgcolor: '#2d3341', mb: 1, borderRadius: 1 }}>
                <ListItemText
                  primary={
                    <Box sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
                      <Typography variant="h6" color="#fff">
                        {report.title}
                      </Typography>
                      <Chip
                        label={report.report_type}
                        color={getReportTypeColor(report.report_type)}
                        size="small"
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
                    onClick={() => handleDeleteReport(report.id)}
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

      {/* Save Report Dialog */}
      <Dialog open={saveDialogOpen} onClose={() => setSaveDialogOpen(false)} maxWidth="sm" fullWidth>
        <DialogTitle sx={{ bgcolor: '#232936', color: '#fff' }}>
          Save Report
        </DialogTitle>
        <DialogContent sx={{ bgcolor: '#232936', color: '#fff' }}>
          <TextField
            fullWidth
            label="Report Title"
            value={saveTitle}
            onChange={(e) => setSaveTitle(e.target.value)}
            margin="normal"
            required
            sx={{
              '& .MuiOutlinedInput-root': {
                '& fieldset': { borderColor: '#444' },
                '&:hover fieldset': { borderColor: '#666' },
                '&.Mui-focused fieldset': { borderColor: '#1976d2' },
              },
              '& .MuiInputLabel-root': { color: '#ccc' },
              '& .MuiInputBase-input': { color: '#fff' },
            }}
          />
          <TextField
            fullWidth
            label="Description (optional)"
            value={saveDescription}
            onChange={(e) => setSaveDescription(e.target.value)}
            margin="normal"
            multiline
            rows={3}
            sx={{
              '& .MuiOutlinedInput-root': {
                '& fieldset': { borderColor: '#444' },
                '&:hover fieldset': { borderColor: '#666' },
                '&.Mui-focused fieldset': { borderColor: '#1976d2' },
              },
              '& .MuiInputLabel-root': { color: '#ccc' },
              '& .MuiInputBase-input': { color: '#fff' },
            }}
          />
          <TextField
            fullWidth
            select
            label="Report Type"
            value={saveType}
            onChange={(e) => setSaveType(e.target.value)}
            margin="normal"
            sx={{
              '& .MuiOutlinedInput-root': {
                '& fieldset': { borderColor: '#444' },
                '&:hover fieldset': { borderColor: '#666' },
                '&.Mui-focused fieldset': { borderColor: '#1976d2' },
              },
              '& .MuiInputLabel-root': { color: '#ccc' },
              '& .MuiInputBase-input': { color: '#fff' },
            }}
          >
            <option value="analysis">Analysis</option>
            <option value="scrape">Scrape Results</option>
            <option value="trends">Trends</option>
          </TextField>
        </DialogContent>
        <DialogActions sx={{ bgcolor: '#232936' }}>
          <Button onClick={() => setSaveDialogOpen(false)} sx={{ color: '#ccc' }}>
            Cancel
          </Button>
          <Button
            onClick={handleSaveReport}
            variant="contained"
            disabled={loading || !saveTitle.trim()}
          >
            {loading ? <CircularProgress size={20} /> : 'Save'}
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  );
};

export default UserReports; 