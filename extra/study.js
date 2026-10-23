/* Study layer. Everything is kept in this browser only (localStorage, keys starting "hb:").
   Views: #review (spaced review of the self-tests), #mock (timed interview), #plans (role tracks), #notes.
   It also saves every answer box, adds a status mark to each page, and opens all answers when printing. */
(function(){
  var S={
    get:function(k,d){try{var v=localStorage.getItem('hb:'+k);return v==null?d:JSON.parse(v)}catch(e){return d}},
    set:function(k,v){try{localStorage.setItem('hb:'+k,JSON.stringify(v))}catch(e){}},
    keys:function(){var o=[];try{for(var i=0;i<localStorage.length;i++){var k=localStorage.key(i);if(k&&k.indexOf('hb:')===0)o.push(k.slice(3))}}catch(e){}return o},
    del:function(k){try{localStorage.removeItem('hb:'+k)}catch(e){}}
  };
  var DAY=86400000,h=HB.h;
  function esc(s){return String(s).replace(/[&<>"]/g,function(c){return {'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]})}
  function frag(s){var t=document.createElement('template');t.innerHTML=s;return t.content}
  function ago(t){var d=Math.floor((Date.now()-t)/DAY);return d<=0?'today':d===1?'yesterday':d+' days ago'}
  function inDays(t){var d=Math.ceil((t-Date.now())/DAY);return d<=0?'now':d===1?'tomorrow':'in '+d+' days'}
  function hash(s){var x=5381;for(var i=0;i<s.length;i++)x=((x<<5)+x+s.charCodeAt(i))|0;return (x>>>0).toString(36)}
  function shuffle(a){for(var i=a.length-1;i>0;i--){var j=Math.floor(Math.random()*(i+1)),t=a[i];a[i]=a[j];a[j]=t}return a}
  function status(slug){var m=S.get('st',{});return m[slug]||null}
  function seen(){return S.get('seen',{})}
  function dotCls(slug){var st=status(slug);return st?st.v:(seen()[slug]?'seen':'')}
  var timer=null;

  /* ---------- navigation ---------- */
  var NAV=[['review','Review'],['mock','Mock interview'],['plans','Plans'],['notes','Notes']];
  (function(){var q=document.getElementById('nav-questions');if(!q)return;var after=q;
    NAV.forEach(function(n){var a=h('a',{href:'#'+n[0],id:'nav-'+n[0],'class':'xnav'});
      if(n[0]==='mock'){a.appendChild(h('span',{'class':'full'},n[1]));a.appendChild(h('span',{'class':'short'},'Mock'))}else a.textContent=n[1];after.parentNode.insertBefore(a,after.nextSibling);after=a})})();

  /* ---------- page enhancements ---------- */
  function onPage(slug,view){
    var sn=seen();if(!sn[slug]){sn[slug]=Date.now();S.set('seen',sn)}
    // status mark
    var top=view.querySelector('header.top'),lede=top&&top.querySelector('.lede');
    if(lede){
      var st=status(slug),m=h('div',{'class':'mark',role:'group','aria-label':'How well you know this page'});
      m.appendChild(h('span',{'class':'label'},'Your status'));
      var seg=h('div',{'class':'seg'});
      [['','Not yet'],['shaky','Shaky'],['solid','Solid']].forEach(function(o){
        var b=h('button',{type:'button','data-v':o[0],'aria-pressed':String((st?st.v:'')===o[0])},o[1]);
        b.addEventListener('click',function(){var all=S.get('st',{});if(o[0])all[slug]={v:o[0],t:Date.now()};else delete all[slug];S.set('st',all);
          seg.querySelectorAll('button').forEach(function(x){x.setAttribute('aria-pressed',String(x===b))});when.textContent=o[0]?'Marked '+o[1].toLowerCase()+' today':''});
        seg.appendChild(b)});
      m.appendChild(seg);
      var when=h('span',{'class':'when'},st?'Marked '+st.v+' '+ago(st.t):'');m.appendChild(when);
      var pr=h('button',{'class':'btn',type:'button'},'Print with answers');pr.addEventListener('click',function(){window.print()});m.appendChild(pr);
      lede.parentNode.insertBefore(m,lede.nextSibling);
    }
    // saved answer boxes
    view.querySelectorAll('textarea[id]').forEach(function(ta){
      var k='ta:'+ta.id,v=S.get(k,'');if(v)ta.value=v;
      if(ta.placeholder)ta.placeholder=ta.placeholder.replace('It stays on this page only.','Saved in this browser only.');
      var note=h('span',{'class':'saved','aria-live':'polite'},v?'Saved':'');ta.parentNode.insertBefore(note,ta.nextSibling);
      var t=null;ta.addEventListener('input',function(){clearTimeout(t);t=setTimeout(function(){
        if(ta.value.trim())S.set(k,ta.value);else S.del(k);S.set('tat:'+ta.id,Date.now());note.textContent=ta.value.trim()?'Saved':''},400)})});
  }

  /* ---------- home ---------- */
  function partsOf(){return Object.keys(HB.D.parts)}
  function dueCount(){var rv=S.get('rv',{}),n=0,now=Date.now();for(var k in rv)if(rv[k].d<=now)n++;return n}
  function onHome(view){
    var parts=document.getElementById('parts');if(!parts)return;
    var P=HB.D.pages,st=S.get('st',{}),solid=0,shaky=0;P.forEach(function(p){var s=st[p.slug];if(s&&s.v==='solid')solid++;else if(s&&s.v==='shaky')shaky++});
    var sn=seen(),opened=P.filter(function(p){return sn[p.slug]}).length,due=dueCount();
    var s='<section class="prog" aria-label="Your progress"><div class="prog-top"><b>Your progress</b><span>'+solid+' solid</span><span>'+shaky+' shaky</span><span>'+opened+' of '+P.length+' opened</span></div><div class="prog-parts">';
    partsOf().forEach(function(k){var ps=P.filter(function(p){return p.code[0]===k}),a=0,b=0;
      ps.forEach(function(p){var x=st[p.slug];if(x&&x.v==='solid')a++;else if(x&&x.v==='shaky')b++});
      s+='<div class="pp"><span>Part '+k+' · '+a+' of '+ps.length+' solid</span><div class="track"><i class="t-solid" style="width:'+(100*a/ps.length)+'%"></i><i class="t-shaky" style="width:'+(100*b/ps.length)+'%"></i></div></div>'});
    s+='</div><div class="go"><a class="pill'+(due?' hot':'')+'" href="#review">'+(due?'Review · '+due+' due':'Review queue')+'</a><a class="pill" href="#mock">Mock interview</a><a class="pill" href="#plans">Study plans</a><a class="pill" href="#notes">Your notes</a></div></section>';
    parts.parentNode.insertBefore(frag(s),parts);
  }
  HB.onlist=function(){
    document.querySelectorAll('#parts a.row').forEach(function(a){var slug=a.getAttribute('href').slice(1),b=a.querySelector('b');
      if(b&&!b.querySelector('.dot')){var c=dotCls(slug);b.insertBefore(h('i',{'class':'dot '+c,title:c==='solid'?'Solid':c==='shaky'?'Shaky':c==='seen'?'Opened':'Not opened'}),b.firstChild)}})};

  HB.onroute=function(cur,view){
    if(timer){clearInterval(timer);timer=null}
    NAV.forEach(function(n){var a=document.getElementById('nav-'+n[0]);if(a)a.setAttribute('aria-current',String(n[0]===cur))});
    if(HB.by[cur])onPage(cur,view);else if(cur==='')onHome(view);
    var t=HB.by[cur]?HB.by[cur].title+' · DS/ML Handbook':cur&&VIEWTITLE[cur]?VIEWTITLE[cur]+' · DS/ML Handbook':'DS/ML Learning Handbook';document.title=t;
  };
  var VIEWTITLE={mix:'Mixed self-test',questions:'Interview questions',review:'Review queue',mock:'Mock interview',plans:'Study plans',notes:'Your notes'};
  HB.views={};

  /* ---------- review queue ---------- */
  var INT=[1,3,7,14,30,60],rvPart='All',rvAll=false;
  function qkey(x){return x.s+'|'+x.n+'|'+hash(x.q)}
  function src(x){var p=HB.by[x.s];return '<a href="#'+x.s+'">'+p.code+' · '+esc(p.title)+'</a>'}
  HB.views.review=function(view){
    var D=HB.D,rv=S.get('rv',{}),sn=seen(),now=Date.now();
    var pool=D.quiz.filter(function(x){return HB.by[x.s]&&(rvPart==='All'||HB.by[x.s].code[0]===rvPart)});
    var due=pool.filter(function(x){var r=rv[qkey(x)];return r&&r.d<=now});
    var fresh=pool.filter(function(x){return !rv[qkey(x)]&&(rvAll||sn[x.s]||status(x.s))});
    var learned=pool.filter(function(x){var r=rv[qkey(x)];return r&&r.d>now}).length;
    var pick=shuffle(due.slice()).slice(0,10);if(pick.length<10)pick=pick.concat(shuffle(fresh.slice()).slice(0,10-pick.length));
    var s='<header class="top"><p class="label">Spaced review of '+D.quiz.length+' self-tests</p><h1>Review queue</h1>'+
      '<p class="lede">Questions you got right come back after longer and longer gaps: 1, 3, 7, 14, 30, then 60 days. Questions you missed come back tomorrow. New questions are drawn from pages you have opened.</p>'+
      '<div class="counts"><div class="stat"><span class="label">Due now</span><span class="v">'+due.length+'</span></div><div class="stat"><span class="label">Scheduled</span><span class="v">'+learned+'</span></div><div class="stat"><span class="label">New available</span><span class="v">'+fresh.length+'</span></div></div>'+
      '<div class="tools"><div class="seg" role="group" aria-label="Part">'+['All'].concat(partsOf()).map(function(P){return '<button type="button" data-part="'+P+'" aria-pressed="'+(P===rvPart)+'">'+(P==='All'?'All parts':'Part '+P)+'</button>'}).join('')+'</div>'+
      '<label><input type="checkbox" id="rvAll"'+(rvAll?' checked':'')+'> Include pages not opened yet</label><button class="btn" type="button" id="rvDeal">Deal again</button></div></header><div class="stack" id="rvStack">';
    if(!pick.length)s+='<p class="empty">'+(fresh.length||due.length?'':'Nothing due. Open a few pages, or tick "Include pages not opened yet", and new questions will appear here.')+'</p>';
    pick.forEach(function(x,i){var r=rv[qkey(x)];
      s+='<div class="card" data-i="'+i+'"><div class="meta"><span>'+src(x)+'</span><span>'+(r?'Box '+r.b+' · due '+inDays(r.d):'New')+'</span></div><p><strong>'+x.q+'</strong></p>'+
        '<details class="reveal"><summary><span class="when-closed">Show answer</span><span class="when-open">Hide answer</span></summary><div class="reveal-body">'+x.a+'</div></details>'+
        '<div class="grade" hidden><span>How did you do?</span><button class="btn miss" type="button" data-g="0">Missed it</button><button class="btn" type="button" data-g="1">Got it</button><span class="res"></span></div></div>'});
    view.replaceChildren(frag(s+'</div>'));
    view.querySelectorAll('[data-part]').forEach(function(b){b.addEventListener('click',function(){rvPart=b.getAttribute('data-part');HB.views.review(view)})});
    document.getElementById('rvAll').addEventListener('change',function(e){rvAll=e.target.checked;HB.views.review(view)});
    document.getElementById('rvDeal').addEventListener('click',function(){HB.views.review(view);window.scrollTo(0,0)});
    view.querySelectorAll('.card').forEach(function(c){var x=pick[+c.getAttribute('data-i')],g=c.querySelector('.grade');
      c.querySelector('details').addEventListener('toggle',function(e){if(e.target.open)g.hidden=false});
      g.querySelectorAll('button').forEach(function(b){b.addEventListener('click',function(){
        var all=S.get('rv',{}),k=qkey(x),r=all[k]||{b:0},ok=b.getAttribute('data-g')==='1';
        r.b=ok?Math.min((all[k]?r.b+1:1),INT.length-1):0;r.d=Date.now()+INT[r.b]*DAY;all[k]=r;S.set('rv',all);
        g.querySelectorAll('button').forEach(function(y){y.disabled=true});g.querySelector('.res').textContent='Back '+inDays(r.d)+'.';c.classList.add('done')})})});
  };

  /* ---------- mock interview ---------- */
  var mk={role:'all',rung:'hard',min:5,cur:null};
  var RN={1:'Recall',2:'Why',3:'What if',4:'Design',5:'Judgment'};
  function rungBody(x){
    var t=document.getElementById('pg-'+x.s);if(!t)return null;
    var r=t.content.querySelectorAll('.rung')[x.r-1];if(!r)return null;
    var b=r.querySelector('.reveal-body');return b?b.cloneNode(true):null;
  }
  HB.views.mock=function(view){
    var hist=S.get('mock',[]);
    var s='<header class="top"><p class="label">'+HB.D.ladder.length+' interview questions</p><h1>Mock interview</h1>'+
      '<p class="lede">One question at a time, against the clock. Answer out loud, jot the outline as you go, then open the follow-ups and the weak and strong answers and grade yourself honestly.</p>'+
      '<div class="tools"><div class="seg" role="group" aria-label="Role">'+[['all','All roles'],['lead','Lead'],['ic','IC'],['mle','MLE']].map(function(r){return '<button type="button" data-k="role" data-v="'+r[0]+'" aria-pressed="'+(mk.role===r[0])+'">'+r[1]+'</button>'}).join('')+'</div>'+
      '<div class="seg" role="group" aria-label="Rungs">'+[['all','Any rung'],['hard','What if, design, judgment']].map(function(r){return '<button type="button" data-k="rung" data-v="'+r[0]+'" aria-pressed="'+(mk.rung===r[0])+'">'+r[1]+'</button>'}).join('')+'</div>'+
      '<div class="seg" role="group" aria-label="Minutes">'+[3,5,8].map(function(m){return '<button type="button" data-k="min" data-v="'+m+'" aria-pressed="'+(mk.min===m)+'">'+m+' min</button>'}).join('')+'</div></div></header>'+
      '<div class="mock" id="mockBox"><button class="btn" type="button" id="mkGo">Draw a question</button></div>';
    if(hist.length){
      var g={0:'Weak',1:'Fair',2:'Strong'},tally=[0,0,0];hist.forEach(function(x){tally[x.g]++});
      s+='<section class="stack hist"><h2 class="label">Your last attempts · '+hist.length+' in all: '+tally[2]+' strong, '+tally[1]+' fair, '+tally[0]+' weak</h2><ul class="qlist">'+
        hist.slice(-12).reverse().map(function(x){var p=HB.by[x.s];return p?'<li><span>'+g[x.g]+'</span><a href="#'+x.s+'">'+p.code+' · '+esc(p.title)+'</a> · rung '+x.r+' · '+ago(x.t)+'</li>':''}).join('')+'</ul></section>';
    }
    view.replaceChildren(frag(s));
    view.querySelectorAll('[data-k]').forEach(function(b){b.addEventListener('click',function(){var k=b.getAttribute('data-k'),v=b.getAttribute('data-v');mk[k]=k==='min'?+v:v;HB.views.mock(view)})});
    document.getElementById('mkGo').addEventListener('click',function(){draw(view)});
  };
  function draw(view){
    var pool=HB.D.ladder.filter(function(x){return HB.by[x.s]&&(mk.role==='all'||x.roles.split(' ').indexOf(mk.role)>=0)&&(mk.rung==='all'||x.r>=3)});
    if(!pool.length)return;
    var x=pool[Math.floor(Math.random()*pool.length)],box=document.getElementById('mockBox'),left=mk.min*60;
    box.replaceChildren(frag('<p class="label">Rung '+x.r+' · '+RN[x.r]+'</p><p class="ask">'+esc(x.q)+'</p>'+
      '<div class="clockrow"><span class="clock" id="mkClock"></span><span id="mkMsg">Think for a few seconds, then answer out loud.</span></div>'+
      '<textarea id="mkNotes" placeholder="Outline your answer as you speak. Not saved."></textarea>'+
      '<div class="go"><button class="btn" type="button" id="mkShow">Open follow-ups and answers</button><button class="btn" type="button" id="mkSkip">Skip</button></div><div id="mkRub"></div>'));
    var clock=document.getElementById('mkClock');
    function tick(){var m=Math.floor(Math.abs(left)/60),s=Math.abs(left)%60;clock.textContent=(left<0?'+':'')+m+':'+(s<10?'0':'')+s;
      clock.className='clock'+(left<=0?' late':'');if(left===0)document.getElementById('mkMsg').textContent='Time. Close with one sentence: your recommendation.';left--}
    if(timer)clearInterval(timer);tick();timer=setInterval(tick,1000);
    document.getElementById('mkSkip').addEventListener('click',function(){draw(view)});
    document.getElementById('mkShow').addEventListener('click',function(){
      if(timer){clearInterval(timer);timer=null}
      var rub=document.getElementById('mkRub'),p=HB.by[x.s],body=rungBody(x);rub.className='rubric';
      rub.replaceChildren(frag('<p class="label">From <a href="#'+x.s+'">'+p.code+' · '+esc(p.title)+'</a></p>'));
      if(body)rub.appendChild(body);
      rub.appendChild(frag('<div class="grade"><span>Grade yourself against the strong answer:</span><button class="btn miss" type="button" data-g="0">Weak</button><button class="btn" type="button" data-g="1">Fair</button><button class="btn" type="button" data-g="2">Strong</button></div>'));
      rub.querySelectorAll('[data-g]').forEach(function(b){b.addEventListener('click',function(){
        var hist=S.get('mock',[]);hist.push({s:x.s,r:x.r,g:+b.getAttribute('data-g'),t:Date.now()});S.set('mock',hist.slice(-200));
        if(+b.getAttribute('data-g')===0){var st=S.get('st',{});if(!st[x.s]||st[x.s].v!=='shaky'){st[x.s]={v:'shaky',t:Date.now()};S.set('st',st)}}
        HB.views.mock(view);window.scrollTo(0,0);draw(view)})});
      document.getElementById('mkShow').disabled=true;
    });
  }

  /* ---------- study plans ---------- */
  var TRACKS={
    lead:{name:'Lead',blurb:'For DS leadership loops: judging evidence, running experiments as a programme, money, and running a team.',weeks:[
      ['Evidence a leader must read',['a1-bayes-base-rates','a2-p-values','a2-confidence-intervals','a2-multiple-testing','a1-clt']],
      ['Experiment design',['a3-experiment-design','a3-sample-size-power','a3-randomisation-unit','a3-validity-checks','a4-sequential-testing']],
      ['Beyond the simple test',['a4-interference','a4-noninferiority','a4-cuped','a5-confounding-dags','a5-diff-in-diff']],
      ['Metrics and product cases',['c3-metric-design','c3-metric-diagnosis','c3-launch-strategy','c3-problem-framing']],
      ['Money and targeting',['c4-unit-economics','c4-incrementality','a5-uplift-hte','a6-partial-pooling']],
      ['ML a leader must judge',['b4-precision-recall','b4-calibration','b1-validation-leakage','d3-monitoring-drift','d3-feedback-loops','b7-llm-evaluation']],
      ['Running the team',['e2-building-team','e2-prioritisation-capacity','e2-stakeholders-pushback','e1-exec-communication']],
      ['Responsibility and foundations',['e3-fairness','d1-data-quality','d1-data-modelling','d3-system-design']]]},
    ic:{name:'IC',blurb:'For senior and staff data scientist loops: probability, inference, experiments, causal inference, modelling, SQL and product cases.',weeks:[
      ['Probability',['a1-bayes-base-rates','a1-expectation-variance','a1-clt','a1-distributions','b0-likelihood-entropy']],
      ['Inference',['a2-p-values','a2-confidence-intervals','a2-multiple-testing','c2-bootstrap-simulation','a6-bayesian-updating']],
      ['Experiments',['a3-experiment-design','a3-sample-size-power','a3-randomisation-unit','a3-validity-checks','a4-cuped']],
      ['Advanced experiments',['a4-sequential-testing','a4-interference','a4-bandits','a4-noninferiority','a6-partial-pooling']],
      ['Causal inference',['a5-confounding-dags','a5-diff-in-diff','a5-matching-propensity','a5-instrumental-variables','a5-uplift-hte']],
      ['Modelling',['b1-bias-variance','b1-validation-leakage','b2-linear-regression','b2-logistic-regression','b3-gradient-boosting','b4-precision-recall']],
      ['SQL and coding',['c1-window-functions','c1-joins-nulls','c1-retention-funnels','c1-sessions-streaks','c2-pandas-patterns']],
      ['Product cases',['c3-metric-design','c3-metric-diagnosis','c3-launch-strategy','c3-problem-framing','c4-unit-economics','c4-incrementality']]]},
    mle:{name:'MLE',blurb:'For ML engineer and applied scientist loops: foundations, models, deep learning and LLMs, data and serving, and system design.',weeks:[
      ['Foundations',['b0-likelihood-entropy','b1-bias-variance','b1-regularisation','b1-validation-leakage','b2-linear-regression','b2-logistic-regression']],
      ['Trees and evaluation',['b3-decision-trees','b3-random-forests','b3-gradient-boosting','b3-feature-importance','b4-precision-recall','b4-roc-auc']],
      ['Evaluation in practice',['b4-class-imbalance','b4-calibration','a1-bayes-base-rates','a2-confidence-intervals','c2-ml-from-scratch']],
      ['Representations',['b5-kmeans','b5-pca','b5-embeddings','b6-backprop','b6-vanishing-gradients']],
      ['Deep learning and LLMs',['b6-optimisers-dropout','b6-debugging-training','b7-attention','b7-model-families-sampling','b7-rag-finetuning']],
      ['LLM systems and ranking',['b7-llm-evaluation','b7-agents-tools','b9-retrieval-ranking','b9-ranking-metrics','b9-position-bias']],
      ['Data and serving',['d2-feature-pipelines','d2-streaming','d2-distributed-processing','d3-serving-deployment','d3-monitoring-drift']],
      ['System design',['d3-system-design','d3-feedback-loops','b8-forecasting-backtests','e3-fairness','a3-experiment-design']]]}
  };
  HB.views.plans=function(view){
    var k=S.get('track','lead'),T=TRACKS[k]||TRACKS.lead,st=S.get('st',{});
    var s='<header class="top"><p class="label">Eight weeks, about five pages a week</p><h1>Study plans</h1>'+
      '<p class="lede">'+esc(T.blurb)+' Mark each page shaky or solid at the top of the page; a week is done when every page in it is solid.</p>'+
      '<div class="tools"><div class="seg" role="group" aria-label="Track">'+Object.keys(TRACKS).map(function(t){return '<button type="button" data-t="'+t+'" aria-pressed="'+(t===k)+'">'+TRACKS[t].name+' track</button>'}).join('')+'</div></div></header><div class="parts">';
    T.weeks.forEach(function(w,i){var ps=w[1].filter(function(x){return HB.by[x]}),done=ps.filter(function(x){return st[x]&&st[x].v==='solid'}).length;
      s+='<div class="week"><h3><span>Week '+(i+1)+' · '+esc(w[0])+'</span><small>'+done+' of '+ps.length+' solid</small></h3><ul class="plist">'+
        ps.map(function(x){var p=HB.by[x];return '<li><i class="dot '+dotCls(x)+'"></i><span class="c">'+p.code+'</span><a href="#'+x+'">'+esc(p.title)+'</a></li>'}).join('')+'</ul></div>'});
    view.replaceChildren(frag(s+'</div>'));
    view.querySelectorAll('[data-t]').forEach(function(b){b.addEventListener('click',function(){S.set('track',b.getAttribute('data-t'));HB.views.plans(view)})});
  };

  /* ---------- notes ---------- */
  function pageOfBox(id){var best=null;HB.D.pages.forEach(function(p){if(id.indexOf('ta-'+p.slug+'-')===0&&(!best||p.slug.length>best.slug.length))best=p});return best}
  HB.views.notes=function(view){
    var gaps=[],ones=[],tries=0;
    S.keys().forEach(function(k){if(k.indexOf('ta:')!==0)return;var id=k.slice(3),p=pageOfBox(id),v=S.get(k,'');if(!p||!v)return;
      var suf=id.slice(('ta-'+p.slug+'-').length),item={p:p,v:v,t:S.get('tat:'+id,0)};
      if(suf==='gap')gaps.push(item);else if(suf==='one')ones.push(item);else tries++});
    function byOrder(a,b){return a.p.i-b.p.i}gaps.sort(byOrder);ones.sort(byOrder);
    function list(items,empty){return items.length?items.map(function(x){return '<div class="note-item"><a href="#'+x.p.slug+'">'+x.p.code+' · '+esc(x.p.title)+'</a><p>'+esc(x.v)+'</p></div>'}).join(''):'<p class="empty">'+empty+'</p>'}
    var s='<header class="top"><p class="label">Kept in this browser only</p><h1>Your notes</h1>'+
      '<p class="lede">Everything you have written in the answer boxes. The open questions are the ones to bring to your next study session.</p>'+
      '<div class="tools"><button class="btn" type="button" id="ntCopy">Copy all as text</button><button class="btn" type="button" id="ntReset">Clear all progress and notes</button><span id="ntMsg"></span></div></header>'+
      '<section class="stack"><h2 class="label">Open questions · '+gaps.length+'</h2>'+list(gaps,'None yet. Section 11 of every page asks for one question you cannot answer.')+'</section>'+
      '<section class="stack"><h2 class="label">Your one-liners · '+ones.length+'</h2>'+list(ones,'None yet. Section 11 asks you to write the whole topic in one sentence.')+'</section>'+
      '<p class="empty">'+tries+' other attempts are saved on their pages.</p>';
    view.replaceChildren(frag(s));
    document.getElementById('ntCopy').addEventListener('click',function(){
      var t='OPEN QUESTIONS\n'+gaps.map(function(x){return '- ['+x.p.code+' '+x.p.title+'] '+x.v}).join('\n')+'\n\nONE-LINERS\n'+ones.map(function(x){return '- ['+x.p.code+' '+x.p.title+'] '+x.v}).join('\n');
      var msg=document.getElementById('ntMsg');
      try{navigator.clipboard.writeText(t).then(function(){msg.textContent='Copied.'},function(){msg.textContent='Copy failed.'})}catch(e){msg.textContent='Copy is not available here.'}});
    document.getElementById('ntReset').addEventListener('click',function(){
      if(!window.confirm('Clear every saved answer, status mark, review schedule and mock history in this browser?'))return;
      S.keys().forEach(function(k){S.del(k)});HB.views.notes(view)});
  };

  /* ---------- print: open every answer, then restore ---------- */
  var closed=[];
  window.addEventListener('beforeprint',function(){closed=[];document.querySelectorAll('details').forEach(function(d){if(!d.open){d.open=true;closed.push(d)}})});
  window.addEventListener('afterprint',function(){closed.forEach(function(d){d.open=false});closed=[]});
})();
