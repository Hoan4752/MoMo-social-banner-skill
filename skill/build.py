"""build.py — dựng banner MoMo HOÀN CHỈNH từ 1 file spec.json → PNG 1080×1080 cho từng phương án + ảnh so sánh.

  python3 skill/build.py projects/<task>                 # dựng mọi phương án trong spec.json
  python3 skill/build.py projects/<task> --only A        # chỉ phương án A
  python3 skill/build.py projects/<task> --keep-html     # giữ HTML tạm để kiểm tra lỗi

Đầu ra (cùng folder task, không folder con):
  banner-<task>-A.png · banner-<task>-B.png · … · banner-<task>-compare.png
Mỗi PNG có đủ layer: nền + sóng chìm · khung QR cắt góc · visual/spot/mascot · logo MoMo (± đối tác) · 3 dải bảo an · chữ.
Xuất ảnh: Chrome/Edge/Brave có sẵn trên máy (headless, ~1s) → dự phòng Python Playwright.
Sau khi xuất: tự kiểm tra (chữ đè dải/khung, >1 cụm nhấn, logo sát notch, thiếu ảnh, khung trống) và in lỗi.
Cú pháp spec: skill/2-banner.md §4.
"""
import argparse, glob, html, json, os, re, shutil, subprocess, sys, tempfile

SKILL = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(SKILL)
STRIP_DEFAULT = {'A': [3, 6, 9], 'B': [1, 4, 7], 'C': [2, 5, 8]}


# ---------------------------------------------------------------- geometry
def geometry(v, partner_aspect=1.2):
    """Toạ độ khung + notch theo layout và số dòng chữ (không bao giờ để khung đè chữ)."""
    L = v.get('layout', 'L1')
    head, sub, cta = v.get('headline', []), v.get('sub', []), v.get('cta')
    hs = v.get('h_size', 54 if L == 'L3' else 50)
    copy_top = 330 if L == 'L3' else 46
    top_logo_h = (v.get('partner_top_h', 38) + 14) if v.get('logo_pos') == 'top' else 0
    text_h = copy_top + top_logo_h + len(head) * hs * 1.22 + max(0, len(head) - 1) * 8
    if sub: text_h += 14 + len(sub) * 28 * 1.22
    if cta: text_h += 72
    if L == 'L3':
        bl_l3 = '0,0' if v.get('logo_pos') == 'top' else (f'{int(v.get("partner_h", 62) * partner_aspect + 24)},95' if v.get('no_momo') and v.get('partner') else '103,95')
        return dict(L=L, hs=hs, copy_top=copy_top, fx=37, fy=38, fw=827, fh=826, tl='295,112', tr='0,0', bl=bl_l3)
    fx, fw = (30, 837) if L == 'L1' else (34, 832)
    fy = int(max(318 if L == 'L2' else 357, text_h + 34))
    tl = '103,41' if L == 'L1' else '73,40'
    if v.get('logo_pos') == 'top':
        bl = '0,0'
    elif v.get('no_momo') and v.get('partner'):
        bl = f'{int(v.get("partner_h", 62) * partner_aspect + 24)},95'
    else:
        bl = f'{int(2 + 81 + 30 + v.get("partner_h", 62) * partner_aspect + 20)},95' if L == 'L2' else '103,95'
    return dict(L=L, hs=hs, copy_top=copy_top, fx=fx, fy=fy, fw=fw, fh=865 - fy, tl=tl, tr='0,0', bl=bl)


def aspect(path):
    try:
        from PIL import Image
        with Image.open(path) as im: return im.width / im.height
    except Exception:
        return 1.2


# ---------------------------------------------------------------- html
def fmt(line):
    s = html.escape(line)
    s = re.sub(r'\[(.+?)\]', r'<span class="hl-box">\1</span>', s)
    return re.sub(r'\{(.+?)\}', r'<span class="hl-sign">\1</span>', s)


def asset(p):  # đường dẫn tuyệt đối (HTML tạm nằm ngoài folder task)
    return 'file://' + os.path.abspath(p)


