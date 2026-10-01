'use strict';

const API = '/api';
let allResources = [];

const chartDefaults = {
  color: 'rgba(232,234,240,0.85)',
  borderColor: 'rgba(255,255,255,0.06)',
  fontFamily: "'DM Mono', monospace",
};

Chart.defaults.color = chartDefaults.color;
Chart.defaults.font.family = chartDefaults.fontFamily;
Chart.defaults.font.size = 11;

const PROVIDER_COLORS = { AWS: '#ff9900', GCP: '#4285f4', Azure: '#0078d4' };
const TYPE_COLORS = ['#3b82f6','#34d399','#fbbf24','#f87171','#a78bfa','#38bdf8','#fb923c'];

// ── Navigation ─────────────────────────────────────────────────────────────
document.querySelectorAll('.nav-item').forEach(link => {
  link.addEventListener('click', e => {
    e.preventDefault();
    const view = link.dataset.view;
    document.querySelectorAll('.nav-item').forEach(l => l.classList.remove('active'));
    link.classList.add('active');
    document.querySelectorAll('.view').forEach(v => v.classList.remove('active'));
    document.getElementById(`view-${view}`).classList.add('active');
    document.getElementById('page-title').textContent =
      link.textContent.trim();
    if (view === 'overview') initOverview();
    if (view === 'resources') renderResources();
    if (view === 'costs') initCosts();
    if (view === 'optimise') initOptimise();
    if (view === 'patterns') initPatterns();
  });
});

// ── Bootstrap ───────────────────────────────────────────────────────────────
async function boot() {
  const data = await fetch(`${API}/resources`).then(r => r.json());
  allResources = data;
  initOverview();
}

// ── Overview ─────────────────────────────────────────────────────────────────
async function initOverview() {
  const costs = await fetch(`${API}/costs`).then(r => r.json());
  const opts = await fetch(`${API}/optimisations`).then(r => r.json());

  // Stat cards
  const statEl = document.getElementById('stat-cards');
  statEl.innerHTML = '';
  const stats = [
    { label: 'Total Monthly', value: `£${costs.total_monthly.toLocaleString()}`, sub: 'across 3 providers', cls: '' },
    { label: 'Projected Annual', value: `£${costs.projected_annual.toLocaleString()}`, sub: 'at current rate', cls: '' },
    { label: 'Resources', value: costs.resource_count, sub: 'active resources', cls: '' },
    { label: 'Potential Savings', value: `£${opts.total_potential_saving.toLocaleString()}`, sub: `${opts.count} recommendations`, cls: 'stat-value--green' },
  ];
  stats.forEach(s => {
    statEl.insertAdjacentHTML('beforeend', `
      <div class="stat-card">
        <div class="stat-label">${s.label}</div>
        <div class="stat-value ${s.cls}">${s.value}</div>
        <div class="stat-sub">${s.sub}</div>
      </div>`);
  });

  // Provider chart
  renderDoughnut('chart-provider',
    Object.keys(costs.by_provider),
    Object.values(costs.by_provider),
    Object.keys(costs.by_provider).map(k => PROVIDER_COLORS[k] || '#888'));

  // Type chart
  renderDoughnut('chart-type',
    Object.keys(costs.by_type),
    Object.values(costs.by_type),
    TYPE_COLORS);

  // Env bar chart
  renderBar('chart-env',
    Object.keys(costs.by_environment),
    Object.values(costs.by_environment));
}

