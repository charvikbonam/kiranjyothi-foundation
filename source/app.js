(function(){
'use strict';
var C = window.KRF_CONFIG;
var KEY = 'krf_achievements_v1';
var CATS = {
  academic:{label:'Academic',page:'academic.html',icon:'🎓'},
  social:{label:'Social Service',page:'social-service.html',icon:'🤝'},
  spiritual:{label:'Spiritual',page:'spiritual.html',icon:'🕉️'},
  agri:{label:'Agricultural',page:'agricultural.html',icon:'🌾'},
  family:{label:'Family & Child Counselling',page:'family-counselling.html',icon:'👨‍👩‍👧'},
  startups:{label:'Startups & Internships',page:'startups-internships.html',icon:'🚀'},
  general:{label:'Foundation News',page:'about.html',icon:'⭐'}
};
/* ---------- English / Telugu language switch ---------- */
var TE = {
 'Home':'హోమ్','About Us':'మా గురించి','Our Initiatives ▾':'మా కార్యక్రమాలు ▾','Achievements':'విజయాలు','Contact Us':'సంప్రదించండి',
 'Explore':'అన్వేషించండి','Explore →':'అన్వేషించండి →','Initiatives':'కార్యక్రమాలు','Reach us':'మమ్మల్ని సంప్రదించండి',
 'Chat on Telegram':'టెలిగ్రామ్‌లో చాట్ చేయండి','Message on Telegram':'టెలిగ్రామ్‌లో సందేశం పంపండి','Open Telegram chat':'టెలిగ్రామ్ చాట్ తెరవండి',
 'Telegram':'టెలిగ్రామ్','Share on Telegram':'టెలిగ్రామ్‌లో షేర్ చేయండి','Send via Telegram':'టెలిగ్రామ్ ద్వారా పంపండి',
 'Our story':'మా కథ','See achievements':'విజయాలు చూడండి','Read our full story →':'మా పూర్తి కథ చదవండి →','Read more →':'మరింత చదవండి →',
 'Since 2004 · For Academic & Rural Development':'2004 నుండి · విద్యా & గ్రామీణాభివృద్ధి కోసం',
 'Together for a Brighter Future…':'ఉజ్వల భవిష్యత్తు కోసం కలిసి…',
 'Years of service':'సేవా సంవత్సరాలు','Focus initiatives':'ప్రధాన కార్యక్రమాలు','Computer courses':'కంప్యూటర్ కోర్సులు','Year of registration':'నమోదైన సంవత్సరం',
 'Our focus areas':'మా ప్రధాన రంగాలు','Six initiatives, one mission':'ఆరు కార్యక్రమాలు, ఒకే లక్ష్యం',
 'Academic Initiatives':'విద్యా కార్యక్రమాలు','Social Service Initiatives':'సామాజిక సేవా కార్యక్రమాలు','Spiritual Initiatives':'ఆధ్యాత్మిక కార్యక్రమాలు',
 'Agricultural Initiatives':'వ్యవసాయ కార్యక్రమాలు','Social Service':'సామాజిక సేవ','Family & Child Counselling':'కుటుంబ & బాల సలహా','Startups & Internships':'స్టార్టప్‌లు & ఇంటర్న్‌షిప్‌లు',
 'Latest achievements':'తాజా విజయాలు','See all achievements →':'అన్ని విజయాలు చూడండి →','All achievements →':'అన్ని విజయాలు →','← All achievements':'← అన్ని విజయాలు',
 'Recent work':'ఇటీవలి పని','Our impact':'మా ప్రభావం','All':'అన్నీ',
 'Academic':'విద్య','Spiritual':'ఆధ్యాత్మిక','Agricultural':'వ్యవసాయం','Foundation News':'సంస్థ వార్తలు',
 'Gallery':'గ్యాలరీ','Our work in action':'ఆచరణలో మా పని','Our campus & community':'మా క్యాంపస్ & సమాజం','Moments from the field':'క్షేత్రం నుండి దృశ్యాలు',
 'What we do':'మేము చేసేది','Where it began':'ఇక్కడ మొదలైంది','Our promise':'మా వాగ్దానం',
 'Who we are':'మేము ఎవరం','Our aims':'మా లక్ష్యాలు','Why we exist':'మేము ఎందుకు ఉన్నాం','Our journey':'మా ప్రయాణం','Milestones':'ముఖ్య ఘట్టాలు',
 'Inside the Foundation':'సంస్థ లోపల','Our people':'మా బృందం','Leadership & team':'నాయకత్వం & బృందం','About us':'మా గురించి',
 'Get in touch':'మమ్మల్ని సంప్రదించండి','Let’s talk':'మాట్లాడుకుందాం','Send us a message':'మాకు సందేశం పంపండి','Your name':'మీ పేరు',
 'Phone / Telegram':'ఫోన్ / టెలిగ్రామ్','Topic':'విషయం','Message':'సందేశం','Address':'చిరునామా','Phone':'ఫోన్','Email':'ఇమెయిల్',
 'Office hours':'కార్యాలయ వేళలు','Find us':'మమ్మల్ని కనుగొనండి','Our location':'మా ప్రదేశం','Search':'వెతుకు',
 'Be part of the change':'మార్పులో భాగమవ్వండి',
 'Volunteer, donate or simply say hello. Message us on Telegram and we will reply personally.':'స్వచ్ఛందంగా సేవ చేయండి, విరాళం ఇవ్వండి, లేదా ఒక్క పలకరింపు పంపండి. టెలిగ్రామ్‌లో మాకు సందేశం పంపండి, మేము వ్యక్తిగతంగా బదులిస్తాం.',
 'Contact us':'మమ్మల్ని సంప్రదించండి','← All achievements ':'← అన్ని విజయాలు '
};
var PH = {'Search achievements…':'విజయాలను వెతకండి…'};
var LANG_KEY = 'krf_lang', curLang = 'en';
var origText = new WeakMap(), origHtml = new WeakMap(), origPh = new WeakMap();

function applyLang(){
  var te = curLang === 'te';
  document.documentElement.lang = te ? 'te' : 'en';
  document.querySelectorAll('[data-te]').forEach(function(el){
    if (te) { if (!origHtml.has(el)) origHtml.set(el, el.innerHTML); el.innerHTML = el.getAttribute('data-te'); }
    else if (origHtml.has(el)) { el.innerHTML = origHtml.get(el); origHtml.delete(el); }
  });
  document.querySelectorAll('[placeholder]').forEach(function(el){
    if (te) { if (!origPh.has(el)) origPh.set(el, el.placeholder); var k = origPh.get(el); if (PH[k]) el.placeholder = PH[k]; }
    else if (origPh.has(el)) { el.placeholder = origPh.get(el); origPh.delete(el); }
  });
  var w = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT, null), nodes = [], n;
  while ((n = w.nextNode())) { if (!/^(SCRIPT|STYLE|TEXTAREA|OPTION)$/.test(n.parentNode.nodeName)) nodes.push(n); }
  nodes.forEach(function(node){
    if (te) {
      if (!origText.has(node)) { if (!TE[node.nodeValue.trim()]) return; origText.set(node, node.nodeValue); }
      var o = origText.get(node), k = o.trim();
      if (TE[k]) node.nodeValue = o.replace(k, TE[k]);
    } else if (origText.has(node)) { node.nodeValue = origText.get(node); origText.delete(node); }
  });
  var b = document.getElementById('langBtn');
  if (b) b.textContent = te ? 'English' : 'తెలుగు';
}
function setLang(l){
  curLang = l === 'te' ? 'te' : 'en';
  try { localStorage.setItem(LANG_KEY, curLang); } catch (e) {}
  applyLang();
}
function initLang(){
  var b = document.getElementById('langBtn');
  if (b) b.addEventListener('click', function(){ setLang(curLang === 'te' ? 'en' : 'te'); });
  var saved = null; try { saved = localStorage.getItem(LANG_KEY); } catch (e) {}
  curLang = saved === 'te' ? 'te' : 'en';
  applyLang();
}

function $(s,r){return (r||document).querySelector(s)}
function $$(s,r){return Array.prototype.slice.call((r||document).querySelectorAll(s))}
function esc(s){return String(s==null?'':s).replace(/[&<>"']/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]})}
function fmtDate(d){if(!d)return '';var x=new Date(d+'T00:00:00');return isNaN(x)?d:x.toLocaleDateString('en-IN',{day:'numeric',month:'short',year:'numeric'})}

/* ---------- achievements data layer ---------- */
function loadPublished(){
  return fetch('data/achievements.json',{cache:'no-store'}).then(function(r){return r.ok?r.json():null})
   .then(function(j){return (Array.isArray(j)&&j.length)?j:(window.KRF_SEED||[])})
   .catch(function(){return window.KRF_SEED||[]});
}
function getLocal(){try{var v=localStorage.getItem(KEY);return v?JSON.parse(v):null}catch(e){return null}}
function saveLocal(list){localStorage.setItem(KEY,JSON.stringify(list))}
function clearLocal(){try{localStorage.removeItem(KEY)}catch(e){}}
function getAll(){
  var l=getLocal();
  var p=l?Promise.resolve(l):loadPublished();
  return p.then(function(list){return list.slice().sort(function(a,b){return (b.date||'').localeCompare(a.date||'')})});
}
function card(a){
  var c=CATS[a.category]||CATS.general, im=(a.images&&a.images[0])||'';
  return '<a class="ach-card rv" href="achievement.html?id='+encodeURIComponent(a.id)+'">'+
   '<div class="im">'+(im?'<img loading="lazy" src="'+esc(im)+'" alt="'+esc(a.title)+'">':c.icon)+'</div>'+
   '<div class="tx"><span class="badge">'+esc(c.label)+'</span><h3>'+esc(a.title)+'</h3>'+
   '<p>'+esc(a.summary)+'</p><span class="meta">'+esc(fmtDate(a.date))+' · <span>Read more →</span></span></div></a>';
}
function paragraphs(t){return String(t||'').split(/\n\s*\n/).map(function(p){return '<p>'+esc(p).replace(/\n/g,'<br>')+'</p>'}).join('')}

/* ---------- telegram ---------- */
function tgLink(){return 'https://t.me/'+encodeURIComponent(C.telegramUsername)}
function sendTelegram(text){
  if(C.telegramProxyUrl){
    return fetch(C.telegramProxyUrl,{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({text:text})}).then(function(r){return r.ok});
  }
  if(C.telegramBotToken&&C.telegramChatId){
    return fetch('https://api.telegram.org/bot'+C.telegramBotToken+'/sendMessage',{method:'POST',headers:{'Content-Type':'application/json'},
      body:JSON.stringify({chat_id:C.telegramChatId,text:text})}).then(function(r){return r.ok});
  }
  return Promise.resolve(null);
}

/* ---------- shared UI ---------- */
document.addEventListener('DOMContentLoaded',function(){
  initLang();
  var burger=$('.burger'),nav=$('nav.main');
  if(burger)burger.addEventListener('click',function(){var o=nav.classList.toggle('open');burger.setAttribute('aria-expanded',o)});
  $$('.dd>button').forEach(function(b){b.addEventListener('click',function(){b.parentNode.classList.toggle('open')})});

  // years of service
  $$('[data-years]').forEach(function(e){e.textContent=new Date().getFullYear()-C.founded});

  // counters
  var io=new IntersectionObserver(function(es){es.forEach(function(en){
    if(!en.isIntersecting)return; var el=en.target; io.unobserve(el);
    if(el.classList.contains('rv'))el.classList.add('in');
    var to=parseFloat(el.getAttribute('data-count')); if(isNaN(to))return;
    var t0=performance.now(); (function step(t){var p=Math.min((t-t0)/1400,1);el.textContent=Math.round(to*p).toLocaleString('en-IN')+(p===1?(el.getAttribute('data-suffix')||''):'');if(p<1)requestAnimationFrame(step)})(t0);
  })},{threshold:.15});
  function observe(){$$('.rv:not(.seen),[data-count]:not(.seen)').forEach(function(e){e.classList.add('seen');io.observe(e)});applyLang()}
  window.KRF_observe=observe; observe();

  // achievement lists
  $$('[data-achievements]').forEach(function(box){
    var cat=box.getAttribute('data-cat'),lim=parseInt(box.getAttribute('data-limit')||'0',10);
    getAll().then(function(all){
      if(cat)all=all.filter(function(a){return a.category===cat});
      if(lim)all=all.slice(0,lim);
      box.innerHTML=all.length?all.map(card).join(''):'<div class="empty">No achievements posted here yet. Check back soon!</div>';
      observe();
    });
  });

  // gallery lightbox
  var lb=$('.lightbox');
  if(lb){$$('.gallery img').forEach(function(i){i.addEventListener('click',function(){lb.innerHTML='<img src="'+i.src+'" alt="">';lb.classList.add('show')})});
    lb.addEventListener('click',function(){lb.classList.remove('show')});
    document.addEventListener('keydown',function(e){if(e.key==='Escape')lb.classList.remove('show')})}

  // telegram links
  $$('[data-tg]').forEach(function(a){a.href=tgLink();a.target='_blank';a.rel='noopener'});

  // contact form
  var cf=$('#contactForm');
  if(cf){cf.addEventListener('submit',function(e){
    e.preventDefault(); var s=$('#cfStatus'),btn=$('button',cf);
    var d={name:cf.name.value.trim(),phone:cf.phone.value.trim(),topic:cf.topic.value,msg:cf.message.value.trim()};
    var text='📩 New message from website\nName: '+d.name+'\nPhone: '+d.phone+'\nTopic: '+d.topic+'\n\n'+d.msg;
    btn.disabled=true; btn.textContent='Sending…';
    sendTelegram(text).then(function(ok){
      if(ok===true){s.className='status ok';s.textContent='Thank you! Your message was delivered to our Telegram. We will reply soon.';cf.reset()}
      else if(ok===null){
        var done=function(){s.className='status ok';s.textContent='Your message is copied. Telegram is opening — just paste and send it to us.';window.open(tgLink(),'_blank')};
        if(navigator.clipboard)navigator.clipboard.writeText(text).then(done,done);else done();
      } else {s.className='status err';s.textContent='Sorry, the message could not be sent. Please tap the Telegram button to message us directly.'}
    }).catch(function(){s.className='status err';s.textContent='Network error. Please message us on Telegram directly.'})
    .then(function(){btn.disabled=false;btn.textContent='Send via Telegram'});
  })}

  // achievements page (filters)
  var list=$('#achList');
  if(list){
    var state={cat:'all',q:''},all=[];
    var chips=$('#chips');
    chips.innerHTML='<button class="chip on" data-c="all">All</button>'+Object.keys(CATS).map(function(k){return '<button class="chip" data-c="'+k+'">'+CATS[k].icon+' '+CATS[k].label+'</button>'}).join('');
    function draw(){
      var r=all.filter(function(a){return (state.cat==='all'||a.category===state.cat)&&(!state.q||(a.title+' '+a.summary+' '+a.body).toLowerCase().indexOf(state.q)>-1)});
      list.innerHTML=r.length?r.map(card).join(''):'<div class="empty">No achievements match your search.</div>'; observe();
    }
    chips.addEventListener('click',function(e){var b=e.target.closest('.chip');if(!b)return;state.cat=b.getAttribute('data-c');$$('.chip',chips).forEach(function(c){c.classList.toggle('on',c===b)});draw()});
    $('#achSearch').addEventListener('input',function(e){state.q=e.target.value.toLowerCase();draw()});
    getAll().then(function(a){all=a;draw()});
  }

  // single achievement page
  var art=$('#article');
  if(art){
    var id=new URLSearchParams(location.search).get('id');
    getAll().then(function(all){
      var a=all.filter(function(x){return x.id===id})[0];
      if(!a){art.innerHTML='<div class="empty">Sorry, we could not find that achievement. <a href="achievements.html">See all achievements</a></div>';return}
      var c=CATS[a.category]||CATS.general; document.title=a.title+' — '+C.orgName;
      var imgs=(a.images||[]);
      art.innerHTML='<span class="badge">'+esc(c.label)+'</span><h1 style="font-size:clamp(2rem,4.5vw,3rem);margin:12px 0 8px">'+esc(a.title)+'</h1>'+
        '<p class="meta">'+esc(fmtDate(a.date))+'</p>'+
        (imgs[0]?'<div class="hero-img"><img src="'+esc(imgs[0])+'" alt="'+esc(a.title)+'"></div>':'')+
        '<p class="lead" style="margin-bottom:22px">'+esc(a.summary)+'</p><div class="body">'+paragraphs(a.body)+'</div>'+
        (imgs.length>1?'<div class="gallery" style="margin-top:30px">'+imgs.slice(1).map(function(s){return '<figure><img loading="lazy" src="'+esc(s)+'" alt=""></figure>'}).join('')+'</div>':'')+
        '<div style="display:flex;gap:12px;flex-wrap:wrap;margin-top:34px"><a class="btn blue" href="'+c.page+'">More in '+esc(c.label)+'</a>'+
        '<a class="btn tg" target="_blank" rel="noopener" href="https://t.me/share/url?url='+encodeURIComponent(location.href)+'&text='+encodeURIComponent(a.title)+'">Share on Telegram</a>'+
        '<a class="btn blue" style="background:#fff;color:var(--blue);border-color:var(--blue)" href="achievements.html">← All achievements</a></div>';
      applyLang(); var lb2=$('.lightbox'); $$('.gallery img,.hero-img img',art).forEach(function(i){i.style.cursor='zoom-in';i.addEventListener('click',function(){lb2.innerHTML='<img src="'+i.src+'" alt="">';lb2.classList.add('show')})});
    });
  }

  // admin panel
  if($('#adminApp'))initAdmin();
});

/* ---------- admin ---------- */
function initAdmin(){
  var login=$('#login'),app=$('#adminApp');
  function show(){login.style.display='none';app.style.display='block';refresh()}
  if(sessionStorage.getItem('krf_admin')==='1')show();
  $('#loginForm').addEventListener('submit',function(e){e.preventDefault();
    if($('#pw').value===C.adminPassword){sessionStorage.setItem('krf_admin','1');show()}
    else{var s=$('#loginStatus');s.className='status err';s.textContent='Wrong password.'}});
  $('#logout').addEventListener('click',function(){sessionStorage.removeItem('krf_admin');location.reload()});

  var cat=$('#f_cat');cat.innerHTML=Object.keys(CATS).map(function(k){return '<option value="'+k+'">'+CATS[k].label+'</option>'}).join('');
  var images=[],editId=null,items=[];
  function msg(t,ok){var s=$('#saveStatus');s.className='status '+(ok?'ok':'err');s.textContent=t}
  function thumbs(){$('#thumbs').innerHTML=images.map(function(s,i){return '<div><img src="'+esc(s)+'" alt=""><button type="button" data-i="'+i+'" title="Remove">×</button></div>'}).join('')}
  $('#thumbs').addEventListener('click',function(e){var b=e.target.closest('button');if(!b)return;images.splice(+b.getAttribute('data-i'),1);thumbs()});
  function compress(file,max){return new Promise(function(res,rej){var fr=new FileReader();fr.onload=function(){var im=new Image();im.onload=function(){
    var s=Math.min(1,max/Math.max(im.width,im.height)),c=document.createElement('canvas');c.width=Math.round(im.width*s);c.height=Math.round(im.height*s);
    c.getContext('2d').drawImage(im,0,0,c.width,c.height);res(c.toDataURL('image/jpeg',.78))};im.onerror=rej;im.src=fr.result};fr.onerror=rej;fr.readAsDataURL(file)})}
  $('#f_img').addEventListener('change',function(e){
    Promise.all(Array.prototype.map.call(e.target.files,function(f){return compress(f,1000)})).then(function(r){images=images.concat(r);thumbs();e.target.value=''}).catch(function(){msg('Could not read that image.',false)});
  });
  function refresh(){getAll().then(function(a){items=a;
    $('#count').textContent=a.length;
    $('#list').innerHTML=a.length?a.map(function(x){return '<div class="row"><div><b>'+esc(x.title)+'</b><br><small>'+esc((CATS[x.category]||CATS.general).label)+' · '+esc(fmtDate(x.date))+'</small></div>'+
      '<div style="display:flex;gap:8px;flex:none"><a class="mini" target="_blank" href="achievement.html?id='+encodeURIComponent(x.id)+'">View</a><button class="mini" data-e="'+esc(x.id)+'">Edit</button><button class="mini danger" data-d="'+esc(x.id)+'">Delete</button></div></div>'}).join(''):'<div class="empty">No achievements yet.</div>'})}
  function persist(list){try{saveLocal(list);return true}catch(e){msg('Browser storage is full. Use smaller or fewer images, or delete old entries after exporting.',false);return false}}
  function reset(){editId=null;images=[];$('#achForm').reset();$('#f_date').value=new Date().toISOString().slice(0,10);thumbs();$('#formTitle').textContent='Add a new achievement';$('#cancelEdit').style.display='none'}
  $('#f_date').value=new Date().toISOString().slice(0,10);
  $('#achForm').addEventListener('submit',function(e){e.preventDefault();
    var f=e.target,list=(getLocal()||items).slice();
    var rec={id:editId||(f.title_.value.toLowerCase().replace(/[^a-z0-9]+/g,'-').replace(/^-|-$/g,'').slice(0,40)+'-'+Date.now().toString(36)),
      title:f.title_.value.trim(),category:f.cat.value,date:f.date.value,summary:f.summary.value.trim(),body:f.body.value.trim(),images:images.slice()};
    var i=list.findIndex(function(x){return x.id===rec.id});
    if(i>-1)list[i]=rec;else list.unshift(rec);
    if(persist(list)){msg(editId?'Achievement updated.':'Achievement added! It now has its own page.',true);reset();refresh()}
  });
  $('#list').addEventListener('click',function(e){
    var ed=e.target.getAttribute('data-e'),dl=e.target.getAttribute('data-d');
    if(ed){var x=items.filter(function(a){return a.id===ed})[0];if(!x)return;editId=x.id;var f=$('#achForm');
      f.title_.value=x.title;f.cat.value=x.category;f.date.value=x.date;f.summary.value=x.summary;f.body.value=x.body;images=(x.images||[]).slice();thumbs();
      $('#formTitle').textContent='Edit achievement';$('#cancelEdit').style.display='inline-flex';scrollTo({top:$('#achForm').offsetTop-120,behavior:'smooth'})}
    if(dl&&confirm('Delete this achievement permanently?')){persist(items.filter(function(a){return a.id!==dl}));refresh()}
  });
  $('#cancelEdit').addEventListener('click',reset);
  $('#export').addEventListener('click',function(){
    var b=new Blob([JSON.stringify(items,null,1)],{type:'application/json'}),a=document.createElement('a');
    a.href=URL.createObjectURL(b);a.download='achievements.json';a.click();
  });
  $('#import').addEventListener('change',function(e){var fl=e.target.files[0];if(!fl)return;var fr=new FileReader();
    fr.onload=function(){try{var j=JSON.parse(fr.result);if(!Array.isArray(j))throw 0;if(persist(j)){msg('Imported '+j.length+' achievements.',true);refresh()}}catch(x){msg('That file is not a valid achievements.json.',false)}};fr.readAsText(fl);e.target.value=''});
  $('#resetPub').addEventListener('click',function(){if(confirm('Discard changes made in this browser and go back to the published list?')){clearLocal();refresh()}});
}
})();
