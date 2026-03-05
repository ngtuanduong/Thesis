# Theo Dõi Kiến Thức: Hiện Trạng Nghiên Cứu (2024-2026)

Theo dõi kiến thức (Knowledge Tracing - KT) là xương sống của mọi hệ thống học tập thích ứng. Nó trả lời câu hỏi: **"Sinh viên hiện tại biết gì?"**

---

## 1. DKT2 (Theo Dõi Kiến Thức Sâu dựa trên xLSTM) — Tháng 1/2025

**Bài báo:** "From Deep Knowledge Tracing to DKT2" — ECML-PKDD 2025

**Mô tả:** Thế hệ tiếp theo của theo dõi kiến thức thay thế LSTM bằng xLSTM (LSTM Mở rộng). Sử dụng mô hình Rasch cho nhúng đầu vào và Lý thuyết Phản hồi Câu hỏi (IRT) cho phân tách đầu ra có thể diễn giải, chia kiến thức đã học thành thành phần "quen thuộc" và "chưa quen thuộc".

**Tại sao tốt hơn:** Liên tục vượt trội hơn 18 mô hình cơ sở (bao gồm DKT, AKT, SAINT, SAKT) trên ba bộ dữ liệu quy mô lớn trong dự đoán một bước, nhiều bước và độ dài lịch sử thay đổi.

**Đổi mới chính:** xLSTM giới thiệu:
- sLSTM: kích hoạt hàm mũ cho quyết định lưu trữ tốt hơn
- mLSTM: bộ nhớ ma trận cho dung lượng lưu trữ tăng với khả năng song song hóa hoàn toàn

**Ứng dụng cho hệ thống:** Theo dõi các khái niệm lập trình nào (vòng lặp, đệ quy, DP, v.v.) sinh viên đã thành thạo. Đầu ra dựa trên IRT phân tách mức độ thành thạo thành "khái niệm sinh viên thoải mái" và "khái niệm họ gặp khó khăn".

**Triển khai:** Mã nguồn mở tại https://github.com/zyy-2001/DKT2

**Tài liệu tham khảo:**
- arXiv: https://arxiv.org/abs/2501.14256
- ECML-PKDD 2025: https://link.springer.com/chapter/10.1007/978-3-032-06109-6_14

---

## 2. srcML-DKT (Theo Dõi Kiến Thức Chuyên Biệt Cho Mã Nguồn) — EDM 2025

**Bài báo:** "srcML-DKT" — Educational Data Mining 2025

**Mô tả:** Mở rộng của Code-DKT sử dụng biểu diễn mã nguồn dựa trên srcML thay vì dựa trên AST. Được thiết kế đặc biệt cho giáo dục lập trình, trích xuất đặc trưng trực tiếp từ mã sinh viên nộp — bao gồm cả mã không biên dịch được.

**Tại sao tốt hơn:** Code-DKT dựa vào AST, chỉ hoạt động với mã có thể phân tích cú pháp. Trong lập trình nhập môn, nhiều bài nộp không thể phân tích cú pháp. srcML biểu diễn cả mã không biên dịch được dưới định dạng XML. Được kiểm nghiệm trên N=610 sinh viên.

**Ứng dụng cho hệ thống:** Áp dụng trực tiếp — theo dõi kiến thức bằng cách phân tích mã nguồn thực tế sinh viên viết, không chỉ câu trả lời đúng/sai. Có thể xác định các mẫu cú pháp và ngữ nghĩa cụ thể để hiểu khái niệm nào sinh viên gặp khó khăn.

**Tài liệu tham khảo:**
- EDM 2025: https://educationaldatamining.org/EDM2025/proceedings/2025.EDM.short-papers.83/index.html

---

## 3. UKT (Theo Dõi Kiến Thức Nhận Biết Độ Không Chắc Chắn) — AAAI 2025

**Bài báo:** "UKT" — AAAI 2025

