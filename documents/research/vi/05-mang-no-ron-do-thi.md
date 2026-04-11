# Mạng Nơ-ron Đồ Thị & Đồ Thị Tri Thức: Hiện Trạng Nghiên Cứu (2024-2026)

Các phương pháp GNN/KG giải quyết câu hỏi: **"Các khái niệm lập trình liên quan với nhau như thế nào, và làm sao tận dụng cấu trúc đó?"**

---

## 1. Gợi Ý Tài Nguyên Giáo Dục Dựa Trên GNN — 2025

**Mô tả:** Sử dụng GNN để mô hình hóa mối quan hệ ba bên giữa sinh viên, tài nguyên học tập và điểm kiến thức. Đạt NDCG@10 là 0,93 trong kịch bản tiêu chuẩn và 0,88 trong kịch bản lỗ hổng kiến thức.

**Tại sao tốt hơn:** Các hệ thống truyền thống xử lý các mục độc lập. GNN mô hình hóa mối quan hệ cấu trúc (tiền đề, tương đồng) giữa các khái niệm và giữa các sinh viên. Nhận thức cấu trúc này dẫn đến gợi ý tốt hơn.

**Ứng dụng cho hệ thống:** Xây dựng đồ thị tri thức:
- Nút = khái niệm lập trình + bài tập + sinh viên
- Cạnh = quan hệ tiền đề, liên kết khái niệm-bài tập, tương tác sinh viên-bài tập
- GNN lan truyền thông tin qua đồ thị này để lấp đầy lỗ hổng kiến thức

**Tài liệu tham khảo:**
- Liu, 2025: https://journals.sagepub.com/doi/10.1177/14727978251374326
- Khảo sát GNN Gợi ý: https://dl.acm.org/doi/10.1145/3694784

---

## 2. Chú Ý Đồ Thị + Học Tăng Cường Sâu Cho Lộ Trình Học Tập — 2025

**Mô tả:** Kết hợp Mạng Chú Ý Đồ Thị (GAT) với RL Actor-Critic để tạo lộ trình học tập cá nhân hóa. GAT gán trọng số quan trọng cho các kết nối khái niệm, RL học trình tự tối ưu.

**Tại sao tốt hơn:** Điểm sinh viên cải thiện **5,8 và 12,8 điểm**, độ chính xác cải thiện **5,3%** so với các mô hình học sâu trước đó. Cơ chế chú ý đồ thị tự động cân nhắc tiền đề nào quan trọng nhất cho từng sinh viên.

**Ứng dụng cho hệ thống:** Mô hình hóa chương trình lập trình dưới dạng đồ thị có hướng. Tác tử RL điều hướng đồ thị, quyết định trình tự khái niệm tối ưu cho từng sinh viên. Ví dụ: Sinh viên A hưởng lợi từ "bảng băm" trước "hai con trỏ", trong khi Sinh viên B sẵn sàng cho "đồ thị" trực tiếp.

**Tài liệu tham khảo:**
- Gu, 2025: https://journals.sagepub.com/doi/10.1177/14727978241313260
- KG+DRL: https://www.nature.com/articles/s41598-025-17918-x

---

## 3. GNN Nhận Biết Danh Mục Tăng Cường Tiền Đề — 2024

**Mô tả:** Mô hình GNN học các quan hệ tiền đề giữa các khái niệm và sử dụng chúng cho gợi ý. Sử dụng cả thông tin danh mục và cấu trúc tiền đề.

**Ứng dụng cho hệ thống:** Mô hình hóa trực tiếp "mảng trước bảng băm" và "đệ quy trước duyệt cây". GNN sử dụng cạnh tiền đề để tránh gợi ý bài tập sinh viên chưa sẵn sàng.

**Tài liệu tham khảo:**
- ACM TKDD: https://dl.acm.org/doi/10.1145/3643644

---

## 4. Xây Dựng Đồ Thị Tri Thức Giáo Dục Hỗ Trợ AI (ACE) — 2024

**Mô tả:** Phương pháp luận để tự động xây dựng Đồ Thị Tri Thức Giáo Dục với các quan hệ tiền đề sử dụng AI.

**Ứng dụng cho hệ thống:** Tự động tạo đồ thị tri thức khái niệm lập trình từ sách giáo khoa, đề cương, hoặc mô tả bài tập — thay vì xây dựng thủ công.

**Tài liệu tham khảo:**
- JEDM: https://jedm.educationaldatamining.org/index.php/JEDM/article/view/737