def resolve_asset(task_dir, rel):
    if not rel: return ''
    p = os.path.join(task_dir, rel)
    if os.path.exists(p): return p
    p_logo = os.path.join(ROOT, 'assets', 'logos', rel)
    if os.path.exists(p_logo): return p_logo
    p_asset = os.path.join(ROOT, 'assets', rel)
    if os.path.exists(p_asset): return p_asset
    return p


def to_html(task_dir, key, v):
    L = v.get('layout', 'L1')
    part = resolve_asset(task_dir, v['partner']) if v.get('partner') else None
    g = geometry(v, aspect(part) if part else 1.2)
    A = lambda rel: asset(os.path.join(ROOT, 'assets', rel))
    T = lambda rel: asset(resolve_asset(task_dir, rel))
    mascot = lambda m: f'<img class="mascot" src="{A("illustrations/" + m["file"])}" alt="" style="left:{m.get("left", 500)}px;top:{m.get("top", 40)}px;width:{m.get("width", 260)}px" />'
    parts = ['<div class="bg-wave"></div>']
    inner = ''
    if L != 'L3' and v.get('visual') and os.path.exists(os.path.join(task_dir, v['visual'])): inner += f'<img class="photo" src="{T(v["visual"])}" alt="" />'
    if L != 'L3': inner += '<div class="frame-texture"></div>'
    if L != 'L3' and v.get('mascot'): inner += mascot(v['mascot'])
    if L != 'L3' and v.get('element'):  # element tách nền đặt TRONG khung (bị khung cắt) — toạ độ tính từ góc khung
        e = v['element']; inner += f'<img class="mascot" src="{T(e["file"])}" alt="" style="left:{e.get("left", 140)}px;top:{e.get("top", 0)}px;width:{e.get("width", 560)}px" />'
    parts.append(f'<section class="qr-frame" data-tl="{g["tl"]}" data-tr="{g["tr"]}" data-bl="{g["bl"]}" data-r="14">{inner}</section>')
    if L == 'L3' and v.get('chip'):
        c = v['chip']; ic = f'<img src="{T(c["icon"])}" alt="" />' if c.get('icon') else ''
        parts.append(f'<div class="tag-chip">{ic}<span>{"<br />".join(html.escape(x) for x in c["label"])}</span></div>')
    if L == 'L3' and v.get('mascot'): parts.append(mascot(v['mascot']))
    if v.get('spot'):
        s = v['spot']; parts.append(f'<img class="spot" src="{T(s["file"])}" alt="" style="left:{s.get("left", 560)}px;top:{s.get("top", 150)}px;width:{s.get("width", 240)}px" />')
    logo = A('logos/momo_wordmark.png')
    if v.get('logo_pos') == 'top':
        pass  # Không hiển thị logo ở góc dưới
    elif v.get('no_momo') and v.get('partner'):
        pw = int(v.get("partner_h", 62) * (aspect(part) if part else 1.2))
        parts.append(f'<div class="logo-cutout" style="width:{pw + 20}px"><img src="{T(v["partner"])}" alt="" style="height:{v.get("partner_h", 62)}px;width:auto;margin-bottom:6px" /></div>')
    elif L == 'L2':
        parts.append(f'<div class="lockup"><img class="momo" src="{logo}" alt="MoMo" /><img class="partner" src="{T(v["partner"])}" alt="" /></div>')
    else:
        parts.append(f'<div class="logo-cutout"><img src="{logo}" alt="MoMo" /></div>')
    for an, n in zip(['top', 'mid' if L == 'L3' else 'step', 'bottom'], v.get('strips', STRIP_DEFAULT.get(key, [2, 5, 8]))):
        parts.append(f'<img class="sec-strip" data-anchor="{an}" src="{A(f"patterns/security_strips/security_strip_{int(n):02d}.png")}" alt="" />')
    top_logo = ''
    if v.get('logo_pos') == 'top' and v.get('partner'):
        top_logo = f'<div class="logo-top" style="margin-bottom:14px"><img src="{T(v["partner"])}" alt="" style="height:{v.get("partner_top_h", 38)}px;width:auto;display:block" /></div>'
    copy = top_logo + '<h1 class="headline">' + ''.join(f'<span class="ln">{fmt(x)}</span>' for x in v.get('headline', [])) + '</h1>'
    if v.get('sub'): copy += '<p class="sub">' + '<br />'.join(fmt(x) for x in v['sub']) + '</p>'
    if v.get('cta'): copy += f'<span class="cta">{html.escape(v["cta"])}</span>'
    parts.append(f'<section class="copy">{copy}</section>')
    if L == 'L3' and v.get('footnote'): parts.append(f'<p class="footnote">{html.escape(v["footnote"])}</p>')
    extra = ('.qr-frame{background:linear-gradient(180deg,var(--panel-top) 0%,var(--panel-mid) 45%,var(--panel-bot) 100%)}'
             '.tag-chip{left:38px;top:39px}.copy{left:75px;top:330px}.sub{font-weight:400;color:#1A1A1A}.footnote{left:160px;top:826px}'
             if L == 'L3' else f'.copy{{left:48px;top:{g["copy_top"]}px}}')
    return f'''<!DOCTYPE html><html lang="vi"><head><meta charset="UTF-8" /><title>{key}</title>
<link rel="stylesheet" href="{asset(os.path.join(SKILL, 'momo.css'))}" /><script src="{asset(os.path.join(SKILL, 'momo.js'))}" defer></script>
<style>.poster{{--fx:{g["fx"]}px;--fy:{g["fy"]}px;--fw:{g["fw"]}px;--fh:{g["fh"]}px;--h-size:{g["hs"]}px;--sub-size:{30 if L == "L3" else 28}px;--partner-h:{v.get("partner_h", 62)}px}}{extra}</style>
</head><body><main class="poster" id="poster" data-theme="{v.get("theme", "pink")}" data-layout="{L}">
{chr(10).join(parts)}
</main></body></html>''', g


