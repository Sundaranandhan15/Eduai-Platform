import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const API_URL = 'http://localhost:8080';

export default function Login() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const params = new URLSearchParams();
      params.append('username', username);
      params.append('password', password);
      
      const res = await axios.post(`${API_URL}/auth/login`, params);
      localStorage.setItem('token', res.data.access_token);
      localStorage.setItem('user_id', '1'); // Mocking user id for demo purposes
      navigate('/dashboard');
    } catch (error) {
      alert('Login failed. Check credentials.');
    }
  };

  return (
    <div className="flex flex-col items-center justify-center mt-20">
      <form onSubmit={handleLogin} className="bg-white p-8 rounded shadow-md w-96">
        <h2 className="text-2xl font-bold mb-6 text-center">Login to EduAI</h2>
        <input 
          type="text" 
          placeholder="Username" 
          value={username} 
          onChange={e => setUsername(e.target.value)}
          className="w-full border p-2 mb-4 rounded" 
          required 
        />
        <input 
          type="password" 
          placeholder="Password" 
          value={password} 
          onChange={e => setPassword(e.target.value)}
          className="w-full border p-2 mb-6 rounded" 
          required 
        />
        <button className="w-full bg-blue-600 text-white p-2 rounded hover:bg-blue-700">Login</button>
        <p className="mt-4 text-center">
          Don't have an account? <a href="/register" className="text-blue-600">Register</a>
        </p>
      </form>
    </div>
  );
}
