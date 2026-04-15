// Clock
function tick(){const n=new Date(),h=String(n.getHours()).padStart(2,'0'),m=String(n.getMinutes()).padStart(2,'0'),s=String(n.getSeconds()).padStart(2,'0');document.getElementById('clk').textContent=h+':'+m;document.getElementById('ht').textContent=h+':'+m+':'+s;const D=['SUN','MON','TUE','WED','THU','FRI','SAT'],M=['JAN','FEB','MAR','APR','MAY','JUN','JUL','AUG','SEP','OCT','NOV','DEC'];document.getElementById('dstr').textContent=D[n.getDay()]+' '+n.getDate()+' '+M[n.getMonth()]+' '+n.getFullYear()}
setInterval(tick,1000);tick();
function stats(){const c=Math.round(20+Math.random()*40),m=Math.round(45+Math.random()*25),l=Math.round(80+Math.random()*120),v=Math.round(85+Math.random()*15);document.getElementById('cv').textContent=c+'%';document.getElementById('mv').textContent=m+'%';document.getElementById('lv').textContent=l+'ms';document.getElementById('vv').textContent=v+'%';document.getElementById('cb').style.width=c+'%';document.getElementById('mb').style.width=m+'%';document.getElementById('lb').style.width=Math.min(l/3,100)+'%';document.getElementById('vb').style.width=v+'%'}
setInterval(stats,2000);stats();

// Enhanced API Connection
let ws=null;
let sessionId = 'session_' + Math.random().toString(36).slice(2, 8);

function connectWS(){
  try{
    ws = new WebSocket('ws://localhost:8765');
    ws.onopen = () => {
      addLog('WebSocket connected', 'ok');
      toast('BACKEND CONNECTED');
    };
    ws.onmessage = (e) => {
      const d = JSON.parse(e.data);
      if(d.type === 'state') setState(d.state);
      if(d.type === 'response'){
        okCount++;
        document.getElementById('so').textContent = okCount;
        setState('speaking');
        addMsg('p', d.text);
        setTimeout(() => setState('idle'), 2000);
      }
      if(d.type === 'command') addMsg('u', d.text);
    };
    ws.onclose = () => {
      addLog('WebSocket disconnected', 'warn');
      setTimeout(connectWS, 3000);
    };
    ws.onerror = () => {
      addLog('WebSocket error', 'warn');
    };
  } catch(e){
    addLog('WebSocket failed', 'warn');
  }
}

// HTTP API Fallback
async function sendToAPI(text) {
  try {
    const response = await fetch('/api/chat', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ 
        message: text, 
        sessionId: sessionId,
        mode: 'normal'
      })
    });
    
    if (!response.ok) {
      throw new Error('API request failed');
    }
    
    const data = await response.json();
    return data.reply;
  } catch (error) {
    addLog('API error: ' + error.message, 'warn');
    return null;
  }
}

connectWS();

// State
let state='idle',sCount=0,vCount=0,tCount=0,okCount=0;
const sd=document.getElementById('sdot'),stxt=document.getElementById('stxt'),pst=document.getElementById('pst');