**Mô tả:** Biểu diễn trạng thái kiến thức sinh viên dưới dạng **phân phối xác suất** thay vì ước lượng điểm. Sử dụng cơ chế tự chú ý Wasserstein cho chuyển đổi trạng thái học tập và học tương phản nhận biết độ không chắc chắn.

**Tại sao tốt hơn:** KT truyền thống cho một điểm tin cậy duy nhất. UKT nắm bắt độ không chắc chắn — "70% tin cậy với độ không chắc chắn CAO" rất khác với "70% tin cậy với độ không chắc chắn THẤP". Điều này ảnh hưởng trực tiếp đến chất lượng gợi ý:
- Độ không chắc chắn cao → gợi ý bài **chẩn đoán** để xác định mức thành thạo thực
- Độ không chắc chắn thấp + thành thạo cao → chuyển sang chủ đề khó hơn
- Độ không chắc chắn thấp + thành thạo thấp → luyện tập có mục tiêu

**Ứng dụng cho hệ thống:** Sử dụng độ không chắc chắn để quyết định giữa bài chẩn đoán và bài nâng cao. Khi không chắc sinh viên biết "đồ thị", cho họ bài chẩn đoán về đồ thị trước.

**Tài liệu tham khảo:**
- arXiv: https://arxiv.org/abs/2501.05415
- AAAI 2025: https://ojs.aaai.org/index.php/AAAI/article/view/35007

---

## 4. LefoKT (Theo Dõi Kiến Thức Học Tập và Quên) — 2025

**Mô tả:** Tách rời các mẫu quên khỏi mức độ liên quan của bài tập thông qua "cơ chế chú ý quên tương đối". Được thiết kế đặc biệt để mô hình hóa hành vi quên đa dạng trong chuỗi tương tác ngày càng dài.

**Tại sao tốt hơn:** Các mô hình KT dựa trên cơ chế chú ý trước đây nhầm lẫn giữa "bài tập nào liên quan" và "kiến thức suy giảm nhanh thế nào". LefoKT tách riêng hai yếu tố này, cho khả năng ngoại suy độ dài tốt hơn — quan trọng cho theo dõi học tập trong cả học kỳ.

**Ứng dụng cho hệ thống:** Kết hợp với lặp lại ngắt quãng. Nếu sinh viên học tìm kiếm nhị phân 3 tuần trước nhưng chưa luyện tập, LefoKT có thể ước tính mức độ họ đã quên.

**Tài liệu tham khảo:**
- pyKT: https://pykt.org/lefokt

---

## 5. HCGKT (Theo Dõi Kiến Thức Đồ Thị Tương Phản Phân Cấp) — 2025

**Mô tả:** Tích hợp cơ chế chú ý lọc đồ thị phân cấp với học tương phản đối kháng và GCN để mô hình hóa các mối quan hệ dữ liệu giáo dục.

**Tại sao tốt hơn:** Nắm bắt mối quan hệ phân cấp giữa các khái niệm kiến thức một cách tự nhiên thông qua cấu trúc đồ thị (ví dụ: "vòng lặp" → "đệ quy" → "quy hoạch động").

**Ứng dụng cho hệ thống:** Mô hình hóa đồ thị tiền đề của các khái niệm lập trình, sau đó sử dụng HCGKT để theo dõi kiến thức trong khi tôn trọng bản chất phân cấp của kiến thức lập trình.

**Tài liệu tham khảo:**
- Springer: https://link.springer.com/chapter/10.1007/978-3-031-98420-4_20

---

## Bộ Công Cụ Triển Khai

| Bộ công cụ | URL | Mô tả |
|-----------|-----|-------|
| pyKT | https://github.com/pykt-team/pykt-toolkit | PyTorch, 10+ mô hình DLKT, tiền xử lý chuẩn hóa |
| pyBKT | https://github.com/CAHLR/pyBKT | KT Bayesian, API scikit-learn, tăng tốc C++ |
