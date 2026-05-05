// Auto-detect: use env variable if set (for production), else localhost
const API_BASE = window._ENV_API_URL || "http://localhost:8000";

let currentTab = 'file';
let selectedFile = null;

function switchTab(tab) {
  currentTab = tab;
  document.querySelectorAll('.tab').forEach((t, i) => {
    t.classList.toggle('active', (i === 0 && tab === 'file') || (i === 1 && tab === 'text'));
  });
  document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
  document.getElementById('tab-' + tab).classList.add('active');
}

// File drag & drop
const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');

dropZone.addEventListener('dragover', e => { e.preventDefault(); dropZone.classList.add('dragover'); });
dropZone.addEventListener('dragleave', () => dropZone.classList.remove('dragover'));
dropZone.addEventListener('drop', e => {
  e.preventDefault();
  dropZone.classList.remove('dragover');
  const file = e.dataTransfer.files[0];
  if (file) setFile(file);
});

fileInput.addEventListener('change', () => {
  if (fileInput.files[0]) setFile(fileInput.files[0]);
});

function setFile(file) {
  selectedFile = file;
  document.getElementById('fileName').textContent = '✓ ' + file.name;
}

async function analyzeResume() {
  hideError();
  const btn = document.querySelector('.analyze-btn');
  const spinner = document.getElementById('loadingSpinner');
  btn.disabled = true;
  spinner.classList.remove('hidden');
  document.getElementById('results').classList.add('hidden');

  try {
    let data;
    if (currentTab === 'file') {
      if (!selectedFile) throw new Error('Please select a resume file first.');
      const form = new FormData();
      form.append('file', selectedFile);
      const res = await fetch(`${API_BASE}/analyze/file`, { method: 'POST', body: form });
      if (!res.ok) { const e = await res.json(); throw new Error(e.detail || 'Analysis failed'); }
      data = await res.json();
    } else {
      const text = document.getElementById('textInput').value.trim();
      if (!text || text.length < 50) throw new Error('Please paste your full resume text (at least 50 characters).');
      const res = await fetch(`${API_BASE}/analyze/text`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text })
      });
      if (!res.ok) { const e = await res.json(); throw new Error(e.detail || 'Analysis failed'); }
      data = await res.json();
    }
    renderResults(data);
  } catch (err) {
    showError(err.message);
  } finally {
    btn.disabled = false;
    spinner.classList.add('hidden');
  }
}

function renderResults(data) {
  animateScore('resumeScore', data.resume_score);
  animateScore('atsScore', data.ats_score);
  setTimeout(() => {
    document.getElementById('resumeBar').style.width = data.resume_score + '%';
    document.getElementById('atsBar').style.width = data.ats_score + '%';
  }, 100);
  document.getElementById('predictedRole').textContent = data.predicted_role || '-';
  document.getElementById('wordCount').textContent = (data.word_count || 0) + ' words';

  const contact = data.contact || {};
  const infoGrid = document.getElementById('contactInfo');
  infoGrid.innerHTML = `
    <div class="info-item"><strong>Name:</strong> ${data.name || 'N/A'}</div>
    <div class="info-item"><strong>Email:</strong> ${contact.email || 'N/A'}</div>
    <div class="info-item"><strong>Phone:</strong> ${contact.phone || 'N/A'}</div>
    <div class="info-item"><strong>GitHub:</strong> ${contact.github ? `<a href="https://${contact.github}" target="_blank" style="color:#a89cff">${contact.github}</a>` : 'N/A'}</div>
    <div class="info-item"><strong>LinkedIn:</strong> ${contact.linkedin ? `<a href="https://${contact.linkedin}" target="_blank" style="color:#7dd3fc">${contact.linkedin}</a>` : 'N/A'}</div>
    <div class="info-item"><strong>Experience:</strong> ${data.experience_years ? data.experience_years + ' year(s)' : 'Not specified'}</div>
  `;

  const catColors = {
    'Languages': 'lang', 'Frontend': 'frontend', 'Backend': 'backend',
    'ML/AI': 'ml', 'Databases': 'db', 'DevOps/Cloud': 'devops',
    'Data Tools': 'data', 'Tools': 'tools'
  };
  const skillsGrid = document.getElementById('skillsGrid');
  const cats = data.skills_by_category || {};
  if (Object.keys(cats).length === 0) {
    skillsGrid.innerHTML = '<p style="color:var(--text-muted);font-size:0.88rem">No recognizable tech skills found. Please include skill keywords.</p>';
  } else {
    skillsGrid.innerHTML = Object.entries(cats).map(([cat, skills]) => `
      <div class="skill-cat">
        <div class="skill-cat-name">${cat}</div>
        <div class="skill-tags">
          ${skills.map(s => `<span class="skill-tag ${catColors[cat] || 'tools'}">${s}</span>`).join('')}
        </div>
      </div>
    `).join('');
  }

  document.getElementById('experienceInfo').innerHTML =
    data.experience_years > 0
      ? `<span style="font-size:1.5rem;font-weight:700;color:var(--primary)">${data.experience_years}</span> year(s) detected`
      : 'Experience duration not found. Add it explicitly.';

  const edu = data.education || [];
  document.getElementById('educationInfo').innerHTML =
    edu.length > 0
      ? edu.map(e => `<div style="color:var(--success);font-weight:600">${e}</div>`).join('')
      : 'No degree/education keywords found.';

  const sugIcons = { skill: '🛠️', content: '📝', link: '🔗' };
  const sugs = data.suggestions || [];
  document.getElementById('suggestionsList').innerHTML =
    sugs.length === 0
      ? '<p style="color:var(--success);font-weight:500">✅ Great resume! No major improvements needed.</p>'
      : sugs.map(s => `
          <div class="suggestion-item ${s.type || 'content'}">
            <span class="suggestion-icon">${sugIcons[s.type] || '💡'}</span>
            <span>${s.msg}</span>
          </div>`).join('');

  document.getElementById('results').classList.remove('hidden');
  document.getElementById('results').scrollIntoView({ behavior: 'smooth' });
}

function animateScore(id, target) {
  const el = document.getElementById(id);
  let val = 0;
  const step = Math.ceil(target / 40);
  const timer = setInterval(() => {
    val = Math.min(val + step, target);
    el.textContent = val;
    if (val >= target) clearInterval(timer);
  }, 25);
}

function showError(msg) {
  const el = document.getElementById('errorMsg');
  el.textContent = '⚠️ ' + msg;
  el.classList.remove('hidden');
}
function hideError() {
  document.getElementById('errorMsg').classList.add('hidden');
}
