import React, { useState } from 'react';
import axios from 'axios';
import { useNavigate } from 'react-router-dom';

const API_URL = 'http://localhost:8080';

export default function Register() {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const navigate = useNavigate();

  const handleRegister = async (e) => {
    e.preventDefault();
    try {
      const res = await axios.post(`${API_URL}/auth/register`, {
        username,
        password
      });
      localStorage.setItem('token', res.data.access_token);
      localStorage.setItem('user_id', '1');
      navigate('/dashboard');
    } catch (error) {
      alert('Registration failed. Username may exist.');
    }
  };

  return (
    <div className="flex flex-col items-center justify-center mt-20">
      <form onSubmit={handleRegister} className="bg-white p-8 rounded shadow-md w-96">
        <h2 className="text-2xl font-bold mb-6 text-center">Register for EduAI</h2>
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
        <button className="w-full bg-green-600 text-white p-2 rounded hover:bg-green-700">Register</button>
        <p className="mt-4 text-center">
          Already have an account? <a href="/login" className="text-green-600">Login</a>
        </p>
      </form>
    </div>
  );
}
