"""img.py — mọi việc xử lý hình cho banner MoMo, 1 file, nhiều lệnh con.

  python3 skill/img.py prompt   projects/<task> [--only B]        # viết prompt tạo hình từ spec (đúng tỉ lệ khung, phong cách, ảnh mẫu)
  python3 skill/img.py removebg in.png out.png [--bg "#FFFFFF"] [--tol 18] [--trim]
  python3 skill/img.py brandify in.png out.png --style S1|S2|S3 [--tone pink-blue|pink-green|blue|mint|yellow-red|peach-blue]
  python3 skill/img.py check    a.png [b.png …] --style S1|S2|S3 [--threshold 65]
  python3 skill/img.py tint     assets/patterns/money-elements_patterns_4.png "#HEX" out.png [--strength 1] [--crop 14]
  python3 skill/img.py strips   assets/patterns/security-03_2-png.webp assets/patterns/security_strips/

Chi tiết quy trình: skill/3-image.md. Cần: Pillow, numpy (pip install pillow numpy).
"""
import argparse, glob, json, os, sys
from collections import deque
import numpy as np
from PIL import Image, ImageFilter

SKILL = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SKILL)
PACKS = {'S1': 'S1_crayon_halftone', 'S2': 'S2_3d_glossy', 'S3': 'S3_photo'}
PALETTE = {
    'momo_pink': '#A50064', 'pink_p1': '#F95396', 'pink_0': '#FF9DBE', 'pink_m1': '#FEC8DC', 'pink_m2': '#FFEFF4',
    'blue_ink': '#1F4FA8', 'blue': '#3E7BD6', 'blue_l': '#9CC3EC', 'blue_xl': '#DCEBFA',
    'mint_d': '#1E8C7A', 'mint': '#93D6C2', 'mint_l': '#DDF4EC', 'yellow': '#F2C230', 'yellow_l': '#FFE9A6',
    'orange': '#FF6340', 'red': '#E5242B', 'ink': '#1A1A2E', 'white': '#FFFFFF', 'paper': '#F7F3F5', 'skin': '#F6D2C0', 'skin_d': '#D9A48C',
}
TONES = {  # gradient map: tối → giữa → sáng (đo từ ref)
    'pink-blue': ['#1F3F8F', '#E9649C', '#FFEFF4'], 'pink-green': ['#1E6E5E', '#EE7FA6', '#FFEFF4'],
    'blue': ['#1F4FA8', '#7FAEE6', '#EEF6FD'], 'mint': ['#16705F', '#7FCFB8', '#EAF9F3'],
    'yellow-red': ['#B81D22', '#F2C230', '#FFF7DA'], 'peach-blue': ['#1F4FA8', '#F59A7A', '#FFEFE6'],
}
# ảnh mẫu nên đính kèm theo phong cách + tone (references/style_packs/)
REFS = {
    ('S1', 'pink-blue'): ['R14', 'R20', 'R21', 'R02'], ('S1', 'pink-green'): ['R18', 'R14', 'R20'],
    ('S1', 'blue'): ['R07', 'R12', 'R01'], ('S1', 'mint'): ['R09', 'R12', 'R14'],
    ('S1', 'yellow-red'): ['R06', 'R19', 'R14'], ('S1', 'peach-blue'): ['R02', 'R07', 'R14'],
    ('S2', None): ['R16', 'R13', 'R23'], ('S3', None): ['R17', 'R24', 'R11'],
}
DNA = {
    'S1': ('Keep EXACTLY the drawing style, line color, halftone shading, engraving lines and palette of the reference illustrations. '
           'Even medium ink outlines in {ink} (never black); flat pastel fills ({fills}); shadows ONLY as halftone dots and parallel hatching; '
           'background with fine wavy parallel engraving lines like a banknote; maximum 3 hues; young Vietnamese people, realistic proportions, casual clothes, cheerful.'),
    'S2': ('Same style as the reference images: rounded clay-like glossy 3D, soft studio light from top-left, very soft contact shadow, smooth gradients, fine grain; '
           'colors MoMo pink #F95396 #FEC8DC #FFEFF4, coin yellow #F2C230.'),
    'S3': 'Natural warm daylight photo, gentle background blur that keeps the context, Vietnamese people in everyday clothes with pink/blue accents, medium shot.',
}
FORBID = {
    'S1': 'FORBIDDEN: 3D, render, clay, glossy, gradients, glow, soft drop shadows, black outlines, anime/chibi, neon, more than 3 hues, plain white background',
    'S2': 'FORBIDDEN: metallic chrome, neon, cyberpunk, tiny clutter, dark background, harsh shadow',
    'S3': 'FORBIDDEN: glossy stock look, harsh studio light, HDR, dark cinematic grading',
}
TONE_FILLS = {'pink-blue': 'MoMo pink #F95396 / #FEC8DC / #FFEFF4 with navy #1F3F8F accents', 'pink-green': 'MoMo pink #F95396 / #FEC8DC with green #1E6E5E accents',
              'blue': 'monochrome blue #7FAEE6 / #DCEBFA / #EEF6FD with one small pink #F95396 accent', 'mint': 'mint #7FCFB8 / #EAF9F3 with one pink #F95396 accent',
              'yellow-red': 'yellow #F2C230 / #FFF7DA with red #B81D22 accents', 'peach-blue': 'peach #F59A7A / #FFEFE6 with blue #1F4FA8 accents'}


