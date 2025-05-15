import React from 'react';
import { Box, Container, Grid, Typography, Link } from '@mui/material';

const Footer = () => {
  return (
    <Box sx={{
      py: 4,
      mt: 'auto',
      background: 'linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%)',
      borderTop: '1px solid #dee2e6'
    }}>
      <Container maxWidth="lg">
        <Grid container spacing={4}>
          <Grid item xs={12} sm={6} md={3}>
            <Typography variant="h6" gutterBottom sx={{ fontWeight: 'bold' }}>
              About
            </Typography>
            <Typography variant="body2">
              PHISHDETECT helps identify phishing URLs and emails to protect you from online scams.
            </Typography>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Typography variant="h6" gutterBottom sx={{ fontWeight: 'bold' }}>
              How to Use
            </Typography>
            <Typography variant="body2">
              Simply paste a URL or email content to check for phishing attempts.
            </Typography>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Typography variant="h6" gutterBottom sx={{ fontWeight: 'bold' }}>
              Contact
            </Typography>
            <Typography variant="body2">
              <Link href="mailto:phishdetect@example.com" color="inherit">
                PHISHDETECT@2025
              </Link>
            </Typography>
          </Grid>
          <Grid item xs={12} sm={6} md={3}>
            <Typography variant="h6" gutterBottom sx={{ fontWeight: 'bold' }}>
              © 2025 PHISHDETECT
            </Typography>
            <Typography variant="body2">
              All rights reserved
            </Typography>
          </Grid>
        </Grid>
      </Container>
    </Box>
  );
};

export default Footer;