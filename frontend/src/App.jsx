import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import DashboardPage from './pages/DashboardPage';
import ProjectsPage from './pages/ProjectsPage';
import UsersPage from './pages/UsersPage';
import TagsPage from './pages/TagsPage';
import AppBuilder from './pages/AppBuilder';
import './index.css';

function App() {
  return (
    <BrowserRouter>
      <div className="flex">
        <Sidebar />
        <div className="flex-1 bg-gray-100 min-h-screen">
          <Routes>
            <Route path="/" element={<DashboardPage />} />
            <Route path="/projects" element={<ProjectsPage />} />
            <Route path="/users" element={<UsersPage />} />
            <Route path="/tags" element={<TagsPage />} />
            <Route path="/builder" element={<AppBuilder />} />
          </Routes>
        </div>
      </div>
    </BrowserRouter>
  );
}

export default App;
