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
