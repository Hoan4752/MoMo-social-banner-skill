# 2 · Dựng banner — layout, preset, spec, lệnh

> Đầu ra của mọi task = **PNG banner hoàn chỉnh đủ layer** (1080×1080), dựng bằng `skill/build.py` từ `spec.json`. Không giao key visual rời, không giao khung trống.

## 1. Banner anatomy — tên gọi chuẩn các element

Dùng đúng các tên này khi viết brief, comment, feedback và đặt class trong HTML.

```
┌──────────────────────────────────────────────┐
│  [6a] headline ……………………………………      [5] sec-strip (top)
│  [6a] headline + [6b] hl-box (box highlight) │ ▓
│  [6c] sub                                    │ ▓
│  [6d] cta (nút)            [1] bg-base + [2] bg-wave (họa tiết chìm)
│                                              │
│   ┌notch tl┐┌──────────────────────┐ notch tr│
│   └────────┘│                      │  [5] sec-strip (step)
│   ┌─────────┘   [3] qr-frame       │ ▓
│   │   [3a] frame-texture           │ ▓
│   │   [3b] key-visual / [3c] photo │ ▓
│   │   [3d] partner-card (nếu có)   │
│   ├──────────┐                     │ ▓
│   │[4] logo- │  notch bl           │ ▓ [5] sec-strip (bottom)
│   │  cutout  │                     │ ▓
└───┴──────────┴─────────────────────┴─────────┘
```

| # | Tên (class) | Là gì | Nguồn / quy tắc |
|---|---|---|---|
| 1 | `bg-base` | Màu nền poster | Pink −2 `#FFEEF4` (hồng) · `#EAF5FD` (xanh banknote) |
| 2 | `bg-wave` | **Họa tiết chìm** (embedded pattern) — sóng song song kiểu vân tiền | File sóng grayscale chính thức `assets/patterns/money-elements_patterns_4.png`, **pre-tint** bằng `skill/img.py tint`. Đậm dần về phải |
| 3 | `qr-frame` | **Khung QR** — khung chứa visual, cắt 3 góc (tl, tr, bl), giữ góc dưới-phải | `skill/momo.js`, khai báo `data-tl / data-tr / data-bl / data-r` |
| 3a | `frame-texture` | Vân khắc bên trong khung (tuỳ chọn) | `money-elements_patterns_17_1.png` pre-tint, opacity thấp |
| 3b | `key-visual` | Hình chính: element tách nền (loại B) | `assets/illustrations/*` hoặc `gen/*.png` |
| 3c | `photo` | Ảnh chữ nhật sạch (loại A) phủ kín khung | `gen/main_visual.png` (tự thay placeholder) |
| 3d | `partner-card` | Thẻ chứa logo đối tác (deal co-brand) | Logo đối tác là layer code (file trong folder task), không để model ảnh vẽ |
| 4 | `logo-cutout` / `lockup` | Logo MoMo (± logo đối tác) đặt trong **notch bl** | Nằm **ngoài** qr-frame, trên nền poster, **không hộp nền riêng** |
| 5 | `sec-strip` | **Dải bảo an** (security strip) — khối hồng + ô chữ "mo mo" | Chỉ dùng `assets/patterns/security_strips/security_strip_01..10.png`, neo bằng `data-anchor` |
| 6a | `headline` | Tiêu đề | MoMo Trust Display, tracking 0, line-height 1.22 |
| 6b | `hl-box` | **Box highlight / box khuyến mãi** — hộp sọc chéo | Khung tối → chữ trắng; khung sáng → chữ hồng. Tối đa 1 lần / headline |
| 6c | `sub` | Dòng phụ | Trust Display cỡ nhỏ hơn hoặc Trust Sans Medium |
| 6d | `cta` | Nút kêu gọi ("LẤY NGAY") | Hộp hồng `#F95396`, viền trắng trong, bóng sọc lệch 6px |
| — | `hl-sign` | Chữ ký tay (MoMo Signature) | Cùng cỡ Display, tối đa 1 lần / headline |
| — | `hl-number` | Số nổi bật ("20K", "10%") | Xem `skill/1-brand.md` §4 |


## 2. Layout (L1–L5) & preset
Canvas 900×900 (xuất ×1.2 = 1080). Chung: bo góc khung 14px · logo MoMo 81px · dải bảo an rộng 47px · tracking 0 · line-height 1.22. `build.py` tự tính toạ độ — **không đặt toạ độ tay**.

