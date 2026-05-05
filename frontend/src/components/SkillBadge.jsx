export default function SkillBadge({ skill }) {
  return (
    <span className="px-3 py-1 bg-indigo-100 text-indigo-700 text-xs font-semibold rounded-full border border-indigo-200">
      {skill}
    </span>
  );
}
