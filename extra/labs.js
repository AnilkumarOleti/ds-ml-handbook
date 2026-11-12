/* Extra labs, added by tools/enhance.py. Spot values agree with the scripts in extra/check/. */

/* a3-experiment-design. extra/check/a3_design.py: 2,000 per arm per day for 14 days detects 0.71 pts on 10% and 13.5% relative on a 3% guardrail. */
HB.lab('a3design',{
  title:'What can a test of this length detect?',
  inputs:[
    {id:'p',label:'Primary metric baseline',vals:[0.02,0.05,0.1,0.2,0.3],value:0.1,fmt:function(v){return (v*100)+'%'}},
    {id:'u',label:'Users per arm per day',vals:[500,1000,2000,5000,10000,20000],value:2000,fmt:function(v){return HB.num(v)}},
    {id:'w',label:'Run length, whole weeks',min:1,max:8,step:1,value:2,fmt:function(v){return v+(v===1?' week':' weeks')}},
    {id:'g',label:'Guardrail baseline (refund rate)',vals:[0.01,0.02,0.03,0.05,0.1],value:0.03,fmt:function(v){return (v*100)+'%'}}
  ],
  run:function(v,HB){
    var z=HB.Phinv(0.975)+HB.Phinv(0.8);
    function mde(p,n){return z*Math.sqrt(2*p*(1-p)/n)}
    var n=v.u*7*v.w,m=mde(v.p,n),g=mde(v.g,n),W=[1,2,3,4,5,6,7,8];
    return {
      stats:[{k:'Users per arm',v:HB.num(n)},
        {k:'Smallest lift detectable',v:(100*m).toFixed(2)+' pts',s:HB.pct(m/v.p,1)+' relative'},
        {k:'Smallest guardrail harm',v:(100*g).toFixed(2)+' pts',s:HB.pct(g/v.g,1)+' relative'}],
      plot:{alt:'Smallest detectable relative change by run length, primary metric and guardrail',
        x:{label:'Weeks',min:1,max:8,ticks:W,fmt:function(x){return String(x)}},
        y:{label:'Smallest detectable change, relative',min:0,max:0.6,ticks:[0,0.15,0.3,0.45,0.6],fmt:function(y){return Math.round(y*100)+'%'}},
        series:[{name:'Primary',pts:W.map(function(w){return [w,mde(v.p,v.u*7*w)/v.p]})},
                {name:'Guardrail',pts:W.map(function(w){return [w,mde(v.g,v.u*7*w)/v.g]})}],
        dots:[{x:v.w,y:Math.min(0.6,m/v.p)}]},
      note:'Two-sided 5%, 80% power. Doubling the run length shrinks every detectable change by only 1/√2. A rare guardrail sees only large harms at the length that suits the primary metric.'}
  }
});

/* b0-likelihood-entropy. extra/check/b0.py: 12 of 200 gives 3.3% to 9.9%; 120 of 2,000 gives 5.0% to 7.1%. */
HB.lab('likelihood',{
  title:'The log-likelihood of a rate',
  inputs:[
    {id:'n',label:'Sellers shown the tool',vals:[20,50,200,1000,2000,5000],value:200,fmt:function(v){return HB.num(v)}},
    {id:'r',label:'Share who used it',vals:[0.01,0.02,0.04,0.06,0.1,0.2,0.4],value:0.06,fmt:function(v){return (v*100)+'%'}}
  ],
  run:function(v,HB){
    var n=v.n,k=Math.max(1,Math.round(v.r*n)),m=k/n;
    function ll(p){return k*Math.log(p)+(n-k)*Math.log(1-p)}
    var top=ll(m);function rel(p){return ll(p)-top}
    function root(a,b){for(var i=0;i<80;i++){var c=(a+b)/2;if((rel(a)+1.92)*(rel(c)+1.92)<=0)b=c;else a=c}return (a+b)/2}
    var lo=root(1e-9,m),hi=root(m,1-1e-9),xmax=Math.min(1,Math.max(0.1,Math.ceil(Math.max(hi*1.25,m*2)*20)/20));
    var pts=HB.range(xmax/400,xmax*(1-1e-6),200).map(function(p){return [p,Math.max(-8,rel(p))]});
    var se=Math.sqrt(m*(1-m)/n);
    return {
      stats:[{k:'Observed',v:k+' of '+HB.num(n)},{k:'Maximum likelihood',v:HB.pct(m,1)},
        {k:'95% likelihood interval',v:HB.pct(lo,1)+' to '+HB.pct(hi,1),s:'normal shortcut '+HB.pct(Math.max(0,m-1.96*se),1)+' to '+HB.pct(m+1.96*se,1)}],
      plot:{alt:'Log-likelihood relative to its peak, by rate',
        x:{label:'Rate',min:0,max:xmax,fmt:function(x){return Math.round(x*1000)/10+'%'}},
        y:{label:'Log-likelihood minus its peak',min:-8,max:0,ticks:[-8,-6,-4,-1.92,0],fmt:function(y){return String(+y.toFixed(2))}},
        series:[{pts:pts}],refs:[{y:-1.92,label:'1.92 below the peak',right:true},{x:lo,label:'',left:true},{x:hi,label:''}],dots:[{x:m,y:0}]},
      note:'Every rate inside the interval is within 1.92 log-units of the best one, a likelihood ratio of about 6.8. More data makes the curve steeper, so the interval narrows with √n.'}
  }
});

/* c4-incrementality. extra/check/c4b.py: 4,000,000 users, 1.95% base, true lift 0.05 pts: 10% holdout has power 0.58 and +-1,626 orders; 20% has 0.82. */
HB.lab('holdout',{
  title:'How big should the holdout be?',
  inputs:[
    {id:'h',label:'Share held out',vals:[0.01,0.02,0.05,0.1,0.2,0.3,0.5],value:0.1,fmt:function(v){return Math.round(v*100)+'%'}},
    {id:'N',label:'Eligible users a month',vals:[500000,1000000,2000000,4000000,10000000],value:4000000,fmt:function(v){return (v/1e6)+' million'}},
    {id:'p',label:'Conversion without ads',vals:[0.005,0.0195,0.05],value:0.0195,fmt:function(v){return (v*100)+'%'}},
    {id:'d',label:'True lift from the ads',vals:[0.0002,0.0005,0.001,0.002],value:0.0005,fmt:function(v){return '+'+(v*100).toFixed(2)+' pts'}}
  ],
  run:function(v,HB){
    function calc(h){var ne=v.N*(1-h),nh=v.N*h,pe=v.p+v.d,se=Math.sqrt(pe*(1-pe)/ne+v.p*(1-v.p)/nh);
      return {ne:ne,se:se,power:HB.Phi(v.d/se-1.96)+HB.Phi(-v.d/se-1.96)}}
    var c=calc(v.h),inc=c.ne*v.d,half=1.96*c.se*c.ne,H=[0.01,0.02,0.05,0.1,0.2,0.3,0.4,0.5];
    return {
      stats:[{k:'Incremental orders',v:HB.num(inc),s:'95% interval about '+HB.num(Math.max(-1e9,inc-half))+' to '+HB.num(inc+half)},
        {k:'Chance of detecting it',v:HB.pct(c.power,0)},
        {k:'Cost of the holdout',v:HB.num(v.N*v.h*v.d)+' orders',s:'the effect the held-out users miss'}],
      plot:{alt:'Power to detect the lift by holdout share',
        x:{label:'Share held out',min:0,max:0.5,ticks:[0,0.1,0.2,0.3,0.4,0.5],fmt:function(x){return Math.round(x*100)+'%'}},
        y:{label:'Chance of detecting the lift',min:0,max:1,ticks:[0,0.2,0.4,0.6,0.8,1],fmt:function(y){return Math.round(y*100)+'%'}},
        series:[{pts:HB.range(0.01,0.5,50).map(function(h){return [h,calc(h).power]})}],refs:[{y:0.8,label:'80%',right:true}],dots:[{x:v.h,y:c.power}]},
      note:'The smaller group sets the precision, so moving users into a small holdout helps a lot at first and then less and less. The cost of the holdout grows in a straight line.'}
  }
});

