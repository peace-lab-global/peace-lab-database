const DATA_URL = '../data/content_index.json';
const FILE_BASE = '../../';
const PAGE_SIZE = 60;
const PROTECTED_EXTENSIONS = new Set(['.json', '.py', '.html', '.css', '.js', '.ts', '.yml', '.yaml']);
const ROLE_LABELS = {
  index: '导航索引',
  readme: '说明文档',
  overview: '概览文档',
  framework: '方法框架',
  guide: '指南手册',
  template: '模板清单',
  system_design: '系统设计',
  taxonomy: '分类体系',
  case_library: '案例资料',
  tool: '工具脚本',
  web_asset: '前端资产',
  data: '结构化数据',
  content: '正文内容',
};

const state = {
  data: null,
  query: '',
  perspective: 'standard',
  pillar: 'all',
  ext: 'all',
  role: 'all',
  depth: 'all',
  sort: 'relevance',
  view: 'cards',
  mode: 'standard',
  visibleCount: PAGE_SIZE,
  filtered: [],
  selectedPath: null,
  previewTab: 'rendered',
  contentCache: new Map(),
};

const perspectives = [
  {
    id: 'standard',
    title: '标准浏览',
    description: '默认模式，平衡检索、筛选与阅读体验',
    predicate: () => true,
  },
  {
    id: 'navigation',
    title: '脉络入口',
    description: '从 INDEX / README / Overview 等入口顺流而下',
    predicate: (entry) => entry.signals.navigation,
  },
  {
    id: 'structured',
    title: '结构档案',
    description: '查看 JSON、taxonomy、数据快照与结构化资料',
    predicate: (entry) => entry.signals.structured,
  },
  {
    id: 'methodology',
    title: '方法手札',
    description: '聚焦 framework / guide / system design 等方法内容',
    predicate: (entry) => entry.signals.methodology,
  },
  {
    id: 'tooling',
    title: '工具侧写',
    description: '查看页面资产、脚本与治理资料',
    predicate: (entry) => entry.signals.tooling,
  },
  {
    id: 'recent',
    title: '最近落笔',
    description: '沿时间线查看最近新增与演进内容',
    predicate: () => true,
    forceSort: 'recent',
  },
];

const modePresets = [
  {
    id: 'standard',
    title: '标准浏览',
    description: '以卡片流与相关度排序，温和进入整个文档库。',
    note: '适合首次进入或希望自由浏览全库时使用。',
    perspective: 'standard',
    view: 'cards',
    sort: 'relevance',
  },
  {
    id: 'atlas',
    title: '目录漫游',
    description: '按目录与导航脉络展开，适合建立整体感。',
    note: '更适合顺着知识结构前进，而非只靠关键词检索。',
    perspective: 'navigation',
    view: 'pillar',
    sort: 'title',
  },
  {
    id: 'themes',
    title: '主题深读',
    description: '从方法、角色与语义聚类中寻找相近文档。',
    note: '适合围绕某个问题做连续阅读与对比。',
    perspective: 'methodology',
    view: 'role',
    sort: 'relevance',
  },
  {
    id: 'recent',
    title: '新近回声',
    description: '优先查看最近更新，快速把握新增内容。',
    note: '适合跟踪近期补充、修订与新建文档。',
    perspective: 'recent',
    view: 'cards',
    sort: 'recent',
  },
];

