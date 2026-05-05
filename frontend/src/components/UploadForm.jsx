import { useState } from 'react';

export default function UploadForm({ onAnalyze, loading }) {
  const [text, setText] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    if (text.trim()) onAnalyze(text);
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white rounded-2xl shadow-2xl p-6">
      <label className="block text-gray-700 font-semibold mb-2 text-lg">📋 Paste Your Resume</label>
      <textarea
        className="w-full h-52 p-4 border border-gray-200 rounded-xl resize-none text-sm text-gray-700 focus:outline-none focus:ring-2 focus:ring-indigo-400"
        placeholder="Paste your resume text here... (name, skills, experience, education)"
        value={text}
        onChange={(e) => setText(e.target.value)}
      />
      <button
        type="submit"
        disabled={loading || !text.trim()}
        className="mt-4 w-full bg-indigo-500 hover:bg-indigo-600 text-white font-bold py-3 rounded-xl transition disabled:opacity-50 disabled:cursor-not-allowed"
      >
        {loading ? '🔍 Analyzing...' : '🚀 Analyze Resume'}
      </button>
    </form>
  );
}