// ── MAIN ORB ──
const cv=document.getElementById('orb-canvas'),cx=cv.getContext('2d');
const OW=260,OH=260,OCX=130,OCY=130,OR=104;
let orbT=0,orbAmp=0,orbTamp=0,orbRx=0,orbRy=0,orbRz=0;
const OP=[];for(let i=0;i<2000;i++){const th=Math.acos(1-2*(i+.5)/2000);const ph=Math.PI*(1+Math.sqrt(5))*i;OP.push({ox:Math.sin(th)*Math.cos(ph),oy:Math.sin(th)*Math.sin(ph),oz:Math.cos(th),ph:Math.random()*Math.PI*2,sp:0.35+Math.random()*0.65,baseA:0.006+Math.random()*0.016,sz:0.42+Math.random()*0.95,lat:th,lng:ph});}
function rot(x,y,z,a,b,c){let s,k,ny,nz,nx;s=Math.sin(a);k=Math.cos(a);ny=y*k-z*s;nz=y*s+z*k;y=ny;z=nz;s=Math.sin(b);k=Math.cos(b);nx=x*k+z*s;nz=-x*s+z*k;x=nx;z=nz;s=Math.sin(c);k=Math.cos(c);nx=x*k-y*s;ny=x*s+y*k;return[nx,ny,z];}
const OC={idle:{h:268,sat:78,c0:'rgba(70,0,140,',c1:'rgba(110,0,190,',c2:'rgba(140,30,220,',c3:'rgba(180,50,255,',sp:'rgba(210,170,255,'},listening:{h:278,sat:92,c0:'rgba(90,0,170,',c1:'rgba(140,0,230,',c2:'rgba(180,50,255,',c3:'rgba(220,80,255,',sp:'rgba(240,200,255,'},thinking:{h:260,sat:84,c0:'rgba(60,0,160,',c1:'rgba(100,20,210,',c2:'rgba(140,60,255,',c3:'rgba(180,80,255,',sp:'rgba(210,190,255,'},speaking:{h:282,sat:96,c0:'rgba(110,0,200,',c1:'rgba(160,0,255,',c2:'rgba(200,60,255,',c3:'rgba(230,100,255,',sp:'rgba(255,225,255,'}};
function drawOrb(){orbT+=0.016;orbAmp+=(orbTamp-orbAmp)*0.055;const spd=state==='idle'?1:state==='listening'?2.8:state==='thinking'?1.5:2.2;orbRx+=0.00032*spd;orbRy+=0.00088*spd;orbRz+=0.00020*spd;cx.clearRect(0,0,OW,OH);const col=OC[state]||OC.idle;[{r:OR*2.1,a:0.05+orbAmp*0.07,c:col.c0},{r:OR*1.55,a:0.07+orbAmp*0.10,c:col.c1},{r:OR*1.18,a:0.09+orbAmp*0.16,c:col.c2},{r:OR*0.88,a:0.07+orbAmp*0.13,c:col.c3}].forEach(g=>{const gr=cx.createRadialGradient(OCX,OCY,0,OCX,OCY,g.r);gr.addColorStop(0,g.c+g.a+')');gr.addColorStop(1,'transparent');cx.fillStyle=gr;cx.fillRect(0,0,OW,OH);});const pts=OP.map(d=>{const w1=Math.sin(d.lat*4+orbT*d.sp*1.1+d.ph)*0.5+0.5;const w2=Math.cos(d.lng*3+orbT*d.sp*0.75)*0.5+0.5;const base=d.baseA*(w1*w2);let vw=0;if(state!=='idle'&&orbAmp>0.01){const rp=Math.sin(d.ph*2+orbT*d.sp*4)*Math.cos(d.lat*3+orbT*1.8);vw=orbAmp*(0.055+Math.abs(rp)*0.06);}const r=1+Math.min(base+vw,0.16);const[x,y,z]=rot(d.ox*r,d.oy*r,d.oz*r,orbRx,orbRy,orbRz);const bright=(z+1)/2;return{px:OCX+x*OR,py:OCY+y*OR,z,bright,sz:d.sz,vw,wave:w1*w2};});pts.sort((a,b)=>a.z-b.z);for(const p of pts){const{px,py,bright,sz,vw,wave}=p;const alpha=Math.min(1,0.07+bright*0.58+vw*2.8);const dotSz=Math.max(0.18,sz*(0.28+bright*0.72)*(1+vw*3.5));const lightness=26+bright*50+vw*75;const hue=col.h+bright*20+wave*12;const sat=col.sat-8+bright*22;if(vw>0.028&&state!=='idle'){const dg=cx.createRadialGradient(px,py,0,px,py,dotSz*2.8);dg.addColorStop(0,`hsla(${hue},${sat}%,${lightness+22}%,${Math.min(1,alpha*1.2)})`);dg.addColorStop(0.45,`hsla(${hue-8},${sat}%,${lightness+5}%,${alpha*0.55})`);dg.addColorStop(1,`hsla(${hue-20},75%,35%,0)`);cx.fillStyle=dg;cx.beginPath();cx.arc(px,py,dotSz*2.8,0,Math.PI*2);cx.fill();}else{cx.fillStyle=`hsla(${hue},${sat}%,${lightness}%,${alpha*0.88})`;cx.beginPath();cx.arc(px,py,dotSz,0,Math.PI*2);cx.fill();}}const rim=cx.createRadialGradient(OCX,OCY,OR*0.80,OCX,OCY,OR*1.10);rim.addColorStop(0,'transparent');rim.addColorStop(0.5,col.c3+(0.10+orbAmp*0.28)+')');rim.addColorStop(1,'transparent');cx.fillStyle=rim;cx.beginPath();cx.arc(OCX,OCY,OR*1.10,0,Math.PI*2);cx.fill();const spec=cx.createRadialGradient(OCX-35,OCY-45,0,OCX-35,OCY-45,OR*0.42);spec.addColorStop(0,col.sp+(0.22+orbAmp*0.18)+')');spec.addColorStop(1,'transparent');cx.fillStyle=spec;cx.beginPath();cx.arc(OCX-35,OCY-45,OR*0.42,0,Math.PI*2);cx.fill();requestAnimationFrame(drawOrb);}
drawOrb();