const el = {
  dataStatus: document.getElementById('dataStatus'),
  overviewGrid: document.getElementById('overviewGrid'),
  focusNote: document.getElementById('focusNote'),
  modeGuide: document.getElementById('modeGuide'),
  searchInput: document.getElementById('searchInput'),
  sortMode: document.getElementById('sortMode'),
  viewMode: document.getElementById('viewMode'),
  pillarFilter: document.getElementById('pillarFilter'),
  extFilter: document.getElementById('extFilter'),
  roleFilter: document.getElementById('roleFilter'),
  depthFilter: document.getElementById('depthFilter'),
  perspectiveStrip: document.getElementById('perspectiveStrip'),
  clearFilters: document.getElementById('clearFilters'),
  resultsMeta: document.getElementById('resultsMeta'),
  groupSummary: document.getElementById('groupSummary'),
  resultsContainer: document.getElementById('resultsContainer'),
  loadMoreBtn: document.getElementById('loadMoreBtn'),
  previewEmpty: document.getElementById('previewEmpty'),
  previewContent: document.getElementById('previewContent'),
  previewKicker: document.getElementById('previewKicker'),
  previewTitle: document.getElementById('previewTitle'),
  previewPath: document.getElementById('previewPath'),
  openFileLink: document.getElementById('openFileLink'),
  copyPathBtn: document.getElementById('copyPathBtn'),
  previewMetrics: document.getElementById('previewMetrics'),
  previewBody: document.getElementById('previewBody'),
  directoryHeatmap: document.getElementById('directoryHeatmap'),
  recentList: document.getElementById('recentList'),
  dataToolList: document.getElementById('dataToolList'),
};

const nf = new Intl.NumberFormat('zh-CN');
const df = new Intl.DateTimeFormat('zh-CN', {
  year: 'numeric',
  month: '2-digit',
  day: '2-digit',
  hour: '2-digit',
  minute: '2-digit',
});

function escapeHtml(value = '') {
  return value
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/'/g, '&#39;');
}

function debounce(fn, wait = 160) {
  let timer = null;
  return (...args) => {
    window.clearTimeout(timer);
    timer = window.setTimeout(() => fn(...args), wait);
  };
}

function formatCount(value) {
  return nf.format(value || 0);
}

function formatBytes(bytes) {
  if (!bytes) return '0 B';
  const units = ['B', 'KB', 'MB', 'GB'];
  let current = bytes;
  let unitIndex = 0;
  while (current >= 1024 && unitIndex < units.length - 1) {
    current /= 1024;
    unitIndex += 1;
  }
  return `${current.toFixed(current >= 10 || unitIndex === 0 ? 0 : 1)} ${units[unitIndex]}`;
}

function formatDate(value) {
  if (!value) return '未知';
  return df.format(new Date(value));
}

function buildFileUrl(path) {
  return new URL(`${FILE_BASE}${path}`, window.location.href).toString();
}

function roleLabel(role) {
  return ROLE_LABELS[role] || role;
}

function isProtectedEntry(entry) {
  return Boolean(entry && (entry.preview_policy === 'metadata_only' || PROTECTED_EXTENSIONS.has(entry.ext)));
}

function syncPreviewTabs(entry) {
  const protectedEntry = isProtectedEntry(entry);
  document.querySelectorAll('.tab-button').forEach((button) => {
    const isRawTab = button.dataset.tab === 'raw';
    button.hidden = protectedEntry && isRawTab;
    if (protectedEntry && isRawTab) {
      button.classList.remove('active');
    }
  });

  if (protectedEntry && state.previewTab === 'raw') {
    state.previewTab = 'rendered';
  }

  document.querySelectorAll('.tab-button').forEach((button) => {
    button.classList.toggle('active', button.dataset.tab === state.previewTab);
  });
}

function renderProtectedPreview(entry) {
  return `
    <div class="content-pane secure-preview">
      <span class="summary-chip">安全预览模式</span>
      <h3>该文件类型已启用源码保护</h3>
      <p>${escapeHtml(entry.excerpt || '该资产仅展示安全摘要与元数据。')}</p>
      <ul>
        <li>卡片列表不再展示源码首行或原始配置片段。</li>
        <li>预览区默认隐藏 HTML / CSS / JavaScript / Python / JSON / YAML 原文。</li>
        <li>如需继续研判，请切换到“元数据”查看路径、角色、标签、更新时间等非敏感信息。</li>
      </ul>
    </div>
  `;
}

function normalizeText(entry) {
  return [
    entry.title,
    entry.path,
    entry.excerpt,
    entry.top_dir_label,
    entry.primary_role,
    ...(entry.tags || []),
    ...((entry.outline || []).map((item) => item.text)),
  ]
    .join(' ')
    .toLowerCase();
}

