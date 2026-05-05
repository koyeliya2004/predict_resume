const API_BASE = (window._ENV_API_URL || "https://koyelog-resume-analyzer-api.hf.space").replace(/\/$/,"");

let currentTab = 'file';
let selectedFile = null;

// Wake up HF Space on page load (it sleeps after inactivity)
fetch(API_BASE + '/').catch(() => {});

function switchTab(tab) {
  currentTab = tab;
  document.querySelectorAll('.tab').forEach((t, i) => {
    t.classList.toggle('active', (i===0&&tab==='file')||(i===1&&tab==='text'));
  });
  document.querySelectorAll('.tab-content').forEach(c => c.classList.remove('active'));
  document.getElementById('tab-'+tab).classList.add('active');
}

const dropZone = document.getElementById('dropZone');
const fileInput = document.getElementById('fileInput');
dropZone.addEventListener('dragover', e => { e.preventDefault(); dropZone.classList.add('dragover'); });
dropZone.addEventListener('dragleave', () => dropZone.classList.remove('dragover'));
dropZone.addEventListener('drop', e => {
  e.preventDefault(); dropZone.classList.remove('dragover');
  if (e.dataTransfer.files[0]) setFile(e.dataTransfer.files[0]);
});
fileInput.addEventListener('change', () => { if (fileInput.files[0]) setFile(fileInput.files[0]); });
function setFile(f) {
  selectedFile = f;
  document.getElementById('fileName').textContent = '\u2713 ' + f.name;
}

async function fetchWithRetry(url, options, retries=2) {
  for (let i=0; i<=retries; i++) {
    try {
      const res = await fetch(url, options);
      return res;
    } catch(e) {
      if (i===retries) throw e;
      showError('Server is waking up... retrying (' + (i+1) + '/' + retries + ')');
      await new Promise(r => setTimeout(r, 4000));
    }
  }
}

async function analyzeResume() {
  hideError();
  const btn = document.querySelector('.analyze-btn');
  const spinner = document.getElementById('loadingSpinner');
  btn.disabled = true;
  btn.textContent = 'Analyzing...';
  spinner.classList.remove('hidden');
  document.getElementById('results').classList.add('hidden');
  const jdText = document.getElementById('jdInput').value.trim();

  try {
    let data;
    if (currentTab === 'file') {
      if (!selectedFile) throw new Error('Please select a resume file first.');
      const form = new FormData();
      form.append('file', selectedFile);
      if (jdText) form.append('jd_text', jdText);
      const res = await fetchWithRetry(API_BASE+'/analyze/file', {method:'POST', body:form});
      if (!res.ok) { const e=await res.json(); throw new Error(e.detail||'Analysis failed'); }
      data = await res.json();
    } else {
      const text = document.getElementById('textInput').value.trim();
      if (!text || text.length < 50) throw new Error('Please paste your full resume text (min 50 characters).');
      const res = await fetchWithRetry(API_BASE+'/analyze/text', {
        method:'POST',
        headers:{'Content-Type':'application/json'},
        body:JSON.stringify({text, jd_text: jdText||null})
      });
      if (!res.ok) { const e=await res.json(); throw new Error(e.detail||'Analysis failed'); }
      data = await res.json();
    }
    renderResults(data);
  } catch(err) {
    if (err.message.includes('fetch') || err.message.includes('network') || err.message.includes('Failed')) {
      showError('\u26a0\ufe0f Cannot reach the server. The HF Space may be sleeping — wait 30 seconds and try again.');
    } else {
      showError(err.message);
    }
  } finally {
    btn.disabled = false;
    btn.textContent = 'Analyze Resume \u2192';
    spinner.classList.add('hidden');
  }
}

