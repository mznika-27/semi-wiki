// 首頁：讀 data/terms.json 產生分類按鈕和詞條卡片。新增詞條不用改這支檔案。
(async function () {
  const res = await fetch('data/terms.json');
  const data = await res.json();
  const cats = data.categories;
  const terms = data.terms;
  let active = 'all';

  document.getElementById('stat-terms').textContent = terms.length;
  document.getElementById('stat-cats').textContent = Object.keys(cats).length;
  document.getElementById('stat-updated').textContent =
    terms.map(t => t.updated).sort().slice(-1)[0] || '–';

  const chips = document.getElementById('chips');
  const mkChip = (key, label, color) => {
    const b = document.createElement('button');
    b.className = 'chip'; b.textContent = label; b.dataset.key = key;
    b.onclick = () => { active = key; render(); };
    b.dataset.color = color || '#10213d';
    chips.appendChild(b);
  };
  mkChip('all', '全部');
  for (const [key, c] of Object.entries(cats)) mkChip(key, c.label, c.color);

  const necks = document.getElementById('necks');
  for (const [key, b] of Object.entries(data.bottlenecks || {})) {
    const box = document.createElement('div');
    box.className = 'nk';
    const links = terms.filter(t => t.bottleneck === key)
      .map(t => `<a href="wiki/${t.slug}.html">${t.name}</a>`).join('');
    box.innerHTML = `<h4>${b.label}</h4><p>${b.desc}</p>${links}`;
    necks.appendChild(box);
  }

  const q = document.getElementById('q');
  q.addEventListener('input', render);

  function render() {
    const kw = q.value.trim().toLowerCase();
    for (const b of chips.children) {
      const on = b.dataset.key === active;
      b.classList.toggle('on', on);
      b.style.background = on ? b.dataset.color : '';
    }
    const list = terms.filter(t =>
      (active === 'all' || t.category === active) &&
      (!kw || [t.name, t.en, t.oneliner, cats[t.category].label].join(' ').toLowerCase().includes(kw)));
    const grid = document.getElementById('grid');
    grid.innerHTML = '';
    for (const t of list) {
      const c = cats[t.category];
      const a = document.createElement('a');
      a.className = 'card'; a.href = `wiki/${t.slug}.html`;
      a.innerHTML = `<span class="bar" style="background:${c.color}"></span>
        <span class="tag cat-${t.category}">${c.label}</span>
        <h3>${t.name}</h3><div class="en">${t.en}</div><p>${t.oneliner}</p>`;
      grid.appendChild(a);
    }
    document.getElementById('empty').hidden = list.length > 0;
  }
  render();
})();