/* d3-system-design. extra/check/d3s.py: capacity 80,000 gives 634.6 lakh a day and 5,000 genuine listings blocked; 50,000 gives 670.6 and 21,000. */
HB.lab('triage',{
  title:'Triage with limited reviewers, 1 crore listings a day',
  inputs:[
    {id:'cap',label:'Reviews a day',vals:[0,20000,50000,80000,150000,300000],value:80000,fmt:function(v){return HB.num(v)}},
    {id:'miss',label:'Cost of a missed counterfeit',vals:[500,1000,2000,5000],value:2000,fmt:function(v){return '₹'+HB.num(v)}},
    {id:'blk',label:'Cost of blocking a genuine listing',vals:[100,300,1000,3000],value:300,fmt:function(v){return '₹'+HB.num(v)}},
    {id:'rev',label:'Cost of one review',vals:[20,40,80],value:40,fmt:function(v){return '₹'+v}}
  ],
  run:function(v,HB){
    var B=[['Very high',0.95,20000],['High',0.6,30000],['Medium',0.2,60000],['Low',0.05,200000],['Very low',0.002,9690000]];
    function auto(p){return Math.min(p*v.miss,(1-p)*v.blk)}
    var order=B.slice().sort(function(a,b){return (auto(b[1])-v.rev)-(auto(a[1])-v.rev)}),left=v.cap,R={};
    order.forEach(function(b){var r=auto(b[1])>v.rev?Math.min(b[2],left):0;R[b[0]]=r;left-=r});
    var cost=0,stopped=0,bad=0,gb=0,rows=[],items=[];
    B.forEach(function(b){var p=b[1],n=b[2],r=R[b[0]],rest=n-r,block=(1-p)*v.blk<p*v.miss;bad+=p*n;
      cost+=r*v.rev+rest*auto(p);stopped+=r*p+(block?rest*p:0);if(block)gb+=rest*(1-p);
      rows.push([b[0],HB.num(n),HB.num(r),(rest?(block?'block ':'allow ')+HB.num(rest):'none')]);
      items.push({label:b[0],value:n?r/n:0,text:HB.pct(n?r/n:0,0)+' reviewed',cls:'s1'})});
    return {
      stats:[{k:'Cost a day',v:'₹'+HB.num(cost/1e5,1)+' lakh'},{k:'Counterfeits stopped',v:HB.pct(stopped/bad,1),s:HB.num(stopped)+' of '+HB.num(bad)},
        {k:'Genuine listings blocked',v:HB.num(gb)},{k:'Reviews unused',v:HB.num(Math.max(0,left))}],
      bars:{title:'Share of each band sent to reviewers',max:1,items:items},
      table:{head:['Band','Listings','Reviewed','The rest'],rows:rows},
      note:'Reviews go first to the band where a review saves most over the best automatic action. That is usually the uncertain middle, not the band the model is surest about.'}
  }
});

/* e1-exec-communication. extra/check/e1.py: 2.0% to 2.3%, 3 million visitors, Rs 900 an order: 9,000 orders, Rs 81 lakh a month; axis from 1.9% gives a lie factor of 20. */
HB.lab('framing',{
  title:'One effect, four ways to say it',
  inputs:[
    {id:'b',label:'Conversion before',vals:[0.005,0.01,0.02,0.05,0.1],value:0.02,fmt:function(v){return (v*100)+'%'}},
    {id:'d',label:'Change in points',vals:[0.001,0.002,0.003,0.005,0.01],value:0.003,fmt:function(v){return '+'+(v*100).toFixed(1)+' pts'}},
    {id:'n',label:'Visitors a month',vals:[300000,1000000,3000000,10000000],value:3000000,fmt:function(v){return HB.num(v)}},
    {id:'ax',label:'Chart axis starts at, share of the lower value',vals:[0,0.5,0.8,0.9,0.95],value:0.95,fmt:function(v){return Math.round(v*100)+'%'}}
  ],
  run:function(v,HB){
    var a=v.b,b=v.b+v.d,orders=v.n*v.d,money=orders*900,start=v.ax*a;
    var vis=(b-start)/(a-start),lie=(vis-1)/(b/a-1);
    return {
      stats:[{k:'Absolute',v:'+'+(v.d*100).toFixed(1)+' pts'},{k:'Relative',v:'+'+HB.pct(v.d/a,0)},
        {k:'Per 1,000 visitors',v:'+'+HB.num(1000*v.d,1)+' orders'},{k:'Contribution a month',v:'₹'+HB.num(money/1e5,1)+' lakh',s:'at ₹900 an order'}],
      bars:{title:'The two bars as drawn, axis from '+(start*100).toFixed(2)+'% · lie factor '+lie.toFixed(1),max:Math.max(1,vis),
        items:[{label:'Before '+HB.pct(a,1),value:1,text:'1.00',cls:'s0'},{label:'After '+HB.pct(b,1),value:vis,text:vis.toFixed(2)+'×',cls:'s1'}]},
      note:'The money depends only on the change in points and the traffic. The relative figure also depends on the base, and the chart\'s height ratio on where the axis starts.'}
  }
});

/* e2-building-team. extra/check/e2b.py: 4 hires at 30/50/45/35/70% need 242 applications and 233 interviewer hours. */
HB.lab('funnel',{
  title:'Hiring funnel, worked backwards',
  inputs:[
    {id:'hires',label:'Hires needed',min:1,max:10,step:1,value:4,fmt:function(v){return String(v)}},
    {id:'ph',label:'Phone screen pass',vals:[0.3,0.4,0.5,0.6],value:0.5,fmt:function(v){return Math.round(v*100)+'%'}},
    {id:'on',label:'Onsite pass',vals:[0.25,0.35,0.5,0.65],value:0.35,fmt:function(v){return Math.round(v*100)+'%'}},
    {id:'acc',label:'Offers accepted',vals:[0.4,0.5,0.6,0.7,0.85],value:0.7,fmt:function(v){return Math.round(v*100)+'%'}}
  ],
  run:function(v,HB){
    var S=[['Application screen',0.3,0.1],['Phone screen',v.ph,1.0],['Take-home and review',0.45,1.5],['Onsite loop',v.on,5.0],['Offer',v.acc,0]];
    var need=v.hires,ent=[];for(var i=S.length-1;i>=0;i--){need=need/S[i][1];ent[i]=need}
    var hours=0,items=[];S.forEach(function(s,i){var hh=ent[i]*s[2];hours+=hh;items.push({label:s[0],value:ent[i],text:HB.num(ent[i])+(s[2]?' · '+HB.num(hh)+' h':''),cls:i===3?'s2':'s1'})});
    return {
      stats:[{k:'Applications',v:HB.num(ent[0]),s:HB.num(ent[0]/v.hires)+' per hire'},{k:'Interviewer hours',v:HB.num(hours),s:'about '+HB.num(hours/40,1)+' working weeks'},
        {k:'Onsite loops',v:HB.num(ent[3])}],
      bars:{title:'Candidates entering each stage, and interviewer hours',max:ent[0],items:items},
      note:'Every stage scales with the stages after it, so a candidate lost at the offer costs the most. Hours per candidate: 0.1 screen, 1 phone, 1.5 take-home review, 5 onsite.'}
  }
});

/* e3-fairness. extra/check/e3.py: separation 2.5, threshold 1.66 gives 80% recall, 4.9% FPR, precision 40.7% at 4% and 14.3% at 1%. */
HB.lab('fairness',{
  title:'One model, two groups of sellers',
  inputs:[
    {id:'pa',label:'Counterfeit rate, new sellers',vals:[0.01,0.02,0.04,0.08],value:0.04,fmt:function(v){return (v*100)+'%'}},
    {id:'pb',label:'Counterfeit rate, established',vals:[0.005,0.01,0.02,0.04],value:0.01,fmt:function(v){return (v*100)+'%'}},
    {id:'ta',label:'Threshold, new sellers',min:0.5,max:3.5,step:0.01,value:1.66,fmt:function(v){return v.toFixed(2)}},
    {id:'tb',label:'Threshold, established',min:0.5,max:3.5,step:0.01,value:1.66,fmt:function(v){return v.toFixed(2)}}
  ],
  run:function(v,HB){
    var d=2.5;
    function g(pi,t){var tpr=1-HB.Phi(t-d),fpr=1-HB.Phi(t),tp=tpr*pi,fp=fpr*(1-pi);return {tpr:tpr,fpr:fpr,prec:tp/(tp+fp),sel:tp+fp,wrong:fpr*(1-pi)*10000}}
    var A=g(v.pa,v.ta),B=g(v.pb,v.tb),ratio=Math.min(A.sel,B.sel)/Math.max(A.sel,B.sel);
    return {
      stats:[{k:'Precision of a flag',v:HB.pct(A.prec,0)+' · '+HB.pct(B.prec,0),s:'new · established'},
        {k:'Counterfeits caught',v:HB.pct(A.tpr,0)+' · '+HB.pct(B.tpr,0)},
        {k:'Genuine sellers flagged',v:HB.pct(A.fpr,1)+' · '+HB.pct(B.fpr,1),s:HB.num(A.wrong)+' · '+HB.num(B.wrong)+' per 10,000'},
        {k:'Selection-rate ratio',v:ratio.toFixed(2),s:ratio<0.8?'below four fifths':'at or above four fifths'}],
      table:{head:['','New sellers','Established'],rows:[
        ['Flagged',HB.pct(A.sel,2),HB.pct(B.sel,2)],['Caught (recall)',HB.pct(A.tpr,1),HB.pct(B.tpr,1)],
        ['Genuine flagged (FPR)',HB.pct(A.fpr,2),HB.pct(B.fpr,2)],['Flags that are right (precision)',HB.pct(A.prec,1),HB.pct(B.prec,1)]]},
      note:'Scores for counterfeit sellers sit 2.5 standard deviations above genuine ones in both groups, so the model is equally good for each. Equal thresholds give equal error rates; equal precision needs different thresholds, unless the base rates match.'}
  }
});

