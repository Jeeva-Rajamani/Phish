import React from 'react';
import { AppBar, Toolbar, Typography, Box } from '@mui/material';
import SecurityIcon from '@mui/icons-material/Security';

const Header = () => {
  return (
    <AppBar position="static" sx={{ 
      background: 'linear-gradient(135deg, #4361ee 0%, #3a0ca3 100%)',
      boxShadow: '0 4px 20px rgba(0,0,0,0.1)',
      mb: 4
    }}>
      <Toolbar>
        <SecurityIcon sx={{ mr: 2, fontSize: '2rem' }} />
        <Typography variant="h4" component="div" sx={{ 
          flexGrow: 1,
          fontWeight: 'bold',
          letterSpacing: '2px',
          textShadow: '1px 1px 3px rgba(0,0,0,0.2)'
        }}>
          PHISHDETECT
        </Typography>
      </Toolbar>
    </AppBar>
  );
};

export default Header;