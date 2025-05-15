import React, { useState } from 'react';
import { 
  TextField, 
  Button, 
  Alert, 
  Snackbar,
  Paper,
  Typography,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  IconButton,
  Collapse,
  Card,
  CardContent,
  Fade,
  Box
} from '@mui/material';
import LinkIcon from '@mui/icons-material/Link';
import ReportIcon from '@mui/icons-material/Report';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import DangerousIcon from '@mui/icons-material/Dangerous';
import CloseIcon from '@mui/icons-material/Close';
import { keyframes } from '@emotion/react';

const pulse = keyframes`
  0% { transform: scale(1); }
  50% { transform: scale(1.05); }
  100% { transform: scale(1); }
`;

export default function UrlChecker() {
  const [url, setUrl] = useState('');
  const [result, setResult] = useState(null);
  const [open, setOpen] = useState(false);
  const [reportDialogOpen, setReportDialogOpen] = useState(false);
  const [expanded, setExpanded] = useState(false);

  const checkUrl = async () => {
    try {
      const response = await fetch('http://localhost:5000/check_url', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ url }),
      });
      
      const data = await response.json();
      setResult(data);
      setOpen(true);
      setExpanded(true);
    } catch (error) {
      console.error('Error checking URL:', error);
      setResult({ message: 'Error checking URL', result: 'error' });
      setOpen(true);
    }
  };

  const handleReport = () => {
    setReportDialogOpen(true);
    setTimeout(() => {
      setReportDialogOpen(false);
    }, 2000);
  };

  return (
    <Paper elevation={0} sx={{ 
      p: 4, 
      borderRadius: 4,
      background: 'transparent',
      width: '100%'
    }}>
      <Typography variant="h4" gutterBottom sx={{ 
        display: 'flex', 
        alignItems: 'center',
        color: 'primary.main',
        fontWeight: 'bold',
        mb: 3
      }}>
        <LinkIcon color="primary" sx={{ mr: 2, fontSize: '2rem' }} />
        URL Safety Checker
      </Typography>
      
      <TextField
        fullWidth
        label="Enter URL to check"
        variant="outlined"
        value={url}
        onChange={(e) => setUrl(e.target.value)}
        sx={{ mb: 3 }}
        InputProps={{
          sx: {
            borderRadius: '12px',
            fontSize: '1.1rem'
          }
        }}
      />
      
      <Box sx={{ display: 'flex', gap: 2 }}>
        <Button
          variant="contained"
          size="large"
          onClick={checkUrl}
          disabled={!url}
          sx={{
            px: 4,
            py: 1.5,
            borderRadius: '12px',
            fontSize: '1.1rem',
            fontWeight: 'bold',
            textTransform: 'none',
            animation: `${pulse} 2s infinite`,
            '&:hover': {
              transform: 'translateY(-2px)',
              boxShadow: '0 6px 12px rgba(67, 97, 238, 0.3)'
            },
            transition: 'all 0.3s ease'
          }}
        >
          Analyze URL
        </Button>
      </Box>

      <Collapse in={expanded} sx={{ mt: 3 }}>
        {result && (
          <Fade in={expanded}>
            <Card sx={{ 
              borderRadius: 3,
              borderLeft: `6px solid ${result.result === 'phishing' ? '#f72585' : '#4cc9f0'}`,
              boxShadow: '0 4px 20px rgba(0,0,0,0.08)'
            }}>
              <CardContent>
                <Box sx={{ display: 'flex', alignItems: 'center', mb: 1 }}>
                  {result.result === 'phishing' ? (
                    <DangerousIcon color="error" sx={{ fontSize: 32, mr: 2 }} />
                  ) : (
                    <CheckCircleIcon color="success" sx={{ fontSize: 32, mr: 2 }} />
                  )}
                  <Typography variant="h6" sx={{ fontWeight: 'bold' }}>
                    {result.result === 'phishing' ? 'Dangerous URL Detected!' : 'URL Looks Safe'}
                  </Typography>
                </Box>
                <Typography variant="body1" sx={{ mb: 2 }}>
                  {result.message.split('\n').map((line, i) => (
                    <React.Fragment key={i}>
                      {line}
                      <br />
                    </React.Fragment>
                  ))}
                </Typography>
                {result.result === 'phishing' && (
                  <Button
                    variant="contained"
                    color="error"
                    size="medium"
                    startIcon={<ReportIcon />}
                    onClick={handleReport}
                    sx={{
                      borderRadius: '12px',
                      fontWeight: 'bold',
                      textTransform: 'none',
                      px: 3,
                      '&:hover': {
                        transform: 'translateY(-2px)',
                        boxShadow: '0 6px 12px rgba(247, 37, 133, 0.3)'
                      },
                      transition: 'all 0.3s ease'
                    }}
                  >
                    Report to CyberCrime
                  </Button>
                )}
              </CardContent>
            </Card>
          </Fade>
        )}
      </Collapse>

      <Dialog 
        open={reportDialogOpen} 
        onClose={() => setReportDialogOpen(false)}
        PaperProps={{
          sx: {
            borderRadius: '16px',
            p: 2,
            background: 'linear-gradient(145deg, #ffffff, #f8f9fa)'
          }
        }}
      >
        <DialogTitle sx={{ fontWeight: 'bold', color: 'primary.main' }}>
          <Box sx={{ display: 'flex', alignItems: 'center' }}>
            <ReportIcon color="primary" sx={{ mr: 1 }} />
            Report Submitted
          </Box>
        </DialogTitle>
        <DialogContent>
          <Typography>
            This phishing attempt has been reported to cybercrime authorities.
          </Typography>
        </DialogContent>
        <DialogActions>
          <Button 
            onClick={() => setReportDialogOpen(false)}
            sx={{ borderRadius: '12px', fontWeight: 'bold' }}
          >
            Close
          </Button>
        </DialogActions>
      </Dialog>
    </Paper>
  );
}