/* a4-long-term-effects. extra/check/a4_longterm.py: 8% first day, 1.5% lasting, time constant 4 days (half-life 2.8): 14-day average 3.54%, 2.4x the lasting lift; within 1.5x after 40 days. */
HB.lab('novelty',{
  title:'How much novelty is in the test average?',
  inputs:[
    {id:'e',label:'Lift on day 1',vals:[0.02,0.04,0.08,0.12],value:0.08,fmt:function(v){return '+'+(v*100)+'%'}},
    {id:'l',label:'Lasting lift',vals:[0,0.005,0.01,0.015,0.02,0.03],value:0.015,fmt:function(v){return '+'+(v*100).toFixed(1)+'%'}},
    {id:'h',label:'Half-life of the novelty',vals:[1,2,2.7726,4,7,14],value:2.7726,fmt:function(v){return v.toFixed(v%1?1:0)+' days'}},
    {id:'t',label:'Test length',vals:[7,14,21,28,42,56],value:14,fmt:function(v){return v+' days'}}
  ],
  run:function(v,HB){
    var tau=v.h/Math.LN2,l=Math.min(v.l,v.e);
    function eff(d){return l+(v.e-l)*Math.exp(-(d-1)/tau)}
    function avg(T){var s=0;for(var d=1;d<=T;d++)s+=eff(d);return s/T}
    var D=HB.range(1,60,60),a=avg(v.t),ymax=Math.max(0.02,Math.ceil(v.e*100/2)*2/100);
    return {
      stats:[{k:'Test average',v:'+'+HB.pct(a,2)},{k:'Last day of the test',v:'+'+HB.pct(eff(v.t),2)},
        {k:'Overstatement',v:l>0?(a/l).toFixed(1)+'×':'all novelty',s:'test average ÷ lasting lift'}],
      plot:{alt:'Daily lift and running average by day',
        x:{label:'Day of test',min:1,max:60,ticks:[1,14,28,42,56],fmt:function(x){return String(Math.round(x))}},
        y:{label:'Lift',min:0,max:ymax,fmt:function(y){return Math.round(y*1000)/10+'%'}},
        series:[{name:'Lift that day',pts:D.map(function(d){return [d,eff(d)]})},{name:'Running average',pts:D.map(function(d){return [d,avg(d)]})}],
        refs:[{y:l,label:'lasting',right:true},{x:v.t,label:'end of test'}],dots:[{x:v.t,y:a}]},
      note:'The running average falls far more slowly than the daily lift, because the first days stay in it. Read the last days, the new users, or a holdout.'}
  }
});

/* a5-balance-overlap. extra/check/a5_balance.py: log-odds propensities sd 1, centres 2 apart, trim at 0.1/0.9 keeps 88.4% of each group; 3 apart keeps 75.7%. */
HB.lab('overlap',{
  title:'How much do you lose to trimming?',
  inputs:[
    {id:'d',label:'Distance between group centres, log-odds',vals:[0.5,1,2,3,4],value:2,fmt:function(v){return String(v)}},
    {id:'a',label:'Trim below a and above 1 − a',vals:[0,0.01,0.05,0.1,0.2],value:0.1,fmt:function(v){return v?String(v):'none'}}
  ],
  run:function(v,HB){
    var mt=v.d/2,mc=-v.d/2,lo=v.a?Math.log(v.a/(1-v.a)):-99,hi=-lo;
    function pdf(x,m){return Math.exp(-0.5*(x-m)*(x-m))/Math.sqrt(2*Math.PI)}
    var kt=HB.Phi(hi-mt)-HB.Phi(lo-mt),kc=HB.Phi(hi-mc)-HB.Phi(lo-mc),X=HB.range(-6,6,121);
    var refs=v.a?[{x:lo,label:'trim'},{x:hi,label:'trim',right:true}]:[];
    return {
      stats:[{k:'Joiners kept',v:HB.pct(kt,1)},{k:'Non-joiners kept',v:HB.pct(kc,1)},
        {k:'Largest control weight (ATT)',v:v.a?((1-v.a)/v.a).toFixed(1):'unbounded',s:'e ÷ (1 − e) at the upper cut'}],
      plot:{alt:'Propensity score distributions on the log-odds scale by group',
        x:{label:'Propensity score',min:-6,max:6,ticks:[-4.595,-2.197,0,2.197,4.595],fmt:function(x){var p=1/(1+Math.exp(-x));return (Math.round(p*100)/100).toString()}},
        y:{label:'Density',min:0,max:0.45,ticks:[0,0.1,0.2,0.3,0.4],fmt:function(y){return y.toFixed(1)}},
        series:[{name:'Joined',pts:X.map(function(x){return [x,pdf(x,mt)]})},{name:'Did not join',pts:X.map(function(x){return [x,pdf(x,mc)]})}],refs:refs},
      note:'The joiners lost to trimming are the ones most unlike any non-joiner. The estimate that remains describes the joiners who had comparable non-joiners.'}
  }
});

/* a5-its-causalimpact. extra/check/a5_its.py: 26 pre weeks, sd 3, 8-week average: 95% half-width 3.53; 8 pre weeks 7.83; 52 pre weeks 2.76. */
HB.lab('its',{
  title:'How precise is a forecast counterfactual?',
  inputs:[
    {id:'n',label:'Weeks of pre-period',vals:[8,13,26,52,104],value:26,fmt:function(v){return v+' weeks'}},
    {id:'s',label:'Week-to-week noise, thousand orders',vals:[1,2,3,5,8],value:3,fmt:function(v){return String(v)}},
    {id:'h',label:'Weeks measured after launch',vals:[2,4,8,16,26],value:8,fmt:function(v){return v+' weeks'}}
  ],
  run:function(v,HB){
    var n=v.n,tb=(n+1)/2,Sxx=n*(n*n-1)/12;
    function band(t){return 1.96*v.s*Math.sqrt(1+1/n+(t-tb)*(t-tb)/Sxx)}
    var mid=n+(v.h+1)/2,line=v.s*Math.sqrt(1/n+(mid-tb)*(mid-tb)/Sxx),noise=v.s/Math.sqrt(v.h),se=Math.sqrt(line*line+noise*noise);
    var K=HB.range(1,26,26),top=Math.ceil(band(n+26)/5)*5+5;
    return {
      stats:[{k:'95% half-width, average effect',v:'±'+(1.96*se).toFixed(2),s:'thousand orders a week'},
        {k:'Smallest detectable average effect',v:(2.8*se).toFixed(1),s:'80% power, 5% two-sided'},
        {k:'Share of error from the trend',v:HB.pct(line*line/(se*se),0)}],
      plot:{alt:'95% band for a single week, by weeks since launch',
        x:{label:'Weeks since launch',min:1,max:26,ticks:[1,8,16,26],fmt:function(x){return String(Math.round(x))}},
        y:{label:'Single-week 95% band, ±',min:0,max:top,fmt:function(y){return String(Math.round(y))}},
        series:[{name:'Single week',pts:K.map(function(k){return [k,band(n+k)]})}],refs:[{x:v.h,label:'end of measurement'}],dots:[{x:v.h,y:band(n+v.h)}]},
      note:'Averaging more weeks shrinks the noise but not the trend error, which grows with distance from the pre-period. Assumes independent weekly errors; autocorrelation widens every number here.'}
  }
});

/* a5-double-ml. extra/check/a5_dml.py: Y = 2D + 5U + e, D = U + v; models capture 80% of U: naive 4.50, outcome model only 2.50, both (DML) 2.19. */
HB.lab('dml',{
  title:'Why two rough models beat one',
  inputs:[
    {id:'g',label:'Confounder’s effect on GMV',vals:[1,2,5,10],value:5,fmt:function(v){return String(v)}},
    {id:'a',label:'Confounder’s pull on the treatment',vals:[0.25,0.5,1,2],value:1,fmt:function(v){return String(v)}},
    {id:'qg',label:'Share of the confounder the GMV model captures',min:0,max:1,step:0.05,value:0.8,fmt:function(v){return Math.round(v*100)+'%'}},
    {id:'qm',label:'Share the treatment model captures',min:0,max:1,step:0.05,value:0.8,fmt:function(v){return Math.round(v*100)+'%'}}
  ],
  run:function(v,HB){
    var th=2,a=v.a,g=v.g;
    function dml(qg,qm){return th+g*a*(1-qg)*(1-qm)/(a*a*(1-qm)*(1-qm)+1)}
    var naive=th+g*a/(a*a+1),one=th+g*a*(1-v.qg)/(a*a+1),both=dml(v.qg,v.qm),Q=HB.range(0,1,41),top=Math.ceil(naive+0.5);
    return {
      stats:[{k:'Raw comparison',v:naive.toFixed(2)},{k:'GMV model only',v:one.toFixed(2)},{k:'Both models (DML)',v:both.toFixed(2),s:'true effect 2.00'}],
      plot:{alt:'Estimate against the share of the confounder the treatment model captures',
        x:{label:'Share the treatment model captures',min:0,max:1,ticks:[0,0.25,0.5,0.75,1],fmt:function(x){return Math.round(x*100)+'%'}},
        y:{label:'Estimate',min:1.5,max:Math.max(3,top),fmt:function(y){return y.toFixed(1)}},
        series:[{name:'DML, at this GMV model',pts:Q.map(function(q){return [q,dml(v.qg,q)]})},{name:'GMV model only',pts:Q.map(function(q){return [q,one]})}],
        refs:[{y:2,label:'truth',right:true}],dots:[{x:v.qm,y:both}]},
      note:'A stylised linear model with one confounder. The bias left by DML is roughly the product of what each model misses, so two imperfect models together beat either alone.'}
  }
});

