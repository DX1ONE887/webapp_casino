const WebApp = window.Telegram.WebApp;
WebApp.expand();

function send(name, payload) {
  WebApp.sendData(JSON.stringify({ game: name, ...payload }));
}

// Дартс
function animateDarts(force, angle) {
  const canvas = document.getElementById('canvas-darts');
  const ctx = canvas.getContext('2d');
  const len = force * 100;
  let t = 0;
  function draw() {
    ctx.clearRect(0,0,300,300);
    const x = 150 + len * Math.cos(angle * Math.PI/180) * (t/30);
    const y = 150 + len * Math.sin(angle * Math.PI/180) * (t/30);
    ctx.beginPath(); ctx.arc(x,y,5,0,2*Math.PI); ctx.fill();
    t++;
    if (t <= 30) requestAnimationFrame(draw);
  }
  draw();
}

function animateWheel(segments) {
  const canvas = document.getElementById('canvas-wheel');
  const ctx = canvas.getContext('2d');
  const N = segments.length;
  const anglePer = 2*Math.PI/N;
  let t = 0;
  const target = Math.random()*2*Math.PI + 10*2*Math.PI;
  function drawWheel(theta) {
    ctx.clearRect(0,0,300,300);
    for (let i=0; i<N; i++) {
      ctx.beginPath();
      ctx.moveTo(150,150);
      ctx.arc(150,150,140,i*anglePer+theta,(i+1)*anglePer+theta);
      ctx.fillStyle = i%2?'#ffd700':'#ff8c00';
      ctx.fill();
    }
  }
  function spin() {
    t++;
    const prog = t/200;
    const theta = target*(1 - Math.exp(-5*prog));
    drawWheel(theta);
    if (t < 200) requestAnimationFrame(spin);
    else {
      const idx = Math.floor(((theta%(2*Math.PI))/(2*Math.PI))*N);
      send('wheel', { segments });
    }
  }
  spin();
}

document.getElementById('btn-darts').addEventListener('click', () => {
  const force = Math.random();
  const angle = Math.random()*360;
  animateDarts(force, angle);
  setTimeout(() => send('darts', { force, angle }), 1000);
});

document.getElementById('btn-mines').addEventListener('click', () => {
  send('mines', { size: 5, num_mines: 5, i: 2, j: 2 });
});

document.getElementById('btn-dice').addEventListener('click', () => {
  send('dice', {});
});

document.getElementById('btn-wheel').addEventListener('click', () => {
  animateWheel(['10','20','50','x2','0','100']);
});