function scoreEntry(entry, query) {
  if (!query) return 0;
  let score = 0;
  if (entry.titleLower.includes(query)) score += 9;
  if (entry.pathLower.includes(query)) score += 6;
  if (entry.excerptLower.includes(query)) score += 4;
  if (entry.searchIndex.includes(query)) score += 2;
  return score;
}

function matchesDepth(entry) {
  if (state.depth === 'all') return true;
  if (state.depth === '0') return entry.depth <= 1;
  if (state.depth === '2') return entry.depth >= 2 && entry.depth <= 3;
  if (state.depth === '4') return entry.depth >= 4;
  return true;
}

function getActivePerspective() {
  return perspectives.find((item) => item.id === state.perspective) || perspectives[0];
}

function filterEntries() {
  const query = state.query.trim().toLowerCase();
  const perspective = getActivePerspective();
  const filtered = state.data.files
    .filter((entry) => perspective.predicate(entry))
    .filter((entry) => (state.pillar === 'all' ? true : entry.top_dir === state.pillar))
    .filter((entry) => (state.ext === 'all' ? true : entry.ext === state.ext))
    .filter((entry) => (state.role === 'all' ? true : entry.primary_role === state.role))
    .filter(matchesDepth)
    .filter((entry) => (query ? entry.searchIndex.includes(query) : true))
    .map((entry) => ({ ...entry, relevance: scoreEntry(entry, query) }));

  const sortMode = perspective.forceSort || state.sort;
  const sorters = {
    relevance: (a, b) => (b.relevance - a.relevance) || (b.modified_ts - a.modified_ts),
    recent: (a, b) => b.modified_ts - a.modified_ts,
    title: (a, b) => a.title.localeCompare(b.title, 'zh-CN'),
    size: (a, b) => b.size - a.size,
    reading: (a, b) => b.reading_minutes - a.reading_minutes,
  };

  filtered.sort(sorters[sortMode] || sorters.relevance);
  state.filtered = filtered;

  if (!filtered.some((entry) => entry.path === state.selectedPath)) {
    state.selectedPath = filtered[0]?.path || null;
  }
}

function renderOverview() {
  const stats = state.data.stats;
  const latestWordCount = stats.latest_word_count?.stats || {};
  const cards = [
    {
      label: '索引文件',
      value: formatCount(stats.total_files),
      hint: '全库可直接浏览的文本文件总量',
    },
    {
      label: '目录节点',
      value: formatCount(stats.total_directories),
      hint: '已进入索引的内容目录数量',
    },
    {
      label: '一级支柱',
      value: formatCount(state.data.pillars.length),
      hint: '按顶层域聚合的知识分区',
    },
    {
      label: '总行数',
      value: formatCount(stats.total_lines),
      hint: '当前索引覆盖的文本总行数',
    },
    {
      label: '累计字符',
      value: formatCount(latestWordCount.total_chars || stats.total_chars),
      hint: '优先展示最新统计快照',
    },
    {
      label: '结构化数据',
      value: formatCount((stats.by_ext['.json'] || 0) + (stats.by_ext['.yml'] || 0) + (stats.by_ext['.yaml'] || 0)),
      hint: 'JSON / YAML 等结构化资产数量',
    },
  ];

  el.overviewGrid.innerHTML = cards
    .map(
      (card) => `
        <article class="metric-card">
          <small>${escapeHtml(card.label)}</small>
          <strong>${card.value}</strong>
          <span>${escapeHtml(card.hint)}</span>
        </article>
      `,
    )
    .join('');
}

function renderPerspectiveStrip() {
  el.perspectiveStrip.innerHTML = perspectives
    .map((item) => `
      <button class="perspective-pill ${item.id === state.perspective ? 'active' : ''}" data-perspective="${item.id}" type="button">
        <strong>${escapeHtml(item.title)}</strong>
        <span>${escapeHtml(item.description)}</span>
      </button>
    `)
    .join('');
}

function viewLabel(view) {
  return {
    cards: '卡片流',
    pillar: '按支柱分组',
    role: '按角色分组',
    directory: '按目录分组',
  }[view] || view;
}

