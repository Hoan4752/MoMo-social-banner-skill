# 5 · Tài nguyên MoMo — link chính thức & cách lấy file

## 1. Link nguồn chính thức
| Nguồn | Link | Dùng khi |
|---|---|---|
| MoMo Partners Brandbook | https://momopartners.m-n.associates/en/home/ (VI: bỏ `/en`) | Logo, màu, font, pattern, mascot, icon, ảnh cho truyền thông |
| Brandbook – Resources | https://momopartners.m-n.associates/en/resources/ | Tải file gốc (cần passcode) |
| Mini App Design Guideline | https://developers.momo.vn/v3/docs/app-center/design-guideline/design-guideline-overview/ | Thiết kế màn hình Mini App |
| Components | https://developers.momo.vn/v3/docs/app-center/design-guideline/components/ | Component UI |
| MoMo Design System | https://ds.momoapp.vn | Token màu, typography, state, component chi tiết |
| MoMo Kits (code) | https://momo-kits.web.app | Thư viện component dev |
| Design Checklist (PDF) | https://developers.momo.vn/v3/docs/app-center/design-guideline/design-checklist | Tự kiểm trước khi nộp Mini App |
| Branding Guideline (Mini App) | https://developers.momo.vn/v3/docs/app-center/design-guideline/branding-guideline | Logo thanh toán, `momo-primary-logo.zip` |

Các trang con brandbook (VI): `/logo/logo-chinh/` · `/logo/cac-phien-ban-logo/` · `/logo/bo-cuc-logo/` · `/mau-sac/bang-mau-momo/` · `/phong-chu/phong-chu-momo/` · `/phong-chu/hieu-ung-chu-noi-bat/` · `/hoa-tiet/hoa-tiet-chim/` · `/hoa-tiet/khung-qr/` · `/hoa-tiet/dai-bang-du-lieu/` · `/hinh-minh-hoa/` · `/tro-thu/{momo,mama-tai-chinh,than-tai,heo-dat}/` · `/bieu-tuong/` · `/nhiep-anh/` · `/ung-dung/`

## 2. Danh mục file tải trên Brandbook (cần passcode)
- **Logo:** màu logo trên nền màu · trên nền xám · bố cục logo (co-branding)
- **Màu:** MoMo color palette (HEX/RGB/CMYK đầy đủ, gồm 7 họ đa sắc)
- **Chữ:** MoMo font family · Highlighted text effects · Box promotion effects
- **Pattern:** Embedded pattern · QR frame · Data ribbon
- **Minh họa:** Character · Object · Illustration pattern · Combination principles
- **Mascot:** MoMo · Mama Tài Chính · Thần Tài · Heo Đất
- **Icon:** 3D · 2D
- **Ảnh:** Photography samples

## 3. Quy trình lấy tài nguyên từ Brandbook
1. Vào trang Resources → chọn mục cần tải.
2. Nhập **passcode** (gửi qua email đã đăng ký với MoMo).
3. Tick xác nhận: tài liệu là tài sản của **M_Service**, chỉ dành cho người được ủy quyền.
4. Bấm **Download resource** → giải nén → đặt vào `assets/<nhóm>/` đúng thư mục.
5. Ghi chú nguồn + ngày tải vào cuối file này (mục 4).

> ⚖️ Brandbook ghi rõ: tài liệu lưu hành nội bộ; đối tác, nhân viên, freelancer **không được sao chép, chia sẻ, tiết lộ**. Không đưa `assets/` lên repo công khai / không gửi cho bên thứ ba.

## 4. Nhật ký tải tài nguyên
| Ngày | Nguồn | File | Lưu tại |
|---|---|---|---|
| (trước 06/2026) | crawl brandbook (script cũ, đã gỡ) | logo, font, pattern, mascot, icon, ảnh | `assets/` |