/* a5-sensitivity-falsification. extra/check/a5_sens.py: RR 1.30 -> E 1.92; 1.18 -> 1.64; benchmark (1.8, 2.5) bias factor 1.36, adjusted 0.95. */
HB.lab('evalue',{
  title:'How strong must a hidden confounder be?',
  inputs:[
    {id:'rr',label:'Estimated risk ratio',vals:[1.1,1.2,1.3,1.5,2,3],value:1.3,fmt:function(v){return v.toFixed(2)}},
    {id:'lo',label:'Lower limit, as a share of the way to the estimate',vals:[0,0.25,0.5,0.6,0.75,1],value:0.6,fmt:function(v){return Math.round(v*100)+'%'}},
    {id:'a',label:'Benchmark confounder: link to treatment',vals:[1.1,1.3,1.5,1.8,2.5,4],value:1.8,fmt:function(v){return v.toFixed(1)}},
    {id:'b',label:'Benchmark confounder: link to outcome',vals:[1.1,1.4,1.5,2,2.5,4],value:2.5,fmt:function(v){return v.toFixed(1)}}
  ],
  run:function(v,HB){
    function E(r){return r<=1?1:r+Math.sqrt(r*(r-1))}
    var lo=1+(v.rr-1)*v.lo,B=v.a*v.b/(v.a+v.b-1),adj=v.rr/B;
    function curve(r){return HB.range(r+0.02,6,120).map(function(a){return [a,Math.min(6.5,r*(a-1)/(a-r))]}).filter(function(p){return p[1]>=1})}
    var ser=[{name:'Erases the estimate',pts:curve(v.rr)}];if(lo>1.0001)ser.push({name:'Erases the lower limit',pts:curve(lo)});
    return {
      stats:[{k:'E-value, estimate',v:E(v.rr).toFixed(2)},{k:'E-value, lower limit',v:lo>1?E(lo).toFixed(2):'1.00',s:'lower limit '+lo.toFixed(2)},
        {k:'Estimate after a confounder like the benchmark',v:adj.toFixed(2),s:'bias factor '+B.toFixed(2)}],
      plot:{alt:'Confounder strengths that would explain the estimate away',
        x:{label:'Confounder’s risk ratio with treatment',min:1,max:6,ticks:[1,2,3,4,5,6],fmt:function(x){return String(Math.round(x))}},
        y:{label:'with outcome',min:1,max:6,ticks:[1,2,3,4,5,6],fmt:function(y){return String(Math.round(y))}},
        series:ser,dots:[{x:v.a,y:v.b}]},
      note:adj<=1?'The benchmark sits beyond the estimate\u2019s curve: a hidden confounder as strong as it would erase the effect.':(lo/B<=1?'A confounder like the benchmark would leave the estimate above 1, but the interval would then include no effect.':'The benchmark sits inside both curves: a confounder that strong would not erase the effect.')}
  }
});

/* a5-mediation. extra/check/a5_mediation.py: a = 1.5, true b = 2.5, total 12, mediator sd 1.5; confounding k = 1.16 (U -> M by k, U -> Y by 4k) gives b_hat 4.00 and indirect 6.0 against a true 3.75. */
HB.lab('mediation',{
  title:'What confounding of the mediator does to the split',
  inputs:[
    {id:'a',label:'Photos added by the new flow',vals:[0.5,1,1.5,2,3],value:1.5,fmt:function(v){return '+'+v}},
    {id:'b',label:'True GMV per extra photo, ₹ thousand',vals:[0,1,2.5,4,6],value:2.5,fmt:function(v){return String(v)}},
    {id:'k',label:'Experience driving both photos and GMV',vals:[0,0.5,0.8,1.162,1.5,2],value:1.162,fmt:function(v){return ['none','weak','moderate','strong','very strong','extreme'][[0,0.5,0.8,1.162,1.5,2].indexOf(v)]}}
  ],
  run:function(v,HB){
    var tot=12,sm=1.5;function bh(k){return v.b+4*k*k/(k*k+sm*sm)}
    var trueInd=v.a*v.b,estInd=v.a*bh(v.k),K=HB.range(0,2,41);
    return {
      stats:[{k:'True share through photos',v:HB.pct(Math.min(1,trueInd/tot),0),s:'indirect '+trueInd.toFixed(2)+' of 12'},
        {k:'Regression’s share',v:HB.pct(estInd/tot,0),s:'indirect '+estInd.toFixed(2)+', ₹'+bh(v.k).toFixed(2)+'k per photo'},
        {k:'Total effect',v:'12.0',s:'unbiased either way'}],
      plot:{alt:'Estimated and true share mediated by strength of confounding',
        x:{label:'Confounding of photos and GMV',min:0,max:2,ticks:[0,0.5,1,1.5,2],fmt:function(x){return x.toFixed(1)}},
        y:{label:'Share of the effect through photos',min:0,max:1.5,ticks:[0,0.25,0.5,0.75,1,1.25,1.5],fmt:function(y){return Math.round(y*100)+'%'}},
        series:[{name:'Regression estimate',pts:K.map(function(k){return [k,v.a*bh(k)/tot]})},{name:'Truth',pts:K.map(function(k){return [k,trueInd/tot]})}],
        dots:[{x:v.k,y:estInd/tot}]},
      note:'Randomising the flow protects the total effect. The split depends on the mediator’s coefficient, which is observational: confounding inflates it with no sign in the total.'}
  }
});

/* c2-monte-carlo. extra/check/c2_montecarlo.py (1M draws): P10 15.6, P50 26.7, P90 44.2 crore, P(>15) 0.915; rho -0.6: 0.982; +0.6: 0.861. This lab uses 20,000 seeded draws, so it agrees to about a point. */
HB.lab('montecarlo',{
  title:'Simulate the sizing',
  inputs:[
    {id:'ah',label:'Adoption, high end (low 5%, likely 10%)',vals:[0.12,0.15,0.2,0.3],value:0.2,fmt:function(v){return Math.round(v*100)+'%'}},
    {id:'lh',label:'Lift, high end (low 3%, likely 6%)',vals:[0.08,0.12,0.2],value:0.12,fmt:function(v){return Math.round(v*100)+'%'}},
    {id:'r',label:'Correlation of adoption and lift',vals:[-0.6,-0.3,0,0.3,0.6],value:0,fmt:function(v){return (v>0?'+':'')+v}},
    {id:'c',label:'Annual cost, ₹ crore',vals:[10,15,20,30],value:15,fmt:function(v){return '₹'+v+' crore'}}
  ],
  run:function(v,HB){
    var s=20261112>>>0;function rnd(){s+=0x6D2B79F5;var t=s;t=Math.imul(t^t>>>15,t|1);t^=t+Math.imul(t^t>>>7,t|61);return ((t^t>>>14)>>>0)/4294967296}
    function nrm(){var u=rnd()||1e-12,w=rnd();return Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*w)}
    function tri(u,lo,m,hi){var c=(m-lo)/(hi-lo);return u<c?lo+Math.sqrt(u*(hi-lo)*(m-lo)):hi-Math.sqrt((1-u)*(hi-lo)*(hi-m))}
    var N=20000,out=new Float64Array(N),above=0;
    for(var i=0;i<N;i++){var z1=nrm(),z2=v.r*z1+Math.sqrt(1-v.r*v.r)*nrm();
      var val=tri(rnd(),4e6,5e6,6e6)*tri(HB.Phi(z1),0.05,0.10,v.ah)*tri(HB.Phi(z2),0.03,0.06,v.lh)*tri(rnd(),6000,7000,8000)/1e7;
      out[i]=val;if(val>v.c)above++}
    var srt=Array.prototype.slice.call(out).sort(function(a,b){return a-b});function q(p){return srt[Math.floor(p*(N-1))]}
    var xmax=Math.max(60,Math.ceil(q(0.99)/20)*20),X=HB.range(0,xmax,121),k=0,pts=X.map(function(x){while(k<N&&srt[k]<=x)k++;return [x,1-k/N]});
    return {
      stats:[{k:'Chance it covers the cost',v:HB.pct(above/N,0)},{k:'Median',v:'₹'+q(0.5).toFixed(1)+' cr'},{k:'80% range',v:'₹'+q(0.1).toFixed(0)+' to '+q(0.9).toFixed(0)+' cr'}],
      plot:{alt:'Chance the value exceeds each amount',
        x:{label:'Annual value, ₹ crore',min:0,max:xmax,fmt:function(x){return String(Math.round(x))}},
        y:{label:'Chance of exceeding',min:0,max:1,ticks:[0,0.25,0.5,0.75,1],fmt:function(y){return Math.round(y*100)+'%'}},
        series:[{pts:pts}],refs:[{x:v.c,label:'cost'}],dots:[{x:v.c,y:above/N}]},
      note:'20,000 draws, triangular inputs, buyers 4 to 6 million and spend ₹6,000 to ₹8,000 fixed. Moving the high ends stretches the right tail; correlation changes how often the bad ends coincide.'}
  }
});