function syncModeFromState() {
  const matched = modePresets.find((item) => item.perspective === state.perspective && item.view === state.view && item.sort === state.sort);
  state.mode = matched?.id || 'standard';
}

function renderModeGuide() {
  el.modeGuide.innerHTML = modePresets
    .map((item) => `
      <button class="mode-card ${item.id === state.mode ? 'active' : ''}" data-mode-preset="${item.id}" type="button">
        <span class="section-kicker">${escapeHtml(item.title)}</span>
        <strong>${escapeHtml(item.description)}</strong>
        <p>${escapeHtml(item.note)}</p>
      </button>
    `)
    .join('');
}

function renderFocusNote() {
  const perspective = getActivePerspective();
  const preset = modePresets.find((item) => item.id === state.mode) || modePresets[0];
  el.focusNote.innerHTML = `
    <span class="section-kicker">Current Flow</span>
    <strong>${escapeHtml(preset.title)}</strong>
    <p>${escapeHtml(preset.note)}</p>
    <small>当前视角：${escapeHtml(perspective.title)} · 当前查看方式：${escapeHtml(viewLabel(state.view))}</small>
  `;
}

function applyModePreset(modeId) {
  const preset = modePresets.find((item) => item.id === modeId);
  if (!preset) return;
  state.mode = preset.id;
  state.perspective = preset.perspective;
  state.view = preset.view;
  state.sort = preset.sort;
  state.visibleCount = PAGE_SIZE;
  el.viewMode.value = state.view;
  el.sortMode.value = state.sort;
  updateView();
}

function populateSelect(target, items, allLabel) {
  const current = target.value;
  target.innerHTML = [`<option value="all">${allLabel}</option>`]
    .concat(items.map((item) => `<option value="${escapeHtml(item.value)}">${escapeHtml(item.label)}</option>`))
    .join('');
  target.value = items.some((item) => item.value === current) ? current : 'all';
}

function renderFilters() {
  const topDirs = Object.keys(state.data.stats.by_top_dir).map((key) => ({
    value: key,
    label: state.data.pillars.find((item) => item.key === key)?.label || key,
  }));
  const exts = Object.keys(state.data.stats.by_ext).map((key) => ({ value: key, label: `${key} · ${formatCount(state.data.stats.by_ext[key])}` }));
  const roles = Object.keys(state.data.stats.by_role).map((key) => ({ value: key, label: `${roleLabel(key)} · ${formatCount(state.data.stats.by_role[key])}` }));

  populateSelect(el.pillarFilter, topDirs, '全部目录');
  populateSelect(el.extFilter, exts, '全部类型');
  populateSelect(el.roleFilter, roles, '全部角色');
}

function buildSummaryChips() {
  const chips = [];
  const activePerspective = getActivePerspective();
  chips.push(`模式：${activePerspective.title}`);
  if (state.query) chips.push(`关键词：${state.query}`);
  if (state.pillar !== 'all') chips.push(`目录：${state.pillar}`);
  if (state.ext !== 'all') chips.push(`类型：${state.ext}`);
  if (state.role !== 'all') chips.push(`角色：${roleLabel(state.role)}`);
  if (state.depth !== 'all') chips.push(`层级：${state.depth}`);
  if (!chips.length) return '';
  return chips.map((item) => `<span class="summary-chip">${escapeHtml(item)}</span>`).join('');
}

function buildMetaBadges(entry) {
  const badges = [
    `<span class="badge accent">${escapeHtml(entry.top_dir)}</span>`,
    `<span class="badge">${escapeHtml(entry.ext)}</span>`,
    `<span class="badge">${escapeHtml(roleLabel(entry.primary_role))}</span>`,
    `<span class="badge">${formatCount(entry.lines)} 行</span>`,
    `<span class="badge">${entry.reading_minutes} 分钟</span>`,
  ];

  if (isProtectedEntry(entry)) {
    badges.splice(3, 0, '<span class="badge warning">安全预览</span>');
  }

  return badges.join('');
}

