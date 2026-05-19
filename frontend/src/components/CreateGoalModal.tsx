'use client';
import { useState } from 'react';

interface CreateGoalModalProps {
  onClose: () => void;
}

export default function CreateGoalModal({ onClose }: CreateGoalModalProps) {
  const [loading, setLoading] = useState(false);
  const [response, setResponse] = useState<string>('');
  const [error, setError] = useState<string>('');
  const [formData, setFormData] = useState({
    user_wallet: 'demo_wallet_' + Math.random().toString(36).substr(2, 9),
    origin: 'Istanbul',
    destination: 'Paris',
    travel_date: '2026-07-15',
    budget_usd: '1500',
    preferences: 'budget travel with local experiences'
  });

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setLoading(true);
    setResponse('');
    setError('');

    try {
      console.log('Sending request to http://localhost:8000/api/goals/create');

      const res = await fetch('http://localhost:8000/api/goals/create', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          user_wallet: formData.user_wallet,
          origin: formData.origin,
          destination: formData.destination,
          travel_date: formData.travel_date,
          budget_usd: parseFloat(formData.budget_usd),
          preferences: formData.preferences
        })
      });

      console.log('Response status:', res.status);

      if (!res.ok) {
        const errorText = await res.text();
        throw new Error(`API Error: ${res.status} - ${errorText}`);
      }

      if (res.body) {
        const reader = res.body.getReader();
        const decoder = new TextDecoder();
        let buffer = '';

        setResponse('🔄 Analyzing your travel goal...\n\n');

        while (true) {
          const { done, value } = await reader.read();
          if (done) break;

          const chunk = decoder.decode(value, { stream: true });
          buffer += chunk;

          // Parse SSE events
          const lines = buffer.split('\n');
          buffer = lines[lines.length - 1];

          for (let i = 0; i < lines.length - 1; i++) {
            const line = lines[i];

            if (line.startsWith('data: ')) {
              try {
                const data = JSON.parse(line.substring(6));
                console.log('Event received:', data);

                if (data.event === 'agent_start') {
                  setResponse(prev => prev + `\n🤖 Starting ${data.agent} agent...\n`);
                } else if (data.event === 'agent_complete') {
                  setResponse(prev => prev + `✓ ${data.agent} completed\n`);
                } else if (data.event === 'done') {
                  setResponse(prev => prev + `\n✨ ANALYSIS COMPLETE!\n\n${data.report}\n`);
                }
              } catch (e) {
                console.log('Raw data:', line.substring(6));
              }
            }
          }
        }

        if (!response) {
          setResponse('✓ Analysis Complete!');
        }
      } else {
        throw new Error('No response body');
      }
    } catch (error) {
      console.error('Error:', error);
      setError(`⚠️ Error: ${error instanceof Error ? error.message : String(error)}`);
      setResponse('');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="fixed inset-0 bg-black/50 flex items-center justify-center p-4 z-50">
      <div className="bg-slate-800 rounded-lg max-w-2xl w-full max-h-[85vh] overflow-y-auto border border-slate-700">
        <div className="p-6 sticky top-0 bg-slate-800 border-b border-slate-700 flex justify-between items-center">
          <h2 className="text-2xl font-bold text-white">Plan Your Trip</h2>
          <button onClick={onClose} className="text-slate-400 hover:text-white text-2xl">✕</button>
        </div>

        <div className="p-6">
          {!response && !error ? (
            <form onSubmit={handleSubmit} className="space-y-4">
              <div>
                <label className="block text-sm font-medium text-slate-300 mb-1">From</label>
                <input
                  type="text"
                  value={formData.origin}
                  onChange={(e) => setFormData({...formData, origin: e.target.value})}
                  className="w-full px-4 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white"
                />
              </div>

              <div>
                <label className="block text-sm font-medium text-slate-300 mb-1">To</label>
                <input
                  type="text"
                  value={formData.destination}
                  onChange={(e) => setFormData({...formData, destination: e.target.value})}
                  className="w-full px-4 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white"
                />
              </div>

              <div className="grid grid-cols-2 gap-4">
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-1">Date</label>
                  <input
                    type="date"
                    value={formData.travel_date}
                    onChange={(e) => setFormData({...formData, travel_date: e.target.value})}
                    className="w-full px-4 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white"
                  />
                </div>
                <div>
                  <label className="block text-sm font-medium text-slate-300 mb-1">Budget (USD)</label>
                  <input
                    type="number"
                    value={formData.budget_usd}
                    onChange={(e) => setFormData({...formData, budget_usd: e.target.value})}
                    className="w-full px-4 py-2 bg-slate-700 border border-slate-600 rounded-lg text-white"
                  />
                </div>
              </div>

              <button
                type="submit"
                disabled={loading}
                className="w-full bg-purple-600 hover:bg-purple-700 disabled:opacity-50 text-white py-3 rounded-lg font-bold transition"
              >
                {loading ? '🔄 Planning...' : '✨ Start AI Planning'}
              </button>
            </form>
          ) : error ? (
            <div className="space-y-4">
              <h3 className="text-xl font-bold text-red-400">Error</h3>
              <div className="bg-red-900/20 border border-red-500 p-4 rounded-lg">
                <p className="text-red-300">{error}</p>
              </div>
              <button
                onClick={() => {
                  setError('');
                  setResponse('');
                }}
                className="w-full bg-slate-600 hover:bg-slate-700 text-white py-3 rounded-lg font-bold transition"
              >
                ← Back to Form
              </button>
            </div>
          ) : (
            <div className="space-y-4">
              <h3 className="text-xl font-bold text-white">AI Analysis</h3>
              <div className="bg-slate-900 p-4 rounded-lg max-h-64 overflow-y-auto border border-slate-700">
                <pre className="text-sm text-slate-300 whitespace-pre-wrap font-mono">{response}</pre>
              </div>
              <button
                onClick={onClose}
                className="w-full bg-green-600 hover:bg-green-700 text-white py-3 rounded-lg font-bold transition"
              >
                ✓ Close
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
