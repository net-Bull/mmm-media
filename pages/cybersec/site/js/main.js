import { createScene } from './scene.js';

const reduce = window.matchMedia && matchMedia('(prefers-reduced-motion: reduce)').matches;
const rail = document.getElementById('rail');

document.getElementById('nl').addEventListener('submit', (e) => {
  e.preventDefault();
  document.getElementById('msg').textContent = 'Anteprima: l’iscrizione non è ancora attiva.';
});

try {
  createScene(document.getElementById('scene'), {
    reduce,
    onProgress: (p) => { rail.style.height = (p * 100).toFixed(1) + '%'; }
  });
  document.body.classList.add('ready');
} catch (err) {
  document.body.classList.add('nogl', 'ready');
}
