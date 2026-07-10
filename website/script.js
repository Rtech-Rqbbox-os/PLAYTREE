const SFX={
  ctx:null,
  init(){if(!this.ctx)this.ctx=new(window.AudioContext||window.webkitAudioContext)()},
  play(type){
    this.init();const c=this.ctx,t=c.currentTime;
    const o=c.createOscillator(),g=c.createGain();
    o.connect(g);g.connect(c.destination);
    switch(type){
      case'click':o.type='sine';o.frequency.setValueAtTime(600,t);o.frequency.exponentialRampToValueAtTime(400,t+.1);g.gain.setValueAtTime(.15,t);g.gain.exponentialRampToValueAtTime(.001,t+.1);o.start(t);o.stop(t+.1);break;
      case'hover':o.type='sine';o.frequency.setValueAtTime(800,t);g.gain.setValueAtTime(.05,t);g.gain.exponentialRampToValueAtTime(.001,t+.06);o.start(t);o.stop(t+.06);break;
      case'confirm':o.type='sine';o.frequency.setValueAtTime(500,t);o.frequency.setValueAtTime(700,t+.1);g.gain.setValueAtTime(.2,t);g.gain.exponentialRampToValueAtTime(.001,t+.25);o.start(t);o.stop(t+.25);break;
      case'error':o.type='sawtooth';o.frequency.setValueAtTime(200,t);o.frequency.exponentialRampToValueAtTime(100,t+.2);g.gain.setValueAtTime(.12,t);g.gain.exponentialRampToValueAtTime(.001,t+.25);o.start(t);o.stop(t+.25);break;
      case'collect':{o.type='sine';o.frequency.setValueAtTime(523,t);o.frequency.setValueAtTime(659,t+.08);o.frequency.setValueAtTime(784,t+.16);g.gain.setValueAtTime(.2,t);g.gain.exponentialRampToValueAtTime(.001,t+.3);o.start(t);o.stop(t+.3);break}
      case'magic':{o.type='sine';o.frequency.setValueAtTime(400,t);o.frequency.exponentialRampToValueAtTime(1200,t+.3);g.gain.setValueAtTime(.15,t);g.gain.exponentialRampToValueAtTime(.001,t+.4);o.start(t);o.stop(t+.4);break}
      case'powerup':{const o2=c.createOscillator(),g2=c.createGain();o2.connect(g2);g2.connect(c.destination);o.type='square';o.frequency.setValueAtTime(300,t);o.frequency.setValueAtTime(500,t+.1);o.frequency.setValueAtTime(700,t+.2);o2.type='sawtooth';o2.frequency.setValueAtTime(305,t);o2.frequency.setValueAtTime(505,t+.1);o2.frequency.setValueAtTime(705,t+.2);g.gain.setValueAtTime(.1,t);g.gain.exponentialRampToValueAtTime(.001,t+.35);g2.gain.setValueAtTime(.05,t);g2.gain.exponentialRampToValueAtTime(.001,t+.35);o.start(t);o.stop(t+.35);o2.start(t);o2.stop(t+.35);break}
      case'heal':{o.type='sine';o.frequency.setValueAtTime(600,t);o.frequency.setValueAtTime(900,t+.15);o.frequency.setValueAtTime(1200,t+.3);g.gain.setValueAtTime(.15,t);g.gain.exponentialRampToValueAtTime(.001,t+.4);o.start(t);o.stop(t+.4);break}
    }
  }
};

document.addEventListener('DOMContentLoaded',()=>{
  document.querySelectorAll('[data-sfx]').forEach(el=>{
    const sfx=el.dataset.sfx;
    el.addEventListener('mouseenter',()=>{if(sfx==='hover')SFX.play('hover')});
    el.addEventListener('click',()=>{if(sfx!=='hover')SFX.play(sfx)});
  });

  initParticles();
  animateCounters();
  initAuth();
});

function initParticles(){
  const c=document.getElementById('particles-bg');
  for(let i=0;i<30;i++){
    const p=document.createElement('div');
    const size=Math.random()*4+1;
    p.style.cssText=`position:absolute;width:${size}px;height:${size}px;background:rgba(80,255,120,${Math.random()*.3+.1});border-radius:50%;left:${Math.random()*100}%;top:${Math.random()*100}%;animation:float ${Math.random()*10+10}s linear infinite;animation-delay:-${Math.random()*10}s`;
    c.appendChild(p);
  }
  const style=document.createElement('style');
  style.textContent='@keyframes float{0%{transform:translateY(100vh) scale(0);opacity:0}10%{opacity:1}90%{opacity:1}100%{transform:translateY(-10vh) scale(1);opacity:0}}';
  document.head.appendChild(style);
}

function animateCounters(){
  document.querySelectorAll('[data-count]').forEach(el=>{
    const target=parseInt(el.dataset.count);
    const duration=2000;
    const start=performance.now();
    const tick=(now)=>{
      const elapsed=now-start;
      const progress=Math.min(elapsed/duration,1);
      const eased=1-Math.pow(1-progress,3);
      el.textContent=Math.floor(eased*target);
      if(progress<1)requestAnimationFrame(tick);
      else el.textContent=target;
    };
    const observer=new IntersectionObserver(entries=>{
      if(entries[0].isIntersecting){requestAnimationFrame(tick);observer.disconnect()}
    },{threshold:.5});
    observer.observe(el);
  });
}

