import React, { useState } from 'react';
import axios from 'axios';

const API_URL = 'http://localhost:8080';

export default function Quiz() {
  const [answer, setAnswer] = useState('');
  const [mastery, setMastery] = useState(0.5);
  const [hint, setHint] = useState('');

  const currentSkill = 5;
  const currentProblem = 42;

  const handleSubmit = async () => {
    try {
      const token = localStorage.getItem('token');
      const isCorrect = answer.trim() === '42' ? 1 : 0; // Mock correct answer = 42
      
      // Submit answer
      await axios.post(`${API_URL}/api/submit/`, {
        skill_id: currentSkill,
        problem_id: currentProblem,
        correct: isCorrect
      }, { headers: { Authorization: `Bearer ${token}` } });
      
      // Predict new mastery
      const predictRes = await axios.post(`${API_URL}/api/predict/`, {
        skill_seq: [currentSkill],
        correct_seq: [isCorrect]
      }, { headers: { Authorization: `Bearer ${token}` } });
      
      const newMastery = predictRes.data.mastery_probabilities[currentSkill];
      setMastery(newMastery);
      setAnswer('');
      alert(isCorrect ? 'Correct!' : 'Incorrect!');
    } catch (e) {
      console.error(e);
    }
  };

  const requestHint = async () => {
    try {
      const token = localStorage.getItem('token');
      const res = await axios.post(`${API_URL}/api/chat/`, {
        question: "I'm stuck on this problem.",
        mastery_prob: mastery
      }, { headers: { Authorization: `Bearer ${token}` } });
      setHint(res.data.hint);
    } catch (e) {
      console.error(e);
      setHint("Failed to get hint from AI Tutor.");
    }
  };

  return (
    <div className="flex h-[80vh] gap-4 p-4">
      {/* Quiz Area */}
      <div className="flex-1 bg-white p-8 rounded shadow-md flex flex-col justify-center">
        <div className="flex justify-between items-center mb-6">
          <h2 className="text-2xl font-bold">Quiz Time</h2>
          <span className="text-sm font-semibold bg-blue-100 text-blue-800 py-1 px-3 rounded-full">
            Mastery: {(mastery * 100).toFixed(1)}%
          </span>
        </div>
        
        <p className="text-lg mb-6">What is the meaning of life, the universe, and everything?</p>
        
        <input 
          type="text" 
          value={answer} 
          onChange={e => setAnswer(e.target.value)} 
          className="border p-3 w-full rounded mb-4"
          placeholder="Type your answer..."
        />
        
        <button onClick={handleSubmit} className="bg-blue-600 text-white py-3 px-6 rounded hover:bg-blue-700">
          Submit Answer
        </button>
      </div>

      {/* AI Hint Panel */}
      <div className="w-1/3 bg-gray-50 border-l p-6 rounded shadow-inner flex flex-col">
        <h3 className="text-xl font-bold mb-4 text-indigo-700 flex items-center">
          <span className="mr-2">🤖</span> AI Tutor
        </h3>
        <p className="text-gray-600 mb-4 flex-1 overflow-y-auto">
          {hint ? hint : "Need help? Ask for a hint!"}
        </p>
        <button onClick={requestHint} className="bg-indigo-600 text-white py-2 rounded hover:bg-indigo-700">
          Get Hint
        </button>
      </div>
    </div>
  );
}