def hex2rgb(h): return [int(h[i:i + 2], 16) for i in (1, 3, 5)]


# ------------------------------------------------------------------ prompt
def cmd_prompt(a):
    sys.path.insert(0, SKILL); from build import geometry, aspect
    task_dir = os.path.abspath(a.task if os.path.isdir(a.task) else os.path.dirname(a.task))
    sp = os.path.join(task_dir, 'spec.json'); spec = json.load(open(sp, encoding='utf-8'))
    for key, var in spec['variants'].items():
        if a.only and key not in a.only.split(','): continue
        v = {**spec.get('defaults', {}), **var}; im = v.get('image')
        if not im: continue
        st, tone, kind = im.get('style', 'S1'), im.get('tone', 'pink-blue'), im.get('kind', 'scene')
        if kind == 'spot':
            ratio, comp = '1:1', 'Isolated on a solid pure white background, full figure, centered, generous margin.'
        else:
            part = os.path.join(task_dir, v['partner']) if v.get('partner') else None
            g = geometry(v, aspect(part) if part else 1.2); r = g['fw'] / g['fh']
            ratio = min(['16:9', '3:2', '4:3', '1:1', '2:1', '5:4'], key=lambda x: abs(eval(x.replace(':', '/')) - r))
            comp = ('Clean rectangle. Main subjects center-right; top-left and bottom-left corners calm and empty '
                    '(they will be cropped by the layout frame; the bottom-left holds the logo).')
        ink = TONES.get(tone, TONES['pink-blue'])[0]
        dna = DNA[st].format(ink=ink, fills=TONE_FILLS.get(tone, ''))
        text = (f"{dna}\nCreate a NEW {'spot illustration' if kind == 'spot' else 'illustration'}, aspect ratio {ratio}: {im['scene']}.\n{comp}\n"
                f"{FORBID[st]}, any text/letters/numbers/logos/QR, frames, borders, pink 'mo mo' strips, the MoMo mascot.")
        refs = REFS.get((st, tone if st == 'S1' else None), REFS[(st, None)] if st != 'S1' else REFS[('S1', 'pink-blue')])
        im['ratio'] = ratio; im['prompt'] = text
        im['attach'] = [f'references/style_packs/{PACKS[st]}/{r}.png' for r in refs]
        im.setdefault('save_as', v.get('visual') or (v.get('spot') or {}).get('file') or f'visual-{key}.png')
        spec['variants'][key]['image'] = im
        print(f'===== {key} · {st} · {tone} · {ratio} → lưu thành {task_dir}/{im["save_as"]}\nĐính kèm: {", ".join(im["attach"])}\n{text}\n')
    json.dump(spec, open(sp, 'w', encoding='utf-8'), ensure_ascii=False, indent=2)
    print('Đã ghi prompt vào spec.json → variants.<X>.image.prompt')


# ------------------------------------------------------------------ removebg
def cmd_removebg(a):
    im = Image.open(a.src).convert('RGBA'); px = np.array(im).astype(int); H, W = px.shape[:2]
    bg = np.array(hex2rgb(a.bg)); near = np.abs(px[:, :, :3] - bg).max(axis=2) <= a.tol
    mask = np.zeros((H, W), bool); q = deque()
    for x in range(W):
        for y in (0, H - 1):
            if near[y, x] and not mask[y, x]: mask[y, x] = True; q.append((y, x))
    for y in range(H):
        for x in (0, W - 1):
            if near[y, x] and not mask[y, x]: mask[y, x] = True; q.append((y, x))
    while q:
        y, x = q.popleft()
        for dy, dx in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            ny, nx = y + dy, x + dx
            if 0 <= ny < H and 0 <= nx < W and near[ny, nx] and not mask[ny, nx]: mask[ny, nx] = True; q.append((ny, nx))
    alpha = Image.fromarray(np.where(mask, 0, 255).astype('uint8')).filter(ImageFilter.GaussianBlur(1.2))
    im.putalpha(Image.fromarray(np.minimum(np.array(alpha), px[:, :, 3]).astype('uint8')))
    if a.trim and im.getbbox(): im = im.crop(im.getbbox())
    im.save(a.out); print(a.out, im.size, f'xoá {mask.mean():.0%} nền')


