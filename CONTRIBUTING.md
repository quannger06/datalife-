# Quy trình hướng A

- Lấy `main` mới nhất, tạo `feature/...` hoặc `fix/...`.
- Mỗi PR chỉ chứa một tính năng và test tương ứng. Không sửa module của người khác nếu không cần.
- Chạy test trên máy, push và mở PR vào `main`.
- CI lỗi: đọc log và sửa nguyên nhân. Không xóa test, bỏ check hoặc đổi tên required check để né lỗi.
- Người quản lý xem diff và merge thủ công khi CI đạt và nhánh cập nhật với main.
- Sau merge phải kiểm tra CI trên main. Không force push hoặc xóa main.
- Không commit secrets. Backend thật cần thống nhất cấu trúc module và API trước khi chia việc.
