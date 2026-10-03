# MoMo Social Banner Skill

An AI agent skill (Claude, Codex, Gemini) for designing **MoMo-branded social banners** — HTML/CSS rendered to fully layered 1080×1080 PNGs, with 2–3 design options per brief and illustrations in the MoMo style.

> Bộ skill cho AI (Claude / Codex / Gemini) để tư vấn và dựng **banner social chuẩn nhận diện MoMo**: HTML/CSS → PNG 1080×1080 đủ layer, 2–3 phương án mỗi brief, hình minh hoạ đúng phong cách MoMo.

## Quick start

```bash
cp -r projects/_template projects/my-task      # 1. new task
# 2. edit projects/my-task/spec.json (brief + variants)
python3 skill/build.py projects/my-task          # 3. build PNGs + compare sheet + QA
```

Optional illustration step: `python3 skill/img.py prompt projects/my-task` → generate → `img.py brandify` → `img.py check`.

## Structure

| Path | Contents |
|---|---|
| `AGENTS.md` | Main instructions for any AI agent (read first) |
| `SKILL.md` | Skill entry point (Claude skill format) |
| `skill/` | Guides (brand, banner, image, advisor, resources), `momo.css`, `momo.js`, `build.py`, `img.py` |
| `assets/` | Brand assets: colors, fonts, icons, illustrations, logos, patterns — see `assets/INDEX.md` |
| `references/` | Reference MoMo banners + style packs |
| `projects/` | Example tasks, one flat folder each |

## Features

- 6-step workflow: advise → spec → image → build → fix → review
- Themes incl. MoMo pink and the Nghiên AI theme (`"theme": "nghien"`)
- Co-branding with partner logos, standalone mode (`"no_momo": true`)
- Automatic QA warnings from `build.py`

## Requirements

Python 3 and Google Chrome / Chromium (headless export).

## Disclaimer

MoMo name, logos, fonts and brand assets belong to M_Service (MoMo). This is an unofficial community project for design workflow purposes.
