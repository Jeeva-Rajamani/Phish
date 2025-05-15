import React, { useState } from 'react';
import { 
  TextField, 
  Button, 
  Paper,
  Typography,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Collapse,
  Card,
  CardContent,
  Fade,
  Box
} from '@mui/material';
import EmailIcon from '@mui/icons-material/Email';
import ReportIcon from '@mui/icons-material/Report';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import DangerousIcon from '@mui/icons-material/Dangerous';
import { keyframes } from '@emotion/react';

const pulse = keyframes`
  0% { transform: scale(1); }
  50% { transform: scale(1.05); }
  100% { transform: scale(1); }
`;

export default function EmailChecker() {
  const [emailText, setEmailText] = useState('');
  const [result, setResult] = useState(null);
  const [expanded, setExpanded] = useState(false);
  const [reportDialogOpen, setReportDialogOpen] = useState(false);

  const checkEmail = async () => {
    try {
      const response = await fetch('http://localhost:5000/check_email', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ email: emailText }),
      });
      
      const data = await response.json();
      setResult(data);
      setExpanded(true);
    } catch (error) {
      console.error('Error checking email:', error);
      setResult({ message: 'Error checking email', result: 'error' });
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
        <EmailIcon color="primary" sx={{ mr: 2, fontSize: '2rem' }} />
        Email Safety Checker
      </Typography>
      
      <TextField
        fullWidth
        multiline
        rows={8}
        label="Paste email content here"
        variant="outlined"
        value={emailText}
        onChange={(e) => setEmailText(e.target.value)}
        sx={{ mb: 3 }}
        InputProps={{
          sx: {
            borderRadius: '12px',
            fontSize: '1.1rem'
          }
        }}
      />
      
      <Button
        variant="contained"
        size="large"
        onClick={checkEmail}
        disabled={!emailText.trim()}
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
        Analyze Email
      </Button>

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
                    {result.result === 'phishing' ? 'Phishing Email Detected!' : 'Email Looks Safe'}
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