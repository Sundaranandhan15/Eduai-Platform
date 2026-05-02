import React from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './pages/Login';
import Register from './pages/Register';
import Dashboard from './pages/Dashboard';
import Quiz from './pages/Quiz';
import Chat from './pages/Chat';

function App() {
  return (
    <Router>
      <div className="min-h-screen flex flex-col font-sans">
        <header className="bg-blue-600 text-white p-4 shadow-md">
          <div className="container mx-auto flex justify-between items-center">
            <h1 className="text-2xl font-bold">EduAI</h1>
            <nav className="flex space-x-4">
              <a href="/dashboard" className="hover:text-blue-200">Dashboard</a>
              <a href="/quiz" className="hover:text-blue-200">Quiz</a>
              <a href="/chat" className="hover:text-blue-200">AI Tutor</a>
            </nav>
          </div>
        </header>
        <main className="flex-grow container mx-auto p-4">
          <Routes>
            <Route path="/" element={<Navigate to="/login" />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/quiz" element={<Quiz />} />
            <Route path="/chat" element={<Chat />} />
          </Routes>
        </main>
      </div>
    </Router>
  );
}

export default App;
