// UI helpers: initialize theme toggle, make cards interactive
(function(){
  function setTheme(t, btn){
    document.documentElement.setAttribute('data-theme', t);
    if(btn) btn.textContent = t === 'dark' ? '☀️' : '🌙';
  }

  function initThemeToggle(){
    const btn = document.getElementById('themeToggle');
    if(!btn) return;
    const stored = localStorage.getItem('theme');
    const prefersDark = window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches;
    setTheme(stored || (prefersDark ? 'dark' : 'light'), btn);
    btn.addEventListener('click', ()=>{
      const cur = document.documentElement.getAttribute('data-theme');
      const next = cur === 'dark' ? 'light' : 'dark';
      setTheme(next, btn);
      localStorage.setItem('theme', next);
    });
  }

  function makeCardsInteractive(scope=document){
    // For anchors and static cards
    const nodes = scope.querySelectorAll('.grid a.card, .card');
    nodes.forEach(el => {
      // ensure focusable
      if (el.tagName !== 'A') el.tabIndex = 0;
      el.addEventListener('mouseenter', ()=> el.classList.add('is-hover'));
      el.addEventListener('mouseleave', ()=> el.classList.remove('is-hover'));
      el.addEventListener('focus', ()=> el.classList.add('is-hover'));
      el.addEventListener('blur', ()=> el.classList.remove('is-hover'));
      // keyboard activation for non-anchor cards
      el.addEventListener('keydown', (e)=>{
        if(e.key === 'Enter' || e.key === ' ') {
          const a = el.querySelector('a');
          if(a) a.click();
        }
      });
    });
  }

  window.initUI = function(){
    initThemeToggle();
    makeCardsInteractive(document);
  };

  // auto-run on script load
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => { try{ window.initUI(); }catch(e){} });
  } else {
    try{ window.initUI(); }catch(e){}
  }
})();
