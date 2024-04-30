import React from 'react';
import './App.css';
import {Footer} from "./components/Footer"
import { useTab } from './components/Contexts/TabContext';
import Home from './components/Home'
import Recommend from './components/Recommend'
import GoogleAuth from './components/GoogleAuth';

function App() {
  const { currentTab } = useTab();
  return (
      <div>
        <GoogleAuth />
        {currentTab === "home" && <Home />}
        {currentTab === "recommend" && <Recommend />}
        <Footer />
      </div>
  );
}

export default App;
