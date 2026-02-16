const modes = { pomodoro: 'Focus Time', shortBreak: 'Short Break', longBreak: 'Long Break' };

let settings = {
  pomodoro: 25,
  shortBreak: 5,
  longBreak: 15,
  autoStartBreaks: false,
  soundEnabled: true
};

const el = id => document.getElementById(id);
const tabs = document.querySelectorAll('.tab');
let min = settings.pomodoro, sec = 0, timer = null, sessions = 0;

function loadSettings() {
  const s = localStorage.getItem('farmSettings');
  if (s) settings = JSON.parse(s);
}

function saveSettings() {
  localStorage.setItem('farmSettings', JSON.stringify(settings));
}

function switchMode(m) {
  clearInterval(timer);
  timer = null;
  min = settings[m];
  sec = 0;
  tabs.forEach(b => b.classList.toggle('active', b.dataset.mode === m));
  el('timerLabel').textContent = modes[m];
  updateDisplay();
}

function updateDisplay() {
  el('timerDisplay').textContent = `${String(min).padStart(2,'0')}:${String(sec).padStart(2,'0')}`;
  document.title = `${String(min).padStart(2,'0')}:${String(sec).padStart(2,'0')} – ${modes[getCurrentMode()]}`;
}

function tick() {
  if (sec > 0) sec--;
  else if (min > 0) { min--; sec = 59; }
  else return completeSession();
  updateDisplay();
}

function startTimer() {
  if (timer) return;
  timer = setInterval(tick, 1000);
  el('startBtn').classList.add('hidden');
  el('pauseBtn').classList.remove('hidden');
}

function pauseTimer() {
  clearInterval(timer);
  timer = null;
  el('pauseBtn').classList.add('hidden');
  el('startBtn').classList.remove('hidden');
}

function resetTimer() {
  pauseTimer();
  const mode = getCurrentMode();
  min = settings[mode];
  sec = 0;
  updateDisplay();
}

function playSound() {
  if (!settings.soundEnabled) return;
  const ctx = new AudioContext(), osc = ctx.createOscillator(), gain = ctx.createGain();
  osc.connect(gain); gain.connect(ctx.destination);
  osc.frequency.value = 800;
  gain.gain.setValueAtTime(0.3, ctx.currentTime);
  gain.gain.exponentialRampToValueAtTime(0.01, ctx.currentTime + 0.5);
  osc.start(); osc.stop(ctx.currentTime + 0.5);
}

function notify() {
  if (Notification.permission === 'granted') {
    new Notification('Pomodoro Timer', {
      body: getCurrentMode() === 'pomodoro' ? 'Take a break now!' : 'Time to focus!'
    });
  }
}

function getCurrentMode() {
  return [...tabs].find(b => b.classList.contains('active')).dataset.mode;
}

function completeSession() {
  clearInterval(timer);
  timer = null;
  playSound();
  notify();

  const mode = getCurrentMode();
  if (mode === 'pomodoro') {
    sessions++;
    el('sessionCount').textContent = sessions;
    switchMode((sessions % 4 === 0) ? 'longBreak' : 'shortBreak');
  } else {
    switchMode('pomodoro');
  }

  if (settings.autoStartBreaks && getCurrentMode() !== 'pomodoro') {
    setTimeout(startTimer, 500);
  }
}

function openSettings() {
  el('settingsPanel').classList.remove('hidden');
}

function closeSettings() {
  el('settingsPanel').classList.add('hidden');
}

function setupKeyboard() {
  document.addEventListener('keydown', e => {
    if (e.code === 'Space') {
      e.preventDefault();
      timer ? pauseTimer() : startTimer();
    }
    if (e.key.toLowerCase() === 'r') resetTimer();
    if (e.key.toLowerCase() === 's') openSettings();
  });
}

function init() {
  loadSettings();
  Notification.requestPermission();

  tabs.forEach(b => b.addEventListener('click', () => switchMode(b.dataset.mode)));

  el('startBtn').addEventListener('click', startTimer);
  el('pauseBtn').addEventListener('click', pauseTimer);
  el('resetBtn').addEventListener('click', resetTimer);
  el('settingsBtn').addEventListener('click', openSettings);
  el('closeSettings').addEventListener('click', closeSettings);
  el('saveSettings').addEventListener('click', () => {
    ['pomodoro', 'shortBreak', 'longBreak'].forEach(m => {
      const v = parseInt(el(m + 'Time').value, 10);
      if (v >= 1) settings[m] = v;
    });
    settings.autoStartBreaks = el('autoStartBreaks').checked;
    settings.soundEnabled = el('soundEnabled').checked;
    saveSettings();
    resetTimer();
    closeSettings();
  });

  setupKeyboard();
  updateDisplay();
}

init();