function renderCard(entry) {
  const tags = (entry.tags || []).slice(0, 6)
    .map((tag) => `<span class="badge">${escapeHtml(tag)}</span>`)
    .join('');

  return `
    <article class="result-card ${entry.path === state.selectedPath ? 'active' : ''}" data-path="${escapeHtml(entry.path)}">
      <div class="card-topline">
        <span class="section-kicker">${escapeHtml(entry.top_dir_label)}</span>
        <span class="summary-chip">${formatDate(entry.modified_at)}</span>
      </div>
      <div class="card-title">
        <h3>${escapeHtml(entry.title)}</h3>
        <div class="card-path">${escapeHtml(entry.path)}</div>
      </div>
      <p>${escapeHtml(entry.excerpt || '暂无摘要')}</p>
      <div class="card-meta">${buildMetaBadges(entry)}</div>
      <div class="card-tags">${tags}</div>
    </article>
  `;
}

function renderGrouped(entries, keyGetter, labelGetter) {
  const groups = new Map();
  entries.forEach((entry) => {
    const key = keyGetter(entry);
    if (!groups.has(key)) groups.set(key, []);
    groups.get(key).push(entry);
  });

  return Array.from(groups.entries())
    .map(([key, items]) => `
      <section class="group-block">
        <div class="group-head">
          <div>
            <span class="section-kicker">${escapeHtml(labelGetter(key))}</span>
            <h3>${escapeHtml(key)}</h3>
          </div>
          <p>${formatCount(items.length)} 项</p>
        </div>
        <div class="group-items">
          ${items.map(renderCard).join('')}
        </div>
      </section>
    `)
    .join('');
}

function renderResults() {
  const visibleEntries = state.filtered.slice(0, state.visibleCount);
  el.resultsMeta.textContent = `命中 ${formatCount(state.filtered.length)} 项，当前展示 ${formatCount(visibleEntries.length)} 项`;
  el.groupSummary.innerHTML = buildSummaryChips(visibleEntries);

  if (!visibleEntries.length) {
    el.resultsContainer.innerHTML = '<div class="group-block"><h3>没有匹配结果</h3><p>请尝试切换视角、清空筛选或更换关键词。</p></div>';
    el.loadMoreBtn.classList.add('hidden');
    renderPreview();
    return;
  }

  if (state.view === 'cards') {
    el.resultsContainer.innerHTML = visibleEntries.map(renderCard).join('');
  } else if (state.view === 'pillar') {
    el.resultsContainer.innerHTML = renderGrouped(visibleEntries, (entry) => entry.top_dir, (key) => state.data.pillars.find((item) => item.key === key)?.label || key);
  } else if (state.view === 'role') {
    el.resultsContainer.innerHTML = renderGrouped(visibleEntries, (entry) => entry.primary_role, (key) => `Role · ${roleLabel(key)}`);
  } else {
    el.resultsContainer.innerHTML = renderGrouped(visibleEntries, (entry) => entry.directory, (key) => `Directory · ${key}`);
  }

  if (state.filtered.length > state.visibleCount) {
    el.loadMoreBtn.classList.remove('hidden');
  } else {
    el.loadMoreBtn.classList.add('hidden');
  }

  renderPreview();
}

function renderHeatmap() {
  const list = state.data.directories
    .filter((item) => item.path !== '.')
    .slice(0, 10);
  const max = Math.max(...list.map((item) => item.file_count), 1);

  el.directoryHeatmap.innerHTML = list
    .map(
      (item) => `
        <div class="bar-item" data-filter-directory="${escapeHtml(item.path)}">
          <div class="bar-head">
            <strong>${escapeHtml(item.path)}</strong>
            <span>${formatCount(item.file_count)} 文件</span>
          </div>
          <div class="bar-track"><div class="bar-fill" style="width:${(item.file_count / max) * 100}%"></div></div>
          <div class="bar-foot">
            <span>${formatBytes(item.total_bytes)}</span>
            <span>${formatDate(item.latest_modified_ts * 1000)}</span>
          </div>
        </div>
      `,
    )
    .join('');
}

