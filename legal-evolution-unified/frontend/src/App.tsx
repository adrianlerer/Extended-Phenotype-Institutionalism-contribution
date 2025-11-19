import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Dashboard from './pages/Dashboard';
import RootFinderPage from './pages/RootFinderPage';
import AcademicWizard from './pages/AcademicWizard';
import Workspace from './pages/Workspace';

function App() {
  // Get base path from import.meta.env for proper GitHub Pages routing
  const basename = import.meta.env.BASE_URL;
  
  return (
    <BrowserRouter basename={basename}>
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
