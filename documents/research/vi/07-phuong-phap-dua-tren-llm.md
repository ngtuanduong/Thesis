# Phương Pháp Dựa Trên LLM: Hiện Trạng Nghiên Cứu (2024-2026)

Các phương pháp LLM giải quyết câu hỏi: **"Mô hình ngôn ngữ lớn có thể nâng cao học tập thích ứng như thế nào?"**

---

## 1. Đồ Thị Tri Thức + RAG + LLM Cho Giáo Dục Lập Trình — 2025

**Bài báo:** ScienceDirect, 2025

**Mô tả:** Khung tích hợp LLM với Sinh Tăng Cường Truy Xuất (RAG) tận dụng đồ thị tri thức và lịch sử tương tác người dùng. Đánh giá mã người học, tạo phản hồi hình thành, và gợi ý bài tập. Được kiểm nghiệm trong ba chế độ: chỉ thích ứng, chỉ GenAI, kết hợp.

**Tại sao tốt hơn:** Chế độ **kết hợp GenAI-thích ứng** đạt được:
- Số lượng bài nộp đúng cao nhất
- Ít lần thử sai/không hoàn thành nhất
- Vượt trội hơn cả chế độ chỉ thích ứng VÀ chỉ GenAI
- Được kiểm nghiệm trên 4.956 bài nộp mã

**Ứng dụng cho hệ thống:** Sử dụng KG để cấu trúc các khái niệm lập trình. Sử dụng RAG để truy xuất ngữ cảnh bài tập liên quan và lịch sử sinh viên. Sử dụng LLM để tạo phản hồi cá nhân hóa và gợi ý bài tập tiếp theo dựa trên các điểm yếu đã xác định.

**Tài liệu tham khảo:**
- ScienceDirect: https://www.sciencedirect.com/science/article/pii/S2666920X25001663

---

## 2. PyTutor (Hệ Thống Dạy Học Thông Minh Dựa Trên ChatGPT) — 2024

**Bài báo:** ScienceDirect, 2024

**Mô tả:** Hệ thống dạy học thông minh cho Python sử dụng ChatGPT để hướng dẫn liên tục, gợi ý giải bài, và giải thích mã.

**Tại sao tốt hơn:** Tương tác cao hơn, tỷ lệ hoàn thành cao hơn, và tỷ lệ thành công cao hơn — đặc biệt hiệu quả cho sinh viên yếu hơn. Đổi mới chính: gợi ý kiểu Socratic "nhắc nhở" và độ cụ thể gợi ý thích ứng.

**Ứng dụng cho hệ thống:** Khi sinh viên gặp khó khăn với bài tập được gợi ý, sử dụng LLM cho gợi ý phân tầng điều chỉnh độ cụ thể dựa trên số lần họ đã xin trợ giúp.

**Tài liệu tham khảo:**
- ScienceDirect: https://www.sciencedirect.com/science/article/pii/S2666920X24001127

---

## 3. Đồ Thị Tri Thức Đa Phương Thức + RAG ITS — 2026

**Bài báo:** Frontiers in Computer Science, 2026

**Mô tả:** ITS dựa trên xây dựng tự động đồ thị tri thức đa phương thức và sinh tăng cường truy xuất.

**Ứng dụng cho hệ thống:** Tự động xây dựng KG từ tài liệu khóa học lập trình và sử dụng RAG cho dạy học và gợi ý phù hợp với ngữ cảnh.

**Tài liệu tham khảo:**
- Frontiers: https://www.frontiersin.org/journals/computer-science/articles/10.3389/fcomp.2026.1777749/full
