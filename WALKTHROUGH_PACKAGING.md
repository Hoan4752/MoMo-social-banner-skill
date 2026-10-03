# WALKTHROUGH: ĐÓNG GÓI QUY TRÌNH THIẾT KẾ BANNER NGHIÊN AI (MOMO BANNER FRAMEWORK)

Tài liệu này xác nhận và hướng dẫn chi tiết cách **đóng gói trọn bộ quy trình thiết kế banner Nghiên AI** (dựa trên hệ thống MoMo Banner Framework). Bạn có thể nén hoặc gửi toàn bộ thư mục này cho bất kỳ ai, và bất kỳ AI nào (Claude, Codex, Gemini) khi mở thư mục này lên đều tự động nắm được 100% quy trình làm banner chuẩn nhận diện mới nhất chỉ với vài câu lệnh ngắn.

---

## 1. Trả lời 2 thắc mắc cốt lõi của bạn

### Câu hỏi 1: Quy trình này đã lưu trong folder hay chỉ nằm trong context chat?
> **Trả lời:** Trước lượt trao đổi này, một số tinh chỉnh kỹ thuật (theme `nghien`, `no_momo: true`, `logo_pos: top`, layer texture đè trên ảnh) nằm ở file code `build.py` và `momo.css`, nhưng tài liệu quy chuẩn (`AGENTS.md`, `skill/2-banner.md`) và file template vẫn theo cấu hình cũ của MoMo.
> 
> 👉 **Hiện tại: ĐÃ ĐÓNG GÓI 100% VÀO FILE HỆ THỐNG TRONG FOLDER:**
> 1. `AGENTS.md`: Đã bổ sung điều khoản nhận diện Nghiên AI, cờ `"no_momo": true`, vị trí logo `"logo_pos": "top"`, và lớp texture bảo an.
> 2. `skill/2-banner.md`: Đã cập nhật bảng theme chính thức thêm dòng **`nghien`** (`#FF623B`, nền `#FFF3EE`, sóng bảo an `#FFD5C8`), cùng quy tắc layer độc lập và texture overlay.
> 3. `skill/build.py`: Đã bổ sung hàm `resolve_asset()` tự động tìm logo trong `assets/logos/` mà không bắt buộc phải copy thủ công vào từng project.
> 4. `projects/_template/spec.json`: Đã cài sẵn preset mặc định cho Nghiên AI.

---

### Câu hỏi 2: Logo Nghiên AI đã có trong assets chưa? Thêm vào có được không?
> **Trả lời:** Ban đầu `assets/logos/` chỉ chứa logo MoMo. 
> 
> 👉 **Hiện tại: ĐÃ TÍCH HỢP ĐẦY ĐỦ 5 FILE LOGO NGHIÊN AI VÀO `assets/logos/`:**
> - `assets/logos/nghienai-logo-mark.png` *(Biểu tượng cờ cam Nghiên AI chuẩn 1:1)*
> - `assets/logos/nghienai-logo-full.png` *(Logo đầy đủ biểu tượng + chữ)*
> - `assets/logos/nghienai-logo-orangetext.png` *(Logo chữ cam nền trong suốt)*
> - `assets/logos/nghienai-logo-mark.svg` *(Bản vector SVG của biểu tượng)*
> - `assets/logos/nghienai-logo-white.svg` *(Bản vector SVG màu trắng)*
> - Đồng thời đã cập nhật file kiểm kê `assets/INDEX.md`.
> 
> *Từ nay, trong bất kỳ file `spec.json` nào, chỉ cần khai báo `"partner": "nghienai-logo-mark.png"` là `build.py` sẽ tự động tìm thấy và nạp thẳng vào banner!*

---

## 2. Bản đồ các tính năng cốt lõi đã được đóng gói

```
┌────────────────────────────────────────────────────────────────────────┐
│                        MoMo Design System                              │
│                                   +                                    │
│                 Nhận Diện Thương Hiệu Nghiên AI                        │
└────────────────────────────────────────────────────────────────────────┘
       │
       ├─► 1. Colography Nghiên AI ("theme": "nghien")
       │     • Primary Coral Orange: #FF623B (khớp mã màu logo & cờ Nghiên AI)
       │     • Secondary Accent:     #E04823 (sọc badge [từ khoá])
       │     • Background Warm Cream:#FFF3EE (nền ấm áp, tương phản chữ đen)
       │     • Sóng Banknote Bảo An: assets/patterns/tinted/bg_wave_nghien.png
       │
       ├─► 2. Chế độ Không Logo MoMo ("no_momo": true)
       │     • Ẩn toàn bộ wordmark MoMo.
       │     • Chỉ dùng duy nhất logo Nghiên AI.
       │
       ├─► 3. Vị trí Logo Linh Hoạt
       │     • Góc dưới-trái (mặc định): Nằm trong notch cắt chuẩn MoMo.
       │     • Trên Title ("logo_pos": "top"): Logo nhỏ (partner_top_h: 38px) 
       │       đặt phía trên Title, góc dưới khung tự động bo tròn không cắt notch.
       │
       ├─► 4. Lớp Texture Bảo An Đè Trên Ảnh Photo
       │     • Code tự động xếp .photo (z-index: 1) và .frame-texture (z-index: 2).
       │     • Vân sóng tiền tệ (#FFAF96) phủ tinh tế trên bề mặt ảnh, mang lại 
       │       chiều sâu thị giác đặc trưng của tờ tiền giấy.
       │
       └─► 5. Bảng So Sánh Thông Minh (Compare Grid)
             • 1 phương án: Xuất thẳng banner lẻ 1080×1080.
             • 2–4 phương án: Bảng so sánh 1 hàng ngang.
             • >4 phương án: Tự động xếp lưới 3 × 3 chuyên nghiệp.
```

