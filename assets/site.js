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

/* forms: validate, then open a pre-filled email to the right inbox */
const f=document.getElementById('pform');
if(f)f.addEventListener('submit',e=>{e.preventDefault();let ok=true;
  [['n',v=>v.trim()],['e',v=>/^[^@\s]+@[^@\s]+\.[^@\s]+$/.test(v)]].forEach(([id,t])=>{const i=document.getElementById(id);if(!i)return;const good=!!t(i.value);i.setAttribute('aria-invalid',!good);i.parentElement.classList.toggle('bad',!good);if(!good)ok=false});
  const note=document.getElementById('fnote');
  if(!ok){if(note)note.textContent='Please fix the highlighted fields.';return}
  const resale=!!f.querySelector('input[name="docs"]');
  const to=resale?'sales@centerpointmgmt.com':'service@centerpointmgmt.com';
  const lines=[];
  f.querySelectorAll('input,select,textarea').forEach(i=>{
    if(i.type==='checkbox'){if(i.checked)lines.push('Document: '+i.parentElement.textContent.trim());return}
    const l=f.querySelector('label[for="'+i.id+'"]');if(i.value)lines.push((l?l.textContent:i.name)+': '+i.value)});
  const subj=resale?'Resale / lender document request':'Management proposal request';
  location.href='mailto:'+to+'?subject='+encodeURIComponent(subj)+'&body='+encodeURIComponent(lines.join('\n'));
  if(note)note.textContent='Your email app should open with the request filled in. If it does not, email '+to+'.';
});
})();
