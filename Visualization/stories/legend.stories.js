import { within, userEvent, expect } from '@storybook/test';

export default {
  title: 'Visualization/Sidebar/Legend',
  render: () => {
    const shell = document.createElement('div');
    shell.style.width = '372px';
    shell.style.height = '680px';
    shell.style.padding = '18px';

    shell.innerHTML = `
      <aside id="sidebar" style="height:100%; width:100%; min-width:0; overflow:auto;">
        <div id="legend" class="panel-section">
          <div class="section-row section-row-heading">
            <div>
              <div class="section-label">领域框架</div>
              <h3>五大研究支柱</h3>
            </div>
            <span class="section-meta">点击聚焦</span>
          </div>
          <button class="legend-item" type="button" data-group="1"><span class="legend-dot" style="background:var(--g1)"></span><span class="legend-label">01 智慧传承</span><span class="legend-count">405</span></button>
          <button class="legend-item" type="button" data-group="2"><span class="legend-dot" style="background:var(--g2)"></span><span class="legend-label">02 心智心理</span><span class="legend-count">864</span></button>
          <button class="legend-item" type="button" data-group="3"><span class="legend-dot" style="background:var(--g3)"></span><span class="legend-label">03 生命科学</span><span class="legend-count">353</span></button>
          <button class="legend-item" type="button" data-group="4"><span class="legend-dot" style="background:var(--g4)"></span><span class="legend-label">04 人文艺术</span><span class="legend-count">607</span></button>
          <button class="legend-item" type="button" data-group="5"><span class="legend-dot" style="background:var(--g5)"></span><span class="legend-label">05 实践增长</span><span class="legend-count">420</span></button>
        </div>
        <div class="panel-section">
          <div class="section-row">
            <div class="section-label">滚动测试</div>
            <span class="section-meta">侧栏可滚动</span>
          </div>
          ${Array.from({ length: 40 }).map((_, i) => `<button class="node-card" type="button"><span class="nc-dot" style="background:var(--g2)"></span><span class="nc-name">节点条目 ${i + 1}</span></button>`).join('')}
        </div>
      </aside>
    `;

    return shell;
  }
};

export const Interactions = {
  play: async ({ canvasElement }) => {
    const canvas = within(canvasElement);
    const btn = canvas.getByRole('button', { name: /01 智慧传承/ });
    await userEvent.hover(btn);
    await userEvent.click(btn);
    await expect(btn).toBeTruthy();
  }
};