// ── SIRI MINI ORB ──
const sc=document.getElementById('siri-canvas'),sx=sc.getContext('2d');
const SW=44,SH=44,SCX=22,SCY=22,SR=17;
let sT=0,sAmp=0,sTamp=0,sRx=0,sRy=0,sRz=0;
const SP=[];for(let i=0;i<320;i++){const th=Math.acos(1-2*(i+.5)/320);const ph=Math.PI*(1+Math.sqrt(5))*i;SP.push({ox:Math.sin(th)*Math.cos(ph),oy:Math.sin(th)*Math.sin(ph),oz:Math.cos(th),ph:Math.random()*Math.PI*2,sp:0.4+Math.random()*0.6,baseA:0.01+Math.random()*0.02,sz:0.5+Math.random()*0.7,lat:th,lng:ph});}
function drawSiriOrb(){sT+=0.018;sAmp+=(sTamp-sAmp)*0.07;const spd=state==='idle'?1:state==='listening'?2.8:2.0;sRx+=0.0004*spd;sRy+=0.001*spd;sRz+=0.00025*spd;sx.clearRect(0,0,SW,SH);const g1=sx.createRadialGradient(SCX,SCY,0,SCX,SCY,SR*1.8);g1.addColorStop(0,'rgba(110,0,200,'+(0.12+sAmp*0.18)+')');g1.addColorStop(1,'transparent');sx.fillStyle=g1;sx.fillRect(0,0,SW,SH);const pts=SP.map(d=>{const w1=Math.sin(d.lat*4+sT*d.sp*1.2+d.ph)*0.5+0.5;const w2=Math.cos(d.lng*3+sT*d.sp*0.8)*0.5+0.5;const base=d.baseA*(w1*w2);const vw=state!=='idle'?sAmp*(0.05+Math.sin(d.ph+sT*d.sp*3)*0.04):0;const r=1+Math.min(base+vw,0.18);const[x,y,z]=rot(d.ox*r,d.oy*r,d.oz*r,sRx,sRy,sRz);const bright=(z+1)/2;return{px:SCX+x*SR,py:SCY+y*SR,z,bright,sz:d.sz,vw,wave:w1*w2};});pts.sort((a,b)=>a.z-b.z);for(const p of pts){const{px,py,bright,sz,vw,wave}=p;const alpha=Math.min(1,0.08+bright*0.65+vw*3);const dotSz=Math.max(0.18,sz*(0.3+bright*0.7)*(1+vw*3.5));const hue=270+bright*20+wave*12;const lightness=28+bright*50+vw*70;if(vw>0.025&&state!=='idle'){const dg=sx.createRadialGradient(px,py,0,px,py,dotSz*2.5);dg.addColorStop(0,`hsla(${hue},95%,${lightness+18}%,${alpha})`);dg.addColorStop(1,`hsla(${hue-20},75%,35%,0)`);sx.fillStyle=dg;sx.beginPath();sx.arc(px,py,dotSz*2.5,0,Math.PI*2);sx.fill();}else{sx.fillStyle=`hsla(${hue},88%,${lightness}%,${alpha*0.9})`;sx.beginPath();sx.arc(px,py,dotSz,0,Math.PI*2);sx.fill();}}const rim=sx.createRadialGradient(SCX,SCY,SR*0.80,SCX,SCY,SR*1.08);rim.addColorStop(0,'transparent');rim.addColorStop(0.6,'rgba(180,50,255,'+(0.10+sAmp*0.28)+')');rim.addColorStop(1,'transparent');sx.fillStyle=rim;sx.beginPath();sx.arc(SCX,SCY,SR*1.08,0,Math.PI*2);sx.fill();const spec=sx.createRadialGradient(SCX-5,SCY-6,0,SCX-5,SCY-6,SR*0.38);spec.addColorStop(0,'rgba(230,190,255,'+(0.18+sAmp*0.14)+')');spec.addColorStop(1,'transparent');sx.fillStyle=spec;sx.beginPath();sx.arc(SCX-5,SCY-6,SR*0.38,0,Math.PI*2);sx.fill();requestAnimationFrame(drawSiriOrb);}
drawSiriOrb();