function renderMiniList(target, entries, titleKey = 'title') {
  target.innerHTML = entries
    .map(
      (entry) => `
        <button class="mini-item" data-path="${escapeHtml(entry.path)}" type="button">
          <h4>${escapeHtml(entry[titleKey])}</h4>
          <p>${escapeHtml(entry.path)}</p>
        </button>
      `,
    )
    .join('');
}

async function loadFileContent(entry) {
  if (state.contentCache.has(entry.path)) return state.contentCache.get(entry.path);
  const response = await fetch(buildFileUrl(entry.path));
  if (!response.ok) throw new Error(`无法读取 ${entry.path}`);
  const content = await response.text();
  state.contentCache.set(entry.path, content);
  return content;
}

function renderInlineMarkdown(text) {
  return escapeHtml(text)
    .replace(/`([^`]+)`/g, '<code>$1</code>')
    .replace(/\*\*([^*]+)\*\*/g, '<strong>$1</strong>')
    .replace(/\[([^\]]+)\]\(([^)]+)\)/g, (_, label, url) => `<a href="${escapeHtml(url)}" target="_blank" rel="noreferrer">${escapeHtml(label)}</a>`);
}

function renderMarkdown(content) {
  const lines = content.split(/\r?\n/);
  let html = '';
  let paragraph = [];
  let listType = null;
  let inCode = false;

  const flushParagraph = () => {
    if (!paragraph.length) return;
    html += `<p>${renderInlineMarkdown(paragraph.join(' '))}</p>`;
    paragraph = [];
  };

  const closeList = () => {
    if (!listType) return;
    html += listType === 'ul' ? '</ul>' : '</ol>';
    listType = null;
  };

  lines.forEach((line) => {
    const codeFence = line.match(/^```(.*)$/);
    if (codeFence) {
      flushParagraph();
      closeList();
      if (!inCode) {
        inCode = true;
        html += `<pre><code data-lang="${escapeHtml(codeFence[1].trim())}">`;
      } else {
        inCode = false;
        html += '</code></pre>';
      }
      return;
    }

    if (inCode) {
      html += `${escapeHtml(line)}\n`;
      return;
    }

    const heading = line.match(/^(#{1,6})\s+(.+)$/);
    if (heading) {
      flushParagraph();
      closeList();
      const level = heading[1].length;
      html += `<h${level}>${renderInlineMarkdown(heading[2].trim())}</h${level}>`;
      return;
    }

    const bullet = line.match(/^[-*]\s+(.+)$/);
    const numbered = line.match(/^\d+\.\s+(.+)$/);
    if (bullet || numbered) {
      flushParagraph();
      const nextType = bullet ? 'ul' : 'ol';
      if (listType !== nextType) {
        closeList();
        listType = nextType;
        html += nextType === 'ul' ? '<ul>' : '<ol>';
      }
      html += `<li>${renderInlineMarkdown((bullet || numbered)[1].trim())}</li>`;
      return;
    }

    const quote = line.match(/^>\s?(.*)$/);
    if (quote) {
      flushParagraph();
      closeList();
      html += `<blockquote>${renderInlineMarkdown(quote[1])}</blockquote>`;
      return;
    }

    if (!line.trim()) {
      flushParagraph();
      closeList();
      return;
    }

    paragraph.push(line.trim());
  });

  flushParagraph();
  closeList();
  return `<div class="content-pane">${html || '<p>暂无可渲染内容。</p>'}</div>`;
}

function renderRaw(content) {
  return `<div class="raw-pane"><pre>${escapeHtml(content)}</pre></div>`;
}

