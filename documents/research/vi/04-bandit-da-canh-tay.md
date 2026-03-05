# Bandit Đa Cánh Tay Cho Giáo Dục: Hiện Trạng Nghiên Cứu (2024-2026)

Thuật toán MAB (Multi-Armed Bandit) giải quyết câu hỏi: **"Nên gợi ý những gì sinh viên cần (khai thác) hay khám phá chủ đề mới?"**

---

## 1. MAB Phân Cấp Cho Hệ Thống Dạy Học Thông Minh — Tháng 8/2024

**Bài báo:** "Hierarchical MAB for ITS" — Tháng 8/2024

**Mô tả:** MAB phân cấp mã nguồn mở hoạt động ở hai cấp độ:
1. **Cấp 1:** Chọn **khái niệm** nào để dạy (mảng, cây, đồ thị, DP)
2. **Cấp 2:** Chọn **độ khó** phù hợp trong khái niệm đó (dễ/trung bình/khó)

Sử dụng Theo Dõi Kiến Thức Bayesian (BKT) để ước lượng mức thành thạo và tích hợp suy giảm trí nhớ.

**Tại sao tốt hơn:** Không giống các phương pháp MAB phẳng, nó xử lý cấu trúc thực của nội dung giáo dục. Phiên bản thích ứng độ khó vượt trội đáng kể so với phiên bản không thích ứng độ khó. Được đánh giá với nhóm mô phỏng 500 sinh viên.

**Ứng dụng cho hệ thống:** Áp dụng trực tiếp.
- Cấp 1: Chọn khái niệm để luyện tập
- Cấp 2: Chọn độ khó trong khái niệm đó
- Cân bằng giữa khám phá khái niệm mới và củng cố điểm yếu
- Trong một khái niệm, khám phá xem sinh viên đã sẵn sàng cho bài khó hơn chưa

**Triển khai:** Mã nguồn mở đầy đủ tại https://github.com/b-castleman/hierarchical-mab-tutoring

**Tài liệu tham khảo:**
- arXiv: https://arxiv.org/abs/2408.07208
- OpenReview: https://openreview.net/forum?id=ag2m818qUm

---

## 2. MAB Với Bỏ Cuộc (MAB-A) — NeurIPS 2024

**Bài báo:** NeurIPS 2024

**Mô tả:** Mô hình MAB tính đến **sự bỏ cuộc của người dùng** — người dùng rời khỏi nền tảng nếu gợi ý quá nhàm chán hoặc quá khó. Các thuật toán ULCB và KL-ULCB tăng khám phá khi người dùng tương tác tốt, giảm khi không tương tác.

**Tại sao tốt hơn:** MAB truyền thống tối ưu hóa cho học tập nhưng bỏ qua sự tương tác. Nếu sinh viên cảm thấy thất vọng hoặc chán, họ ngừng sử dụng nền tảng hoàn toàn. MAB-A mô hình hóa điều này một cách rõ ràng.

**Ứng dụng cho hệ thống:** Giám sát xem sinh viên hoàn thành hay bỏ các bài tập được gợi ý:
- Sinh viên bỏ cuộc → chuyển hướng về vùng thoải mái (khai thác)
- Sinh viên hoàn thành → tăng khám phá chủ đề mới/khó hơn

**Tài liệu tham khảo:**
- NeurIPS 2024: https://neurips.cc/virtual/2024/poster/98312
- JMLR: https://jmlr.org/papers/v25/22-1251.html
