# Mini App · MoMo Mini App UI Guideline (developers.momo.vn)

> Nguồn: https://developers.momo.vn/v3/docs/app-center/design-guideline/design-guideline-overview/ (đọc 01/10/2026).
> Dùng khi thiết kế **màn hình app / Mini App** chạy trong MoMo — khác với poster social (xem 01, 02).
> Spec chi tiết component/token nằm ở Design System: https://ds.momoapp.vn · Kit code: https://momo-kits.web.app

## 1. 5 nguyên tắc thiết kế
1. **Clear** — chữ đọc rõ ở mọi cỡ, icon dễ nhận ra.
2. **Consistent** — chữ, icon, màu, layout đồng nhất giữa các màn.
3. **Customer Owned** — người dùng quyết định; app chỉ gợi ý & cảnh báo.
4. **Recognizable** — layout dễ đoán, trực quan, tổ chức nhất quán.
5. **Error Free** — chủ động ngăn lỗi thay vì chỉ báo lỗi.

## 2. 11 nguyên tắc UX
1. Mỗi màn hình 1 trọng tâm; bỏ phần tử không liên quan.
2. Phân rõ thông tin chính/phụ; không dồn quá nhiều nội dung 1 cấp.
3. Điều hướng rõ (đang ở đâu, đi đâu, quay lại). **Navigation bar dùng màu thương hiệu merchant**, không dùng màu MoMo Super App; không phù hợp → dùng trắng.
4. Giao diện dễ hiểu nhanh; bỏ yếu tố không phục vụ quyết định.
5. Bước hành động rõ ràng; hạn chế pop-up.
6. Báo lỗi chính xác, chỉ ra trường lỗi, hướng dẫn sửa; lỗi hệ thống kèm lựa chọn xử lý.
7. Giảm thời gian chờ: progress bar cho tải lâu, cho phép hủy, 1 loading liên tục (không nhiều loading cùng lúc).
8. UX writing: đơn giản, nhất quán, ngôn ngữ quen thuộc, không thuật ngữ.
9. Tab bar: tránh nếu không cần; tối đa **3 module**.
10. Giảm nhập liệu: dùng API/auto-fill, lựa chọn có sẵn.
11. Tutorial chỉ cho thao tác phức tạp nhiều bước; dùng tooltip để giới thiệu tính năng.

## 3. Foundation
| Mục | Quy định |
|---|---|
| **Màu Primary** | Nav bar, nút chính, progress, slider, trạng thái active/focus — dùng **màu thương hiệu merchant**. ❗Không dùng màu giống/na ná hồng MoMo |
| **Màu khác** | Grayscale (trung tính) · Status: Error / Warning / Success / Info |
| **Typography** | **San Francisco** (UI app) — khác với font MoMo Trust dùng cho truyền thông |
| **Layout** | Spacing là **bội số 4px** · lề trái/phải **16px** · khoảng cách giữa phần tử **12px** · có chuẩn carousel trượt ngang |
| **State** | Trạng thái phải phân biệt rõ; Disabled = không tương tác được nhưng vẫn hiển thị |

## 4. Icon Mini App
- Logo merchant **128×128px**; đơn giản, không dùng ảnh chụp, 1 ý chính / icon.
- 5 thành phần: Merchant logo · Background · Service name · Container · Tag line.

## 5. Components
- Bộ component chuẩn của MoMo: https://ds.momoapp.vn/9346742a0/p/069928-avatar/b/961510
- Cài đặt/tải kit: https://momo-kits.web.app/?path=/docs/core-navigation--page

## 6. Branding logo MoMo trong Mini App
- Trang thanh toán: dùng logo **không wordmark**; chữ "MoMo"/"Paid with MoMo Wallet" đặt **bên phải** logo.
- Icon & wordmark màu trắng (không trong suốt); bản standalone: hồng-trắng hoặc đen-trắng.
- Vùng trống quanh logo = X (2X = chiều cao logo). Tối thiểu: logo vuông **40px**, logo tròn **44px**.
- Không xoay, kéo méo, đổi màu. Biến thể/thay icon phải được MoMo duyệt. Tải: `momo-primary-logo.zip` (trang Branding Guidelines).

## 7. Design Checklist
- File PDF "Design Guideline Checklist" tại https://developers.momo.vn/v3/docs/app-center/design-guideline/design-checklist
- ❗Thiết kế không đạt chuẩn sẽ ảnh hưởng việc duyệt phát hành Mini App.