/* c2-power-simulation. Lab model: a quarter of users buy; buyers' revenue lognormal. Seeded, 200 simulated tests per setting, so rates carry about ±3 points of simulation error; extra/check/c2_powersim.py runs the fuller session-level model. */
HB.lab('powersim',{
  title:'Run 200 tests and count',
  inputs:[
    {id:'n',label:'Users per arm',vals:[1000,2000,5000,10000],value:5000,fmt:function(v){return HB.num(v)}},
    {id:'s',label:'Skew of buyers’ revenue (lognormal σ)',vals:[0.5,1,1.5,2],value:1.5,fmt:function(v){return String(v)}},
    {id:'l',label:'True lift',vals:[0,0.05,0.1,0.15,0.2],value:0.2,fmt:function(v){return v?'+'+Math.round(v*100)+'%':'none (A/A)'}}
  ],
  run:function(v,HB){
    var st=987654321>>>0;function rnd(){st+=0x6D2B79F5;var t=st;t=Math.imul(t^t>>>15,t|1);t^=t+Math.imul(t^t>>>7,t|61);return ((t^t>>>14)>>>0)/4294967296}
    function nrm(){var u=rnd()||1e-12,w=rnd();return Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*w)}
    var n=v.n,S=200,raw=0,cap=0,a=new Float64Array(n),b=new Float64Array(n),all=new Float64Array(2*n);
    function draw(arr,m){for(var i=0;i<n;i++)arr[i]=rnd()<0.25?Math.exp(6+v.s*nrm())*m:0}
    function ttest(x,y,c){var mx=0,my=0,vx=0,vy=0,i,u;for(i=0;i<n;i++){mx+=Math.min(x[i],c);my+=Math.min(y[i],c)}mx/=n;my/=n;
      for(i=0;i<n;i++){u=Math.min(x[i],c)-mx;vx+=u*u;u=Math.min(y[i],c)-my;vy+=u*u}vx/=n-1;vy/=n-1;return Math.abs(mx-my)/Math.sqrt(vx/n+vy/n)>1.96}
    for(var k=0;k<S;k++){draw(a,1);draw(b,1+v.l);
      if(ttest(a,b,Infinity))raw++;
      all.set(a);all.set(b,n);var srt=Array.prototype.slice.call(all).sort(function(p,q){return p-q});
      if(ttest(a,b,srt[Math.floor(0.99*(2*n-1))]))cap++}
    var mu=0.25*Math.exp(6+v.s*v.s/2),m2=0.25*Math.exp(12+2*v.s*v.s),cv=Math.sqrt(m2-mu*mu)/mu,form=v.l?HB.Phi(v.l/(cv*Math.sqrt((1+(1+v.l)*(1+v.l))/n))-1.96):0.05;
    var lab=v.l?'power':'false positive rate';
    return {
      stats:[{k:'Formula',v:HB.pct(form,0),s:lab+', assumes normal'},{k:'Simulated, raw',v:HB.pct(raw/S,0),s:lab},{k:'Simulated, capped at P99',v:HB.pct(cap/S,0),s:lab}],
      bars:{title:v.l?'Share of 200 tests significant (power)':'Share of 200 A/A tests significant (should be about 5%)',max:1,items:[
        {label:'Formula',value:form,text:HB.pct(form,0)},{label:'Raw t-test',value:raw/S,text:HB.pct(raw/S,0)},{label:'Capped t-test',value:cap/S,text:HB.pct(cap/S,0)}]},
      note:'Each setting reruns 200 seeded tests, so rates are within about ±3 points. With heavy tails the formula can miss in either direction, the raw test runs below 5% in A/A yet stays weak, and capping recovers much of the power.'}
  }
});

/* c3-key-drivers. Two standardised inputs: R2(A)=ra^2, R2(B)=rb^2, R2(AB)=(ra^2+rb^2-2 ra rb r)/(1-r^2). extra/check/c3_drivers.py worked case: 0.30, 0.20, 0.38 -> 0.24, 0.14. */
HB.lab('shapley2',{
  title:'Coefficients against fair shares',
  inputs:[
    {id:'ra',label:'Delivery’s correlation with CSAT',vals:[0.2,0.3,0.4,0.5,0.6,0.7],value:0.6,fmt:function(v){return v.toFixed(1)}},
    {id:'rb',label:'Packaging’s correlation with CSAT',vals:[0.2,0.3,0.4,0.5,0.57,0.6,0.7],value:0.57,fmt:function(v){return v.toFixed(2)}},
    {id:'r',label:'Correlation between delivery and packaging',vals:[0,0.3,0.5,0.7,0.8,0.9,0.95],value:0.95,fmt:function(v){return v.toFixed(2)}}
  ],
  run:function(v,HB){
    var ra=v.ra,rb=v.rb,r=v.r,d=1-r*r,ok=(ra*ra+rb*rb-2*ra*rb*r)/d<=0.999;
    if(!ok)return {stats:[{k:'Not possible',v:'—',s:'these three correlations cannot occur together'}],note:'Lower one of the correlations: two inputs this alike cannot relate this differently to the outcome.'};
    var r2a=ra*ra,r2b=rb*rb,r2ab=(r2a+r2b-2*ra*rb*r)/d,ba=(ra-r*rb)/d,bb=(rb-r*ra)/d,sa=(r2a+r2ab-r2b)/2,sb=(r2b+r2ab-r2a)/2;
    var mx=Math.max(Math.abs(ba),Math.abs(bb),sa,sb,0.4);
    return {
      stats:[{k:'R², both inputs',v:r2ab.toFixed(2)},{k:'Shapley shares',v:sa.toFixed(2)+' / '+sb.toFixed(2),s:'delivery / packaging'},{k:'Coefficients',v:ba.toFixed(2)+' / '+bb.toFixed(2),s:'delivery / packaging, standardised'}],
      bars:{title:'Delivery and packaging, two ways',max:mx,items:[
        {label:'Delivery share',value:sa,text:sa.toFixed(2)},{label:'Packaging share',value:sb,text:sb.toFixed(2)},
        {label:'Delivery coefficient',value:Math.abs(ba),text:ba.toFixed(2),cls:'s2'},{label:'Packaging coefficient',value:Math.abs(bb),text:bb.toFixed(2),cls:'s2'}]},
      note:bb<=0.02&&sb>0.05?'Packaging adds nothing once delivery is known, yet takes a sizeable fair share because it moves with delivery.':'Shares always add to R² and stay positive; coefficients answer “holding the other fixed” and can shrink to zero or turn negative.'}
  }
});

