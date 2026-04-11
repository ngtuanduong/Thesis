# Xếp Hạng Elo & Lý Thuyết Phản Hồi Câu Hỏi: Hiện Trạng Nghiên Cứu (2024-2026)

Elo/IRT giải quyết câu hỏi: **"Làm sao hiệu chuẩn kỹ năng sinh viên VÀ độ khó bài tập đồng thời?"**

---

## 1. Xếp Hạng Elo Với Giá Trị K Động — Tháng 12/2025

**Bài báo:** Springer, Tháng 12/2025

**Mô tả:** Cải tiến mới cho Elo, tự động điều chỉnh tham số nhạy cảm K dựa trên xu hướng quan sát được. Khi thay đổi xếp hạng cho thấy xu hướng tăng/giảm nhất quán (sinh viên đang học hoặc gặp khó khăn), K tăng. Ngược lại, K giảm để ổn định.

**Tại sao tốt hơn:** Elo K cố định truyền thống buộc phải đánh đổi:
- K lớn → theo dõi học nhanh nhưng không ổn định
- K nhỏ → ổn định nhưng phản ứng chậm

K động thích ứng với tốc độ học của cá nhân. Được xác nhận trên nền tảng Math Garden.

**Ứng dụng cho hệ thống:** Xếp hạng cả sinh viên VÀ bài tập bằng Elo. Khi sinh viên tiến bộ nhanh trong "thuật toán đồ thị", K động phát hiện xu hướng tăng, tăng độ nhạy, và nhanh chóng ghép họ với bài đồ thị khó hơn. Khi tiến bộ ổn định, K giảm cho xếp hạng trạng thái ổn định chính xác.

**Tài liệu tham khảo:**
- Springer: https://link.springer.com/article/10.1007/s11257-025-09439-z

---

## 2. Xếp Hạng Elo Cho Bài Tập Lập Trình — Đã Chứng Minh

**Bài báo:** ACM TOCE

**Mô tả:** Áp dụng Elo để đồng thời ước lượng kỹ năng người học và độ khó bài tập. Mỗi lần tương tác cập nhật cả hai xếp hạng.

**Tại sao tốt hơn:** Chi phí tính toán thấp, đơn giản, hoạt động với kích thước mẫu nhỏ (khác với IRT cần bộ dữ liệu hiệu chuẩn lớn), tự nhiên xử lý thay đổi kỹ năng theo thời gian. Được kiểm nghiệm trên 76 bài tập, 299 người dùng, 50.055 lần thử, hơn 300.000 unit test.

**Ứng dụng cho hệ thống:** Áp dụng trực tiếp. Mỗi lần thử cập nhật cả hai xếp hạng. Gợi ý bài tập có độ khó cao hơn một chút so với xếp hạng kỹ năng sinh viên (Vùng Phát Triển Gần Nhất).

**Tài liệu tham khảo:**
- ACM TOCE: https://dl.acm.org/doi/10.1145/3511886

---

## 3. Elo Đa Chiều — EDM 2025

**Mô tả:** Theo dõi mức thành thạo chuyên biệt theo khái niệm của sinh viên và độ khó câu hỏi sử dụng Elo đa biến. Vượt trội hơn hồi quy logistic với hiệu suất khởi động lạnh được cải thiện.

**Ứng dụng cho hệ thống:** Thay vì một Elo cho mỗi sinh viên, duy trì xếp hạng riêng cho từng khái niệm (mảng, cây, DP, v.v.). Cho phép gợi ý có mục tiêu.

**Tài liệu tham khảo:**
- EDM 2025: https://educationaldatamining.org/EDM2025/proceedings/2025.EDM.long-papers.99/index.html

---

## 4. Hệ Thống Xếp Hạng Trên Các Nền Tảng Thực Tế

| Nền tảng | Hệ thống | Chi tiết |
|----------|----------|----------|
| Codeforces | Elo tổng quát (nhiều người chơi) | Xếp hạng sinh viên + bài tập đồng thời |
| CodeChef/DMOJ | Elo-MMR (Bayesian) | Tương thích khuyến khích, thời gian tuyến tính, bền vững |
| Math Garden | Elo giá trị K động | Thời gian thực với tích hợp thời gian phản hồi |

**Triển khai Elo-MMR:** https://github.com/EbTech/Elo-MMR

---

## Vùng Phát Triển Gần Nhất (ZPD)

ZPD xác định ba vùng:
- **Có thể tự làm:** Quá dễ, học tập hạn chế
- **ZPD (điểm tối ưu):** Có thể giải với một số hỗ trợ — học tập tối đa
- **Không thể làm kể cả có trợ giúp:** Quá khó, gây thất vọng, không học được

**Vận hành hóa ZPD:** Sử dụng xếp hạng Elo, ZPD = bài tập có độ khó từ +100 đến +300 điểm Elo so với kỹ năng hiện tại của sinh viên. Elo giá trị K động đặc biệt phù hợp vì nó thích ứng với tốc độ học.

**Tài liệu tham khảo:**
- Springer: https://link.springer.com/chapter/10.1007/3-540-47987-2_75
- NWEA 2025: https://www.nwea.org/blog/2025/the-zone-of-proximal-development-zpd-the-power-of-just-right/
