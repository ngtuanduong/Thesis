# Lặp Lại Ngắt Quãng: Hiện Trạng Nghiên Cứu (2024-2026)

Lặp lại ngắt quãng (Spaced Repetition) giải quyết câu hỏi: **"Khi nào sinh viên nên ôn tập một khái niệm đã học?"**

---

## 1. FSRS (Bộ Lập Lịch Lặp Lại Ngắt Quãng Tự Do) — Tiêu Chuẩn Hiện Đại

**Mô tả:** Thuật toán lặp lại ngắt quãng dựa trên học máy, mã nguồn mở. Mô hình hóa trí nhớ với ba biến số:
- **Độ khó (Difficulty):** Khái niệm này khó đến mức nào đối với sinh viên?
- **Độ ổn định (Stability):** Bao lâu trước khi xác suất nhớ lại giảm đáng kể?
- **Khả năng truy xuất (Retrievability):** Xác suất nhớ lại hiện tại là bao nhiêu?

**Tại sao tốt hơn:** Đạt được **ít hơn 20-30% số lần ôn tập** cho cùng mức độ ghi nhớ so với SM-2 (thuật toán được Anki sử dụng hàng thập kỷ). Hiện đã được tích hợp vào Anki (từ v23.10) và RemNote. Không giống SM-2 với khoảng cách cố định, FSRS học các mẫu trí nhớ cá nhân.

**Ứng dụng cho hệ thống:** Sau khi sinh viên giải một bài về "hai con trỏ", FSRS dự đoán khi nào họ bắt đầu quên và lên lịch bài ôn tập vào thời điểm tối ưu. Ngăn chặn mẫu phổ biến: học → bỏ qua → quên hoàn toàn.

**Triển khai:**
- Gói Python: `pip install fsrs`
- GitHub: https://github.com/open-spaced-repetition/free-spaced-repetition-scheduler
- Wiki: https://github.com/open-spaced-repetition/fsrs4anki/wiki

---

## 2. LECTOR (Lặp Lại Hướng Kiểm Tra Dựa Trên Khái Niệm Tăng Cường LLM) — Tháng 8/2025

**Bài báo:** "LECTOR" — Tháng 8/2025

**Mô tả:** Kết hợp LLM với lặp lại ngắt quãng. Sử dụng Học Trong Ngữ Cảnh (ICL) để đánh giá độ tương đồng ngữ nghĩa giữa các khái niệm, xác định các mục "dễ nhầm lẫn" cần được củng cố cùng nhau.

**Tại sao tốt hơn:** Đạt **tỷ lệ thành công 90,2%** so với 88,4% của phương pháp cơ sở tốt nhất (SSP-MMC) trên 100 người học mô phỏng trong 100 ngày. Đổi mới chính: giải quyết **nhầm lẫn ngữ nghĩa** — các khái niệm tương tự mà người học hay nhầm lẫn.

**Ứng dụng cho hệ thống:** Lập trình có nhiều khái niệm dễ nhầm lẫn:
- BFS và DFS
- Thao tác Stack và Queue
- Merge Sort và Quick Sort
- Phương pháp lặp và đệ quy

LECTOR xác định khi sinh viên nhầm lẫn các thuật toán tương tự và lên lịch luyện tập có mục tiêu buộc phân biệt giữa chúng.

**Tài liệu tham khảo:**
- arXiv: https://arxiv.org/abs/2508.03275
- OpenReview: https://openreview.net/forum?id=wprP6MbBYd