# ------------------------------------------------------------------ brandify
def _nudge(rgb, s):
    P = np.array([hex2rgb(h) for h in PALETTE.values()], float); flat = rgb.reshape(-1, 3); out = np.empty_like(flat)
    w = np.array([0.30, 0.59, 0.11]) * 3
    for i in range(0, len(flat), 200000):
        c = flat[i:i + 200000]; d = (((c[:, None, :] - P[None]) ** 2) * w).sum(-1)
        out[i:i + 200000] = c * (1 - s) + P[d.argmin(1)] * s
    return out.reshape(rgb.shape)


def _gradmap(rgb, tone, s):
    st = np.array([hex2rgb(h) for h in TONES[tone]], float)
    t = np.clip(((rgb @ np.array([0.299, 0.587, 0.114])) / 255 - 0.08) / 0.86, 0, 1)[..., None]
    lo = st[0] + (st[1] - st[0]) * np.clip(t * 2, 0, 1); hi = st[1] + (st[2] - st[1]) * np.clip(t * 2 - 1, 0, 1)
    return rgb * (1 - s) + np.where(t < 0.5, lo, hi) * s


def _halftone(rgb, amt, cell=6):
    h, w = rgb.shape[:2]; lum = (rgb @ np.array([0.299, 0.587, 0.114])) / 255
    yy, xx = np.mgrid[0:h, 0:w]; u = ((xx + yy) % cell) - cell / 2; v = ((xx - yy) % cell) - cell / 2
    dist = np.sqrt(u ** 2 + v ** 2) / (cell / 2); dark = np.clip((0.62 - lum) / 0.62, 0, 1)
    k = ((dist < dark * 1.1) * dark * amt)[..., None]; ink = np.array(hex2rgb(PALETTE['ink']), float)
    return rgb * (1 - k) + (rgb * ink / 255) * k


def _engrave(rgb, amt):
    src = os.path.join(ROOT, 'assets', 'patterns', 'money-elements_patterns_17_1.png')
    if not os.path.exists(src): return rgb
    pat = Image.open(src).convert('RGBA'); pat = pat.crop((14, 14, pat.width - 14, pat.height - 14))
    h, w = rgb.shape[:2]; sc = w * 1.3 / pat.width; pat = pat.resize((int(pat.width * sc), int(pat.height * sc)))
    tile = Image.new('L', (w, h), 0)
    for y in range(0, h, pat.height): tile.paste(pat.getchannel('A'), (w - pat.width, y))
    k = (np.array(tile, float) / 255 * amt)[..., None]; tint = np.array(hex2rgb(PALETTE['pink_0']), float)
    return rgb * (1 - k) + (rgb * tint / 255) * k


def cmd_brandify(a):
    im = Image.open(a.src).convert('RGBA'); arr = np.array(im); rgb = arr[:, :, :3].astype(float)
    if a.tone: rgb = _gradmap(rgb, a.tone, a.tone_strength)
    rgb = _nudge(rgb, a.strength if a.strength is not None else {'S1': .55, 'S2': .30, 'S3': .15}[a.style])
    if a.style == 'S1': rgb = _engrave(_halftone(rgb, a.dots), a.lines)
    elif a.style == 'S2': rgb = rgb + np.random.default_rng(7).normal(0, 6, rgb.shape[:2])[..., None]
    Image.fromarray(np.dstack([np.clip(rgb, 0, 255).astype('uint8'), arr[:, :, 3]]), 'RGBA').save(a.out)
    print(a.out, '· brandify', a.style, a.tone or '')


# ------------------------------------------------------------------ check
def _load(p, size=320):
    im = Image.open(p).convert('RGBA'); im.thumbnail((size, size)); x = np.array(im)
    return x[:, :, :3].astype(float), x[:, :, 3] > 128


def _hist(rgb, m):
    hsv = np.array(Image.fromarray(rgb.astype('uint8')).convert('HSV'))[m]
    h, _, _ = np.histogram2d(hsv[:, 0], hsv[:, 1], bins=[18, 6], range=[[0, 256], [0, 256]]); return h / max(h.sum(), 1)


def _grad(rgb, m):
    g = rgb.mean(-1); mag = np.abs(np.diff(g, axis=1))[:-1, :] + np.abs(np.diff(g, axis=0))[:, :-1]
    return float((mag[m[:-1, :-1]] > 40).mean())