function renderDoughnut(id, labels, data, colors) {
  const canvas = document.getElementById(id);
  if (canvas._chart) canvas._chart.destroy();
  canvas._chart = new Chart(canvas, {
    type: 'doughnut',
    data: {
      labels,
      datasets: [{
        data,
        backgroundColor: colors.map(c => c + 'cc'),
        borderColor: colors,
        borderWidth: 1.5,
        hoverOffset: 6,
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      cutout: '68%',
      plugins: {
        legend: { position: 'right', labels: { boxWidth: 12, padding: 14 } },
        tooltip: {
          callbacks: {
            label: ctx => ` £${ctx.parsed.toLocaleString()}`,
          },
        },
      },
    },
  });
}

function renderBar(id, labels, data) {
  const canvas = document.getElementById(id);
  if (canvas._chart) canvas._chart.destroy();
  canvas._chart = new Chart(canvas, {
    type: 'bar',
    data: {
      labels,
      datasets: [{
        data,
        backgroundColor: ['rgba(59,130,246,0.7)','rgba(251,191,36,0.7)','rgba(52,211,153,0.7)'],
        borderRadius: 6,
        borderSkipped: false,
      }],
    },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      indexAxis: 'y',
      plugins: { legend: { display: false } },
      scales: {
        x: {
          grid: { color: 'rgba(255,255,255,0.04)' },
          ticks: { callback: v => `£${v.toLocaleString()}` },
        },
        y: { grid: { display: false } },
      },
    },
  });
}

// ── Resources ─────────────────────────────────────────────────────────────────
function renderResources() {
  const tbody = document.getElementById('resource-rows');
  const provider = document.getElementById('filter-provider').value;
  const type = document.getElementById('filter-type').value;
  const env = document.getElementById('filter-env').value;

  const filtered = allResources.filter(r =>
    (!provider || r.provider === provider) &&
    (!type || r.resource_type === type) &&
    (!env || r.tags.env === env));

  tbody.innerHTML = filtered.map(r => {
    const util = r.utilisation_pct;
    const fillColor = util >= 60 ? '#34d399' : util >= 20 ? '#fbbf24' : '#f87171';
    const eff = r.cost_efficiency_score;
    const effClass = eff >= 60 ? 'eff--high' : eff >= 30 ? 'eff--med' : 'eff--low';
    return `
      <tr>
        <td><span class="resource-name">${r.name}</span></td>
        <td><span class="provider-pill provider-pill--${r.provider}">${r.provider}</span></td>
        <td style="color:var(--text2);font-size:.78rem">${r.resource_type}</td>
        <td style="color:var(--text3);font-family:var(--mono);font-size:.75rem">${r.region}</td>
        <td>
          <div class="util-bar-wrap">
            <div class="util-bar"><div class="util-fill" style="width:${util}%;background:${fillColor}"></div></div>
            <span class="util-label">${util}%</span>
          </div>
        </td>
        <td><span class="cost-mono">£${r.monthly_cost.toLocaleString()}</span></td>
        <td><span class="eff-score ${effClass}">${eff}</span></td>
      </tr>`;
  }).join('');
}

document.querySelectorAll('.filter-select').forEach(s =>
  s.addEventListener('change', renderResources));

// ── Costs ─────────────────────────────────────────────────────────────────────
async function initCosts() {
  const costs = await fetch(`${API}/costs`).then(r => r.json());
  const el = document.getElementById('cost-stat-cards');
  el.innerHTML = '';
  Object.entries(costs.by_provider).forEach(([k, v]) => {
    el.insertAdjacentHTML('beforeend', `
      <div class="stat-card">
        <div class="stat-label">${k}</div>
        <div class="stat-value" style="color:${PROVIDER_COLORS[k]||'var(--text)'}">£${v.toLocaleString()}</div>
        <div class="stat-sub">£${(v * 12).toLocaleString()} annual</div>
      </div>`);
  });

  // Forecast line chart (simple projection)
  const canvas = document.getElementById('chart-forecast');
  if (canvas._chart) canvas._chart.destroy();
  const months = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec'];
  const datasets = Object.entries(costs.by_provider).map(([prov, monthly]) => ({
    label: prov,
    data: months.map((_, i) => Math.round(monthly * (1 + i * 0.015))),
    borderColor: PROVIDER_COLORS[prov],
    backgroundColor: (PROVIDER_COLORS[prov] || '#888') + '18',
    fill: true,
    tension: 0.4,
    pointRadius: 3,
  }));

  canvas._chart = new Chart(canvas, {
    type: 'line',
    data: { labels: months, datasets },
    options: {
      responsive: true,
      maintainAspectRatio: false,
      plugins: { legend: { position: 'top' } },
      scales: {
        y: {
          grid: { color: 'rgba(255,255,255,0.04)' },
          ticks: { callback: v => `£${v.toLocaleString()}` },
        },
        x: { grid: { color: 'rgba(255,255,255,0.04)' } },
      },
    },
  });
}

// ── Optimise ─────────────────────────────────────────────────────────────────
async function initOptimise() {
  const data = await fetch(`${API}/optimisations`).then(r => r.json());
  const el = document.getElementById('opt-stat-cards');
  el.innerHTML = `
    <div class="stat-card">
      <div class="stat-label">Recommendations</div>
      <div class="stat-value">${data.count}</div>
      <div class="stat-sub">actionable items</div>
    </div>
    <div class="stat-card">
      <div class="stat-label">Monthly Saving</div>
      <div class="stat-value stat-value--green">£${data.total_potential_saving.toLocaleString()}</div>
      <div class="stat-sub">if all applied</div>
    </div>
    <div class="stat-card">
      <div class="stat-label">Annual Saving</div>
      <div class="stat-value stat-value--green">£${(data.total_potential_saving * 12).toLocaleString()}</div>
      <div class="stat-sub">projected</div>
    </div>`;

  const listEl = document.getElementById('opt-list');
  listEl.innerHTML = data.recommendations.map(r => `
    <div class="opt-item">
      <div style="flex:1">
        <div style="display:flex;align-items:center;gap:10px;margin-bottom:.6rem">
          <span class="opt-severity sev--${r.severity}">${r.severity}</span>
          <span style="font-family:var(--mono);font-size:.72rem;color:var(--text3)">${r.resource_name}</span>
        </div>
        <div class="opt-title">${r.title}</div>
        <div class="opt-desc">${r.description}</div>
        <div class="opt-action">→ ${r.action}</div>
      </div>
      <div class="opt-saving">
        <div class="opt-saving-val">£${r.estimated_monthly_saving}</div>
        <div class="opt-saving-label">saved/mo</div>
      </div>
    </div>`).join('');
}

// ── Patterns ─────────────────────────────────────────────────────────────────
async function initPatterns() {
  const data = await fetch(`${API}/patterns`).then(r => r.json());
  const grid = document.getElementById('patterns-grid');
  grid.innerHTML = data.map(p => `
    <div class="pattern-card">
      <div class="pattern-header">
        <div class="pattern-name">${p.name}</div>
        <span class="pattern-provider provider-pill provider-pill--${p.provider}">${p.provider}</span>
      </div>
      <div class="pattern-desc">${p.description}</div>
      <div class="use-case-tags">${p.use_cases.map(u => `<span class="use-case-tag">${u}</span>`).join('')}</div>
      <div class="pattern-components">${p.components.map(c =>
        `<span class="component-chip">${c.icon} ${c.name}</span>`).join('')}</div>
      <div class="pattern-meta">
        <div>SLA <span>${p.reliability_tier}</span></div>
        <div>From <span>£${p.estimated_monthly_cost}/mo</span></div>
      </div>
    </div>`).join('');
}

boot();