| Mã | Tên | Khi dùng | Khung (fx,fy,fw,fh) · notch | Ref |
|---|---|---|---|---|
| **L1** | Visual + logo MoMo | Ưu đãi có hình, không đối tác | 30, ≥357 (tự hạ theo chữ), 837, tới y 865 · tl 103×41 · bl **103×95** | R13 R14 R17–R20 R24 |
| **L2** | Visual + co-brand | Deal/sự kiện có đối tác | 34, ≥318, 832, tới y 865 · tl 73×40 · bl = 2+81+30+logo đối tác+20 (mark 62px ≈ **209×95**, có chữ ≈ 383×95) | R01 R02 R05 R07–R09 R15 |
| **L3** | Editorial panel (không cần hình) | Mẹo, câu hỏi, thông báo; khi chưa có hình | 37, 38, 827, 826 · tl **295×112** (tag-chip) · bl 103×95 · dải bảo an top/**mid**/bottom | R04 R16 |
| L4 | Thẻ sản phẩm / bảng giá | So sánh gói | chưa có — giai đoạn 4 | R10 R23 |
| L5 | Logo trên + chip chủ đề dưới | Chuỗi bài theo chủ đề | chưa có — giai đoạn 4 | R11 R21 R22 |

### Theme (`"theme"`) — màu đo từ ref

| Theme | bg | sóng nền | hl-box | frame |
|---|---|---|---|---|
| pink | `#FFEEF4` | `#FFD3E3` | `#F95396 / #DD2B86` | `#FFE1EC → #FBC4D9` |
| blue | `#EAF5FD` | `#C6DFF4` | `#1F5FC4 / #174C9E` | `#A8CCF5 → #6EA7EB` |
| mint | `#E4F9F2` | `#C4EBDD` | `#1E8C7A / #157062` | `#D3F2E8 → #A9E0CF` |
| yellow | `#FFF7DA` | (chưa) | `#E5242B / #B81D22` | `#FFF0B8 → #FFE08A` |
| peach | `#FFEFE6` | `#FFD5C8` | `#FF623B / #E04823` | `#FFE0CF → #FFC2A3` |
| **nghien** | `#FFF3EE` | `#FFD5C8` | `#FF623B / #E04823` | `#FFE2D8 → #FFC0AC` |


### Kiểu nhấn headline (tối đa 1 / headline)

| Kiểu | Class | Khi dùng | Ref |
|---|---|---|---|
| Box sọc | `hl-box` | Từ khoá lợi ích / con số / tên sự kiện | đa số |
| Chữ ký tay | `hl-sign` | Từ cảm xúc đầu câu ("Đừng", "nhẹ ví", "thật nhanh", "độc quyền") | R01, R07, R15, R18–R20 |
| Số nổi bật | `hl-number` | Giá/giảm giá đặt trong visual ("45k", "79k") | R08, R15 |