# ---------------------------------------------------------------- render
def find_chrome():
    if os.environ.get('CHROME_BIN'): return os.environ['CHROME_BIN']
    home = os.path.expanduser('~')
    cands = ['/Applications/Google Chrome.app/Contents/MacOS/Google Chrome', '/Applications/Chromium.app/Contents/MacOS/Chromium',
             '/Applications/Microsoft Edge.app/Contents/MacOS/Microsoft Edge', '/Applications/Brave Browser.app/Contents/MacOS/Brave Browser']
    cands += sorted(glob.glob(home + '/Library/Caches/ms-playwright/chromium*/chrome-mac*/Chromium.app/Contents/MacOS/Chromium'), reverse=True)
    cands += sorted(glob.glob(home + '/Library/Caches/ms-playwright/chromium_headless_shell*/chrome-mac*/headless_shell'), reverse=True)
    cands += [shutil.which(x) for x in ('google-chrome', 'chromium', 'chromium-browser')]
    cands += sorted(glob.glob('/opt/pw-browsers/chromium-*/chrome-linux/chrome'), reverse=True)
    return next((c for c in cands if c and os.path.exists(c)), None)


def render(html_path, png_path, scale=1.2):
    """Trả về list lỗi QA (đọc từ body[data-qa])."""
    url = 'file://' + html_path + '#render'
    chrome = find_chrome()
    if chrome:
        base = [chrome, '--headless=new', '--no-sandbox', '--disable-gpu', '--hide-scrollbars', '--mute-audio',
                f'--force-device-scale-factor={scale}', '--window-size=900,1100', '--virtual-time-budget=4000']
        tmp = png_path + '.tmp.png'
        subprocess.run(base + [f'--screenshot={tmp}', url], capture_output=True, timeout=60)
        if os.path.exists(tmp):
            px = round(900 * scale)
            try:
                from PIL import Image
                Image.open(tmp).convert('RGB').crop((0, 0, px, px)).save(png_path); os.remove(tmp)
            except ImportError:
                subprocess.run(['sips', '--cropToHeightWidth', str(px), str(px), '--cropOffset', '0', '0', tmp, '--out', png_path], capture_output=True)
                os.remove(tmp)
            dom = subprocess.run(base + ['--dump-dom', url], capture_output=True, text=True, timeout=60).stdout
            m = re.search(r'data-qa="([^"]*)"', dom)
            return json.loads(html.unescape(m.group(1))) if m else ['(không đọc được kết quả QA)']
    try:
        from playwright.sync_api import sync_playwright
    except ImportError:
        sys.exit('❌ Không tìm thấy Chrome/Edge/Brave và chưa có Playwright. Cài Google Chrome (khuyên dùng) '
                 'hoặc: pip install playwright && playwright install chromium-headless-shell')
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={'width': 900, 'height': 900}, device_scale_factor=scale)
        pg.goto(url); pg.wait_for_timeout(1200)
        pg.locator('#poster').screenshot(path=png_path)
        qa = pg.evaluate('document.body.dataset.qa || "[]"'); b.close()
        return json.loads(qa)


