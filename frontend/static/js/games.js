const WebApp = window.Telegram.WebApp;
WebApp.expand();

// Утилиты
function sendAction(action, payload={}) {
  WebApp.sendData(JSON.stringify({ action, ...payload }));
}

// Анимация Дартс
function animateDarts(force, angle) {
  const canvas = document.createElement('canvas');
  canvas.width = canvas.height = 300;
  canvas.classList.add('mx-auto', 'my-4');
  document.body.appendChild(canvas);
  const ctx = canvas.getContext('2d');
  let t = 0, len = 100 * force, rad = angle*Math.PI/180;
  function frame() {
    ctx.clearRect(0,0,300,300);
    const progress = Math.min(1, t/30);
    const x = 150 + len*Math.cos(rad)*progress;
    const y = 150 + len*Math.sin(rad)*progress;
    ctx.beginPath(); ctx.arc(x,y,8,0,2*Math.PI); ctx.fillStyle="#f59e0b"; ctx.fill();
    if (t++ < 30) requestAnimationFrame(frame);
  }
  frame();
}

// Примеры обработчиков
document.getElementById('btn-darts').onclick = () => {
  const force = Math.random(), angle = Math.random()*360;
  animateDarts(force, angle);
  setTimeout(()=> sendAction('darts', { force, angle }), 1000);
};

document.getElementById('btn-mines').onclick = () => {
  // Здесь можно отрисовать поле Canvas перед отправкой
  sendAction('mines', { size:5, num_mines:5, i:2, j:2 });
};

document.getElementById('btn-dice').onclick = () => {
  // 3D-анимацию кубика можно добавить, пока — простой таймер
  setTimeout(()=> sendAction('dice'), 800);
};

document.getElementById('btn-wheel').onclick = () => {
  const segments = ['10','20','50','x2','0','100'];
  // Canvas-анимация колеса здесь...
  setTimeout(()=> sendAction('wheel', { segments }), 2000);
};

document.getElementById('btn-pay').onclick = () => {
  sendAction('pay');
};
