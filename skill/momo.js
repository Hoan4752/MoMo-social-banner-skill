/* MoMo QR-frame clipper — cắt góc ảnh/visual đúng chuẩn khung QR (cắt 3 góc, giữ góc dưới phải).
   Dùng: <div class="qr-frame" data-tl="31,95" data-tr="94,25" data-bl="368,100" data-r="6"> ...ảnh/scene... </div>
   - tl = [rộng, cao] notch góc trên-trái · tr = [rộng, cao] bậc góc trên-phải · bl = [rộng, cao] notch góc dưới-trái (vùng đặt logo)
   - r  = bo góc mọi đỉnh (px). Mọi thứ bên trong wrapper (ảnh generate, scene code) đều bị cắt theo khung.
   - Logo/lockup KHÔNG đặt trong wrapper: đặt ở layer riêng, nằm trong vùng notch `bl`, trên nền poster. */
(function () {
  function roundedPath(pts, r) {
    const n = pts.length; let d = '';
    for (let i = 0; i < n; i++) {
      const p0 = pts[(i - 1 + n) % n], p1 = pts[i], p2 = pts[(i + 1) % n];
      const v1 = [p0[0] - p1[0], p0[1] - p1[1]], v2 = [p2[0] - p1[0], p2[1] - p1[1]];
      const l1 = Math.hypot(...v1), l2 = Math.hypot(...v2), rr = Math.min(r, l1 / 2, l2 / 2);
      const a = [p1[0] + v1[0] / l1 * rr, p1[1] + v1[1] / l1 * rr], b = [p1[0] + v2[0] / l2 * rr, p1[1] + v2[1] / l2 * rr];
      d += (i ? ' L' : 'M') + a[0] + ' ' + a[1] + ' Q' + p1[0] + ' ' + p1[1] + ' ' + b[0] + ' ' + b[1];
    }
    return d + ' Z';
  }
  function num(s) { return (s || '0,0').split(',').map(Number); }
  function apply(el) {
    const W = el.offsetWidth, H = el.offsetHeight;
    const [tlw, tlh] = num(el.dataset.tl), [trw, trh] = num(el.dataset.tr), [blw, blh] = num(el.dataset.bl), r = +(el.dataset.r || 6);
    const pts = [[tlw, 0], [W - trw, 0], [W - trw, trh], [W, trh], [W, H], [blw, H], [blw, H - blh], [0, H - blh], [0, tlh], [tlw, tlh]]
      .filter((p, i, a) => i === 0 || p[0] !== a[i - 1][0] || p[1] !== a[i - 1][1]);
    el.style.clipPath = "path('" + roundedPath(pts, r) + "')";
  }
  /* Dải bảo an (security strip) neo theo khung — KHÔNG đặt toạ độ tay:
     <img class="sec-strip" data-anchor="top|step|mid|bottom" src="../../assets/patterns/security_strips/security_strip_01.png">
     - Rộng = --strip-w (mặc định 45px ≈ 5% canvas 900), cao theo tỉ lệ gốc (~1:4), không kéo méo.
     - Mép phải dải = mép phải khung.
     - top    : đỉnh dải cách mép trên canvas = lề trái của khung (cùng lề poster)
     - step   : đỉnh dải = đáy bậc góc trên-phải (data-tr) của khung
     - mid    : dải nằm giữa chiều cao khung (dùng cho layout L3 khung cao gần full canvas)
     - bottom : đáy dải = đáy khung */
  function placeStrips(frame) {
    const poster = frame.offsetParent || frame.parentElement;
    const [, trh] = num(frame.dataset.tr);
    const fx = frame.offsetLeft, fy = frame.offsetTop, fw = frame.offsetWidth, fh = frame.offsetHeight;
    poster.querySelectorAll('.sec-strip').forEach(img => {
      const go = () => {
        const w = parseFloat(getComputedStyle(img).getPropertyValue('--strip-w')) || 45;
        const h = w * img.naturalHeight / img.naturalWidth;
        const top = { top: fx, step: fy + trh, mid: fy + (fh - h) / 2, bottom: fy + fh - h }[img.dataset.anchor || 'top'];
        Object.assign(img.style, { position: 'absolute', width: w + 'px', height: h + 'px', left: (fx + fw - w) + 'px', top: top + 'px' });
      };
      img.complete && img.naturalWidth ? go() : img.addEventListener('load', go, { once: true });
    });
  }
  /* Chế độ xuất ảnh: mở file với #render → poster dính góc trên-trái, không lề, không nền xám
     (dùng cho Chrome headless CLI: skill/build.py) */
  if (location.hash === '#render') {
    const st = document.createElement('style');
    st.textContent = 'html,body{margin:0!important;padding:0!important;background:none!important;display:block!important;height:auto!important;overflow:hidden!important}';
    document.head.appendChild(st);
  }
  window.momoQrFrame = () => document.querySelectorAll('.qr-frame').forEach(f => { apply(f); placeStrips(f); });
  if (document.readyState !== 'loading') window.momoQrFrame(); else document.addEventListener('DOMContentLoaded', window.momoQrFrame);
})();

