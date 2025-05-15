import React, { useState } from 'react';
import { Container, Tabs, Tab, Box, CssBaseline, ThemeProvider, createTheme } from '@mui/material';
import Header from './components/Header';
import Footer from './components/Footer';
import UrlChecker from './components/UrlChecker';
import EmailChecker from './components/EmailChecker';

const theme = createTheme({
  palette: {
    primary: {
      main: '#4361ee',
    },
    secondary: {
      main: '#3f37c9',
    },
    error: {
      main: '#f72585',
    },
    success: {
      main: '#4cc9f0',
    },
    background: {
      default: '#f8f9fa',
    },
  },
  typography: {
    fontFamily: '"Poppins", "Roboto", "Helvetica", "Arial", sans-serif',
  },
});

function App() {
  const [activeTab, setActiveTab] = useState(0);

  const handleTabChange = (event, newValue) => {
    setActiveTab(newValue);
  };

  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
        <Header />
        <Container maxWidth="lg" sx={{ py: 4, flex: 1 }}>
          <Tabs 
            value={activeTab}
            onChange={handleTabChange}
            centered
            sx={{
              mb: 4,
              '& .MuiTabs-indicator': {
                height: 4,
                borderRadius: '4px 4px 0 0',
              }
            }}
          >
            <Tab 
              label="URL Detector" 
              sx={{
                fontSize: '1.1rem',
                fontWeight: 'bold',
                '&.Mui-selected': { color: 'primary.main' }
              }} 
            />
            <Tab 
              label="Email Detector" 
              sx={{
                fontSize: '1.1rem',
                fontWeight: 'bold',
                '&.Mui-selected': { color: 'primary.main' }
              }} 
            />
          </Tabs>

          <Box sx={{ 
            p: 3, 
            borderRadius: 4,
            background: 'linear-gradient(145deg, #ffffff, #f0f2f5)',
            boxShadow: '0 8px 32px rgba(31, 38, 135, 0.1)'
          }}>
            {activeTab === 0 && <UrlChecker />}
            {activeTab === 1 && <EmailChecker />}
          </Box>
        </Container>
        <Footer />
      </Box>
    </ThemeProvider>
  );
}

export default App;