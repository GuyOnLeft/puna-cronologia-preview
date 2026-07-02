#!/usr/bin/env python3
"""B — full draft. Year selector + editorial chapters, each with a large AUTO-RUNNING
captioned carousel (no click-to-enlarge). Bilingual, videos, all content, brand palette.
Data: tools/years.json (recovered from the deployed build). Writes ../index.html."""
import pathlib, json, sys
HERE = pathlib.Path(__file__).parent
YEARS = json.loads((HERE/"years.json").read_text())
OUTDIR = pathlib.Path(sys.argv[1]) if len(sys.argv)>1 else HERE.parent
DATA = json.dumps(YEARS, ensure_ascii=False)

HTML='''<!doctype html><html lang="es"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1"><title>Camino de Cambio</title>
<link href="https://fonts.googleapis.com/css2?family=Outfit:wght@500;600;700;800&family=DM+Sans:ital,wght@0,400;0,500;1,400&display=swap" rel="stylesheet">
<style>
:root{--bg:#ffead2;--fg:#2a1f2e;--coral:#ff5a4a;--secondary:#9e69b1;--accent:#79408d;--muted:#78677e;--card:#ffffff;--border:#d8cede;--yc:#ff5a4a}
*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--fg);font-family:"DM Sans",sans-serif;line-height:1.55}
h1,h2,h3,.ynum{font-family:"Outfit",sans-serif;margin:0;letter-spacing:-.02em}
a{color:inherit}
.nav{position:sticky;top:0;z-index:60;background:#2a1f2e;color:#ffe;display:flex;align-items:center;gap:12px;padding:11px 20px}
.nav b{color:var(--coral)}.nav .sp{margin-left:auto}
.nav a.map{font-size:13px;text-decoration:none;border:1px solid #fff3;padding:5px 13px;border-radius:999px}
.toggle{display:flex;border:1px solid #fff3;border-radius:999px;overflow:hidden}
.toggle button{background:transparent;color:#ffe;border:0;padding:5px 12px;font:inherit;font-size:12px;cursor:pointer}
.toggle button.on{background:var(--coral);color:#fff}
.hero{text-align:center;padding:54px 22px 26px}
.hero .eyebrow{text-transform:uppercase;letter-spacing:.22em;font-size:12px;color:var(--muted)}
.hero h1{font-size:clamp(40px,7vw,64px);font-weight:800;margin:8px 0 0}
.hero p{color:var(--muted);max-width:640px;margin:14px auto 0;font-size:17px}
.tabs{position:sticky;top:46px;z-index:55;background:var(--bg);display:flex;gap:8px;justify-content:center;flex-wrap:wrap;padding:14px 18px;border-bottom:1px solid var(--border)}
.tabs button{font:inherit;font-weight:700;font-size:15px;border:1px solid var(--border);background:var(--card);color:var(--fg);padding:8px 20px;border-radius:999px;cursor:pointer}
.ybody{max-width:1180px;margin:0 auto;padding:30px 22px 80px}
.yhead{display:flex;align-items:baseline;gap:14px;margin:6px 0 6px}
.yhead .ynum{font-size:clamp(40px,7vw,72px);font-weight:800;color:var(--yc)}
.yhead .ylabel{font-size:clamp(18px,2.3vw,26px);font-weight:600}
.yintro{color:var(--fg);opacity:.85;max-width:820px;font-size:16px;margin:0 0 30px}
.chapter{display:grid;grid-template-columns:0.82fr 1.18fr;gap:30px;align-items:start;margin:0 0 46px;padding-top:30px;border-top:1px solid var(--border)}
.chapter:first-of-type{border-top:0;padding-top:6px}
.isub{color:var(--yc);font-weight:700;font-size:12.5px;text-transform:uppercase;letter-spacing:.07em}
.chapter h3{font-size:24px;margin:6px 0 12px}
.chapter .txt p{color:var(--fg);opacity:.9;font-size:15.5px;margin:0 0 14px}
.vid{margin-top:12px}.vid video{width:100%;border-radius:12px;display:block;background:#2a1f2e}
.vid .vcap{font-size:12px;color:var(--muted);margin-top:6px}
.carousel{position:relative;border-radius:16px;overflow:hidden;background:#2a1f2e;box-shadow:0 20px 50px -30px #0007}
.track{display:flex;transition:transform .6s cubic-bezier(.22,.61,.36,1)}
.slide{min-width:100%;position:relative}
.slide img{width:100%;height:min(64vh,540px);object-fit:cover;display:block}
.slide figcaption{position:absolute;left:0;right:0;bottom:0;padding:34px 20px 16px;color:#fff;font-size:14.5px;background:linear-gradient(transparent,#000b)}
.cbtn{position:absolute;top:50%;transform:translateY(-50%);background:#0007;color:#fff;border:0;width:42px;height:42px;border-radius:50%;cursor:pointer;font-size:20px;display:flex;align-items:center;justify-content:center;opacity:0;transition:.2s}
.carousel:hover .cbtn{opacity:1}.prev{left:12px}.next{right:12px}
.dots{position:absolute;top:14px;right:14px;display:flex;gap:6px}
.dots i{width:7px;height:7px;border-radius:50%;background:#ffffff66;cursor:pointer;transition:.2s}
.dots i.on{background:#fff;width:20px;border-radius:6px}
.counter{position:absolute;top:12px;left:14px;background:#0007;color:#fff;font-size:11px;padding:3px 9px;border-radius:999px}
@media(max-width:820px){.chapter{grid-template-columns:1fr;gap:16px}.slide img{height:52vh}}
.chapter.solo{grid-template-columns:1fr;max-width:860px}
.soon{padding:16px 0 46px}
.soon-badge{display:inline-block;color:#fff;font-weight:700;font-size:13px;padding:8px 18px;border-radius:999px;letter-spacing:.06em;text-transform:uppercase}
.foot{background:#2a1f2e;color:#ffffffaa;text-align:center;padding:26px;font-size:13px}
</style></head><body>
<div class="nav"><b>Camino de Cambio</b>
  <span style="font-size:12px;opacity:.6" data-es="borrador · formato B" data-en="draft · format B">borrador · formato B</span>
  <span class="sp"></span>
  <div class="toggle"><button data-lang="es" class="on">ES</button><button data-lang="en">EN</button></div>
</div>
<div class="hero">
  <div class="eyebrow" data-es="Nuestro Impacto" data-en="Our Impact">Nuestro Impacto</div>
  <h1>Camino de Cambio</h1>
</div>
<div class="tabs" id="tabs"></div>
<div class="ybody" id="ybody"></div>
<div class="foot" data-es="Vista previa de diseño · Fundación Puna" data-en="Design preview · Fundación Puna">Vista previa · Fundación Puna</div>
<script>
const YEARS=__DATA__;
let LANG='es', activeYear=YEARS[0].year;
const tabsEl=document.getElementById('tabs'), body=document.getElementById('ybody');
let timers=[];
function clearTimers(){timers.forEach(t=>clearInterval(t));timers=[];}
function carouselHTML(it,cid){
  const slides=it.photos.map(p=>`<figure class="slide"><img loading="lazy" src="${p.u}" alt=""><figcaption>${p[LANG]}</figcaption></figure>`).join('');
  const dots=it.photos.map((_,i)=>`<i data-g="${i}" class="${i===0?'on':''}"></i>`).join('');
  return `<div class="carousel" id="${cid}"><div class="track">${slides}</div>`+
    (it.photos.length>1?`<button class="cbtn prev">‹</button><button class="cbtn next">›</button>`+
      `<div class="dots">${dots}</div><div class="counter"><span class="cur">1</span>/${it.photos.length}</div>`:'')+`</div>`;
}
function videoHTML(it){
  if(!it.video) return '';
  return `<div class="vid"><video src="${it.video.u}" controls playsinline preload="metadata"></video>`+
         `<div class="vcap">▶ ${it.video[LANG]}</div></div>`;
}
function renderYear(){
  const y=YEARS.find(x=>x.year===activeYear);
  document.documentElement.style.setProperty('--yc',y.color);
  tabsEl.querySelectorAll('button').forEach(b=>{const on=b.dataset.y===activeYear;
    b.style.background=on?y.color:'var(--card)';b.style.color=on?'#fff':'var(--fg)';b.style.borderColor=on?'transparent':'var(--border)';});
  let html=`<div class="yhead" style="--yc:${y.color}"><div class="ynum">${y.year}</div><div class="ylabel">${y['label_'+LANG]}</div></div>`+
           `<p class="yintro">${y['intro_'+LANG]||''}</p>`;
  if(!y.items.length){
    html+=`<div class="soon"><span class="soon-badge" style="background:${y.color}">${LANG==='es'?'Próximamente':'Coming soon'}</span></div>`;
  }
  y.items.forEach((it,idx)=>{const cid=`c_${y.year}_${idx}`; const hasPh=it.photos.length>0;
    html+=`<div class="chapter${hasPh?'':' solo'}" style="--yc:${y.color}"><div class="txt">`+
      (it['sub_'+LANG]?`<div class="isub">${it['sub_'+LANG]}</div>`:`<div class="isub">${y.year}</div>`)+
      `<h3>${it['t_'+LANG]}</h3><p>${it['text_'+LANG]}</p>${videoHTML(it)}</div>`+
      (hasPh?`<div>${carouselHTML(it,cid)}</div>`:'')+`</div>`;});
  clearTimers();
  body.innerHTML=html;
  y.items.forEach((it,idx)=>{if(it.photos.length>1)initCarousel(`c_${y.year}_${idx}`, it.photos.length);});
  window.scrollTo({top:0});
}
function initCarousel(id,n){
  if(n<=1) return;
  const el=document.getElementById(id); if(!el) return;
  const track=el.querySelector('.track'), dots=[...el.querySelectorAll('.dots i')], cur=el.querySelector('.cur');
  let i=0, timer=null;
  const go=k=>{i=(k+n)%n;track.style.transform=`translateX(${-i*100}%)`;dots.forEach((d,j)=>d.classList.toggle('on',j===i));if(cur)cur.textContent=i+1;};
  const start=()=>{timer=setInterval(()=>go(i+1),4200);timers.push(timer);};
  const reset=()=>{clearInterval(timer);start();};
  el.querySelector('.next').onclick=()=>{go(i+1);reset();};
  el.querySelector('.prev').onclick=()=>{go(i-1);reset();};
  dots.forEach(d=>d.onclick=()=>{go(+d.dataset.g);reset();});
  el.onmouseenter=()=>clearInterval(timer);
  el.onmouseleave=()=>start();
  start();
}
function buildTabs(){
  tabsEl.innerHTML=YEARS.map(y=>`<button data-y="${y.year}">${y.year}</button>`).join('');
  tabsEl.querySelectorAll('button').forEach(b=>b.onclick=()=>{activeYear=b.dataset.y;renderYear();});
}
function setLang(l){LANG=l;document.documentElement.lang=l;
  document.querySelectorAll('[data-es]').forEach(el=>{const v=el.getAttribute('data-'+l);if(v!==null)el.textContent=v;});
  document.querySelectorAll('.toggle button').forEach(b=>b.classList.toggle('on',b.dataset.lang===l));
  renderYear();
}
document.querySelectorAll('.toggle button').forEach(b=>b.onclick=()=>setLang(b.dataset.lang));
buildTabs(); renderYear();
</script></body></html>'''
HTML=HTML.replace("__DATA__",DATA)
(OUTDIR/"index.html").write_text(HTML,encoding="utf-8")
print("wrote",OUTDIR/"index.html","— B draft:",len(YEARS),"years,",sum(len(y["items"]) for y in YEARS),"chapters")