def cmd_check(a):
    pack = sorted(glob.glob(os.path.join(ROOT, 'references', 'style_packs', PACKS[a.style], '*.png')))
    if not pack: sys.exit('Không thấy bộ ảnh mẫu ' + PACKS[a.style])
    refs = [_load(p) for p in pack]; rh = np.mean([_hist(*r) for r in refs], 0); rg = np.mean([_grad(*r) for r in refs])
    P = np.array([hex2rgb(h) for h in PALETTE.values()], float)
    for f in a.files:
        rgb, m = _load(f); px = rgb[m]
        pal = float((np.sqrt(((px[:, None] - P[None]) ** 2).sum(-1)).min(1) < 48).mean() * 100)
        col = float(np.sqrt(_hist(rgb, m) * rh).sum() * 100); gd = _grad(rgb, m)
        tex = float(max(0, 100 - abs(gd - rg) / max(rg, 1e-3) * 100)); tot = .35 * pal + .40 * col + .25 * tex
        tips = [t for c, t in [(pal < 55, 'màu lệch bảng MoMo → brandify'), (col < 60, 'phân bố màu khác ref → đính kèm thêm ảnh mẫu'),
                               (tex < 50, 'chất nét khác ref (' + ('quá mượt' if gd < rg else 'quá rối') + ')')] if c]
        print(f'{"PASS" if tot >= a.threshold else "RETRY":5} {tot:5.1f} | palette {pal:5.1f} · color {col:5.1f} · texture {tex:5.1f} | {os.path.basename(f)}' + (' → ' + '; '.join(tips) if tips else ''))


# ------------------------------------------------------------------ tint / strips
def cmd_tint(a):
    im = Image.open(a.src).convert('RGBA'); w, h = im.size; im = im.crop((a.crop, a.crop, w - a.crop, h - a.crop))
    A = np.array(im)[:, :, 3].astype(float); x = int(A.mean(axis=0).argmax())
    col = A[:, max(0, x - 3):x + 3].mean(axis=1); c = col - col.mean()
    period = 8 + int(np.argmax([np.dot(c[:-l], c[l:]) / len(c[l:]) for l in range(8, len(c) // 2)]))
    im = im.crop((0, 0, im.width, (A.shape[0] // period) * period))
    out = Image.new('RGBA', im.size, tuple(hex2rgb(a.color)) + (0,))
    out.putalpha(im.getchannel('A').point(lambda v: min(255, int(v * a.strength)))); out.save(a.out)
    print(a.out, im.size, 'chu kỳ', period)


def cmd_strips(a):
    os.makedirs(a.outdir, exist_ok=True); im = Image.open(a.src).convert('RGB'); x = np.array(im).astype(int)
    pink = (x[:, :, 0] > 200) & (x[:, :, 1] < 190); cols = np.where(pink.sum(axis=0) > 3)[0]
    runs, s, p = [], cols[0], cols[0]
    for c in cols[1:]:
        if c != p + 1: runs.append((s, p)); s = c
        p = c
    runs.append((s, p))
    for i, (x0, x1) in enumerate(runs, 1):
        rows = np.where(pink[:, x0:x1 + 1].sum(axis=1) > 2)[0]
        im.crop((x0, rows.min(), x1 + 1, rows.max() + 1)).save(os.path.join(a.outdir, f'security_strip_{i:02d}.png'))
    print(len(runs), 'dải →', a.outdir)


def main():
    ap = argparse.ArgumentParser(); sub = ap.add_subparsers(dest='cmd', required=True)
    p = sub.add_parser('prompt'); p.add_argument('task'); p.add_argument('--only'); p.set_defaults(f=cmd_prompt)
    p = sub.add_parser('removebg'); p.add_argument('src'); p.add_argument('out'); p.add_argument('--bg', default='#FFFFFF')
    p.add_argument('--tol', type=int, default=18); p.add_argument('--trim', action='store_true'); p.set_defaults(f=cmd_removebg)
    p = sub.add_parser('brandify'); p.add_argument('src'); p.add_argument('out'); p.add_argument('--style', choices=PACKS, required=True)
    p.add_argument('--tone', choices=list(TONES)); p.add_argument('--tone-strength', type=float, default=.85)
    p.add_argument('--strength', type=float); p.add_argument('--lines', type=float, default=.18); p.add_argument('--dots', type=float, default=.35)
    p.set_defaults(f=cmd_brandify)
    p = sub.add_parser('check'); p.add_argument('files', nargs='+'); p.add_argument('--style', choices=PACKS, required=True)
    p.add_argument('--threshold', type=float, default=65); p.set_defaults(f=cmd_check)
    p = sub.add_parser('tint'); p.add_argument('src'); p.add_argument('color'); p.add_argument('out')
    p.add_argument('--strength', type=float, default=1.0); p.add_argument('--crop', type=int, default=14); p.set_defaults(f=cmd_tint)
    p = sub.add_parser('strips'); p.add_argument('src'); p.add_argument('outdir'); p.set_defaults(f=cmd_strips)
    a = ap.parse_args(); a.f(a)


if __name__ == '__main__':
    main()