/* c3-metric-sensitivity. extra/check/c3_sensitivity.py: 500,000 per arm, MDE = 2.8 x CV x sqrt(2/n): GMV CV 8 -> 4.48%; capped CV 5 + CUPED rho .6 -> 2.24%; add-to-cart CV 1.73 -> 0.97%. Power for 1%: GMV 0.09, add-to-cart 0.82. */
HB.lab('sensitivity',{
  title:'What can this metric detect?',
  inputs:[
    {id:'cv',label:'Metric’s CV per user',vals:[1.5,1.73,3,4.9,8,12],value:8,fmt:function(v){return String(v)}},
    {id:'cap',label:'Capping',vals:[1,0.625],value:1,fmt:function(v){return v===1?'none':'at P99.9 (CV × 0.625)'}},
    {id:'rho',label:'CUPED pre-period correlation',vals:[0,0.3,0.5,0.6,0.8],value:0,fmt:function(v){return v?String(v):'not used'}},
    {id:'e',label:'Typical true effect of a feature',vals:[0.005,0.01,0.02,0.05],value:0.01,fmt:function(v){return (v*100)+'%'}}
  ],
  run:function(v,HB){
    var cv=v.cv*v.cap*Math.sqrt(1-v.rho*v.rho),N=[50000,100000,200000,500000,1000000,2000000,5000000];
    function pw(n){return HB.Phi(v.e/(cv*Math.sqrt(2/n))-1.96)}
    function mde(n){return 2.8*cv*Math.sqrt(2/n)}
    var need=Math.pow(2.8*cv/v.e,2)*2;
    return {
      stats:[{k:'Effective CV',v:cv.toFixed(2)},{k:'MDE at 500,000 per arm',v:HB.pct(mde(500000),2)},
        {k:'Users per arm for 80% power',v:need>=1e6?(need/1e6).toFixed(1)+' M':HB.num(Math.round(need/1000)*1000)}],
      plot:{alt:'Power to detect the typical effect, by users per arm',
        x:{label:'Users per arm',min:50000,max:5000000,log:true,ticks:[50000,200000,500000,2000000,5000000],fmt:function(x){return x>=1e6?(x/1e6)+'M':(x/1000)+'k'}},
        y:{label:'Power',min:0,max:1,ticks:[0,0.2,0.4,0.6,0.8,1],fmt:function(y){return Math.round(y*100)+'%'}},
        series:[{pts:HB.range(Math.log10(50000),Math.log10(5000000),60).map(function(t){var n=Math.pow(10,t);return [n,pw(n)]})}],
        refs:[{y:0.8,label:'80%',right:true},{x:500000,label:'this test'}],dots:[{x:500000,y:pw(500000)}]},
      note:'Halving the CV does what quadrupling the traffic does. A low CV is only half the story: the metric must also be one that features move, in the same direction as the outcome.'}
  }
});

/* c3-anomaly-detection. extra/check/c3_anomaly.py: 200 series x 30 days, 3 sigma: 16.2 false/month (normal), 79.4 (t4); 2-consecutive at 2 sigma: 6.2; 2.5 sigma drop caught within 3 days 0.669 vs 0.626; precision with 2 incidents/month 8% vs 17%. */
HB.lab('alerts',{
  title:'The false alert budget',
  inputs:[
    {id:'s',label:'Series monitored',vals:[20,50,200,500,2000],value:200,fmt:function(v){return HB.num(v)}},
    {id:'k',label:'Threshold, in robust σ',vals:[2,2.5,3,3.5,4,4.5],value:3,fmt:function(v){return v+'σ'}},
    {id:'r',label:'Rule',vals:[1,2],value:1,fmt:function(v){return v===1?'one day beyond':'two days in a row beyond'}},
    {id:'t',label:'Residual tails',vals:[0,1],value:0,fmt:function(v){return v?'heavy (t, 4 df)':'normal'}},
    {id:'d',label:'Size of a real drop',vals:[1.5,2,2.5,3,4],value:2.5,fmt:function(v){return v+'σ'}}
  ],
  run:function(v,HB){
    function tail(x){if(!v.t)return 1-HB.Phi(x);var z=x*Math.SQRT2;return 0.5-z*(z*z+6)/(2*Math.pow(z*z+4,1.5))}
    var q=v.r===1?2*tail(v.k):2*Math.pow(tail(v.k),2),fa=v.s*30*q,p=tail(v.k-v.d),det=v.r===1?1-Math.pow(1-p,3):2*p*p-p*p*p,tp=2*det,prec=tp/(tp+fa);
    var K=HB.range(2,5,61);
    function fam(k){return v.s*30*(v.r===1?2*tail(k):2*Math.pow(tail(k),2))}
    return {
      stats:[{k:'False alerts a month',v:fa<10?fa.toFixed(1):HB.num(fa)},{k:'Real drop caught within 3 days',v:HB.pct(det,0)},
        {k:'Share of alerts that are real',v:HB.pct(prec,0),s:'with 2 real incidents a month'}],
      plot:{alt:'False alerts a month by threshold',
        x:{label:'Threshold, σ',min:2,max:5,ticks:[2,3,4,5],fmt:function(x){return x.toFixed(0)+'σ'}},
        y:{label:'False alerts a month (log)',min:-1,max:4,ticks:[-1,0,1,2,3,4],fmt:function(y){return HB.num(Math.pow(10,y),y<0?1:0)}},
        series:[{pts:K.map(function(k){return [k,Math.log10(Math.max(0.1,fam(k)))]})}],refs:[{y:Math.log10(20),label:'a workable budget',right:true}],dots:[{x:v.k,y:Math.log10(Math.max(0.1,fa))}]},
      note:'Every series adds false alerts. Heavy tails multiply them; requiring two days in a row cuts them sharply for a small loss in detection. Even then most alerts are false, because real incidents are rare.'}
  }
});

/* c5-path-analysis. extra/check/c5_paths.py: conversion from home 6.54%; listing->cart 25%: 8.27%; cart->checkout 70%: 7.63%; checkout->buy 80%: 7.48%. */
HB.lab('markov',{
  title:'Which step is worth fixing?',
  inputs:[
    {id:'lc',label:'Listing → cart',vals:[0.15,0.2,0.25,0.3,0.35],value:0.2,fmt:function(v){return Math.round(v*100)+'%'}},
    {id:'ck',label:'Cart → checkout',vals:[0.5,0.6,0.7,0.8],value:0.6,fmt:function(v){return Math.round(v*100)+'%'}},
    {id:'kp',label:'Checkout → buy',vals:[0.6,0.7,0.8,0.9],value:0.7,fmt:function(v){return Math.round(v*100)+'%'}}
  ],
  run:function(v,HB){
    function solve(lc,ck,kp){
      var Q=[[0,.5,.2,0,0],[0,.2,.55,0,0],[0,.25,.1,lc,0],[0,0,.15,0,ck],[0,0,0,0,0]],r=[0,0,0,0,kp],A=[],i,j,k;
      for(i=0;i<5;i++){A.push([]);for(j=0;j<5;j++)A[i].push((i===j?1:0)-Q[i][j]);A[i].push(r[i])}
      for(k=0;k<5;k++){var p=A[k][k];for(j=k;j<6;j++)A[k][j]/=p;for(i=0;i<5;i++)if(i!==k){var f=A[i][k];for(j=k;j<6;j++)A[i][j]-=f*A[k][j]}}
      return A.map(function(row){return row[5]})}
    var b=solve(v.lc,v.ck,v.kp),base=solve(0.2,0.6,0.7)[0],names=['Home','Search','Listing','Cart','Checkout'];
    return {
      stats:[{k:'Conversion from home',v:HB.pct(b[0],2)},{k:'Change against today',v:(b[0]>=base?'+':'')+HB.pct(b[0]/base-1,0),s:'today '+HB.pct(base,2)},{k:'From a listing',v:HB.pct(b[2],1)}],
      bars:{title:'Chance of eventually buying, by starting page',max:1,items:names.map(function(n,i){return {label:n,value:b[i],text:HB.pct(b[i],1)}})},
      note:'Changes are taken from the “leave” share. A small gain on a page that sessions visit often, and come back to, can be worth more than a large gain near the end.'}
  }
});

