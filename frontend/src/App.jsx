import { useState } from 'react';
import axios from 'axios';
import UploadForm from './components/UploadForm';
import ResultCard from './components/ResultCard';

const API_URL = 'http://localhost:8000'; // Change to your Render URL after deployment

function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleAnalyze = async (text) => {
    setLoading(true);
    setError('');
    setResult(null);
    try {
      const res = await axios.post(`${API_URL}/analyze`, { resume_text: text });
      setResult(res.data);
    } catch (err) {
      setError('Failed to analyze resume. Make sure the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex flex-col items-center justify-center px-4 py-10">
      <div className="w-full max-w-2xl">
        <div className="text-center mb-8">
          <h1 className="text-4xl font-bold text-white mb-2">🧠 AI Resume Analyzer</h1>
          <p className="text-indigo-200 text-lg">Paste your resume and get instant AI-powered insights</p>
        </div>

        <UploadForm onAnalyze={handleAnalyze} loading={loading} />

        {error && (
          <div className="mt-4 p-4 bg-red-100 border border-red-400 text-red-700 rounded-xl">
            ⚠️ {error}
          </div>
        )}

        {result && <ResultCard result={result} />}
      </div>
    </div>
  );
}

export default App;