## 3. Luật cứng của từng layer
- **bg-wave:** chỉ dùng sóng grayscale chính thức đã tô màu sẵn trong `assets/patterns/tinted/` (tạo mới: `python3 skill/img.py tint assets/patterns/money-elements_patterns_4.png "#HEX" assets/patterns/tinted/bg_wave_<theme>.png`). Không vẽ sóng bằng CSS/SVG, không dùng CSS mask (lỗi khi mở file://).
- **qr-frame:** mọi hình (visual / element / mascot) nằm TRONG khung → khung tự cắt 3 góc (tl, tr, bl), góc dưới-phải luôn nguyên. Hình được phép tràn khung để giấu chi tiết thừa. Khung tự động phủ lớp `.frame-texture` hoa văn sóng bảo an lên bề mặt ảnh photo (`.photo`) để tạo chiều sâu thị giác.
- **logo-cutout / lockup:**
  - *Mặc định MoMo:* nằm NGOÀI khung, trong notch dưới-trái, MoMo trái — đối tác phải — cách 30px (1 chữ "O").
  - *Chế độ Nghiên AI / Không dùng MoMo (`"no_momo": true`):* Chỉ hiển thị logo đối tác / Nghiên AI. Tự động lấy logo từ task dir hoặc thư mục chung `assets/logos/`.
  - *Logo trên Title (`"logo_pos": "top"`):* Đặt logo nhỏ gọn phía trên Title (`partner_top_h: 38`), góc dưới-trái của khung tự động bo tròn liền mạch, không cắt notch.
- **sec-strip:** chỉ dùng 10 module `assets/patterns/security_strips/`, neo theo khung (top / step|mid / bottom), mép phải = mép phải khung.
- **copy:** headline MoMo Trust Display 50–54px, ≤ 3 dòng, mỗi dòng ≤ ~22 ký tự, đúng 1 cụm nhấn; sub Trust Sans ≤ 2 dòng; tiếng Việt đủ dấu.

## 4. spec.json — 1 file cho cả task
```json
{
  "task": "ten-task",
  "brief": {"goal": "…", "audience": "…", "copy_goc": {"headline": "…", "sub": "…"}, "missing": "…"},
  "defaults": {"partner": "logo-doi-tac.png", "partner_h": 62},
  "variants": {
    "A": {"layout": "L3", "theme": "pink", "formula": "Câu hỏi gợi tò mò",
           "title_options": ["… ✅", "…", "…"],
           "chip": {"icon": "logo-doi-tac.png", "label": ["Dòng 1", "Dòng 2"]},
           "headline": ["Dòng 1", "có [cụm nhấn]", "dòng 3?"], "sub": ["…"], "footnote": "(*) …"},
    "B": {"layout": "L2", "theme": "pink", "headline": ["…"], "sub": ["…"], "cta": "LẤY NGAY",
           "visual": "visual-B.png",
           "image": {"style": "S1", "tone": "pink-blue", "kind": "scene", "scene": "mô tả cảnh bằng tiếng Anh"}}
  },
  "log": [{"date": "YYYY-MM-DD", "agent": "…", "note": "…"}]
}
```
Trường hình (chọn 1 hoặc kết hợp): `"visual"` ảnh chữ nhật phủ kín khung · `"element": {"file", "left", "top", "width"}` element tách nền đặt TRONG khung (toạ độ từ góc khung, bị khung cắt) · `"spot"` element đặt tự do trên poster · `"mascot": {"file": "mascot_momo_14-1.png", "left", "top", "width"}` mascot chính thức từ `assets/illustrations/`.
Cú pháp nhấn: `[..]` = hl-box · `{..}` = hl-sign. Tuỳ chọn khác: `"strips": [3,6,9]`, `"h_size": 52`.
Mẫu chạy được: `projects/nghien-connect-4/spec.json` (L3 + 2×L2), `projects/student-pass-u22/spec.json` (L1 + element).

## 5. Lệnh
```bash
python3 skill/build.py projects/<task>            # → banner-<task>-A.png, -B.png, … + banner-<task>-compare.png
python3 skill/build.py projects/<task> --only B   # dựng 1 phương án
python3 skill/build.py projects/<task> --keep-html  # giữ HTML để soi lỗi (xoá sau khi xong)
```
Xuất ảnh bằng Chrome/Edge/Brave có sẵn (headless, ~1s/banner); không có thì dùng Python Playwright (`pip install playwright && playwright install chromium-headless-shell`).

## 6. QA
`build.py` tự báo ⚠️: chữ đè dải bảo an / đè khung · >1 cụm nhấn · logo sát mép notch · thiếu file · ảnh không tải · khung trống. **Có ⚠️ = chưa xong** → sửa spec, build lại.
Tự xem PNG thêm: hình đúng phong cách (skill/3-image.md) · mascot đúng vai (01 §7) · không bịa thông tin · nội dung đúng brief.

## 7. Danh mục banner thật R01–R24 (references/)

| Mã | Layout | Theme | Highlight | Nội dung |
|---|---|---|---|---|
| R01 | L2 | pink | hl-box + hl-sign | Metro cuối tuần |
| R02 | L2 | peach | hl-box | ePass |
| R03 | L1 (không khung) | mint | — | Độc quyền 500k |
| R04 | L3 (logo trên) | pink | hl-box | Quỹ chi tiêu |
| R05 | L2 | blue | hl-box | CapCut Pro 20k |
| R06 | L1 (không khung) | yellow | hl-box | Thanh toán điện |
| R07 | L2 | blue | hl-sign | Metro gửi xe |
| R08 | L2 | pink/red | hl-number | Youtube Premium 45k |
| R09 | L2 (wordmark) | mint | hl-box | Vote Game Awards |
| R10 | L4 | pink/red | hl-box | Gói A89D |
| R11 | L5 | pink | hl-box | Shopee hoàn 30% |
| R12 | L1 | blue | hl-box | Thanh toán mọi nơi |
| R13 | L1 | pink | — | Ví Trả Sau |
| R14 | L1 | pink | hl-box | Student Pass U22 |
| R15 | L2 | mint | hl-sign + hl-number | Vé Gameverse |
| R16 | L3 | pink | hl-box | Thanh toán quốc tế |
| R17 | L1 (ảnh) | pink | hl-box | After You |
| R18 | L1 | pink | hl-sign | Trạm chụp ảnh |
| R19 | L1 | yellow | hl-sign | Thanh toán Thái Lan |
| R20 | L1 | pink | hl-sign | eSIM du lịch |
| R21 | L5 (co-brand trên) | pink | hl-box | Gameverse sinh viên |
| R22 | L5 (ảnh sự kiện) | purple | — | Chống lừa đảo |
| R23 | L4 | pink | hl-box | MOMO79 3GB |
| R24 | L1 (ảnh) | pink | hl-box | Loa báo chuyển khoản |