// ── SIRI POPUP CONTROLS ──
let siriAutoHideTimer=null;
function showSiri(statusText,transcriptText){const popup=document.getElementById('siri-popup');const statusEl=document.getElementById('siri-status');const transcriptEl=document.getElementById('siri-transcript');const waveEl=document.getElementById('siri-waveform');popup.classList.add('show');statusEl.textContent=statusText||'LISTENING';statusEl.className=statusText==='STANDBY'?'':'active';if(transcriptText){transcriptEl.textContent=transcriptText;transcriptEl.classList.add('show');}else{transcriptEl.textContent='';transcriptEl.classList.remove('show');}const isActive=state==='listening'||state==='speaking';waveEl.className='siri-waveform'+(isActive?' active':'');sTamp=isActive?(0.35+Math.random()*0.2):0.05;if(siriAutoHideTimer)clearTimeout(siriAutoHideTimer);}
function hideSiri(){document.getElementById('siri-popup').classList.remove('show');document.getElementById('siri-transcript').classList.remove('show');document.getElementById('siri-waveform').className='siri-waveform';sTamp=0;if(siriAutoHideTimer)clearTimeout(siriAutoHideTimer);}
function siriAutoHide(ms){if(siriAutoHideTimer)clearTimeout(siriAutoHideTimer);siriAutoHideTimer=setTimeout(hideSiri,ms||3000);}

// ── ORB AMP ──
function setOrbAmp(s){if(s==='listening'){let v=0;const iv=setInterval(()=>{if(state!=='listening'){clearInterval(iv);orbTamp=0;return;}orbTamp=0.35+Math.sin(v*1.1)*0.2+Math.random()*0.15;v+=0.22;},80);}else if(s==='speaking'){let v=0;const iv=setInterval(()=>{if(state!=='speaking'){clearInterval(iv);orbTamp=0;return;}orbTamp=0.22+Math.abs(Math.sin(v*1.6))*0.28+Math.random()*0.1;v+=0.15;},65);}else if(s==='thinking'){let v=0;const iv=setInterval(()=>{if(state!=='thinking'){clearInterval(iv);orbTamp=0;return;}orbTamp=0.08+Math.sin(v*0.8)*0.06;v+=0.1;},100);}else{orbTamp=0;}}

