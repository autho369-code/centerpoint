(function(){
const d=document.documentElement;
requestAnimationFrame(()=>requestAnimationFrame(()=>d.classList.add('loaded')));

/* mobile menu */
const burger=document.querySelector('.burger');
const closeMenu=()=>{d.classList.remove('menu-open');if(burger){burger.setAttribute('aria-expanded','false');burger.setAttribute('aria-label','Open menu')}};
if(burger)burger.addEventListener('click',()=>{const o=d.classList.toggle('menu-open');burger.setAttribute('aria-expanded',o);burger.setAttribute('aria-label',o?'Close menu':'Open menu')});
document.querySelectorAll('.overlay a').forEach(a=>a.addEventListener('click',closeMenu));

/* desktop dropdowns */
const closeDD=()=>document.querySelectorAll('.dd.open').forEach(x=>{x.classList.remove('open');x.querySelector('.dd-btn').setAttribute('aria-expanded','false')});
document.querySelectorAll('.dd').forEach(dd=>{const b=dd.querySelector('.dd-btn');
  b.addEventListener('click',()=>{const o=!dd.classList.contains('open');closeDD();dd.classList.toggle('open',o);b.setAttribute('aria-expanded',o)});});
document.addEventListener('click',e=>{if(!e.target.closest('.dd'))closeDD()});
document.addEventListener('keydown',e=>{if(e.key==='Escape'){closeDD();closeMenu()}});

/* scroll reveal */
if('IntersectionObserver' in window){
  const io=new IntersectionObserver(es=>es.forEach(e=>{if(e.isIntersecting){e.target.classList.add('in');io.unobserve(e.target)}}),{threshold:.12});
  document.querySelectorAll('.reveal,.steps').forEach(el=>io.observe(el));
}else document.querySelectorAll('.reveal,.steps').forEach(el=>el.classList.add('in'));

/* forms: each form validates, then opens a pre-filled email to its own inbox (data-to) */
const EM=/^[^@\s]+@[^@\s]+\.[^@\s]+$/;
const check=i=>{const v=(i.value||'').trim();if(i.type==='checkbox')return !i.required||i.checked;
  if(i.type==='email')return v?EM.test(v):!i.required;return !i.required||!!v};
const mark=(i,good)=>{i.setAttribute('aria-invalid',!good);const fl=i.closest('.field');if(fl)fl.classList.toggle('bad',!good)};
document.querySelectorAll('form.cp-form').forEach(f=>{
  f.addEventListener('input',e=>{const i=e.target;if(i.closest('.field.bad')&&check(i))mark(i,true)});
  f.addEventListener('change',e=>{const i=e.target;if(i.type==='radio'){const g=i.closest('[data-radio]');if(g){g.removeAttribute('aria-invalid');mark(g.querySelector('input'),true)}return}if(i.closest('.field.bad')&&check(i))mark(i,true)});
  f.addEventListener('submit',e=>{e.preventDefault();let first=null;
    f.querySelectorAll('input,select,textarea').forEach(i=>{if(i.closest('[data-group],[data-radio]'))return;const good=check(i);mark(i,good);if(!good&&!first)first=i});
    f.querySelectorAll('[data-radio][data-req]').forEach(g=>{const good=!!g.querySelector('input:checked');const i=g.querySelector('input');mark(i,good);g.setAttribute('aria-invalid',!good);if(!good&&!first)first=i});
    const note=f.querySelector('.fnote');
    if(first){if(note)note.textContent='Please fix the highlighted fields.';first.focus();return}
    const lines=[];
    f.querySelectorAll('.field').forEach(fl=>{
      const g=fl.querySelector('[data-group]');
      if(g){const v=[...g.querySelectorAll('input:checked')].map(x=>x.value);if(v.length)lines.push(g.dataset.group+': '+v.join(', '));return}
      const r=fl.querySelector('[data-radio]');
      if(r){const c=r.querySelector('input:checked');if(c)lines.push(r.dataset.radio+': '+c.value);return}
      if(fl.classList.contains('fsec')){lines.push('\n'+fl.textContent.trim().toUpperCase());return}
      const i=fl.querySelector('input,select,textarea');if(!i)return;
      if(i.type==='checkbox'){if(i.checked)lines.push(i.dataset.l);return}
      const v=i.value.trim();if(!v)return;
      const l=fl.querySelector('label[for="'+i.id+'"]');const name=l?(l.dataset.l||l.textContent):i.name;
      lines.push(i.tagName==='TEXTAREA'?'\n'+name+':\n'+v:name+': '+v)});
    lines.push('\nSent from '+location.href);
    const to=f.dataset.to;
    location.href='mailto:'+to+'?subject='+encodeURIComponent(f.dataset.subject)+'&body='+encodeURIComponent(lines.join('\n'));
    if(note)note.textContent='Your email app should open with this filled in. Press send to deliver it. If nothing opens, email '+to+'.';
  });
});
})();
