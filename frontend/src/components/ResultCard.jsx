import SkillBadge from './SkillBadge';

export default function ResultCard({ result }) {
  return (
    <div className="mt-6 bg-white rounded-2xl shadow-2xl p-6 space-y-5">
      <h2 className="text-2xl font-bold text-gray-800">📊 Analysis Result</h2>

      <div className="grid grid-cols-2 gap-4">
        <InfoBox label="👤 Name" value={result.name} />
        <InfoBox label="🏷️ Predicted Role" value={result.predicted_role} highlight />
        <InfoBox label="📅 Experience" value={`${result.experience_years} year(s)`} />
      </div>

      <div>
        <h3 className="text-lg font-semibold text-gray-700 mb-2">🛠️ Detected Skills</h3>
        <div className="flex flex-wrap gap-2">
          {result.skills.length > 0
            ? result.skills.map((skill) => <SkillBadge key={skill} skill={skill} />)
            : <span className="text-gray-400">No skills detected</span>}
        </div>
      </div>

      {result.suggestions.length > 0 && (
        <div>
          <h3 className="text-lg font-semibold text-gray-700 mb-2">💡 Suggestions</h3>
          <ul className="space-y-1">
            {result.suggestions.map((s, i) => (
              <li key={i} className="flex items-start gap-2 text-gray-600 text-sm">
                <span className="text-yellow-500">→</span> {s}
              </li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

function InfoBox({ label, value, highlight }) {
  return (
    <div className={`p-3 rounded-xl border ${highlight ? 'bg-indigo-50 border-indigo-200' : 'bg-gray-50 border-gray-200'}`}>
      <p className="text-xs text-gray-500 mb-1">{label}</p>
      <p className={`font-bold text-sm ${highlight ? 'text-indigo-600' : 'text-gray-800'}`}>{value}</p>
    </div>
  );
}