// ── SET STATE ──
function setState(s){state=s;const wf=document.getElementById('wf');wf.className='wf '+(['listening','speaking'].includes(s)?'on':'');sd.style.background='';sd.style.boxShadow='';if(s==='idle'){sd.className='sdot';stxt.textContent='STANDBY — SAY "PRAGYA"';pst.textContent='STANDBY';siriAutoHide(1800);}else if(s==='listening'){sd.className='sdot a';stxt.textContent='LISTENING...';pst.textContent='LISTENING';showSiri('LISTENING');document.getElementById('siri-waveform').classList.add('active');sTamp=0.4;}else if(s==='thinking'){sd.className='sdot';sd.style.background='#aa66ff';sd.style.boxShadow='0 0 8px #aa66ff';stxt.textContent='PROCESSING...';pst.textContent='THINKING';showSiri('THINKING...');document.getElementById('siri-waveform').classList.remove('active');sTamp=0.12;}else if(s==='speaking'){sd.className='sdot g';stxt.textContent='RESPONDING...';pst.textContent='SPEAKING';const msgs=document.getElementById('msgs');const lastAI=[...msgs.querySelectorAll('.msg.p')].pop();const txt=lastAI?lastAI.textContent.replace('PRAGYA','').trim().slice(0,60):'';showSiri('SPEAKING',txt);document.getElementById('siri-waveform').classList.add('active');sTamp=0.35;siriAutoHide(4000);}setOrbAmp(s);}

function activateManual(){if(state!=='idle')return;addLog('Manual activation','ok');toast('PRAGYA ACTIVATED');setState('listening');setTimeout(()=>setState('idle'),3000)}

// ── MIC ──
let micOn=false,rec=null;
function toggleMic(){if(!('webkitSpeechRecognition'in window||'SpeechRecognition'in window)){toast('USE CHROME FOR VOICE');return}if(micOn){if(rec)rec.stop();micOn=false;document.getElementById('bm').classList.remove('on');setState('idle');return}const SR=window.SpeechRecognition||window.webkitSpeechRecognition;rec=new SR();rec.lang='en-IN';rec.continuous=false;rec.interimResults=true;rec.onstart=()=>{micOn=true;document.getElementById('bm').classList.add('on');setState('listening');};rec.onresult=(e)=>{const t=Array.from(e.results).map(r=>r[0].transcript).join(' ');document.getElementById('ci').value=t;if(e.results[e.results.length-1].isFinal)cmd(t,'voice')};rec.onerror=()=>{micOn=false;document.getElementById('bm').classList.remove('on');setState('idle')};rec.onend=()=>{micOn=false;document.getElementById('bm').classList.remove('on')};rec.start()}

function sendText(){const i=document.getElementById('ci'),v=i.value.trim();if(!v)return;i.value='';cmd(v,'text')}
function sq(t){cmd(t,'text')}

// Enhanced command processing with API integration
async function cmd(text,src){
  if(!text.trim())return;
  sCount++;
  if(src==='voice')vCount++;
  else tCount++;
  document.getElementById('sc').textContent=sCount;
  document.getElementById('st').textContent=sCount;
  document.getElementById('sv').textContent=vCount;
  document.getElementById('stc').textContent=tCount;
  addMsg('u',text);
  addLog('CMD ['+src.toUpperCase()+']: '+text.slice(0,30),'');
  addRecent(text);
  setState('thinking');
  
  // Try WebSocket first
  if(ws && ws.readyState===1){
    ws.send(JSON.stringify({type:'command',text}));
    return;
  }
  
  // Fallback to HTTP API
  const startTime = Date.now();
  try {
    const response = await sendToAPI(text);
    const latency = Date.now() - startTime;
    document.getElementById('lv').textContent = latency + 'ms';
    document.getElementById('lb').style.width = Math.min(latency/3, 100) + '%';
    
    if(response) {
      okCount++;
      document.getElementById('so').textContent = okCount;
      setState('speaking');
      addMsg('p', response);
      addLog('API response received', 'ok');
      
      // Text-to-speech
      if('speechSynthesis'in window){
        const u=new SpeechSynthesisUtterance(response);
        u.rate=0.95;
        u.onend=()=>setState('idle');
        speechSynthesis.speak(u);
      } else {
        setTimeout(()=>setState('idle'),2000);
      }
    } else {
      throw new Error('No response from API');
    }
  } catch (error) {
    // Local fallback
    const rep=local(text);
    okCount++;
    document.getElementById('so').textContent=okCount;
    setState('speaking');
    addMsg('p',rep);
    addLog('Local response fallback','ok');
    if('speechSynthesis'in window){
      const u=new SpeechSynthesisUtterance(rep);
      u.rate=0.95;
      u.onend=()=>setState('idle');
      speechSynthesis.speak(u);
    } else setTimeout(()=>setState('idle'),2000);
  }
}

