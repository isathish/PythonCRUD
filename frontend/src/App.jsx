import React from 'react';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Sidebar from './components/Sidebar';
import AppBuilder from './pages/AppBuilder';
import './index.css';

function App() {
  return (
    <BrowserRouter>
      <div className="flex">
        <Sidebar />
        <div className="flex-1 bg-gray-100 min-h-screen">
          <Routes>
            <Route path="/" element={<AppBuilder />} />
          </Routes>
        </div>
      </div>
    </BrowserRouter>
  );
}

export default App;