function renderMeta(entry) {
  const rows = [
    ['标题', entry.title],
    ['路径', entry.path],
    ['一级目录', entry.top_dir_label],
    ['目录', entry.directory],
    ['角色', entry.roles.map(roleLabel).join(' · ')],
    ['类型', entry.ext],
    ['预览策略', isProtectedEntry(entry) ? '仅安全摘要与元数据' : '允许正文与原始内容预览'],
    ['大小', formatBytes(entry.size)],
    ['行数', `${formatCount(entry.lines)} 行`],
    ['阅读时长', `${entry.reading_minutes} 分钟`],
    ['最近更新', formatDate(entry.modified_at)],
    ['标签', (entry.tags || []).join(' · ') || '—'],
    ['章节', (entry.outline || []).map((item) => `${'H'.repeat(item.level)} ${item.text}`).join(' / ') || '—'],
  ];

  return `
    <div class="meta-pane">
      <div class="meta-grid">
        ${rows
          .map(
            ([label, value]) => `
              <div class="meta-row">
                <strong>${escapeHtml(label)}</strong>
                <span>${escapeHtml(String(value || '—'))}</span>
              </div>
            `,
          )
          .join('')}
      </div>
    </div>
  `;
}

async function renderPreview() {
  const entry = state.filtered.find((item) => item.path === state.selectedPath);
  if (!entry) {
    el.previewEmpty.hidden = false;
    el.previewContent.hidden = true;
    return;
  }

  const protectedEntry = isProtectedEntry(entry);

  el.previewEmpty.hidden = true;
  el.previewContent.hidden = false;
  el.previewKicker.textContent = entry.top_dir_label;
  el.previewTitle.textContent = entry.title;
  el.previewPath.textContent = entry.path;
  el.openFileLink.hidden = protectedEntry;
  if (!protectedEntry) {
    el.openFileLink.href = buildFileUrl(entry.path);
  } else {
    el.openFileLink.removeAttribute('href');
  }
  el.previewMetrics.innerHTML = buildMetaBadges(entry);
  syncPreviewTabs(entry);

  if (state.previewTab === 'meta') {
    el.previewBody.innerHTML = renderMeta(entry);
    return;
  }

  if (protectedEntry) {
    el.previewBody.innerHTML = renderProtectedPreview(entry);
    return;
  }

  el.previewBody.innerHTML = '<div class="content-pane"><p>正在读取原始文件内容…</p></div>';

  try {
    const content = await loadFileContent(entry);
    if (entry.path !== state.selectedPath) return;

    if (state.previewTab === 'raw') {
      el.previewBody.innerHTML = renderRaw(content);
      return;
    }

    if (entry.ext === '.md') {
      el.previewBody.innerHTML = renderMarkdown(content);
    } else {
      el.previewBody.innerHTML = renderRaw(content);
    }
  } catch (error) {
    el.previewBody.innerHTML = `<div class="content-pane"><p>${escapeHtml(error.message)}</p><p>请确认当前页面通过仓库根目录的静态服务访问。</p></div>`;
  }
}

function updateView() {
  syncModeFromState();
  filterEntries();
  renderModeGuide();
  renderFocusNote();
  renderPerspectiveStrip();
  renderResults();
}

function selectEntry(path) {
  state.selectedPath = path;
  window.history.replaceState(null, '', `#${encodeURIComponent(path)}`);
  document.querySelectorAll('.result-card').forEach((card) => {
    card.classList.toggle('active', card.dataset.path === path);
  });
  renderPreview();
}

