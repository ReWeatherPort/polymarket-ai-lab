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

  // Mobile nav toggle: insert hamburger and handle open/close
  function initMobileNav(){
    const navs = document.querySelectorAll('nav');
    navs.forEach(nav => {
      if (nav.querySelector('.nav-hamburger')) return; // already added
      const btn = document.createElement('button');
      btn.className = 'nav-hamburger btn-ghost';
      btn.setAttribute('aria-label','打開選單');
      btn.innerHTML = '☰';
      btn.style.display = 'none';
      btn.style.fontSize = '18px';
      btn.style.lineHeight = '1';
      btn.style.background = 'transparent';
      btn.style.border = 'none';
      btn.style.cursor = 'pointer';
      btn.addEventListener('click', ()=>{
        nav.classList.toggle('nav-open');
      });
      // Insert as first child for visual ordering
      nav.insertBefore(btn, nav.firstChild);
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
    initMobileNav();
  };

  // Lightweight toast notifications
  function createToastContainer(){
    let c = document.getElementById('toast-container');
    if(!c){
      c = document.createElement('div');
      c.id = 'toast-container';
      c.style.position = 'fixed';
      c.style.right = '20px';
      c.style.bottom = '20px';
      c.style.zIndex = 99999;
      c.style.display = 'flex';
      c.style.flexDirection = 'column';
      c.style.gap = '8px';
      document.body.appendChild(c);
    }
    return c;
  }

  function showToast(message, opts){
    opts = opts || {};
    const timeout = opts.timeout || 4500;
    const type = opts.type || 'default';
    const c = createToastContainer();
    const el = document.createElement('div');
    el.className = 'toast toast-' + type;
    el.textContent = message;
    // use theme-aware CSS classes instead of hard-coded inline colors
    el.classList.add(type === 'error' ? 'toast-error' : 'toast-default');
    el.style.padding = '10px 14px';
    el.style.borderRadius = '8px';
    el.style.boxShadow = '0 6px 24px rgba(2,6,23,0.15)';
    el.style.maxWidth = '320px';
    el.style.fontSize = '13px';
    el.style.opacity = '0';
    el.style.transition = 'opacity .18s ease, transform .18s ease';
    c.appendChild(el);
    requestAnimationFrame(()=>{ el.style.opacity = '1'; el.style.transform = 'translateY(0)'; });
    const tid = setTimeout(()=>{
      try{ el.style.opacity = '0'; el.style.transform = 'translateY(8px)'; setTimeout(()=>el.remove(),180); }catch(e){}
    }, timeout);
    el.addEventListener('click', ()=>{ clearTimeout(tid); el.remove(); });
    return el;
  }

  window.showToast = showToast;

  // auto-run on script load
  if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => { try{ window.initUI(); }catch(e){} });
  } else {
    try{ window.initUI(); }catch(e){}
  }
})();
