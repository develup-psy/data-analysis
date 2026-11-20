(() => {
  const stage = document.getElementById('stage');
  const viewport = document.getElementById('viewport');
  const slides = [...stage.querySelectorAll(':scope > section.slide')];
  const counter = document.getElementById('counter');
  const partname = document.getElementById('partname');
  const progress = document.getElementById('progress');
  const notesPanel = document.getElementById('notes');
  const noteTitle = document.getElementById('noteTitle');
  const notePage = document.getElementById('notePage');
  const noteText = document.getElementById('noteText');
  const promptModal = document.getElementById('promptModal');
  const promptTitle = document.getElementById('promptTitle');
  const promptFull = document.getElementById('promptFull');
  const copyStatus = document.getElementById('copyStatus');
  const blackout = document.getElementById('blackout');
  const noteStorageKey = 'data-analysis-lecture-notes-v1';
  const initialNotes = slides.map(slide => slide.querySelector('.speaker-note')?.textContent || '');
  let index = 0;
  let currentPrompt = '';
  let toastTimer;
  let savedNotes = {};

  try { savedNotes = JSON.parse(localStorage.getItem(noteStorageKey) || '{}'); } catch { savedNotes = {}; }

  function fit() {
    stage.style.transform = `translate(-50%, -50%) scale(${Math.min(viewport.clientWidth / 1920, viewport.clientHeight / 1080)})`;
  }

  function noteAt(i) {
    return Object.prototype.hasOwnProperty.call(savedNotes, i) ? savedNotes[i] : initialNotes[i];
  }

  function saveNote() {
    savedNotes[index] = noteText.value;
    try {
      localStorage.setItem(noteStorageKey, JSON.stringify(savedNotes));
      document.getElementById('noteStatus').textContent = '이 브라우저에 저장됨';
    } catch {
      document.getElementById('noteStatus').textContent = '저장되지 않음 · 노트 파일을 내려받으세요';
    }
  }

  function show(n) {
    index = Math.max(0, Math.min(n, slides.length - 1));
    slides.forEach((slide, i) => slide.classList.toggle('active', i === index));
    const active = slides[index];
    active.classList.remove('active');
    void active.offsetWidth;
    active.classList.add('active');
    active.querySelectorAll('.reveal').forEach((element, i) => element.style.setProperty('--delay', `${180 + i * 180}ms`));
    counter.textContent = `${index + 1} / ${slides.length}`;
    partname.textContent = active.dataset.part;
    progress.style.width = `${(index + 1) / slides.length * 100}%`;
    document.getElementById('prev').disabled = index === 0;
    document.getElementById('next').disabled = index === slides.length - 1;
    noteTitle.textContent = active.dataset.title;
    notePage.textContent = `${index + 1} / ${slides.length} · ${active.dataset.part}`;
    noteText.value = noteAt(index);
    history.replaceState(null, '', `#slide-${index + 1}`);
  }

  function next() { if (index < slides.length - 1) show(index + 1); }
  function previous() { if (index > 0) show(index - 1); }
  function closePrompt() { promptModal.classList.remove('open'); currentPrompt = ''; }
  function closeNotes() { notesPanel.classList.remove('open'); }
  function toast(message) {
    copyStatus.textContent = message;
    copyStatus.classList.add('visible');
    clearTimeout(toastTimer);
    toastTimer = setTimeout(() => copyStatus.classList.remove('visible'), 2200);
  }

  async function copy(text) {
    try {
      await navigator.clipboard.writeText(text);
    } catch {
      const area = document.createElement('textarea');
      area.value = text;
      area.style.position = 'fixed';
      area.style.opacity = '0';
      document.body.appendChild(area);
      area.select();
      const worked = document.execCommand('copy');
      area.remove();
      if (!worked) { toast('복사 실패 · 내용 보기에서 직접 선택하세요'); return; }
    }
    toast('프롬프트 복사됨');
  }

  stage.addEventListener('click', event => {
    const copyButton = event.target.closest('.copy-prompt');
    const viewButton = event.target.closest('.view-prompt');
    if (!copyButton && !viewButton) return;
    const item = event.target.closest('.prompt-item');
    const prompt = item.querySelector('.prompt-text').content.textContent.trim();
    if (copyButton) { copy(prompt); return; }
    currentPrompt = prompt;
    promptTitle.textContent = item.querySelector('h2').textContent;
    promptFull.textContent = prompt;
    promptModal.classList.add('open');
    document.getElementById('promptClose').focus();
  });

  document.getElementById('modalCopy').addEventListener('click', () => copy(currentPrompt));
  document.getElementById('promptClose').addEventListener('click', closePrompt);
  promptModal.addEventListener('click', event => { if (event.target === promptModal) closePrompt(); });
  document.getElementById('notesButton').addEventListener('click', () => notesPanel.classList.toggle('open'));
  document.getElementById('closeNotes').addEventListener('click', closeNotes);
  notesPanel.addEventListener('click', event => { if (event.target === notesPanel) closeNotes(); });
  noteText.addEventListener('input', saveNote);
  document.getElementById('saveNotes').addEventListener('click', saveNote);
  document.getElementById('downloadNotes').addEventListener('click', () => {
    const data = { format: 'data-analysis-lecture-notes', version: 1, slides: slides.map((slide, i) => ({ page: i + 1, title: slide.dataset.title, note: noteAt(i) })) };
    const url = URL.createObjectURL(new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' }));
    const link = document.createElement('a');
    link.href = url;
    link.download = 'lecture-speaker-notes.json';
    link.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
    document.getElementById('noteStatus').textContent = '노트 파일 다운로드';
  });
  document.getElementById('uploadNotes').addEventListener('change', async event => {
    const file = event.target.files?.[0];
    if (!file) return;
    try {
      const data = JSON.parse(await file.text());
      if (data.format !== 'data-analysis-lecture-notes' || !Array.isArray(data.slides)) throw new Error('형식 오류');
      data.slides.forEach(item => { if (Number.isInteger(item.page) && typeof item.note === 'string') savedNotes[item.page - 1] = item.note; });
      noteText.value = noteAt(index);
      localStorage.setItem(noteStorageKey, JSON.stringify(savedNotes));
      document.getElementById('noteStatus').textContent = '노트 파일 불러옴';
    } catch { document.getElementById('noteStatus').textContent = '노트 파일을 읽지 못했습니다'; }
  });
  document.getElementById('prev').addEventListener('click', previous);
  document.getElementById('next').addEventListener('click', next);
  document.getElementById('fullButton').addEventListener('click', async () => {
    try { if (document.fullscreenElement) await document.exitFullscreen(); else await document.documentElement.requestFullscreen(); } catch {}
  });
  document.addEventListener('keydown', event => {
    if (['INPUT', 'TEXTAREA'].includes(event.target.tagName)) return;
    if (event.key === 'Escape') { closePrompt(); closeNotes(); blackout.style.display = 'none'; return; }
    if (promptModal.classList.contains('open') || notesPanel.classList.contains('open')) return;
    if (event.key.toLowerCase() === 'n') { notesPanel.classList.toggle('open'); return; }
    if (event.key.toLowerCase() === 'f') { document.getElementById('fullButton').click(); return; }
    if (event.key.toLowerCase() === 'b') { blackout.style.display = blackout.style.display === 'block' ? 'none' : 'block'; return; }
    if (event.key.toLowerCase() === 'r') { show(index); return; }
    if (['ArrowRight', 'ArrowLeft', ' ', 'Home', 'End'].includes(event.key)) event.preventDefault();
    if (event.key === 'ArrowRight' || event.key === ' ') next();
    if (event.key === 'ArrowLeft') previous();
    if (event.key === 'Home') show(0);
    if (event.key === 'End') show(slides.length - 1);
  });
  window.addEventListener('resize', fit);
  window.addEventListener('hashchange', () => {
    const target = Number(location.hash.match(/^#slide-(\d+)$/)?.[1]);
    if (Number.isInteger(target) && target > 0) show(target - 1);
  });
  fit();
  const initial = Number(location.hash.match(/^#slide-(\d+)$/)?.[1] || 1) - 1;
  show(initial);
})();
