import React, { createContext, useContext, useState, ReactNode } from 'react';

interface TabContextType {
  currentTab: string;
  setCurrentTab: (index: string) => void;
}

const TabContext = createContext<TabContextType | undefined>(undefined);

interface TabProviderProps {
  children: ReactNode; // Adding type for children here
}

export const TabProvider: React.FC<TabProviderProps> = ({ children }) => {
  const [currentTab, setCurrentTab] = useState("");

  return (
    <TabContext.Provider value={{ currentTab, setCurrentTab }}>
      {children}
    </TabContext.Provider>
  );
};

export const useTab = () => {
  const context = useContext(TabContext);
  if (!context) {
    throw new Error('useTab must be used within a TabProvider');
  }
  return context;
};