/* c5-segmentation-rfm. 600 seeded synthetic buyers drawn like extra/check/c5_rfm.py (which uses 50,000): raw-unit k-means puts most buyers in one cluster; log + standardise gives balanced segments. */
HB.lab('rfm',{
  title:'Cluster buyers, with and without scaling',
  inputs:[
    {id:'sc',label:'Features',vals:[0,1],value:0,fmt:function(v){return v?'log, then standardised':'raw units'}},
    {id:'k',label:'Clusters',vals:[2,3,4,5,6],value:4,fmt:function(v){return String(v)}}
  ],
  run:function(v,HB){
    var s=7>>>0;function rnd(){s+=0x6D2B79F5;var t=s;t=Math.imul(t^t>>>15,t|1);t^=t+Math.imul(t^t>>>7,t|61);return ((t^t>>>14)>>>0)/4294967296}
    function nrm(){var u=rnd()||1e-12,w=rnd();return Math.sqrt(-2*Math.log(u))*Math.cos(2*Math.PI*w)}
    function pois(l){var L=Math.exp(-l),k=0,p=1;do{k++;p*=rnd()}while(p>L);return k-1}
    var n=600,X=[],i,j,c;
    for(i=0;i<n;i++){var e=nrm(),f=pois(Math.exp(0.8+0.7*e))+1,r=Math.min(365,-Math.log(rnd()||1e-12)*Math.exp(4.2-0.6*e)),m=f*Math.exp(7.3+0.2*e+0.8*nrm());X.push([r,f,m])}
    var F=X.map(function(x){return v.sc?[Math.log1p(x[0]),Math.log1p(x[1]),Math.log1p(x[2])]:x.slice()});
    if(v.sc){for(j=0;j<3;j++){var mu=0,sd=0;for(i=0;i<n;i++)mu+=F[i][j];mu/=n;for(i=0;i<n;i++)sd+=(F[i][j]-mu)*(F[i][j]-mu);sd=Math.sqrt(sd/n);for(i=0;i<n;i++)F[i][j]=(F[i][j]-mu)/sd}}
    var best=null;
    for(var rs=0;rs<5;rs++){var C=[],lab=new Array(n),used={};
      while(C.length<v.k){var p=Math.floor(rnd()*n);if(!used[p]){used[p]=1;C.push(F[p].slice())}}
      for(var it=0;it<50;it++){for(i=0;i<n;i++){var bd=Infinity;for(c=0;c<v.k;c++){var d=0;for(j=0;j<3;j++)d+=(F[i][j]-C[c][j])*(F[i][j]-C[c][j]);if(d<bd){bd=d;lab[i]=c}}}
        for(c=0;c<v.k;c++){var sum=[0,0,0],cnt=0;for(i=0;i<n;i++)if(lab[i]===c){cnt++;for(j=0;j<3;j++)sum[j]+=F[i][j]}if(cnt)for(j=0;j<3;j++)C[c][j]=sum[j]/cnt}}
      var sse=0;for(i=0;i<n;i++)for(j=0;j<3;j++)sse+=(F[i][j]-C[lab[i]][j])*(F[i][j]-C[lab[i]][j]);
      if(!best||sse<best.sse)best={sse:sse,lab:lab.slice()}}
    function med(a){a=a.slice().sort(function(p,q){return p-q});return a.length?a[Math.floor(a.length/2)]:0}
    var rows=[];for(c=0;c<v.k;c++){var mem=X.filter(function(_,i){return best.lab[i]===c});
      rows.push({sh:mem.length/n,r:med(mem.map(function(x){return x[0]})),f:med(mem.map(function(x){return x[1]})),m:med(mem.map(function(x){return x[2]}))})}
    rows.sort(function(a,b){return b.sh-a.sh});
    return {
      stats:[{k:'Largest cluster',v:HB.pct(rows[0].sh,0)},{k:'Smallest cluster',v:HB.pct(rows[rows.length-1].sh,1)}],
      bars:{title:'Share of buyers in each cluster',max:1,items:rows.map(function(r,i){return {label:'Cluster '+(i+1),value:r.sh,text:HB.pct(r.sh,0)}})},
      table:{head:['Cluster','Share','Median recency, days','Median orders','Median spend, ₹'],rows:rows.map(function(r,i){return [i+1,HB.pct(r.sh,0),Math.round(r.r),Math.round(r.f),HB.num(Math.round(r.m/100)*100)]})},
      note:v.sc?'With fair scales, clusters differ on recency, frequency and spend together.':'In raw units, spend in rupees outweighs everything: clusters are spend bands, and recency barely differs between most of them.'}
  }
});

/* c5-text-analytics. extra/check/c5_text.py: se .90, sp .97: true 2% -> observed 4.74%, precision 38%; true 5% -> 7.35%, 61%; observed 18% -> true 17.2%. */
HB.lab('tagging',{
  title:'What the tagger counts against what is there',
  inputs:[
    {id:'se',label:'Sensitivity: true cases caught',vals:[0.7,0.8,0.9,0.95],value:0.9,fmt:function(v){return Math.round(v*100)+'%'}},
    {id:'sp',label:'Specificity: non-cases left alone',vals:[0.9,0.95,0.97,0.99,0.995],value:0.97,fmt:function(v){return (v*100).toFixed(1)+'%'}},
    {id:'p',label:'True share of the theme',vals:[0.01,0.02,0.05,0.1,0.17,0.3],value:0.02,fmt:function(v){return Math.round(v*100)+'%'}}
  ],
  run:function(v,HB){
    function obs(p){return v.se*p+(1-v.sp)*(1-p)}
    var o=obs(v.p),prec=v.se*v.p/o,P=HB.range(0,0.3,61);
    return {
      stats:[{k:'Share the tagger reports',v:HB.pct(o,1)},{k:'Tags that are right (precision)',v:HB.pct(prec,0)},{k:'Overstatement',v:(o/v.p).toFixed(1)+'×'}],
      plot:{alt:'Reported share against true share',
        x:{label:'True share',min:0,max:0.3,ticks:[0,0.1,0.2,0.3],fmt:function(x){return Math.round(x*100)+'%'}},
        y:{label:'Reported share',min:0,max:0.35,ticks:[0,0.1,0.2,0.3],fmt:function(y){return Math.round(y*100)+'%'}},
        series:[{name:'Tagger',pts:P.map(function(p){return [p,obs(p)]})},{name:'Perfect',pts:P.map(function(p){return [p,p]})}],dots:[{x:v.p,y:o}]},
      note:'False positives add (1 − specificity) of every comment without the theme. For rare themes that is more than the real cases, so raw counts mislead; correct with π = (reported − (1 − sp)) ÷ (se + sp − 1).'}
  }
});

/* c5-activation. extra/check/c5_activation.py: 10,000 sellers by listings in 14 days; >=5: 25% reach it, 73.2% vs 23.0% retained, 51.5% of retained covered; nudge: 1 pt / 8 pts = 12.5 pts per seller moved. */
HB.lab('aha',{
  title:'Pick the threshold',
  inputs:[
    {id:'k',label:'Activation threshold, listings in 14 days',vals:[1,3,5,10],value:5,fmt:function(v){return v+'+'}},
    {id:'c',label:'Share of the gap that is causal',vals:[0.1,0.25,0.5,1],value:0.25,fmt:function(v){return Math.round(v*100)+'%'}}
  ],
  run:function(v,HB){
    var B=[[3000,.10],[3000,.25],[1500,.45],[1500,.70],[1000,.78]],start={1:1,3:2,5:3,10:4}[v.k],N=10000,R=0,nh=0,rh=0,nm=0,rm=0,i;
    for(i=0;i<5;i++){R+=B[i][0]*B[i][1];if(i>=start){nh+=B[i][0];rh+=B[i][0]*B[i][1]}else{nm+=B[i][0];rm+=B[i][0]*B[i][1]}}
    var gap=rh/nh-rm/nm,gain=0.25*gap*v.c;
    return {
      stats:[{k:'Sellers reaching it',v:HB.pct(nh/N,0)},{k:'Retained: reached vs not',v:HB.pct(rh/nh,0)+' vs '+HB.pct(rm/nm,0),s:'gap '+(100*gap).toFixed(0)+' pts'},
        {k:'Retained sellers it covers',v:HB.pct(rh/R,0)},{k:'Retention gain if 25% more reach it',v:'+'+(100*gain).toFixed(1)+' pts',s:'at this causal share'}],
      bars:{title:'Active at day 90, by listings in the first 14 days',max:1,items:[['0',0],['1 to 2',1],['3 to 4',2],['5 to 9',3],['10+',4]].map(function(b){return {label:b[0],value:B[b[1]][1],text:HB.pct(B[b[1]][1],0),cls:b[1]>=start?'':'s0'}})},
      note:'Higher thresholds separate more sharply but cover fewer of the sellers who stay. The nudge test in this page measured a causal share of about a quarter.'}
  }
});

/* c5-churn-propensity. extra/check/c5_churn.py: cost 150, value 2,500, 10,000 per decile: top 3 by risk +0; deciles 3-5 +12.5 lakh; break-even cut 6 points. */
HB.lab('churn',{
  title:'Who should get the offer?',
  inputs:[
    {id:'c',label:'Cost per buyer targeted',vals:[50,75,100,150,200],value:150,fmt:function(v){return '₹'+v}},
    {id:'v',label:'Value of a saved buyer',vals:[1000,2500,5000],value:2500,fmt:function(v){return '₹'+HB.num(v)}},
    {id:'o',label:'Rank buyers by',vals:[0,1],value:0,fmt:function(v){return v?'measured uplift':'churn risk'}},
    {id:'k',label:'Deciles targeted',min:1,max:10,step:1,value:3,fmt:function(v){return String(v)}}
  ],
  run:function(v,HB){
    var up=[.04,.06,.08,.08,.07,.05,.02,.01,.01,0],n=10000,i,pr=up.map(function(u){return n*(u*v.v-v.c)});
    var order=[0,1,2,3,4,5,6,7,8,9];if(v.o)order.sort(function(a,b){return up[b]-up[a]||a-b});
    var chosen=order.slice(0,v.k),tot=0,best=0;chosen.forEach(function(d){tot+=pr[d]});pr.forEach(function(p){if(p>0)best+=p});
    function lakh(x){return (x<0?'−':'+')+'₹'+(Math.abs(x)/1e5).toFixed(1)+' lakh'}
    return {
      stats:[{k:'Profit of this targeting',v:lakh(tot)},{k:'Best possible',v:lakh(best),s:'every decile above break-even'},{k:'Break-even cut',v:(100*v.c/v.v).toFixed(1)+' pts'}],
      bars:{title:'Profit by risk decile (1 = riskiest); targeted deciles in blue',max:Math.max.apply(null,pr.map(Math.abs)),items:pr.map(function(p,d){return {label:'Decile '+(d+1),value:Math.abs(p),text:lakh(p),cls:chosen.indexOf(d)>=0?(p>=0?'':'s2'):'s0'}})},
      note:'Orange bars are targeted deciles that lose money. Ranking by risk targets the buyers most likely to leave; ranking by uplift targets the buyers the offer keeps.'}
  }
});