def compare(pngs, out):
    try:
        from PIL import Image, ImageDraw, ImageFont
    except ImportError:
        print('⚠️  Thiếu Pillow → bỏ qua ảnh compare (pip install pillow)'); return
    ims = [Image.open(p).convert('RGB').resize((540, 540)) for _, p in pngs]
    cols = 3 if len(ims) > 4 else len(ims)
    rows = (len(ims) + cols - 1) // cols
    W = Image.new('RGB', (cols * 560 + 20, rows * 600 + 20), (245, 245, 245)); d = ImageDraw.Draw(W)
    try: font = ImageFont.truetype(os.path.join(ROOT, 'assets', 'fonts', 'momotrustdisplay-webfont-1.ttf'), 26)
    except Exception: font = ImageFont.load_default()
    for i, ((k, _), im) in enumerate(zip(pngs, ims)):
        r, c = divmod(i, cols)
        x = 20 + c * 560
        y = 20 + r * 600
        W.paste(im, (x, y + 40)); d.text((x, y + 8), f'Mẫu {k}', fill=(165, 0, 100), font=font)
    W.save(out)


# ---------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('task'); ap.add_argument('--only'); ap.add_argument('--keep-html', action='store_true')
    a = ap.parse_args()
    task_dir = a.task if os.path.isdir(a.task) else os.path.dirname(a.task)
    task_dir = os.path.abspath(task_dir)
    spec = json.load(open(os.path.join(task_dir, 'spec.json'), encoding='utf-8'))
    name = spec.get('task') or os.path.basename(task_dir)
    defaults = spec.get('defaults', {})
    done, problems = [], 0
    for key, var in spec['variants'].items():
        if a.only and key not in a.only.split(','): continue
        v = {**defaults, **var}
        warn = []
        for f in [v.get('visual'), v.get('partner') if (v.get('layout') == 'L2' or v.get('no_momo')) else None,
                  (v.get('spot') or {}).get('file'), (v.get('element') or {}).get('file'), (v.get('chip') or {}).get('icon')]:
            if f and not os.path.exists(resolve_asset(task_dir, f)): warn.append(f'Thiếu file: {f}')
        if v.get('layout') in ('L1', 'L2') and not (v.get('visual') and os.path.exists(os.path.join(task_dir, v['visual']))) and not v.get('mascot') and not v.get('spot') and not v.get('element'):
            warn.append('Khung visual TRỐNG — cần hình (skill/3-image.md) hoặc đổi sang L3')
        doc, g = to_html(task_dir, key, v)
        hp = os.path.join(task_dir if a.keep_html else tempfile.gettempdir(), f'banner-{name}-{key}.html')
        open(hp, 'w', encoding='utf-8').write(doc)
        png = os.path.join(task_dir, f'banner-{name}-{key}.png')
        warn += render(hp, png)
        if not a.keep_html: os.remove(hp)
        status = '✅' if not warn else '⚠️ '
        problems += bool(warn)
        print(f'{status} {key} · {v.get("layout")} · {v.get("theme", "pink")} · khung y={g["fy"]} h={g["fh"]} · {os.path.basename(png)}')
        for w in warn: print('     -', w)
        done.append((key, png))
    if len(done) > 1:
        cp = os.path.join(task_dir, f'banner-{name}-compare.png'); compare(done, cp); print('🖼  ', os.path.basename(cp))
    for f in glob.glob(os.path.join(task_dir, '*.tmp.png')): os.remove(f)
    print('Xong.' if not problems else f'Xong, {problems} phương án cần sửa (xem ⚠️ ở trên).', 'Gửi ảnh vào chat để review.')


if __name__ == '__main__':
    main()
