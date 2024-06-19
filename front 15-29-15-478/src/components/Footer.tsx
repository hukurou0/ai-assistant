import React from 'react';
import { Box, Tabs, Tab, Typography } from '@mui/material';
import { useTab } from './Contexts/TabContext'; // Make sure this path is correct

export const Footer: React.FC = () => {
  const { currentTab, setCurrentTab } = useTab();  // Using context to get value and setValue

  const handleChange = (event: React.SyntheticEvent, newValue: string) => {
    setCurrentTab(newValue);
  };

  

  return (
    <Box component="footer">
      <Tabs value={currentTab} onChange={handleChange} centered>
        <Tab label="ホーム" value="home" />
        <Tab label="推奨" value="recommend"/>
      </Tabs>
    <Typography variant="body2" color="text.secondary" align="center" sx={{ pt: 3 }}>
        © 2024 Your Company Name
    </Typography>
    </Box>
  );
};