function bindEvents() {
  el.searchInput.addEventListener('input', debounce((event) => {
    state.query = event.target.value;
    state.visibleCount = PAGE_SIZE;
    updateView();
  }));

  el.sortMode.addEventListener('change', (event) => {
    state.sort = event.target.value;
    updateView();
  });

  el.viewMode.addEventListener('change', (event) => {
    state.view = event.target.value;
    updateView();
  });

  el.pillarFilter.addEventListener('change', (event) => {
    state.pillar = event.target.value;
    state.visibleCount = PAGE_SIZE;
    updateView();
  });

  el.extFilter.addEventListener('change', (event) => {
    state.ext = event.target.value;
    state.visibleCount = PAGE_SIZE;
    updateView();
  });

  el.roleFilter.addEventListener('change', (event) => {
    state.role = event.target.value;
    state.visibleCount = PAGE_SIZE;
    updateView();
  });

  el.depthFilter.addEventListener('change', (event) => {
    state.depth = event.target.value;
    state.visibleCount = PAGE_SIZE;
    updateView();
  });

  el.clearFilters.addEventListener('click', () => {
    state.query = '';
    state.mode = 'standard';
    state.perspective = 'standard';
    state.pillar = 'all';
    state.ext = 'all';
    state.role = 'all';
    state.depth = 'all';
    state.sort = 'relevance';
    state.view = 'cards';
    state.visibleCount = PAGE_SIZE;
    el.searchInput.value = '';
    el.sortMode.value = 'relevance';
    el.viewMode.value = 'cards';
    el.depthFilter.value = 'all';
    renderFilters();
    updateView();
  });

  el.loadMoreBtn.addEventListener('click', () => {
    state.visibleCount += PAGE_SIZE;
    renderResults();
  });

  document.addEventListener('click', (event) => {
    const modeButton = event.target.closest('[data-mode-preset]');
    if (modeButton) {
      applyModePreset(modeButton.dataset.modePreset);
      return;
    }

    const perspectiveButton = event.target.closest('[data-perspective]');
    if (perspectiveButton) {
      state.perspective = perspectiveButton.dataset.perspective;
      state.visibleCount = PAGE_SIZE;
      updateView();
      return;
    }

    const resultCard = event.target.closest('[data-path]');
    if (resultCard) {
      selectEntry(resultCard.dataset.path);
      return;
    }

    const heatmapItem = event.target.closest('[data-filter-directory]');
    if (heatmapItem) {
      state.view = 'directory';
      el.viewMode.value = 'directory';
      state.query = heatmapItem.dataset.filterDirectory;
      el.searchInput.value = state.query;
      state.visibleCount = PAGE_SIZE;
      updateView();
    }
  });

  document.querySelectorAll('.tab-button').forEach((button) => {
    button.addEventListener('click', () => {
      document.querySelectorAll('.tab-button').forEach((item) => item.classList.toggle('active', item === button));
      state.previewTab = button.dataset.tab;
      renderPreview();
    });
  });

  el.copyPathBtn.addEventListener('click', async () => {
    if (!state.selectedPath) return;
    try {
      await navigator.clipboard.writeText(state.selectedPath);
      el.copyPathBtn.textContent = '已复制';
    } catch (error) {
      el.copyPathBtn.textContent = '复制失败';
    }
    window.setTimeout(() => {
      el.copyPathBtn.textContent = '复制路径';
    }, 1200);
  });
}

function prepareData(payload) {
  payload.files = payload.files.map((entry) => ({
    ...entry,
    titleLower: entry.title.toLowerCase(),
    pathLower: entry.path.toLowerCase(),
    excerptLower: (entry.excerpt || '').toLowerCase(),
    searchIndex: normalizeText(entry),
  }));
  return payload;
}

function renderStaticInsights() {
  renderHeatmap();
  renderMiniList(el.recentList, state.data.latest_files.slice(0, 8));
  renderMiniList(
    el.dataToolList,
    state.data.files
      .filter((entry) => entry.signals.tooling || entry.signals.structured)
      .sort((a, b) => b.modified_ts - a.modified_ts)
      .slice(0, 8),
  );
}

async function bootstrap() {
  try {
    const response = await fetch(DATA_URL);
    if (!response.ok) {
      throw new Error('索引数据加载失败');
    }

    state.data = prepareData(await response.json());
    renderOverview();
    renderFilters();
    renderStaticInsights();
    filterEntries();

    const hashPath = decodeURIComponent(window.location.hash.replace(/^#/, ''));
    if (hashPath && state.data.files.some((entry) => entry.path === hashPath)) {
      state.selectedPath = hashPath;
    }

    el.dataStatus.textContent = `索引已就绪 · ${formatCount(state.data.stats.total_files)} 文件`;
    updateView();
    bindEvents();
  } catch (error) {
    el.dataStatus.textContent = '索引加载失败';
    el.resultsContainer.innerHTML = `<div class="group-block"><h3>无法加载页面索引</h3><p>${escapeHtml(error.message)}</p><p>请先生成 \`Tools/data/content_index.json\`，并通过本地静态服务访问当前页面。</p></div>`;
    el.loadMoreBtn.classList.add('hidden');
  }
}

bootstrap();