---

## 3. Hướng dẫn sử dụng cho người khác (Cheat-sheet Prompting)

Khi bạn nén thư mục này gửi cho đồng nghiệp, bạn bè hoặc dùng trên máy khác với Claude / Codex / Gemini, người dùng chỉ cần mở folder trong môi trường làm việc và gõ các câu lệnh mẫu sau:

### Mẫu 1: Yêu cầu tư vấn 3 phương án (Khuyên dùng khi bắt đầu sự kiện mới)
> *"Làm cho mình banner Nghiên Connect #[Số], chủ đề [Tên chủ đề] cho [Đối tượng]. Không dùng logo MoMo, dùng logo Nghiên AI và theme nhận diện Nghiên AI."*

👉 **AI sẽ tự động:**
1. Tạo folder `projects/nghien-connect-[Số]/`.
2. Lập `spec.json` với 3 phương án khác nhau rõ rệt (L2 minh hoạ S1, L3 thẻ editorial, L2 chữ ký tay).
3. Tự lấy logo `assets/logos/nghienai-logo-mark.png`, bật `"no_momo": true`, theme `"nghien"`.
4. Sinh ảnh minh hoạ S1 đạt điểm chuẩn PASS ≥ 65.
5. Chạy `python3 skill/build.py` xuất ra bảng so sánh `banner-...-compare.png` gửi vào chat kèm đề xuất.

---

### Mẫu 2: Yêu cầu chốt đúng 1 bản banner cụ thể với ảnh chụp thực tế
> *"Chốt cho mình mẫu số [X] với ảnh chụp thực tế này: [đường dẫn ảnh]. Theme Nghiên AI cam san hô, phủ lớp texture bảo an trên ảnh."*

👉 **AI sẽ tự động:**
1. Cắt cúp ảnh đúng tỉ lệ khung L2 (1.603 : 1), tối ưu headroom và bố cục.
2. Cập nhật `spec.json` chỉ giữ duy nhất 1 biến thể đã chọn.
3. Kích hoạt layer texture đè trên ảnh với độ trong suốt chuẩn.
4. Xuất file PNG banner 1080 × 1080 px hoàn chỉnh, 0 lỗi cảnh báo QA.

---

## 4. Danh mục lệnh đầu cuối tiện ích (Terminal Commands)

Dành cho ai muốn chạy lệnh thủ công trong Terminal:

| Mục đích | Lệnh chạy Terminal |
|---|---|
| **Build toàn bộ banner & xuất so sánh** | `python3 skill/build.py projects/<tên-task>` |
| **Chỉ build riêng 1 variant (VD: mẫu A)** | `python3 skill/build.py projects/<tên-task> --only A` |
| **Tự động viết prompt tạo hình từ spec** | `python3 skill/img.py prompt projects/<tên-task>` |
| **Chấm điểm phong cách MoMo S1** | `python3 skill/img.py check <đường-dẫn-ảnh> --style S1` |
| **Kéo màu ảnh AI về chuẩn MoMo** | `python3 skill/img.py brandify in.png out.png --style S1 --tone peach-blue` |
| **Nhuộm hoa văn sóng mới (Tint wave)** | `python3 skill/img.py tint assets/patterns/money-elements_patterns_4.png "#HEX" out.png` |

---

## 5. Danh mục các file cấu hình quan trọng đã cập nhật

- **Quy chuẩn tổng:** `AGENTS.md`
- **Đặc tả Banner & Theme:** `skill/2-banner.md`
- **Đặc tả Stylesheet:** `skill/momo.css`
- **Bộ máy dựng ảnh & QA:** `skill/build.py`
- **Kho logo thương hiệu:** `assets/INDEX.md` và thư mục `assets/logos/`
- **Mẫu dự án chuẩn:** `projects/_template/spec.json`
