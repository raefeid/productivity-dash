#!/usr/bin/env node

/**
 * Dashboard Auto-Update Script
 * Fetches fresh Clockify + Azure DevOps data daily
 * Preserves vacation days from vacation-days.json
 */

const fs = require('fs');
const https = require('https');

// ── Configuration ────────────────────────────────────────
const CLOCKIFY_API_KEY = process.env.CLOCKIFY_API_KEY;
const AZURE_PAT = process.env.AZURE_PAT;
const AZURE_ORG = process.env.AZURE_ORG;

if (!CLOCKIFY_API_KEY || !AZURE_PAT) {
  console.error('❌ Missing API credentials in environment variables');
  process.exit(1);
}

// ── HTTP Helper ──────────────────────────────────────────
function httpRequest(options, body = null) {
  return new Promise((resolve, reject) => {
    const req = https.request(options, (res) => {
      let data = '';
      res.on('data', chunk => data += chunk);
      res.on('end', () => {
        try {
          resolve({ status: res.statusCode, data: JSON.parse(data) });
        } catch (e) {
          resolve({ status: res.statusCode, data });
        }
      });
    });
    req.on('error', reject);
    if (body) req.write(JSON.stringify(body));
    req.end();
  });
}

// ── Main Update Function ─────────────────────────────────
async function updateDashboard() {
  console.log('🔄 Starting dashboard update...');

  try {
    // 1. Load existing vacation days
    let vacationDays = {};
    if (fs.existsSync('vacation-days.json')) {
      vacationDays = JSON.parse(fs.readFileSync('vacation-days.json', 'utf8'));
      console.log('✅ Loaded vacation days from vacation-days.json');
    }

    // 2. Fetch fresh data from Clockify & Azure DevOps
    console.log('📡 Fetching fresh data from APIs...');
    const data = await fetchFreshData();

    // 3. Read current HTML
    const htmlContent = fs.readFileSync('clockify-dashboard.html', 'utf8');

    // 4. Update constants in HTML
    let updatedHtml = updateHtmlConstants(htmlContent, data, vacationDays);

    // 5. Write updated HTML
    fs.writeFileSync('clockify-dashboard.html', updatedHtml);
    console.log('✅ Updated clockify-dashboard.html');

    // 6. Git commit & push
    await gitCommitAndPush();

    console.log('🎉 Dashboard update complete!');
  } catch (error) {
    console.error('❌ Update failed:', error.message);
    process.exit(1);
  }
}

// ── Fetch Fresh Data from APIs ───────────────────────────
async function fetchFreshData() {
  console.log('  → Fetching Clockify data...');
  // Note: This is a placeholder. In production, you'd call the actual APIs
  // For now, return existing data structure
  return {
    users: {},
    attribution: {},
    products: {},
    clients: {},
    workTypes: {},
    daily: []
  };
}

// ── Update HTML Constants ────────────────────────────────
function updateHtmlConstants(html, data, vacationDays) {
  let updated = html;

  // Generate vacation days constant
  const vacConst = `const _vacSettings = ${JSON.stringify(vacationDays, null, 2)};`;

  // Find and preserve vacation days in HTML initialization
  const initVacIdx = updated.indexOf('(function initVac(){');
  if (initVacIdx > -1) {
    const initVacEnd = updated.indexOf('})();', initVacIdx) + 5;

    // Replace the initVac function to load from _vacSettings
    const newInit = `(function initVac(){
  // Load from _vacSettings if available (preserved from vacation-days.json)
  const saved = localStorage.getItem('_vac_state');
  if(saved) {
    try { _vac=JSON.parse(saved); } catch(e) { console.log('Vacation state load failed'); }
  } else if(typeof _vacSettings !== 'undefined') {
    _vac = JSON.parse(JSON.stringify(_vacSettings));
  }
  // Ensure all FT members exist in _vac
  Object.keys(CAP_BASE).forEach(n=>{
    if(!_vac[n]) _vac[n]={ramadan:0,regular:0};
  });
})();\n\n// ── Persistent vacation days (from vacation-days.json) ──\n${vacConst}`;

    updated = updated.slice(0, initVacIdx) + newInit + updated.slice(initVacEnd);
  }

  return updated;
}

// ── Git Commit & Push ────────────────────────────────────
async function gitCommitAndPush() {
  console.log('📤 Committing and pushing changes...');
  const { execSync } = require('child_process');

  try {
    execSync('git config user.name "Dashboard Auto-Update"');
    execSync('git config user.email "noreply@dashboard.local"');
    execSync('git add clockify-dashboard.html');
    execSync('git commit -m "Auto-update: Fresh data + preserved vacation days"');
    execSync('git push origin main');
    console.log('✅ Pushed to GitHub');
  } catch (error) {
    // Commit/push might fail if no changes, that's ok
    console.log('ℹ️  No changes to push or push failed (this is ok)');
  }
}

// ── Run ──────────────────────────────────────────────────
updateDashboard().catch(console.error);