/* c6-opportunity-sizing. extra/check/c6_sizing.py: 1,000 cr x 40% x 60% = 240 cr exposed; x 3% x 60% = 4.32 cr if it works; x 8/20 = 1.73 cr expected; build 2 cr; test first (0.3 cr) 0.63 cr. */
HB.lab('sizing',{
  title:'From the pitch to the expected value',
  inputs:[
    {id:'el',label:'Share of GMV eligible',vals:[0.2,0.3,0.4,0.5,0.7,1],value:0.4,fmt:function(v){return Math.round(v*100)+'%'}},
    {id:'ex',label:'Share of eligible buyers exposed',vals:[0.3,0.45,0.6,0.8,1],value:0.6,fmt:function(v){return Math.round(v*100)+'%'}},
    {id:'l',label:'Lift if it works, measured',vals:[0.01,0.02,0.03,0.05,0.1],value:0.03,fmt:function(v){return (v*100)+'%'}},
    {id:'p',label:'Share kept long term',vals:[0.4,0.6,0.8,0.9,1],value:0.6,fmt:function(v){return Math.round(v*100)+'%'}},
    {id:'w',label:'Chance it works',vals:[0.2,0.3,0.4,0.6,1],value:0.4,fmt:function(v){return Math.round(v*100)+'%'}}
  ],
  run:function(v,HB){
    var G=1000,exp=G*v.el*v.ex,iw=exp*v.l*v.p,ev=iw*v.w,cost=2,test=Math.max(0,v.w*(iw-cost))-0.3;
    function cr(x){return '₹'+(x<10?x.toFixed(1):HB.num(Math.round(x)))+' cr'}
    return {
      stats:[{k:'Value if it works',v:cr(iw),s:'a year, on '+cr(exp)+' exposed GMV'},{k:'Expected value',v:cr(ev),s:'against a ₹2 crore build'},{k:'Build now, net',v:(ev-cost>=0?'+':'−')+cr(Math.abs(ev-cost))},{k:'Test first (₹0.3 cr), net',v:(test>=0?'+':'−')+cr(Math.abs(test))}],
      bars:{title:'From the pitch down, ₹ crore a year (log scale)',max:3,items:[
        {label:'Pitch: 10% of category',value:Math.log10(100)+1,text:cr(100),cls:'s0'},{label:'Build cost',value:Math.log10(cost)+1,text:cr(cost),cls:'s0'},
        {label:'If it works',value:Math.max(0,Math.log10(iw)+1),text:cr(iw)},{label:'Expected',value:Math.max(0,Math.log10(ev)+1),text:cr(ev),cls:'s2'}]},
      note:'The pitch skips three steps: the exposed base, your own record of what similar ideas achieved and kept, and the chance that this one fails. A cheap test is worth most when expected value sits near the cost.'}
  }
});

/* c6-price-elasticity. extra/check/c6_elasticity.py: 100,000 orders at ₹40, ₹80 commission; ₹50 at e = -0.4: orders 91,461, fee 45.7 lakh, commission lost 6.8 lakh, net -1.1 lakh/day; break-even e = -0.36; ₹30: +3.4 lakh. */
HB.lab('elasticity',{
  title:'Does the fee change pay?',
  inputs:[
    {id:'e',label:'Elasticity of orders to the fee',vals:[-0.2,-0.36,-0.4,-0.6,-0.8,-1.2],value:-0.4,fmt:function(v){return v.toFixed(2)}},
    {id:'f',label:'New fee (now ₹40)',vals:[30,35,40,45,50],value:50,fmt:function(v){return '₹'+v}},
    {id:'c',label:'Commission per order',vals:[0,40,80,120],value:80,fmt:function(v){return '₹'+v}}
  ],
  run:function(v,HB){
    var Q0=100000,F0=40;function q(F){return Q0*Math.pow(F/F0,v.e)}function net(F){return ((F+v.c)*q(F)-(F0+v.c)*Q0)/1e5}
    var Q1=q(v.f),dfee=(v.f*Q1-F0*Q0)/1e5,dcom=v.c*(Q1-Q0)/1e5,be=Math.log((F0+v.c)/(50+v.c))/Math.log(50/F0),F=HB.range(30,50,41);
    function lk(x){return (x>=0?'+':'−')+'₹'+Math.abs(x).toFixed(1)+' lakh'}
    var vals=F.map(net),lo=Math.min.apply(null,vals),hi=Math.max.apply(null,vals),pad=Math.max(1,(hi-lo)*0.15);
    return {
      stats:[{k:'Orders a day',v:HB.num(Math.round(Q1)),s:(Q1>=Q0?'+':'')+HB.pct(Q1/Q0-1,1)},{k:'Fee revenue',v:lk(dfee)},{k:'Commission',v:lk(dcom)},{k:'Net a day',v:lk(dfee+dcom),s:'break-even for ₹50: ε = '+be.toFixed(2)}],
      plot:{alt:'Net daily change in revenue by new fee',
        x:{label:'New delivery fee',min:30,max:50,ticks:[30,35,40,45,50],fmt:function(x){return '₹'+Math.round(x)}},
        y:{label:'Net change, ₹ lakh a day',min:Math.floor(lo-pad),max:Math.ceil(hi+pad),fmt:function(y){return y.toFixed(0)}},
        series:[{pts:F.map(function(x,i){return [x,vals[i]]})}],refs:[{y:0,label:'no change',right:true}],dots:[{x:v.f,y:net(v.f)}]},
      note:'Constant elasticity is a local approximation, so keep changes within about ±25% of today’s fee. With commission on every order, a fee rise must clear the commission it loses, not just raise fee revenue.'}
  }
});

/* c6-qual-quant. extra/check/c6_qualquant.py: shares 20/30/50, response 18/9.3/3.2%, PSAT 4.6/4.4/3.9: unweighted 4.39, weighted 4.19, Kish n_eff 5,010 of 7,990. */
HB.lab('weighting',{
  title:'Who answered, and what weighting costs',
  inputs:[
    {id:'rh',label:'Heavy buyers’ response rate',vals:[0.05,0.1,0.18,0.3],value:0.18,fmt:function(v){return Math.round(v*100)+'%'}},
    {id:'rl',label:'Light buyers’ response rate',vals:[0.005,0.01,0.032,0.06,0.1],value:0.032,fmt:function(v){return (v*100).toFixed(1)+'%'}},
    {id:'pl',label:'Light buyers’ PSAT',vals:[3.5,3.9,4.2,4.4],value:3.9,fmt:function(v){return v.toFixed(1)}}
  ],
  run:function(v,HB){
    var pop=[0.2,0.3,0.5],rr=[v.rh,0.093,v.rl],ps=[4.6,4.4,v.pl],N=100000,resp=pop.map(function(p,i){return p*rr[i]}),tot=resp.reduce(function(a,b){return a+b});
    var sh=resp.map(function(x){return x/tot}),unw=0,w=0,sw=0,sw2=0,n=N*tot;
    for(var i=0;i<3;i++){unw+=sh[i]*ps[i];w+=pop[i]*ps[i];var wt=pop[i]/sh[i];sw+=sh[i]*n*wt;sw2+=sh[i]*n*wt*wt}
    var ess=sw*sw/sw2;
    return {
      stats:[{k:'PSAT as reported',v:unw.toFixed(2),s:'respondents, unweighted'},{k:'PSAT, weighted to all buyers',v:w.toFixed(2)},
        {k:'Effective sample',v:HB.num(Math.round(ess)),s:'of '+HB.num(Math.round(n))+' answers ('+HB.pct(ess/n,0)+')'}],
      bars:{title:'Share of buyers and share of answers',max:0.8,items:[
        {label:'Heavy: buyers',value:0.2,text:'20%',cls:'s0'},{label:'Heavy: answers',value:sh[0],text:HB.pct(sh[0],0)},
        {label:'Medium: buyers',value:0.3,text:'30%',cls:'s0'},{label:'Medium: answers',value:sh[1],text:HB.pct(sh[1],0)},
        {label:'Light: buyers',value:0.5,text:'50%',cls:'s0'},{label:'Light: answers',value:sh[2],text:HB.pct(sh[2],0)}]},
      note:'Weighting restores each group’s true share, at the cost of precision: the rarer light buyers’ answers, the larger their weights and the smaller the effective sample. It cannot fix differences within a group.'}
  }
});
