# 4 · Tư vấn — từ mục tiêu → 2–3 phương án

> Áp dụng cho mọi agent (Claude, Codex, Gemini). Mọi phương án ghi chung trong 1 `spec.json` (skill/2-banner.md §4).

## 1. Khi nào dùng
| Người dùng gửi | Agent làm |
|---|---|
| Chỉ có **mục tiêu / task** ("làm banner mời workshop X", "quảng bá deal Y") | **Advisor mode**: tư vấn layout + đặt title → dựng **3 phương án** (tối thiểu 2) |
| Có mục tiêu + vài ý copy nhưng chưa chốt layout | Advisor mode, giữ nguyên copy người dùng ở ít nhất 1 phương án |
| Đã ghi **rõ layout (L1–L5) + title chính xác** (+ theme) | **Không tư vấn**, dựng đúng 1 bản theo yêu cầu |

## 2. Quy trình Advisor (5 bước)

1. **Hiểu mục tiêu** — rút ra (hỏi tối đa 1 câu nếu thiếu thông tin quyết định):
   - Loại thông điệp: ưu đãi/giảm giá · sự kiện/mời tham gia · kiến thức/mẹo · thông báo tính năng · co-brand đối tác
   - Có đối tác/logo đối tác? · Có visual sẵn hay cần gen? · Con số nổi bật (giá, %, ngày)? · Đối tượng (sinh viên, brand marketer, người đi du lịch…)
2. **Chọn layout** theo bảng §3 → chọn 2–3 layout/theme **khác nhau rõ** (không phải 3 bản chỉ đổi màu).
3. **Đặt title** cho mỗi phương án theo 1 công thức khác nhau (§4). Mỗi title: headline ≤ 3 dòng, mỗi dòng ≤ ~22 ký tự ở 50px; đúng 1 highlight; sub ≤ 2 dòng.
4. **Ghi vào `spec.json`** (variants A/B/C, kèm `formula`, `title_options` đánh dấu ✅ option chọn, `image` nếu cần hình) → tạo hình (skill/3-image.md) → `python3 skill/build.py projects/<task>` → PNG từng phương án + `compare.png`.
5. **Gửi `banner-<task>-compare.png` vào chat** và trình bày dạng bảng: phương án · layout · theme · headline · lý do chọn · cần thêm gì (visual/logo). Đề xuất 1 phương án nên chọn. Người dùng chọn → mới làm tiếp visual/hoàn thiện.

## 3. Bảng chọn layout theo mục tiêu

| Mục tiêu | Ưu tiên | Phương án thay thế |
|---|---|---|
| Giảm giá / deal có đối tác | **L2** | L4 (nếu cần bảng giá), L1 |
| Ưu đãi không có đối tác, có hình minh hoạ | **L1** | L2 (nếu có kênh như App Store) |
| Sự kiện / workshop / mời tham gia | **L2** (logo đơn vị tổ chức) | L3 (câu hỏi gợi tò mò), L5 |
| Kiến thức / mẹo / câu hỏi | **L3** | L1 |
| So sánh gói / bảng giá / thẻ sản phẩm | **L4** | L2 |
| Chuỗi bài theo chủ đề (series) | **L5** hoặc **L3** (tag-chip = tên series) | L1 |
| Không có visual & cần gấp | **L3** (không cần gen ảnh) | — |

Theme: pink mặc định; blue cho công nghệ/du lịch/thanh toán quốc tế; mint cho game/giới trẻ/sức khoẻ; yellow cho hoá đơn/điện nước/Tết; peach cho giao thông/xe.

## 4. Công thức đặt title (mỗi phương án dùng 1 công thức khác nhau)

| Công thức | Mẫu | Ví dụ ref |
|---|---|---|
| **Lợi ích + con số** | `<Sản phẩm>` / `<lợi ích> [hl: con số]` | "Capcut Pro / MoMo tặng deal giảm [20k]" |
| **Câu hỏi gợi tò mò** | `<Tình huống>` / `[hl: từ khoá] thì` / `<câu hỏi>?` | "Đi cửa hàng tiện lợi / ở [nước ngoài] thì / nên mua gì?" |
| **Lời khuyên "Đừng"** | `[sign: Đừng] <nỗi đau>` + sub giải pháp | "[Đừng] để mình lag giữa đường" |
| **Đối tượng + quyền lợi** | `<Đối tượng> <hành vi>` / `nhận [hl: quyền lợi]` | "Sinh viên mê xem phim / U22 nhận [ưu đãi giá vé]" |
| **Kêu gọi hành động** | `<Động từ> cho <X>` / `được [hl: danh hiệu]` | "Vote cho MoMo là / kênh thanh toán / được [yêu thích nhất]" |
| **Tên sự kiện + câu hook** | `<Tên sự kiện> [hl: #số]` / `<câu hook>` | "Nghiên Connect [#4] / Brand Marketing / muốn học không?" |

Giọng văn MoMo: thân thiện, ngắn, dùng từ đời thường, không thuật ngữ; không hứa hẹn con số không có trong brief.

## 5. Mẫu trình bày kết quả

| | A | B | C |
|---|---|---|---|
| Layout · theme | L3 · pink | L2 · pink | L2 · blue |
| Headline | … | … | … |
| Sub | … | … | … |
| Vì sao | … | … | … |
| Cần thêm | icon 3D | visual 16:9 | visual 16:9 |

**Đề xuất:** <phương án> vì <lý do>.

Ví dụ: `projects/nghien-connect-4/spec.json`.