function local(t){t=t.toLowerCase();if(t.includes('time'))return'It is '+new Date().toLocaleTimeString('en-IN')+'.';if(t.includes('hello')||t.includes('hi'))return"Hello! I'm Pragya. How can I assist?";if(t.includes('joke'))return"Why do programmers prefer dark mode? Because light attracts bugs!";return'Command acknowledged. Connect the Python backend for full AI responses.';}

function addMsg(r,t){const m=document.getElementById('msgs'),d=document.createElement('div');d.className='msg '+(r==='u'?'u':'p');d.innerHTML='<div class="ml">'+(r==='u'?'YOU':'PRAGYA')+'</div>'+t.replace(/&/g,'&amp;').replace(/</g,'&lt;');m.appendChild(d);m.scrollTop=m.scrollHeight}
function addLog(msg,type){const l=document.getElementById('log'),n=new Date(),t=String(n.getHours()).padStart(2,'0')+':'+String(n.getMinutes()).padStart(2,'0')+':'+String(n.getSeconds()).padStart(2,'0'),i=document.createElement('div');i.className='li '+type;i.innerHTML='<span class="lt">'+t+'</span><span class="lm">'+msg+'</span>';l.appendChild(i);if(l.children.length>20)l.removeChild(l.firstChild);l.scrollTop=l.scrollHeight}
function addRecent(t){const el=document.getElementById('rc');if(el.children.length===1&&el.children[0].textContent==='No commands yet...')el.innerHTML='';const d=document.createElement('div');d.style.cssText='font-family:Share Tech Mono,monospace;font-size:10px;color:var(--text-dim);padding:4px 0;border-bottom:1px solid var(--border);cursor:pointer';d.textContent='> '+t.slice(0,38);d.onclick=()=>{document.getElementById('ci').value=t};el.insertBefore(d,el.firstChild);if(el.children.length>8)el.removeChild(el.lastChild)}
function toast(msg){const t=document.getElementById('toast');t.textContent=msg;t.classList.add('show');setTimeout(()=>t.classList.remove('show'),2800)}

// Wake word detection
let tb='';document.addEventListener('keypress',e=>{if(e.target.tagName==='INPUT')return;tb+=e.key.toLowerCase();if(tb.length>10)tb=tb.slice(-10);if(tb.includes('pragya')){tb='';addLog('Wake word: "pragya"','ok');toast('WAKE WORD DETECTED');setState('listening');setTimeout(()=>setState('idle'),3000)}});

// Automation features
function setupAutomation() {
  // Auto-reconnect WebSocket
  setInterval(() => {
    if (!ws || ws.readyState !== 1) {
      connectWS();
    }
  }, 5000);
  
  // Periodic status updates
  setInterval(() => {
    if (ws && ws.readyState === 1) {
      ws.send(JSON.stringify({type: 'ping'}));
    }
  }, 30000);
  
  // Session persistence
  localStorage.setItem('pragya_session', sessionId);
  localStorage.setItem('pragya_stats', JSON.stringify({
    total: sCount,
    voice: vCount,
    text: tCount,
    success: okCount
  }));
}

// Load previous session
function loadSession() {
  const savedSession = localStorage.getItem('pragya_session');
  if (savedSession) {
    sessionId = savedSession;
  }
  
  const savedStats = localStorage.getItem('pragya_stats');
  if (savedStats) {
    const stats = JSON.parse(savedStats);
    sCount = stats.total || 0;
    vCount = stats.voice || 0;
    tCount = stats.text || 0;
    okCount = stats.success || 0;
    
    document.getElementById('sc').textContent = sCount;
    document.getElementById('st').textContent = sCount;
    document.getElementById('sv').textContent = vCount;
    document.getElementById('stc').textContent = tCount;
    document.getElementById('so').textContent = okCount;
  }
}

// Initialize
loadSession();
setupAutomation();
addLog('System boot complete','ok');
addLog('Wake word engine active','ok');
addLog('API integration ready','ok');
toast('PRAGYA ONLINE — SAY MY NAME');
