# AGENTS.md — MoMo Banner Skill (đọc file này trước tiên)

Áp dụng cho mọi AI (Claude, Codex, Gemini). Folder chỉ dùng để thiết kế banner social chuẩn nhận diện **MoMo**.

## Đầu ra
- Mỗi task giao **PNG banner hoàn chỉnh đủ layer** (1080×1080): `projects/<task>/banner-<task>-<A|B|C>.png` + `banner-<task>-compare.png`.
- **Làm xong phải gửi ảnh vào ô chat để người dùng review** (Claude: gửi file · Codex/Gemini: hiển thị `![](projects/<task>/banner-<task>-compare.png)` + đường dẫn). Chưa gửi ảnh = chưa xong.
- Không giao key visual rời, không giao khung trống, không có ⚠️ từ `build.py`.

## 6 bước
1. **Tư vấn** — chỉ có mục tiêu → 3 phương án khác nhau rõ (layout · theme · công thức title · hình), mỗi phương án 3 option title. Người dùng đã chốt layout + title → làm đúng 1 bản. → `skill/4-advisor.md`
2. **Viết `projects/<task>/spec.json`** (brief + variants + log). → `skill/2-banner.md §4`
3. **Hình** (nếu layout cần): `python3 skill/img.py prompt projects/<task>` → tạo hình theo phong cách S1 (mặc định, không 3D) → `img.py brandify` → `img.py check` PASS ≥ 65. Chưa có hình → dùng L3. → `skill/3-image.md`
4. **Build:** `python3 skill/build.py projects/<task>` → PNG + compare + QA tự động.
5. **Sửa** spec đến khi không còn ⚠️; tự xem PNG.
6. **Gửi ảnh review** + bảng so sánh + 1 đề xuất; ghi 1 dòng vào `log` của spec.

## Luật cứng
- Logo, chữ, khung cắt góc, sóng nền, 3 dải bảo an, mascot → luôn do code dựng; model ảnh chỉ vẽ hình minh hoạ.
- Logo MoMo & Đối tác:
  - Mặc định: Logo MoMo `assets/logos/momo_wordmark.png`. Đối tác: MoMo trái — đối tác phải — cách 1 chữ "O".
  - **Chế độ Nghiên AI / Độc lập (`"no_momo": true`):** Không dùng logo MoMo, dùng logo Nghiên AI (`assets/logos/nghienai-logo-mark.png` hoặc `nghienai-logo-full.png`). Vị trí logo: trong notch đáy hoặc trên Title (`"logo_pos": "top"`).
  - **Theme Nghiên AI (`"theme": "nghien"`):** Cam san hô `#FF623B`, sọc `#E04823`, nền kem `#FFF3EE`, sóng bảo an tông ấm (`bg_wave_nghien.png`).
  - **Lớp Texture:** Code tự động phủ `.frame-texture` hoa văn bảo an banknote lên trên ảnh photo (`.photo`).
- Font: Display (headline) · Trust Sans (sub) · Signature (nhấn). Tracking 0, line-height 1.22. Headline ≤ 3 dòng, đúng 1 cụm nhấn.
- Không bịa thông tin (giá, ngày, địa điểm, diễn giả) ngoài brief.
- Chi tiết brand: `skill/1-brand.md` · Mini App UI: `skill/miniapp.md` · link & cách lấy tài nguyên: `skill/5-resources.md`.

## Giữ folder sạch
- Mỗi task chỉ có: `spec.json` · hình đầu vào (`visual-*.png`, `element-*.png`, logo đối tác) · `banner-*.png`. Không folder con.
- Không tạo bản `_v2`: sửa thẳng `spec.json` rồi build lại. Không lưu HTML (chỉ `--keep-html` khi soi lỗi, xong xoá).
- Không tạo `node_modules`, `package.json`, symlink/shortcut tới project khác. Không sửa `skill/`, `assets/`, `references/` nếu người dùng chưa duyệt.
- Bắt đầu task mới: copy `projects/_template/spec.json`.

## Bản đồ
| Path | Nội dung |
|---|---|
| `skill/` | 6 file hướng dẫn · `momo.css` · `momo.js` · `build.py` · `img.py` |
| `assets/` | File thương hiệu gốc (chỉ đọc) — xem `assets/INDEX.md` |
| `references/` | 24 banner MoMo thật (R01–R24) + `style_packs/` ảnh mẫu phong cách |
| `projects/<task>/` | Mỗi task 1 folder phẳng |

## CHANGELOG
- 2026-10-03 — Đóng gói trọn bộ nhận diện Nghiên AI: tích hợp logo Nghiên AI vào `assets/logos/`, theme `nghien` (#FF623B) + sóng bảo an `bg_wave_nghien`, hỗ trợ `no_momo: true`, `logo_pos: "top"`, tự động phủ `.frame-texture` lên trên ảnh photo, tự tìm asset logo trong `assets/logos/`.
- 2026-10-02 — Tái cấu trúc: gộp guidelines/kit/scripts → `skill/` (9 docs → 6, 3 CSS → 1, 9 script → `build.py` + `img.py`); project = `spec.json` + hình + PNG; build tự xuất compare + QA; img.py tự viết prompt. Xoá 6 project cũ + claude_deal50k.
- 2026-10-02 — Style lock S1/S2/S3 + style_packs; Chrome headless xuất ảnh; preset bo góc 14, logo 81, notch 103×95 / co-brand tự tính.
- 2026-10-01 — Folder chỉ còn MoMo; đối chiếu brandbook chính thức.
