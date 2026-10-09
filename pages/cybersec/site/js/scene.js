// Scena 3D: città di chip e circuiti con strati di rete neurale sospesi.
// Camera in volo guidata dallo scroll. Post-processing: bloom, aberrazione cromatica, grana, vignettatura.
import * as THREE from 'three';
import { EffectComposer } from '../vendor/postprocessing/EffectComposer.js';
import { RenderPass } from '../vendor/postprocessing/RenderPass.js';
import { UnrealBloomPass } from '../vendor/postprocessing/UnrealBloomPass.js';
import { ShaderPass } from '../vendor/postprocessing/ShaderPass.js';

export function createScene(canvas, opts) {
  const reduce = !!opts.reduce;
  const small = Math.min(innerWidth, innerHeight) < 700;
  const renderer = new THREE.WebGLRenderer({ canvas, antialias: false, powerPreference: 'high-performance' });
  const pr = Math.min(window.devicePixelRatio || 1, small ? 1.25 : 1.5);
  renderer.setPixelRatio(pr);
  renderer.setClearColor(0x05070d, 1);

  const scene = new THREE.Scene();
  const camera = new THREE.PerspectiveCamera(62, 1, 0.1, 900);
  const uTime = { value: 0 }, uCamZ = { value: 40 }, uCamX = { value: 0 };
  const U = { uTime, uCamZ, uCamX };

  const common =
    'uniform float uTime; uniform float uCamZ; uniform float uCamX;' +
    'float hash(vec2 p){ return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453); }' +
    'vec3 FOG = vec3(0.02, 0.027, 0.05);' +
    'vec3 ICE = vec3(0.36, 0.82, 1.0); vec3 AMBER = vec3(1.0, 0.4, 0.1);' +
    'float pulse(vec3 w){ float d = length(w.xz - vec2(uCamX, uCamZ)); float r = mod(uTime * 46.0, 300.0); return exp(-pow((d - r) / 7.0, 2.0)) * (1.0 - r / 300.0); }' +
    'float fogF(vec3 w){ float d = length(cameraPosition - w); return 1.0 - exp(-pow(d * 0.0046, 2.0)); }';

  let seed = 11;
  const rnd = () => { seed = (seed * 16807) % 2147483647; return (seed - 1) / 2147483646; };

  // --- chip
  const chipMat = new THREE.ShaderMaterial({
    uniforms: U,
    vertexShader:
      'varying vec3 vW; varying vec3 vN; varying vec2 vL; varying float vSeed;' +
      'void main(){ mat4 m = modelMatrix * instanceMatrix; vec4 wp = m * vec4(position, 1.0);' +
      'vW = wp.xyz; vN = normalize(mat3(m) * normal); vL = position.xz; vSeed = instanceMatrix[3].x * 0.137 + instanceMatrix[3].z * 0.071;' +
      'gl_Position = projectionMatrix * viewMatrix * wp; }',
    fragmentShader: common +
      'varying vec3 vW; varying vec3 vN; varying vec2 vL; varying float vSeed;' +
      'void main(){' +
      ' vec3 V = normalize(cameraPosition - vW);' +
      ' vec3 col = vec3(0.024, 0.032, 0.056);' +
      ' if (vN.y > 0.5) {' +
      '  float r = max(abs(vL.x), abs(vL.y));' +
      '  float ring = step(fract(r * 7.0 + vSeed), 0.07) * step(r, 0.47);' +
      '  float core = step(r, 0.21);' +
      '  vec2 gq = fract(vL * 16.0);' +
      '  float grid = max(step(0.88, gq.x), step(0.88, gq.y));' +
      '  float act = step(0.955, hash(floor(vL * 16.0) + vSeed)) * core;' +
      '  col += ICE * (ring * 0.85 + core * 0.1 + grid * core * 0.3);' +
      '  col += AMBER * act * 1.2;' +
      ' } else {' +
      '  float u = abs(vN.x) > 0.5 ? vW.z : vW.x;' +
      '  float y = vW.y;' +
      '  float pins = step(y, 1.5) * step(fract(u * 1.4), 0.55);' +
      '  col += vec3(0.5, 0.58, 0.68) * pins * 0.34;' +
      '  float row = floor(y * 0.45); float hb = hash(vec2(row, vSeed));' +
      '  float band = step(0.7, hb) * step(0.84, fract(y * 0.45)) * step(0.3, fract(u * 0.3 + hb * 5.0)) * step(1.5, y);' +
      '  col += mix(ICE, AMBER, step(0.93, hb)) * band * 0.95;' +
      ' }' +
      ' float fr = pow(1.0 - abs(dot(vN, V)), 3.0);' +
      ' col += vec3(0.16, 0.38, 0.6) * fr * 0.3;' +
      ' col += AMBER * pulse(vW) * 0.7;' +
      ' col = mix(col, FOG, clamp(fogF(vW), 0.0, 1.0)); gl_FragColor = vec4(col, 1.0); }'
  });
  const N = small ? 620 : 1500;
  const geo = new THREE.BoxGeometry(1, 1, 1); geo.translate(0, 0.5, 0);
  const chips = new THREE.InstancedMesh(geo, chipMat, N);
  const dummy = new THREE.Object3D();
  for (let i = 0; i < N; i++) {
    const sd = rnd() < 0.5 ? -1 : 1;
    const x = sd * (15 + rnd() * 135), z = 70 - rnd() * 760;
    const w = 5 + rnd() * 12, d = 5 + rnd() * 12;
    const tower = rnd() < 0.22;
    const h = tower ? 10 + Math.pow(rnd(), 2) * 55 * (1 - Math.min(Math.abs(x), 140) / 230) : 1.6 + rnd() * 4.5;
    dummy.position.set(x, 0, z); dummy.scale.set(w, Math.max(h, 1.6), d); dummy.updateMatrix();
    chips.setMatrixAt(i, dummy.matrix);
  }
  chips.frustumCulled = false; scene.add(chips);

  // --- terreno a reticolo
  const ground = new THREE.Mesh(new THREE.PlaneGeometry(700, 900), new THREE.ShaderMaterial({
    uniforms: U,
    vertexShader: 'varying vec3 vW; void main(){ vec4 wp = modelMatrix * vec4(position, 1.0); vW = wp.xyz; gl_Position = projectionMatrix * viewMatrix * wp; }',
    fragmentShader: common + 'varying vec3 vW;' +
      'void main(){ vec2 p = vW.xz / 2.5; vec2 gr = abs(fract(p - 0.5) - 0.5) / fwidth(p);' +
      ' float line = 1.0 - min(min(gr.x, gr.y), 1.0);' +
      ' vec2 p2 = vW.xz / 20.0; vec2 g2 = abs(fract(p2 - 0.5) - 0.5) / fwidth(p2); float big = 1.0 - min(min(g2.x, g2.y), 1.0);' +
      ' vec3 col = vec3(0.022, 0.03, 0.052) + ICE * (line * 0.05 + big * 0.2);' +
      ' col += AMBER * pulse(vW) * (0.35 + big);' +
      ' col = mix(col, FOG, clamp(fogF(vW), 0.0, 1.0)); gl_FragColor = vec4(col, 1.0); }'
  }));
  ground.rotation.x = -Math.PI / 2; ground.position.set(0, 0, -330); scene.add(ground);

  // --- piste e collegamenti neurali (impulsi che viaggiano lungo aD)
  const LP = [], LD = [], LS = [], LK = [], NP = [], NS = [], NK = [], NZ = [];
  function addSeg(ax, ay, az, bx, by, bz, d0, s, k) {
    LP.push(ax, ay, az, bx, by, bz);
    LD.push(d0, d0 + Math.sqrt((bx - ax) ** 2 + (by - ay) ** 2 + (bz - az) ** 2));
    LS.push(s, s); LK.push(k, k);
  }
  function bus(pts, lanes, spacing, kindBias) {
    const n = pts.length, off = [];
    for (let i = 0; i < n; i++) {
      const a = pts[Math.max(i - 1, 0)], b = pts[i], c = pts[Math.min(i + 1, n - 1)];
      const d0 = [b[0] - a[0], b[1] - a[1]], d1 = [c[0] - b[0], c[1] - b[1]];
      const l0 = Math.hypot(d0[0], d0[1]) || 1, l1 = Math.hypot(d1[0], d1[1]) || 1;
      let n0 = [-d0[1] / l0, d0[0] / l0], n1 = [-d1[1] / l1, d1[0] / l1];
      if (i === 0) n0 = n1; if (i === n - 1) n1 = n0;
      const dp = n0[0] * n1[0] + n0[1] * n1[1];
      off.push([(n0[0] + n1[0]) / (1 + dp), (n0[1] + n1[1]) / (1 + dp)]);
    }
    for (let L = 0; L < lanes; L++) {
      const o = (L - (lanes - 1) / 2) * spacing, s = rnd(), k = rnd() < kindBias ? 1 : 0;
      let dist = rnd() * 40;
      for (let j = 0; j < n - 1; j++) {
        const ax = pts[j][0] + off[j][0] * o, az = pts[j][1] + off[j][1] * o;
        const bx = pts[j + 1][0] + off[j + 1][0] * o, bz = pts[j + 1][1] + off[j + 1][1] * o;
        addSeg(ax, 0.06, az, bx, 0.06, bz, dist, s, k);
        dist += Math.hypot(bx - ax, bz - az);
      }
    }
    for (let q = 1; q < n; q++) { NP.push(pts[q][0], 0.3, pts[q][1]); NS.push(rnd()); NK.push(rnd() < 0.3 ? 1 : 0); NZ.push(2.2); }
  }
  bus([[-3, 90], [-3, -110], [3, -135], [3, -310], [-4, -340], [-4, -640]], 14, 0.8, 0.12);
  const DIRS = [[1, 0], [0.7071, 0.7071], [0, 1], [-0.7071, 0.7071], [-1, 0], [-0.7071, -0.7071], [0, -1], [0.7071, -0.7071]];
  const B = small ? 60 : 150;
  for (let b = 0; b < B; b++) {
    let px = (rnd() - 0.5) * 300, pz = 70 - rnd() * 720, di = Math.floor(rnd() * 8);
    const pts = [[px, pz]], steps = 3 + Math.floor(rnd() * 5);
    for (let st = 0; st < steps; st++) {
      const len = 10 + rnd() * 36, dv = DIRS[di];
      px += dv[0] * len; pz += dv[1] * len; pts.push([px, pz]);
      const r = rnd(); di = (di + (r < 0.4 ? 1 : r < 0.8 ? 7 : r < 0.9 ? 2 : 6)) % 8;
    }
    bus(pts, 3 + Math.floor(rnd() * 6), 0.9, 0.2);
  }
  const layers = [], LN = small ? 7 : 9;
  for (let l = 0; l < LN; l++) {
    const z0 = 10 - l * 62, nodes = [];
    for (let rr = 0; rr < 4; rr++) for (let cc = 0; cc < 7; cc++) {
      const nx = (cc - 3) * 11 + (rnd() - 0.5) * 6, ny = 9 + rr * 8 + (rnd() - 0.5) * 5, nz = z0 + (rnd() - 0.5) * 8;
      nodes.push([nx, ny, nz]); NP.push(nx, ny, nz); NS.push(rnd()); NK.push(rnd() < 0.25 ? 1 : 0); NZ.push(7 + rnd() * 5);
    }
    layers.push(nodes);
  }
  for (let l2 = 0; l2 < LN - 1; l2++) {
    layers[l2].forEach((a) => {
      for (let c3 = 0; c3 < 3; c3++) {
        const t = layers[l2 + 1][Math.floor(rnd() * 28)];
        addSeg(a[0], a[1], a[2], t[0], t[1], t[2], 0, rnd(), rnd() < 0.2 ? 1 : 0);
      }
    });
  }
  const lg = new THREE.BufferGeometry();
  lg.setAttribute('position', new THREE.Float32BufferAttribute(LP, 3));
  lg.setAttribute('aD', new THREE.Float32BufferAttribute(LD, 1));
  lg.setAttribute('aSeed', new THREE.Float32BufferAttribute(LS, 1));
  lg.setAttribute('aKind', new THREE.Float32BufferAttribute(LK, 1));
  const lines = new THREE.LineSegments(lg, new THREE.ShaderMaterial({
    uniforms: U, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending,
    vertexShader: 'attribute float aD; attribute float aSeed; attribute float aKind; varying float vD; varying float vS; varying float vK; varying float vF;' +
      'void main(){ vec4 wp = modelMatrix * vec4(position, 1.0); vD = aD; vS = aSeed; vK = aKind;' +
      ' float d = length(cameraPosition - wp.xyz); vF = exp(-pow(d * 0.0046, 2.0)); gl_Position = projectionMatrix * viewMatrix * wp; }',
    fragmentShader: 'uniform float uTime; varying float vD; varying float vS; varying float vK; varying float vF;' +
      'void main(){ float f = fract(vD * 0.03 - uTime * (0.5 + vS * 0.9) + vS * 7.0); float g = exp(-f * 8.0);' +
      ' vec3 c = mix(vec3(0.36, 0.82, 1.0), vec3(1.0, 0.4, 0.1), vK); float a = (0.2 + g * 1.2) * vF; gl_FragColor = vec4(c, a); }'
  }));
  lines.frustumCulled = false; scene.add(lines);

  const pg = new THREE.BufferGeometry();
  pg.setAttribute('position', new THREE.Float32BufferAttribute(NP, 3));
  pg.setAttribute('aSeed', new THREE.Float32BufferAttribute(NS, 1));
  pg.setAttribute('aKind', new THREE.Float32BufferAttribute(NK, 1));
  pg.setAttribute('aSize', new THREE.Float32BufferAttribute(NZ, 1));
  const dots = new THREE.Points(pg, new THREE.ShaderMaterial({
    uniforms: U, transparent: true, depthWrite: false, blending: THREE.AdditiveBlending,
    vertexShader: 'attribute float aSeed; attribute float aKind; attribute float aSize; uniform float uTime; varying float vS; varying float vK; varying float vF;' +
      'void main(){ vec4 wp = modelMatrix * vec4(position, 1.0); vec4 mv = viewMatrix * wp; vS = aSeed; vK = aKind;' +
      ' float d = length(cameraPosition - wp.xyz); vF = exp(-pow(d * 0.0046, 2.0));' +
      ' gl_PointSize = clamp(aSize * 130.0 / -mv.z, 2.0, 34.0); gl_Position = projectionMatrix * mv; }',
    fragmentShader: 'uniform float uTime; varying float vS; varying float vK; varying float vF;' +
      'void main(){ float d = length(gl_PointCoord - 0.5); float core = smoothstep(0.5, 0.0, d);' +
      ' float blink = 0.5 + 0.5 * sin(uTime * (1.2 + vS * 2.4) + vS * 40.0);' +
      ' vec3 c = mix(vec3(0.5, 0.86, 1.0), vec3(1.0, 0.45, 0.14), vK);' +
      ' gl_FragColor = vec4(c, (pow(core, 2.2) * (0.45 + 0.9 * blink)) * vF); }'
  }));
  dots.frustumCulled = false; scene.add(dots);

  // --- post-processing
  const composer = new EffectComposer(renderer);
  composer.addPass(new RenderPass(scene, camera));
  const bloom = new UnrealBloomPass(new THREE.Vector2(256, 256), small ? 0.55 : 0.8, 0.7, 0.18);
  composer.addPass(bloom);
  const finish = new ShaderPass({
    uniforms: { tDiffuse: { value: null }, uTime: uTime, uAspect: { value: 1 } },
    vertexShader: 'varying vec2 vUv; void main(){ vUv = uv; gl_Position = projectionMatrix * modelViewMatrix * vec4(position, 1.0); }',
    fragmentShader:
      'uniform sampler2D tDiffuse; uniform float uTime; varying vec2 vUv;' +
      'float h(vec2 p){ return fract(sin(dot(p, vec2(12.9898, 78.233))) * 43758.5453); }' +
      'void main(){' +
      ' vec2 c = vUv - 0.5; float r2 = dot(c, c);' +
      ' vec2 off = c * r2 * 0.012;' +
      ' vec3 col = vec3(texture2D(tDiffuse, vUv + off).r, texture2D(tDiffuse, vUv).g, texture2D(tDiffuse, vUv - off).b);' +
      ' col *= 1.0 - smoothstep(0.18, 0.62, r2) * 0.55;' +
      ' col += (h(vUv * 900.0 + fract(uTime) * 61.0) - 0.5) * 0.035;' +
      ' gl_FragColor = vec4(col, 1.0); }'
  });
  composer.addPass(finish);

  let prog = 0, progT = 0, mx = 0, my = 0, tx = 0, ty = 0, intro = reduce ? 1 : 0;
  function measure() {
    const max = Math.max(1, document.documentElement.scrollHeight - innerHeight);
    progT = Math.min(1, Math.max(0, scrollY / max));
  }
  function resize() {
    const w = innerWidth, h = innerHeight;
    renderer.setSize(w, h, false);
    composer.setPixelRatio(pr); composer.setSize(w, h);
    camera.aspect = w / h; camera.fov = w < h ? 74 : 62; camera.updateProjectionMatrix();
    measure();
  }
  addEventListener('resize', resize);
  addEventListener('scroll', measure, { passive: true });
  addEventListener('pointermove', (e) => { tx = e.clientX / innerWidth - 0.5; ty = e.clientY / innerHeight - 0.5; }, { passive: true });
  resize();

  const t0 = performance.now();
  let running = true;
  document.addEventListener('visibilitychange', () => { running = !document.hidden; if (running) requestAnimationFrame(frame); });
  function frame(now) {
    if (!running) return;
    const t = (now - t0) / 1000;
    prog += (progT - prog) * (reduce ? 1 : 0.06);
    mx += (tx - mx) * 0.05; my += (ty - my) * 0.05;
    intro = Math.min(1, intro + 0.006);
    const e = 1 - Math.pow(1 - intro, 3);
    uTime.value = reduce ? 1.2 : t;
    // all'apertura la camera scende dall'alto e avanza fino alla strada
    const z = 40 - prog * 560 + (1 - e) * 70;
    uCamZ.value = z; uCamX.value = mx * 4;
    camera.position.set(mx * 5 + (reduce ? 0 : Math.sin(t * 0.25) * 1.2), 6 + prog * 9 - my * 2 + (1 - e) * 26, z);
    camera.lookAt(mx * 9, 9 + prog * 6 - my * 3 - (1 - e) * 7, z - 46);
    composer.render();
    opts.onProgress && opts.onProgress(prog);
    requestAnimationFrame(frame);
  }
  requestAnimationFrame(frame);
  return { renderer };
}