/* QA tự động — chạy sau khi font tải xong, ghi kết quả vào <body data-qa="[...]"> để build.py đọc (chrome --dump-dom).
   Kiểm: chữ đè dải bảo an / đè khung visual, quá 1 cụm nhấn, logo tràn khỏi notch. */
(function () {
  function qa() {
    const P = document.getElementById('poster'); if (!P) return;
    const pr = P.getBoundingClientRect(), out = [];
    const rel = el => { const r = el.getBoundingClientRect(); return { l: r.left - pr.left, t: r.top - pr.top, r: r.right - pr.left, b: r.bottom - pr.top, w: r.width }; };
    const strips = [...P.querySelectorAll('.sec-strip')].map(rel);
    const stripL = strips.length ? Math.min(...strips.map(s => s.l)) : 818;
    const frame = P.querySelector('.qr-frame'), f = frame && rel(frame);
    const L = P.dataset.layout || '';
    P.querySelectorAll('.headline .ln, .sub, .cta').forEach(el => {
      const range = document.createRange(); range.selectNodeContents(el);
      const rr = range.getBoundingClientRect(), right = rr.right - pr.left, bottom = rr.bottom - pr.top;
      const txt = el.textContent.trim().slice(0, 30);
      if (right > stripL - 8) out.push(`Chữ đè dải bảo an: "${txt}" (x=${Math.round(right)} > ${Math.round(stripL - 8)})`);
      if (f && L !== 'L3' && bottom > f.t - 8) out.push(`Chữ đè khung visual: "${txt}"`);
      if (L === 'L3' && bottom > 790) out.push(`Chữ xuống quá thấp, sát footnote/logo: "${txt}"`);
    });
    const hl = P.querySelectorAll('.headline .hl-box, .headline .hl-sign').length;
    if (hl > 1) out.push(`Headline có ${hl} cụm nhấn (luật: tối đa 1)`);
    const lk = P.querySelector('.lockup, .logo-cutout');
    if (lk && frame) {
      const bl = (frame.dataset.bl || '0,0').split(',').map(Number), imgs = [...lk.querySelectorAll('img')].map(rel);
      const right = imgs.length ? Math.max(...imgs.map(i => i.r)) : 0;
      if (right - f.l > bl[0] - 12) out.push(`Logo sát/tràn mép notch dưới-trái (cần ≥ 12px khoảng thở)`);
    }
    P.querySelectorAll('img').forEach(i => { if (i.complete && !i.naturalWidth) out.push('Ảnh không tải được: ' + i.getAttribute('src')); });
    document.body.dataset.qa = JSON.stringify(out);
  }
  const run = () => (document.fonts ? document.fonts.ready : Promise.resolve()).then(() => setTimeout(qa, 300));
  if (document.readyState === 'complete') run(); else window.addEventListener('load', run);
})();
