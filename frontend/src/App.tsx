import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import RootFinderPage from './pages/RootFinderPage';
import AcademicWizard from './pages/AcademicWizard';
import Workspace from './pages/Workspace';

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Dashboard />} />
        <Route path="/wizard" element={<AcademicWizard />} />
        <Route path="/rootfinder" element={<RootFinderPage />} />
        <Route path="/workspace" element={<Workspace />} />
        {/* Add more routes as needed */}
        <Route path="*" element={<Dashboard />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;
