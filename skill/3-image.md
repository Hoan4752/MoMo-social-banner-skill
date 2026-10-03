# 3 · Hình ảnh — tạo bằng ChatGPT/Gemini, khoá phong cách MoMo, ghép vào banner

> Nguyên tắc: **code dựng layout, model ảnh chỉ vẽ hình.** Logo, chữ, khung, sóng nền, dải bảo an, mascot → không bao giờ để model ảnh vẽ.

## 1. Nguồn hình (ưu tiên từ trên xuống)
1. Asset chính thức trong `assets/illustrations/` (mascot_*, THAN_TAI_*, HEODAT_*, money-illustration_*) — xem `assets/INDEX.md`.
2. Hình AI tạo mới theo quy trình dưới đây.
3. Chưa có hình → dùng layout **L3** (không cần hình). Không giao banner khung trống.

## 2. Ba phong cách — mỗi hình chỉ 1 phong cách, không trộn
| Mã | Tên | Bộ ảnh mẫu `references/style_packs/` | Dùng khi |
|---|---|---|---|
| **S1** (mặc định) | Minh hoạ nét + chấm halftone | `S1_crayon_halftone/` — R01 R02 R06 R07 R09 R12 R14 R18 R19 R20 R21 | Người, cảnh đời thường, câu chuyện |
| S2 | 3D bóng (clay) | `S2_3d_glossy/` — R13 R16 R23 | Chỉ khi brief yêu cầu: icon, đồ vật, thẻ, xu |
| S3 | Ảnh thật | `S3_photo/` — R11 R17 R24 | Quán, sản phẩm thật, người thật |

**DNA S1:** nét viền mực đều màu đậm của hue chính (navy #1F3F8F / xanh #1F4FA8 / magenta #A50064 — **không bao giờ đen**) · mảng pastel phẳng, tối đa 2–3 hue theo cặp (hồng+navy R14/R20/R21 · hồng+xanh lá R18 · xanh đơn sắc R07/R12 · mint R09 · vàng+đỏ R06/R19) · bóng chỉ bằng chấm halftone & nét gạch song song · nền có đường khắc lượn sóng như tiền giấy · người Việt trẻ, tỉ lệ thật.
**CẤM S1:** 3D, render, glossy, gradient, glow, bóng mềm, viền đen dày, anime/chibi, neon, >3 hue, nền trắng trơn, chữ/số/logo/QR/khung/viền, mascot MoMo.

## 3. Quy trình 6 bước
1. **Mô tả hình trong spec** (mỗi phương án cần hình):
   `"image": {"style": "S1", "tone": "pink-blue", "kind": "scene" | "spot", "scene": "mô tả cảnh bằng tiếng Anh"}`
   `tone`: pink-blue · pink-green · blue · mint · yellow-red · peach-blue (khớp `theme` của banner).
2. **Sinh prompt tự động:** `python3 skill/img.py prompt projects/<task>` → in prompt đúng tỉ lệ khung (16:9, 3:2…), đúng DNA + CẤM, danh sách ảnh mẫu cần đính kèm, tên file cần lưu; đồng thời ghi vào `spec.json`.
3. **Tạo hình** (ChatGPT / Gemini / công cụ có sẵn): mỗi hình 1 cuộc chat mới, đính kèm 3–4 ảnh mẫu được liệt kê, dán prompt.
   - Nếu lệch style: *"Take reference image #1 as the base image and keep its exact line color, line weight, halftone dots, engraving lines and palette — only replace the content."* (tối đa 3 lần)
   - ChatGPT xin được PNG nền trong suốt cho `spot`; Gemini hay tự chèn chữ → nhắc "no text" 2 lần.
4. **Hậu kỳ** (ghi đè lên chính file, không giữ file tạm):
   ```bash
   python3 skill/img.py removebg spot.png spot.png --trim            # chỉ với kind=spot (nền trắng; nền đen: --bg "#000000")
   python3 skill/img.py brandify visual-B.png visual-B.png --style S1 --tone pink-blue
   ```
   brandify: kéo màu về bảng MoMo + (S1) gradient map về cặp màu, chấm halftone, vân khắc chính thức. ⚠️ `--tone` đổi màu mọi thứ — nếu có mascot thì chỉ dùng tone có hồng hoặc ghép mascot riêng (`"mascot"` trong spec).
5. **Chấm điểm:** `python3 skill/img.py check visual-B.png --style S1` → **PASS ≥ 65** (11/11 ảnh mẫu S1 đạt 69.7–86.7; ảnh lệch style 39–63). RETRY → quay lại bước 3. Element tách nền điểm thấp hơn — chấm lại trên PNG banner cuối.
6. **Build:** `python3 skill/build.py projects/<task>` — hình tự vào khung, khung tự cắt góc.

## 4. Khung prompt (khi tự viết, không dùng `img.py prompt`)
```text
Keep EXACTLY the drawing style, line color, halftone shading, engraving lines and palette of the reference illustrations.
<DNA S1 với màu theo tone>
Create a NEW illustration, aspect ratio <W:H>: <cảnh>.
Clean rectangle. Main subjects center-right; top-left and bottom-left corners calm and empty (cropped by the layout frame; bottom-left holds the logo).
FORBIDDEN: <CẤM S1>, any text/letters/numbers/logos/QR, frames, borders, pink 'mo mo' strips, the MoMo mascot.
```
