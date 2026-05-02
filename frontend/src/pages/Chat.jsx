import React, { useState } from 'react';
import axios from 'axios';

const API_URL = 'http://localhost:8080';

export default function Chat() {
  const [messages, setMessages] = useState([
    { sender: 'AI', text: "Hello! I'm your AI Tutor. What would you like to learn today?" }
  ]);
  const [input, setInput] = useState('');

  const handleSend = async () => {
    if (!input.trim()) return;
    
    const userMessage = { sender: 'User', text: input };
    setMessages(prev => [...prev, userMessage]);
    setInput('');
    
    try {
      const token = localStorage.getItem('token');
      // Sending chat request with an assumed average mastery
      const res = await axios.post(`${API_URL}/api/chat/`, {
        question: input,
        mastery_prob: 0.5 
      }, { headers: { Authorization: `Bearer ${token}` } });
      
      const aiMessage = { sender: 'AI', text: res.data.hint };
      setMessages(prev => [...prev, aiMessage]);
    } catch (e) {
      console.error(e);
      setMessages(prev => [...prev, { sender: 'AI', text: 'Error connecting to the AI Tutor.' }]);
    }
  };

  return (
    <div className="flex flex-col h-[80vh] bg-white rounded shadow-md">
      <div className="bg-indigo-600 text-white p-4 rounded-t flex items-center">
        <span className="text-2xl mr-2">🤖</span>
        <h2 className="text-xl font-bold">AI Tutor Chat</h2>
      </div>
      
      <div className="flex-1 overflow-y-auto p-4 space-y-4 bg-gray-50">
        {messages.map((msg, idx) => (
          <div key={idx} className={`flex ${msg.sender === 'User' ? 'justify-end' : 'justify-start'}`}>
            <div className={`max-w-md p-3 rounded-lg ${msg.sender === 'User' ? 'bg-blue-500 text-white rounded-br-none' : 'bg-white border rounded-bl-none shadow-sm'}`}>
              <p>{msg.text}</p>
            </div>
          </div>
        ))}
      </div>
      
      <div className="p-4 bg-white border-t flex gap-2">
        <input 
          type="text" 
          value={input} 
          onChange={e => setInput(e.target.value)} 
          onKeyPress={e => e.key === 'Enter' && handleSend()}
          className="flex-1 border p-3 rounded outline-none focus:border-indigo-500"
          placeholder="Ask a question..."
        />
        <button onClick={handleSend} className="bg-indigo-600 text-white px-6 py-3 rounded hover:bg-indigo-700 font-bold">
          Send
        </button>
      </div>
    </div>
  );
}