function initAuth(){
  const authBtn=document.getElementById('auth-btn');
  const signupBtn=document.getElementById('signup-btn');
  const modal=document.getElementById('auth-modal');
  const overlay=modal.querySelector('.modal-overlay');
  const closeBtn=modal.querySelector('.modal-close');
  const loginPanel=document.getElementById('auth-login');
  const registerPanel=document.getElementById('auth-register');
  const profilePanel=document.getElementById('auth-profile');
  const showReg=document.getElementById('show-register');
  const showLogin=document.getElementById('show-login');
  const loginForm=document.getElementById('login-form');
  const registerForm=document.getElementById('register-form');
  const logoutBtn=document.getElementById('logout-btn');
  const msgEl=document.getElementById('auth-message');

  function getUsers(){try{return JSON.parse(localStorage.getItem('rhystech_users')||'{}')}catch{return{}}}
  function saveUsers(u){localStorage.setItem('rhystech_users',JSON.stringify(u))}
  function getSession(){try{return JSON.parse(localStorage.getItem('rhystech_session')||'null')}catch{return null}}
  function saveSession(s){s?localStorage.setItem('rhystech_session',JSON.stringify(s)):localStorage.removeItem('rhystech_session')}
  function showMsg(txt,type){msgEl.textContent=txt;msgEl.className='auth-msg '+type;setTimeout(()=>msgEl.className='auth-msg hidden',3000)}

  function showPanel(panel){
    loginPanel.classList.add('hidden');registerPanel.classList.add('hidden');profilePanel.classList.add('hidden');
    panel.classList.remove('hidden');msgEl.className='auth-msg hidden';
  }

  function updateAuthBtn(){
    const session=getSession();
    if(session){
      authBtn.textContent=session.name.charAt(0).toUpperCase();
      authBtn.classList.add('btn-accent');
      signupBtn.style.display='none';
    }else{
      authBtn.textContent='Sign In';
      authBtn.classList.remove('btn-accent');
      signupBtn.style.display='inline-block';
    }
  }

  function openModal(){
    const session=getSession();
    if(session){
      const users=getUsers();
      const u=users[session.email]||{};
      document.getElementById('profile-avatar').textContent=session.name.charAt(0).toUpperCase();
      document.getElementById('profile-name').textContent=session.name;
      document.getElementById('profile-email').textContent=session.email;
      document.getElementById('profile-since').textContent=u.created||'2026';
      document.getElementById('profile-hours').textContent=u.hours||0;
      document.getElementById('profile-rounds').textContent=u.rounds||0;
      document.getElementById('profile-bosses').textContent=u.bosses||0;
      showPanel(profilePanel);
    }else{
      showPanel(loginPanel);
    }
    modal.classList.remove('hidden');
  }

  function openModalRegister(){
    showPanel(registerPanel);
    modal.classList.remove('hidden');
  }

  authBtn.addEventListener('click',openModal);
  signupBtn.addEventListener('click',openModalRegister);
  overlay.addEventListener('click',()=>modal.classList.add('hidden'));
  closeBtn.addEventListener('click',()=>modal.classList.add('hidden'));
  showReg.addEventListener('click',e=>{e.preventDefault();showPanel(registerPanel)});
  showLogin.addEventListener('click',e=>{e.preventDefault();showPanel(loginPanel)});

  loginForm.addEventListener('submit',e=>{
    e.preventDefault();
    const email=document.getElementById('login-email').value.trim().toLowerCase();
    const pass=document.getElementById('login-password').value;
    const users=getUsers();
    if(!users[email]){showMsg('Account not found','error');SFX.play('error');return}
    if(users[email].password!==pass){showMsg('Wrong password','error');SFX.play('error');return}
    saveSession({email,name:users[email].name});
    SFX.play('powerup');showMsg('Welcome back, '+users[email].name+'!','success');
    setTimeout(()=>{updateAuthBtn();modal.classList.add('hidden')},1000);
  });

  registerForm.addEventListener('submit',e=>{
    e.preventDefault();
    const name=document.getElementById('reg-name').value.trim();
    const email=document.getElementById('reg-email').value.trim().toLowerCase();
    const pass=document.getElementById('reg-password').value;
    const confirm=document.getElementById('reg-confirm').value;
    if(pass!==confirm){showMsg('Passwords do not match','error');SFX.play('error');return}
    const users=getUsers();
    if(users[email]){showMsg('Email already registered','error');SFX.play('error');return}
    users[email]={name,email,password:pass,created:new Date().getFullYear(),hours:0,rounds:0,bosses:0,cosmetics:{}};
    saveUsers(users);
    saveSession({email,name});
    SFX.play('heal');showMsg('Account created! Welcome, '+name+'!','success');
    setTimeout(()=>{updateAuthBtn();modal.classList.add('hidden')},1200);
  });

  logoutBtn.addEventListener('click',()=>{
    saveSession(null);updateAuthBtn();modal.classList.add('hidden');
    SFX.play('click');
  });

  updateAuthBtn();

  const trailerBtn=document.getElementById('trailer-btn');
  if(trailerBtn){
    trailerBtn.addEventListener('click',()=>window.open('trailer.html','_blank'));
  }
}
