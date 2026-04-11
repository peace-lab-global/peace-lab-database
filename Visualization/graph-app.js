(function () {
  if ('scrollRestoration' in history) history.scrollRestoration = 'manual';
  window.scrollTo(0, 0);
  document.documentElement.scrollTop = 0;
  document.body.scrollTop = 0;

  const container = document.getElementById('graph-container');
  const svg = d3.select('#graph-svg');
  const tooltip = document.getElementById('tooltip');
  const app = document.getElementById('app');
  const sidebar = document.getElementById('sidebar');
  const sidebarToggle = document.getElementById('sidebar-toggle');
  const sidebarBackdrop = document.getElementById('sidebar-backdrop');
  const W = 2400, H = 1600;

  svg.attr('viewBox', [0, 0, W, H]);

  const CM = { 0: '#d9dee6', 1: '#b68b4c', 2: '#7584a0', 3: '#6e8c82', 4: '#9a6f68', 5: '#597f98' };
  const RM = { 0: 24, 1: 14, 2: 8, 3: 4 };
  const FS = { 0: 12, 1: 10, 2: 8, 3: 7 };

  document.getElementById('node-count').textContent = graphData.nodes.length;
  document.getElementById('cross-count').textContent = graphData.links.filter(l => l.type === 'cross-ref').length;

  function setSidebarOpen(open) {
    if (!sidebar || !app) return;
    sidebar.classList.toggle('open', open);
    app.classList.toggle('sidebar-open', open);
    if (sidebarToggle) sidebarToggle.setAttribute('aria-expanded', open ? 'true' : 'false');
    if (open) document.getElementById('search-input')?.focus();
  }

  if (sidebarToggle && sidebar && sidebarBackdrop && app) {
    sidebarToggle.setAttribute('aria-expanded', 'false');
    sidebarToggle.addEventListener('click', () => setSidebarOpen(!sidebar.classList.contains('open')));
    sidebarBackdrop.addEventListener('click', () => setSidebarOpen(false));
    window.addEventListener('keydown', e => { if (e.key === 'Escape') setSidebarOpen(false); });
  }

  const g = svg.append('g');
  let isApplyingViewportTransform = false;
  let hasUserAdjustedViewport = false;
  let autoFitTimer = null;
  const zoomBehavior = d3.zoom()
    .scaleExtent([0.15, 4])
    .on('zoom', e => {
      if (!isApplyingViewportTransform && e.sourceEvent) hasUserAdjustedViewport = true;
      g.attr('transform', e.transform);
    });
  svg.call(zoomBehavior);

  document.getElementById('zoom-in').onclick = () => svg.transition().call(zoomBehavior.scaleBy, 1.4);
  document.getElementById('zoom-out').onclick = () => svg.transition().call(zoomBehavior.scaleBy, 0.7);
  document.getElementById('zoom-reset').onclick = () => {
    hasUserAdjustedViewport = false;
    fitToView({ force: true, duration: 520 });
  };
  document.getElementById('zoom-fit').onclick = () => {
    hasUserAdjustedViewport = false;
    fitToView({ force: true, duration: 520 });
  };

  function applyTransform(transform, duration = 600) {
    svg.interrupt();
    isApplyingViewportTransform = true;

    const finish = () => {
      isApplyingViewportTransform = false;
    };

    if (duration <= 0) {
      svg.call(zoomBehavior.transform, transform);
      finish();
      return;
    }

    svg.transition()
      .duration(duration)
      .ease(d3.easeCubicOut)
      .call(zoomBehavior.transform, transform)
      .on('end interrupt cancel', finish);
  }

  function getGraphBounds() {
    const laidOutNodes = nodes.filter(n => Number.isFinite(n.x) && Number.isFinite(n.y));
    if (!laidOutNodes.length) return null;

    let minX = Infinity;
    let maxX = -Infinity;
    let minY = Infinity;
    let maxY = -Infinity;

    laidOutNodes.forEach(n => {
      const radius = RM[n.level] + (n.level <= 1 ? 42 : n.level === 2 ? 24 : 12);
      minX = Math.min(minX, n.x - radius);
      maxX = Math.max(maxX, n.x + radius);
      minY = Math.min(minY, n.y - radius);
      maxY = Math.max(maxY, n.y + radius);
    });

    return {
      minX,
      maxX,
      minY,
      maxY,
      width: Math.max(maxX - minX, 1),
      height: Math.max(maxY - minY, 1),
      centerX: (minX + maxX) / 2,
      centerY: (minY + maxY) / 2
    };
  }

  function getFitViewport() {
    const rect = container.getBoundingClientRect();
    const header = document.getElementById('graph-header');
    const info = document.getElementById('graph-info');
    const controls = document.getElementById('controls');
    const paddingX = Math.max(32, Math.min(84, rect.width * 0.06));
    const paddingTop = Math.max(paddingX, (header?.offsetHeight || 0) + 44);
    const paddingBottom = Math.max(paddingX, Math.max(info?.offsetHeight || 0, controls?.offsetHeight || 0) + 40);

    return {
      width: Math.max(rect.width - paddingX * 2, 160),
      height: Math.max(rect.height - paddingTop - paddingBottom, 160),
      centerX: rect.width / 2,
      centerY: (paddingTop + (rect.height - paddingBottom)) / 2
    };
  }

  function fitToView(options = {}) {
    if (!options.force && (selectedNode || hasUserAdjustedViewport)) return false;

    const bounds = getGraphBounds();
    if (!bounds) return false;

    const viewport = getFitViewport();
    const scaleX = viewport.width / bounds.width;
    const scaleY = viewport.height / bounds.height;
    const baseScale = Math.min(scaleX, scaleY) * 0.96;
    const minReadableScale = Math.max(0.5, Math.min(0.9, Math.min(viewport.width / 960, viewport.height / 720)));
    const targetScale = Math.min(1.8, Math.max(minReadableScale, baseScale));
    const targetTransform = d3.zoomIdentity
      .translate(viewport.centerX, viewport.centerY)
      .scale(targetScale)
      .translate(-bounds.centerX, -bounds.centerY);

    applyTransform(targetTransform, options.duration ?? 680);
    return true;
  }

  function scheduleAutoFit(options = {}) {
    if (autoFitTimer) window.clearTimeout(autoFitTimer);

    const attempt = (remaining = options.retries ?? 10) => {
      const ready = nodes.some(n => Number.isFinite(n.x) && Number.isFinite(n.y));
      const settling = simulation && simulation.alpha() > (options.alphaThreshold ?? 0.16);

      if (!ready || (settling && remaining > 0)) {
        autoFitTimer = window.setTimeout(() => attempt(remaining - 1), options.delay ?? 120);
        return;
      }

      fitToView(options);
    };

    attempt();
  }

  const nodes = graphData.nodes.map(d => ({ ...d }));
  const links = graphData.links.map(d => ({ ...d }));
  const nodeById = new Map(nodes.map(n => [n.id, n]));

  function getPillar(node) {
    if (node.level === 0) return 'root';
    if (node.level === 1) return node.id;
    let cur = node;
    while (cur && cur.parent) cur = nodeById.get(cur.parent);
    return cur ? cur.id : 'root';
  }

  const pillars = nodes.filter(n => n.level === 1);
  const pillarAngles = {};
  pillars.forEach((p, i) => { pillarAngles[p.id] = (2 * Math.PI * i / 5) - Math.PI / 2; });

  function assignRadialPositions() {
    const cx = W / 2, cy = H / 2;
    const root = nodes.find(n => n.level === 0);
    root.fx = cx; root.fy = cy;

    pillars.forEach(p => {
      const a = pillarAngles[p.id];
      p.fx = cx + 200 * Math.cos(a);
      p.fy = cy + 200 * Math.sin(a);
    });

    nodes.filter(n => n.level === 2).forEach(n => {
      const pid = n.parent;
      const pa = pillarAngles[pid] || 0;
      const siblings = nodes.filter(s => s.parent === pid && s.level === 2);
      const idx = siblings.indexOf(n);
      const span = Math.min(siblings.length * 0.18, 0.9);
      const a = pa - span / 2 + (span / (siblings.length - 1 || 1)) * idx;
      const r = 420;
      n.fx = cx + r * Math.cos(a);
      n.fy = cy + r * Math.sin(a);
    });

    nodes.filter(n => n.level === 3).forEach(n => {
      const parent = nodes.find(p => p.id === n.parent);
      if (!parent || parent.fx == null) return;
      const siblings = nodes.filter(s => s.parent === n.parent && s.level === 3);
      const idx = siblings.indexOf(n);
      const baseAngle = Math.atan2(parent.fy - cy, parent.fx - cx);
      const span = Math.min(siblings.length * 0.06, 0.6);
      const a = baseAngle - span / 2 + (span / (siblings.length - 1 || 1)) * idx;
      const r = 600 + (idx % 2) * 30;
      n.fx = cx + r * Math.cos(a);
      n.fy = cy + r * Math.sin(a);
    });
  }

  function assignTreePositions() {
    const cx = W / 2, cy = H / 2;
    const root = nodes.find(n => n.level === 0);
    root.fx = cx; root.fy = 80;

    pillars.forEach((p, i) => {
      const spacing = W / (pillars.length + 1);
      p.fx = spacing * (i + 1);
      p.fy = 250;

      const l2 = nodes.filter(n => n.parent === p.id && n.level === 2);
      const l2spacing = spacing / (l2.length + 1);
      l2.forEach((c2, j) => {
        c2.fx = p.fx - spacing / 2 + l2spacing * (j + 1);
        c2.fy = 500;

        const l3 = nodes.filter(n => n.parent === c2.id && n.level === 3);
        const l3w = spacing / (l2.length + 1);
        const l3spacing = l3w / (l3.length + 1);
        l3.forEach((c3, k) => {
          c3.fx = c2.fx - l3w / 2 + l3spacing * (k + 1);
          c3.fy = 740 + (k % 3) * 30;
        });
      });
    });
  }

  function clearFixed() { nodes.forEach(n => { n.fx = null; n.fy = null; }); }

  const linkG = g.append('g').attr('class', 'links');
  const nodeG = g.append('g').attr('class', 'nodes');
  const labelG = g.append('g').attr('class', 'labels');

  const linkEls = linkG.selectAll('line')
    .data(links).join('line')
    .attr('class', d => 'link-' + d.type)
    .attr('stroke-width', d => d.type === 'cross-ref' ? 0.8 : 1.2);

  const nodeEls = nodeG.selectAll('circle')
    .data(nodes).join('circle')
    .attr('r', d => RM[d.level])
    .attr('fill', d => CM[d.group])
    .attr('fill-opacity', d => d.level === 0 ? 1 : d.level === 1 ? 0.9 : d.level === 2 ? 0.7 : 0.5)
    .attr('stroke', d => d.level <= 1 ? '#fff' : CM[d.group])
    .attr('stroke-width', d => d.level === 0 ? 2.5 : d.level === 1 ? 1.5 : 0.5)
    .attr('stroke-opacity', d => d.level <= 1 ? 0.8 : 0.3)
    .style('cursor', 'pointer')
    .on('pointerenter', onHover)
    .on('pointerleave', onLeave)
    .on('click', onClick)
    .call(d3.drag().on('start', dragStart).on('drag', dragging).on('end', dragEnd));

  const labelEls = labelG.selectAll('text')
    .data(nodes).join('text')
    .text(d => d.level <= 2 ? d.label : '')
    .attr('font-size', d => FS[d.level])
    .attr('fill', d => d.level === 0 ? '#fff' : d.level === 1 ? CM[d.group] : 'rgba(203,213,225,0.7)')
    .attr('text-anchor', 'middle')
    .attr('dy', d => RM[d.level] + (d.level <= 1 ? 16 : 12))
    .style('pointer-events', 'none')
    .style('font-weight', d => d.level <= 1 ? '700' : d.level === 2 ? '500' : '400')
    .style('text-shadow', d => d.level <= 1 ? '0 1px 6px rgba(0,0,0,0.8)' : 'none');

  let simulation;
  let currentMode = 'radial';
  let selectedNode = null;

  function buildSim(fixed) {
    return d3.forceSimulation(nodes)
      .alphaDecay(0.03)
      .velocityDecay(0.35)
      .force('link', d3.forceLink(links).id(d => d.id)
        .distance(d => d.type === 'cross-ref' ? 300 : d.source.level === 0 ? 180 : d.source.level === 1 ? 120 : 80)
        .strength(d => d.type === 'cross-ref' ? 0.05 : 0.4))
      .force('charge', d3.forceManyBody().strength(d =>
        d.level === 0 ? -800 : d.level === 1 ? -400 : d.level === 2 ? -120 : -40))
      .force('center', d3.forceCenter(W / 2, H / 2).strength(0.02))
      .force('collision', d3.forceCollide().radius(d => RM[d.level] + 12).strength(0.9))
      .force('x', d3.forceX(W / 2).strength(0.005))
      .force('y', d3.forceY(H / 2).strength(0.005))
      .on('tick', tick);
  }

  function tick() {
    linkEls.attr('x1', d => d.source.x).attr('y1', d => d.source.y)
           .attr('x2', d => d.target.x).attr('y2', d => d.target.y);
    nodeEls.attr('cx', d => d.x).attr('cy', d => d.y);
    labelEls.attr('x', d => d.x).attr('y', d => d.y);
  }

  function switchMode(mode) {
    currentMode = mode;
    hasUserAdjustedViewport = false;
    clearFixed();
    if (simulation) simulation.stop();

    if (mode === 'radial') assignRadialPositions();
    else if (mode === 'tree') assignTreePositions();

    simulation = buildSim(mode !== 'force');
    simulation.alpha(mode === 'force' ? 1 : 0.3).restart();

    if (selectedNode) {
      scheduleAutoFit({ force: true, duration: 0, retries: 3, alphaThreshold: 0.3 });
      window.setTimeout(() => zoomToNode(selectedNode, { duration: 420 }), 180);
      return;
    }

    scheduleAutoFit({ force: true, duration: 700, retries: 12, alphaThreshold: mode === 'force' ? 0.22 : 0.12 });
  }

  function dragStart(e, d) {
    if (!e.active) simulation.alphaTarget(0.3).restart();
    d.fx = d.x; d.fy = d.y;
  }
  function dragging(e, d) { d.fx = e.x; d.fy = e.y; }
  function dragEnd(e, d) {
    if (!e.active) simulation.alphaTarget(0);
    if (currentMode === 'force') { d.fx = null; d.fy = null; }
  }

  function getConnected(nodeId) {
    const set = new Set([nodeId]);
    links.forEach(l => {
      const s = typeof l.source === 'object' ? l.source.id : l.source;
      const t = typeof l.target === 'object' ? l.target.id : l.target;
      if (s === nodeId) set.add(t);
      if (t === nodeId) set.add(s);
    });
    const children = nodes.filter(n => n.parent === nodeId);
    children.forEach(c => set.add(c.id));
    const parent = nodes.find(n => n.id === nodeId);
    if (parent && parent.parent) set.add(parent.parent);
    return set;
  }

  function applyHighlight(connected) {
    nodeEls.attr('fill-opacity', n => connected.has(n.id) ? (n.level <= 1 ? 1 : 0.9) : 0.08)
           .attr('r', n => connected.has(n.id) ? RM[n.level] * (n.level <= 1 ? 1.15 : 1.1) : RM[n.level]);
    labelEls.attr('fill-opacity', n => connected.has(n.id) ? 1 : 0.04)
            .text(n => connected.has(n.id) ? n.label : (n.level <= 2 ? n.label : ''));
    linkEls.attr('stroke-opacity', l => {
      const s = typeof l.source === 'object' ? l.source.id : l.source;
      const t = typeof l.target === 'object' ? l.target.id : l.target;
      return (connected.has(s) && connected.has(t)) ? (l.type === 'cross-ref' ? 0.7 : 0.5) : 0.02;
    });
  }

  function resetHighlight() {
    nodeEls.attr('fill-opacity', d => d.level === 0 ? 1 : d.level === 1 ? 0.9 : d.level === 2 ? 0.7 : 0.5)
           .attr('r', d => RM[d.level]);
    labelEls.attr('fill-opacity', 1).text(d => d.level <= 2 ? d.label : '');
    linkEls.attr('stroke-opacity', d => d.type === 'cross-ref' ? 0.25 : 0.2);
  }

  function onHover(e, d) {
    if (selectedNode) return;
    const connected = getConnected(d.id);
    applyHighlight(connected);
    const tt = tooltip;
    tt.querySelector('.tt-name').textContent = d.label;
    tt.querySelector('.tt-desc').textContent = d.description || '';
    tt.querySelector('.tt-meta').textContent = d.fileCount ? d.fileCount + ' 篇文档' : '';
    tt.style.display = 'block';
    positionTooltip(e);
  }

  function onLeave() {
    if (selectedNode) return;
    resetHighlight();
    tooltip.style.display = 'none';
  }

  function positionTooltip(e) {
    const rect = container.getBoundingClientRect();
    let x = e.clientX - rect.left + 14;
    let y = e.clientY - rect.top - 8;
    if (x + 260 > rect.width) x = e.clientX - rect.left - 270;
    if (y + 80 > rect.height) y = rect.height - 90;
    tooltip.style.left = x + 'px';
    tooltip.style.top = y + 'px';
  }

  svg.on('pointermove', e => { if (tooltip.style.display === 'block') positionTooltip(e); });

  function onClick(e, d) {
    e.stopPropagation();
    selectedNode = d;
    const connected = getConnected(d.id);
    applyHighlight(connected);
    showDetail(d);
    highlightListItem(d.id);
    zoomToNode(d);
  }

  function getFocusViewport() {
    const rect = container.getBoundingClientRect();
    const detailPanel = document.getElementById('detail-panel');
    const padding = Math.max(24, Math.min(48, Math.min(rect.width, rect.height) * 0.05));
    let left = padding;
    let right = rect.width - padding;

    if (detailPanel.classList.contains('open')) {
      const panelStyle = window.getComputedStyle(detailPanel);
      const isOverlayingGraph = panelStyle.position === 'absolute' || panelStyle.position === 'fixed';

      if (isOverlayingGraph) {
        const overlapWidth = Math.min(detailPanel.offsetWidth || 0, rect.width * 0.45);
        right = Math.max(left + 120, right - overlapWidth);
      }
    }

    return {
      centerX: (left + right) / 2,
      centerY: rect.height / 2,
      width: Math.max(right - left, 120),
      height: Math.max(rect.height - padding * 2, 120)
    };
  }

  function getFocusScale(d, viewport) {
    const currentScale = d3.zoomTransform(svg.node()).k || 1;
    const minScaleByLevel = [1.05, 1.3, 1.75, 2.2];
    const minScale = minScaleByLevel[d.level] || 1.6;
    const referenceWidth = d.level <= 1 ? 640 : d.level === 2 ? 460 : 320;
    const referenceHeight = d.level <= 1 ? 520 : d.level === 2 ? 380 : 260;
    const suggestedScale = Math.min(viewport.width / referenceWidth, viewport.height / referenceHeight);
    return Math.max(currentScale, Math.min(3.2, Math.max(minScale, suggestedScale)));
  }

  function zoomToNode(d, options = {}) {
    if (d.x == null || d.y == null) return;

    const viewport = getFocusViewport();
    const targetScale = getFocusScale(d, viewport);
    const targetTransform = d3.zoomIdentity
      .translate(viewport.centerX, viewport.centerY)
      .scale(targetScale)
      .translate(-d.x, -d.y);

    applyTransform(targetTransform, options.duration ?? 650);
  }

  function showDetail(d) {
    const panel = document.getElementById('detail-panel');
    const breadcrumb = document.getElementById('detail-breadcrumb');
    const nameEl = document.getElementById('detail-name');
    const descEl = document.getElementById('detail-desc');
    const statsEl = document.getElementById('detail-stats');
    const childrenEl = document.getElementById('detail-children');
    const crossEl = document.getElementById('detail-cross');

    let path = [];
    let cur = d;
    while (cur) { path.unshift(cur.label); cur = cur.parent ? nodeById.get(cur.parent) : null; }
    breadcrumb.textContent = path.join(' › ');
    nameEl.textContent = d.label;
    nameEl.style.color = CM[d.group];
    descEl.textContent = d.description || '';

    statsEl.innerHTML = d.fileCount
      ? `<div class="ds-item"><span class="ds-label">文档数</span><span class="ds-value">${d.fileCount}</span></div>`
      : '';

    const childNodes = nodes.filter(n => n.parent === d.id);
    let html = '';
    if (childNodes.length) {
      html += '<div class="dc-section"><div class="dc-section-title">子节点</div>';
      childNodes.forEach(c => {
        html += `<div class="dc-item" data-id="${c.id}"><span class="dc-dot" style="background:${CM[c.group]}"></span>${c.label}${c.fileCount ? `<span class="dc-tag">${c.fileCount}</span>` : ''}</div>`;
      });
      html += '</div>';
    }

    const related = links.filter(l => {
      const s = typeof l.source === 'object' ? l.source.id : l.source;
      const t = typeof l.target === 'object' ? l.target.id : l.target;
      return (s === d.id || t === d.id) && l.type === 'cross-ref';
    });
    if (related.length) {
      html += '<div class="dc-section"><div class="dc-section-title">交叉引用</div>';
      related.forEach(l => {
        const s = typeof l.source === 'object' ? l.source.id : l.source;
        const t = typeof l.target === 'object' ? l.target.id : l.target;
        const other = s === d.id ? t : s;
        const otherNode = nodes.find(n => n.id === other);
        if (otherNode) {
          html += `<div class="dc-item" data-id="${other}"><span class="dc-dot" style="background:${CM[otherNode.group]}"></span>${otherNode.label}<span class="dc-tag">${l.label || ''}</span></div>`;
        }
      });
      html += '</div>';
    }

    childrenEl.innerHTML = html;
    crossEl.innerHTML = '';
    panel.classList.add('open');

    childrenEl.querySelectorAll('.dc-item').forEach(item => {
      item.addEventListener('click', () => {
        const nid = item.dataset.id;
        const nd = nodeById.get(nid);
        if (nd) { selectedNode = nd; showDetail(nd); highlightListItem(nid); applyHighlight(getConnected(nid)); zoomToNode(nd); }
      });
    });
  }

  document.getElementById('detail-close').onclick = () => {
    document.getElementById('detail-panel').classList.remove('open');
    selectedNode = null;
    resetHighlight();
    document.querySelectorAll('.node-card.active').forEach(c => c.classList.remove('active'));
  };

  svg.on('click', () => {
    selectedNode = null;
    resetHighlight();
    document.getElementById('detail-panel').classList.remove('open');
    tooltip.style.display = 'none';
    document.querySelectorAll('.node-card.active').forEach(c => c.classList.remove('active'));
  });

  function ensureCardVisible(card) {
    const list = document.getElementById('node-list');
    if (!card || !list) return;

    const margin = 12;
    const cardTop = card.offsetTop;
    const cardBottom = cardTop + card.offsetHeight;
    const viewTop = list.scrollTop;
    const viewBottom = viewTop + list.clientHeight;

    if (cardTop < viewTop + margin) {
      list.scrollTo({ top: Math.max(cardTop - margin, 0), behavior: 'smooth' });
      return;
    }

    if (cardBottom > viewBottom - margin) {
      list.scrollTo({ top: Math.max(cardBottom - list.clientHeight + margin, 0), behavior: 'smooth' });
    }
  }

  function highlightListItem(id) {
    document.querySelectorAll('.node-card.active').forEach(c => c.classList.remove('active'));
    const card = document.querySelector(`.node-card[data-id="${id}"]`);
    if (card) {
      card.classList.add('active');
      ensureCardVisible(card);
    }
  }

  function buildSidebar(filter) {
    const list = document.getElementById('node-list');
    list.innerHTML = '';
    const pillarNames = { p1: '智慧传承', p2: '心智与心理学', p3: '生命科学', p4: '人文与艺术', p5: '实践与增长' };
    const pillarOrder = ['p1', 'p2', 'p3', 'p4', 'p5'];
    const groups = {};

    nodes.forEach(n => {
      if (filter && !n.label.includes(filter) && !(n.description || '').includes(filter)) return;
      const pid = getPillar(n);
      if (!groups[pid]) groups[pid] = [];
      groups[pid].push(n);
    });

    const ordered = Object.keys(groups).sort((a, b) => {
      if (a === 'root') return -1;
      if (b === 'root') return 1;
      return pillarOrder.indexOf(a) - pillarOrder.indexOf(b);
    });

    ordered.forEach(pid => {
      const title = document.createElement('div');
      title.className = 'nl-group-title';
      const g = groups[pid][0].group;
      title.innerHTML = `<span class="nl-dot" style="background:${CM[g]}"></span>${pillarNames[pid] || '根'}`;
      list.appendChild(title);

      groups[pid].forEach(n => {
        const card = document.createElement('button');
        card.className = 'node-card';
        card.type = 'button';
        card.dataset.id = n.id;
        card.innerHTML = `<span class="nc-dot" style="background:${CM[n.group]}"></span><span class="nc-name" style="padding-left:${(n.level - 1) * 10}px">${n.label}</span>${n.fileCount ? `<span class="nc-count">${n.fileCount}</span>` : ''}`;
        list.appendChild(card);
      });
    });
  }

  buildSidebar();

  document.getElementById('search-input').addEventListener('input', e => buildSidebar(e.target.value));

  const nodeList = document.getElementById('node-list');
  nodeList.addEventListener('click', e => {
    const card = e.target.closest('.node-card');
    if (!card || !nodeList.contains(card)) return;
    const n = nodeById.get(card.dataset.id);
    if (!n) return;
    selectedNode = n;
    showDetail(n);
    highlightListItem(n.id);
    applyHighlight(getConnected(n.id));
    zoomToNode(n);
  });

  nodeList.addEventListener('keydown', e => {
    if (e.key !== 'Enter' && e.key !== ' ') return;
    const card = e.target.closest('.node-card');
    if (!card || !nodeList.contains(card)) return;
    e.preventDefault();
    const n = nodeById.get(card.dataset.id);
    if (!n) return;
    selectedNode = n;
    showDetail(n);
    highlightListItem(n.id);
    applyHighlight(getConnected(n.id));
    zoomToNode(n);
  });

  function getPillarConnected(pillar) {
    const connected = new Set([pillar.id, 'root']);
    const addDescendants = (pid) => {
      nodes.filter(n => n.parent === pid).forEach(c => { connected.add(c.id); addDescendants(c.id); });
    };
    addDescendants(pillar.id);
    links.forEach(l => {
      const s = typeof l.source === 'object' ? l.source.id : l.source;
      const t = typeof l.target === 'object' ? l.target.id : l.target;
      if (s === pillar.id) connected.add(t);
      if (t === pillar.id) connected.add(s);
    });
    return connected;
  }

  const legend = document.getElementById('legend');
  legend.addEventListener('click', e => {
    const item = e.target.closest('.legend-item');
    if (!item || !legend.contains(item)) return;
    const group = parseInt(item.dataset.group);
    const pillar = nodes.find(n => n.level === 1 && n.group === group);
    if (!pillar) return;
    applyHighlight(getPillarConnected(pillar));
    selectedNode = pillar;
    showDetail(pillar);
    zoomToNode(pillar);
  });

  legend.addEventListener('keydown', e => {
    if (e.key !== 'Enter' && e.key !== ' ') return;
    const item = e.target.closest('.legend-item');
    if (!item || !legend.contains(item)) return;
    e.preventDefault();
    const group = parseInt(item.dataset.group);
    const pillar = nodes.find(n => n.level === 1 && n.group === group);
    if (!pillar) return;
    applyHighlight(getPillarConnected(pillar));
    selectedNode = pillar;
    showDetail(pillar);
    zoomToNode(pillar);
  });

  legend.addEventListener('pointerover', e => {
    if (selectedNode) return;
    const item = e.target.closest('.legend-item');
    if (!item || !legend.contains(item)) return;
    const group = parseInt(item.dataset.group);
    const pillar = nodes.find(n => n.level === 1 && n.group === group);
    if (!pillar) return;
    applyHighlight(getPillarConnected(pillar));
  });

  legend.addEventListener('pointerout', e => {
    if (selectedNode) return;
    const item = e.target.closest('.legend-item');
    if (!item || !legend.contains(item)) return;
    if (item.contains(e.relatedTarget)) return;
    resetHighlight();
  });

  legend.addEventListener('focusin', e => {
    if (selectedNode) return;
    const item = e.target.closest('.legend-item');
    if (!item || !legend.contains(item)) return;
    const group = parseInt(item.dataset.group);
    const pillar = nodes.find(n => n.level === 1 && n.group === group);
    if (!pillar) return;
    applyHighlight(getPillarConnected(pillar));
  });

  legend.addEventListener('focusout', e => {
    if (selectedNode) return;
    const item = e.target.closest('.legend-item');
    if (!item || !legend.contains(item)) return;
    if (item.contains(e.relatedTarget)) return;
    resetHighlight();
  });

  document.querySelectorAll('.mode-btn').forEach(btn => {
    btn.addEventListener('click', () => {
      document.querySelectorAll('.mode-btn').forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      switchMode(btn.dataset.mode);
    });
  });

  switchMode('radial');

  window.addEventListener('resize', () => {
    svg.attr('viewBox', [0, 0, W, H]);
    if (window.innerWidth > 760) setSidebarOpen(false);
    if (selectedNode) {
      zoomToNode(selectedNode, { duration: 0 });
      return;
    }

    if (!hasUserAdjustedViewport) scheduleAutoFit({ force: true, duration: 0, retries: 2, alphaThreshold: 0.24 });
  });
})();