function renderResults(data) {
  animateScore('resumeScore', data.resume_score);
  animateScore('atsScore', data.ats_score);
  setTimeout(() => {
    document.getElementById('resumeBar').style.width = data.resume_score+'%';
    document.getElementById('atsBar').style.width = data.ats_score+'%';
  }, 100);
  document.getElementById('predictedRole').textContent = data.predicted_role||'-';
  document.getElementById('wordCount').textContent = (data.word_count||0)+' words';

  // JD Match
  const jdCard = document.getElementById('jdMatchCard');
  if (data.jd_match && data.jd_match.jd_skills_total > 0) {
    jdCard.style.display = 'block';
    const jd = data.jd_match;
    document.getElementById('jdMatchContent').innerHTML = `
      <div class="jd-match-score">${jd.match_score}%</div>
      <div class="jd-match-sub">Matched ${jd.matched_skills.length} of ${jd.jd_skills_total} skills from the job description</div>
      ${jd.matched_skills.length ? `<div class="jd-tag-label">\u2705 Matched</div><div class="jd-tags">${jd.matched_skills.map(s=>`<span class="jd-tag-matched">${s}</span>`).join('')}</div>` : ''}
      ${jd.missing_skills.length ? `<div class="jd-tag-label">\u274c Missing</div><div class="jd-tags">${jd.missing_skills.map(s=>`<span class="jd-tag-missing">${s}</span>`).join('')}</div>` : ''}
    `;
  } else { jdCard.style.display='none'; }

  // Section Checklist
  const sections = data.section_checklist||{};
  document.getElementById('sectionChecklist').innerHTML = Object.entries(sections).map(([name,present])=>
    `<div class="check-item ${present?'yes':'no'}">${present?'\u2705':'\u274c'} ${name}</div>`
  ).join('');

  // Contact Info
  const c = data.contact||{};
  document.getElementById('contactInfo').innerHTML = `
    <div class="info-item"><strong>Name:</strong> ${data.name||'N/A'}</div>
    <div class="info-item"><strong>Email:</strong> ${c.email||'N/A'}</div>
    <div class="info-item"><strong>Phone:</strong> ${c.phone||'N/A'}</div>
    <div class="info-item"><strong>GitHub:</strong> ${c.github?`<a href="https://${c.github}" target="_blank" style="color:#a89cff">${c.github}</a>`:'N/A'}</div>
    <div class="info-item"><strong>LinkedIn:</strong> ${c.linkedin?`<a href="https://${c.linkedin}" target="_blank" style="color:#7dd3fc">${c.linkedin}</a>`:'N/A'}</div>
    <div class="info-item"><strong>Experience:</strong> ${data.experience_years?data.experience_years+' year(s)':'Not specified'}</div>
  `;

  // Skills by category
  const catColors = {'Languages':'lang','Frontend':'frontend','Backend':'backend','ML/AI':'ml','Databases':'db','DevOps/Cloud':'devops','Data Tools':'data','Tools':'tools'};
  const cats = data.skills_by_category||{};
  document.getElementById('skillsGrid').innerHTML = Object.keys(cats).length===0
    ? '<p style="color:var(--text-muted);font-size:0.88rem">No skills detected.</p>'
    : Object.entries(cats).map(([cat,skills])=>`
        <div class="skill-cat">
          <div class="skill-cat-name">${cat}</div>
          <div class="skill-tags">${skills.map(s=>`<span class="skill-tag ${catColors[cat]||'tools'}">${s}</span>`).join('')}</div>
        </div>`).join('');

  // Experience & Education
  document.getElementById('experienceInfo').innerHTML = data.experience_years>0
    ? `<span style="font-size:1.5rem;font-weight:700;color:var(--primary)">${data.experience_years}</span> year(s) detected`
    : 'Not found. Add experience duration explicitly.';
  const edu = data.education||[];
  document.getElementById('educationInfo').innerHTML = edu.length>0
    ? edu.map(e=>`<div style="color:var(--success);font-weight:600">${e}</div>`).join('')
    : 'No education keywords found.';

  // Suggestions
  const sugIcons = {skill:'\ud83d\udee0\ufe0f', content:'\ud83d\udcdd', link:'\ud83d\udd17'};
  const sugs = data.suggestions||[];
  document.getElementById('suggestionsList').innerHTML = sugs.length===0
    ? '<p style="color:var(--success);font-weight:500">\u2705 Great resume! No major improvements needed.</p>'
    : sugs.map(s=>`<div class="suggestion-item ${s.type||'content'}"><span class="suggestion-icon">${sugIcons[s.type]||'\ud83d\udca1'}</span><span>${s.msg}</span></div>`).join('');

  document.getElementById('results').classList.remove('hidden');
  document.getElementById('results').scrollIntoView({behavior:'smooth'});
}

function animateScore(id, target) {
  const el = document.getElementById(id);
  let val=0, step=Math.ceil(target/40);
  const t = setInterval(()=>{ val=Math.min(val+step,target); el.textContent=val; if(val>=target) clearInterval(t); }, 25);
}

function showError(msg) { const el=document.getElementById('errorMsg'); el.textContent=msg; el.classList.remove('hidden'); }
function hideError() { document.getElementById('errorMsg').classList.add('hidden'); }
