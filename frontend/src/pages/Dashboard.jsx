import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const API_URL = 'http://localhost:8080';

export default function Dashboard() {
  const [history, setHistory] = useState([]);
  
  useEffect(() => {
    const fetchProgress = async () => {
      try {
        const token = localStorage.getItem('token');
        const userId = localStorage.getItem('user_id') || '1';
        const res = await axios.get(`${API_URL}/api/progress/${userId}`, {
          headers: { Authorization: `Bearer ${token}` }
        });
        setHistory(res.data.history || []);
      } catch (e) {
        console.error(e);
      }
    };
    fetchProgress();
  }, []);

  // Mock data if history is empty
  const radarData = history.length > 0 ? 
    history[history.length - 1].slice(0, 5).map((val, idx) => ({ subject: `Skill ${idx}`, A: val * 100, fullMark: 100 })) :
    [
      { subject: 'Math', A: 80, fullMark: 100 },
      { subject: 'Science', A: 65, fullMark: 100 },
      { subject: 'History', A: 90, fullMark: 100 },
      { subject: 'English', A: 70, fullMark: 100 },
      { subject: 'Art', A: 85, fullMark: 100 },
    ];

  const lineData = history.length > 0 ?
    history.map((probs, idx) => ({ name: `T${idx}`, avg: (probs.reduce((a,b)=>a+b,0)/probs.length)*100 })) :
    [
      { name: 'Jan', avg: 40 },
      { name: 'Feb', avg: 45 },
      { name: 'Mar', avg: 55 },
      { name: 'Apr', avg: 65 },
      { name: 'May', avg: 75 },
    ];

  return (
    <div className="p-4">
      <h2 className="text-3xl font-bold mb-8">Student Dashboard</h2>
      
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div className="bg-white p-4 rounded shadow-md h-96">
          <h3 className="text-xl font-bold mb-4 text-center">Skill Mastery Radar</h3>
          <ResponsiveContainer width="100%" height="100%">
            <RadarChart cx="50%" cy="50%" outerRadius="80%" data={radarData}>
              <PolarGrid />
              <PolarAngleAxis dataKey="subject" />
              <PolarRadiusAxis angle={30} domain={[0, 100]} />
              <Radar name="Student" dataKey="A" stroke="#8884d8" fill="#8884d8" fillOpacity={0.6} />
              <Tooltip />
            </RadarChart>
          </ResponsiveContainer>
        </div>

        <div className="bg-white p-4 rounded shadow-md h-96">
          <h3 className="text-xl font-bold mb-4 text-center">Progress Over Time</h3>
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={lineData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis dataKey="name" />
              <YAxis domain={[0, 100]} />
              <Tooltip />
              <Legend />
              <Line type="monotone" dataKey="avg" stroke="#82ca9d" activeDot={{ r: 8 }} name="Average Mastery %" />
            </LineChart>
          </ResponsiveContainer>
        </div>
      </div>
    </div>
  );
}
