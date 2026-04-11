# Kiến Trúc Đề Xuất: Hệ Thống Gợi Ý Thích Ứng Đa Tầng

## Vấn Đề Với Hệ Thống Hiện Tại

Hệ thống hiện tại sử dụng **lọc dựa trên nội dung cơ bản với độ tương đồng cosine** — cùng kỹ thuật được sử dụng cho gợi ý sản phẩm ("người mua X cũng mua Y"). Nó không có trí tuệ sư phạm: không theo dõi kiến thức, không hiệu chuẩn độ khó, không mô hình quên, không nhận biết tiền đề.

## Đề Xuất: Kiến Trúc Thích Ứng 5 Tầng

Mỗi tầng giải quyết một nhu cầu sư phạm khác nhau. Sự kết hợp này là mới và có thể công bố.

```
+------------------------------------------------------------------+
|  Tầng 5: Phản Hồi LLM (Nâng Cao Tùy Chọn)                       |
|  KG + RAG + LLM cho gợi ý, giải thích, phản hồi mã              |
+------------------------------------------------------------------+
|  Tầng 4: Lập Lịch Ôn Tập (FSRS)                                  |
|  Khi nào sinh viên nên ôn tập khái niệm đã học?                  |
+------------------------------------------------------------------+
|  Tầng 3: Chọn Bài Tập (MAB Phân Cấp)                             |
|  Khái niệm nào + độ khó nào để gợi ý tiếp?                      |
+------------------------------------------------------------------+
|  Tầng 2: Hiệu Chuẩn Độ Khó (Elo Giá Trị K Động)                 |
|  Sinh viên giỏi đến đâu? Mỗi bài khó thế nào?                   |
+------------------------------------------------------------------+
|  Tầng 1: Theo Dõi Kiến Thức (BKT hoặc DKT2)                      |
|  Sinh viên hiện tại biết gì theo từng khái niệm?                 |
+------------------------------------------------------------------+
|  Nền Tảng: Đồ Thị Tri Thức Các Khái Niệm Lập Trình              |
|  Mối quan hệ tiền đề giữa các khái niệm                         |
+------------------------------------------------------------------+
```

---

## Tầng 1: Theo Dõi Kiến Thức — "Sinh viên biết gì?"

**Kỹ thuật:** Theo Dõi Kiến Thức Bayesian (BKT) qua pyBKT, hoặc DKT2 cho tính mới cao hơn

**Chức năng:**
- Theo dõi xác suất thành thạo theo từng khái niệm (ví dụ: P(biết mảng) = 0,85, P(biết DP) = 0,30)
- Cập nhật sau mỗi lần nộp bài (đúng/sai)
- Mô hình hóa tốc độ học theo từng khái niệm cho từng sinh viên

**Tại sao tốt hơn hiện tại:**
- Hiện tại: nhị phân (đã giải hoặc chưa), chỉ có trọng số theo độ khó
- Đề xuất: ước lượng thành thạo xác suất theo từng khái niệm, cập nhật liên tục

**Triển khai:** pyBKT (đơn giản, có thể diễn giải) hoặc DKT2 (tiên tiến nhất, phức tạp hơn)

---

## Tầng 2: Hiệu Chuẩn Độ Khó — "Mỗi bài khó thế nào cho sinh viên này?"

**Kỹ thuật:** Xếp Hạng Elo Giá Trị K Động

**Chức năng:**
- Duy trì xếp hạng Elo cho mỗi sinh viên theo từng chiều khái niệm (Elo Đa Chiều)
- Duy trì xếp hạng Elo cho mỗi bài tập
- Giá trị K thích ứng: tăng khi sinh viên đang học nhanh, giảm khi ổn định
- Trực tiếp vận hành hóa Vùng Phát Triển Gần Nhất: gợi ý bài +100 đến +300 Elo so với sinh viên

**Tại sao tốt hơn hiện tại:**
- Hiện tại: hoàn toàn không có mô hình độ khó, chỉ có nhãn DỄ/TRUNG BÌNH/KHÓ
- Đề xuất: ước lượng độ khó liên tục, cá nhân hóa, thích ứng với tốc độ học

---

## Tầng 3: Chọn Bài Tập — "Nên cho sinh viên bài nào tiếp?"

**Kỹ thuật:** Bandit Đa Cánh Tay Phân Cấp

**Chức năng:**
- Cấp 1 (cánh tay khái niệm): Chọn khái niệm nào để luyện tập, cân bằng:
  - Khái niệm có mức thành thạo thấp (khai thác)
  - Khái niệm mới sinh viên chưa thử (khám phá)
  - Thứ tự tiền đề từ đồ thị tri thức
- Cấp 2 (cánh tay độ khó): Trong khái niệm đã chọn, chọn độ khó:
  - Sử dụng nhắm ZPD dựa trên Elo
  - Xem xét xu hướng thành thạo (đang tiến bộ → khó hơn, đang gặp khó → dễ hơn)

**Tại sao tốt hơn hiện tại:**
- Hiện tại: độ tương đồng cosine trả về bài "tương tự nhất" (hiệu ứng phòng vọng)
- Đề xuất: khám phá-khai thác thông minh với nhận biết tiền đề

---

## Tầng 4: Lập Lịch Ôn Tập — "Khi nào sinh viên nên ôn tập?"

**Kỹ thuật:** FSRS (Bộ Lập Lịch Lặp Lại Ngắt Quãng Tự Do)

**Chức năng:**
- Sau khi thành thạo một khái niệm, lên lịch bài ôn tập ở khoảng cách tối ưu
- Mô hình hóa đường cong quên theo từng sinh viên, từng khái niệm
- Tích hợp với Tầng 3: lựa chọn cánh tay MAB xem xét cả "học mới" và "cần ôn tập"

**Tại sao tốt hơn hiện tại:**
- Hiện tại: hoàn toàn không có cơ chế ôn tập. Khi đã giải, khái niệm "xong mãi mãi"
- Đề xuất: lập lịch ôn tập tối ưu khoa học, hiệu quả hơn 20-30% so với SM-2

---

## Tầng 5: Phản Hồi LLM (Nâng Cao)

**Kỹ thuật:** Đồ Thị Tri Thức + RAG + LLM

**Chức năng:**
- Khi sinh viên gặp khó, cung cấp gợi ý phân tầng (không đáp án trực tiếp)
- Phân tích mã nộp để xác định hiểu lầm cụ thể
- Tạo giải thích cá nhân hóa dựa trên lịch sử sinh viên
- Độ cụ thể gợi ý thích ứng: gợi ý mơ hồ trước, cụ thể hơn nếu vẫn gặp khó

**Tại sao tốt hơn hiện tại:**
- Hiện tại: không có hệ thống gợi ý hoặc phản hồi
- Đề xuất: đã chứng minh đạt tỷ lệ bài nộp đúng cao nhất (kết hợp > chỉ thích ứng > chỉ GenAI)

---

## Nền Tảng: Đồ Thị Tri Thức

**Bao gồm:**
- Các khái niệm lập trình là nút (mảng, bảng băm, cây, đồ thị, DP, v.v.)
- Cạnh tiền đề (có hướng): "mảng" → "bảng băm" → "mẫu hai tổng"
- Cạnh tương đồng (vô hướng): "BFS" ~ "DFS", "merge sort" ~ "quick sort"
- Bài tập liên kết với các khái niệm mà chúng kiểm tra

**Cách xây dựng:**
- Xây dựng thủ công ban đầu từ tag bài tập
- Nâng cao qua trích xuất tiền đề tự động dựa trên LLM (phương pháp ACE)
- Có thể tinh chỉnh theo thời gian từ dữ liệu hiệu suất sinh viên

---

## Luồng Dữ Liệu: Chu Trình Gợi Ý Hoàn Chỉnh

```
1. Sinh viên yêu cầu gợi ý
   |
2. Tầng 1 (KT): Tính mức thành thạo hiện tại theo từng khái niệm
   |-- P(mảng) = 0,92, P(đệ quy) = 0,75, P(DP) = 0,20, P(đồ thị) = 0,10
   |
3. Tầng 4 (FSRS): Kiểm tra khái niệm nào cần ôn tập
   |-- "đệ quy" luyện tập lần cuối 14 ngày trước, đến hạn ôn tập
   |
4. Tầng 3 (MAB): Quyết định: ôn tập đệ quy HAY học thứ mới?
   |-- Nếu ôn tập: chọn khái niệm đệ quy
   |-- Nếu mới: khám phá giữa DP (thành thạo thấp) và đồ thị (chưa thử)
   |
5. Tầng 2 (Elo): Chọn bài ở độ khó phù hợp
   |-- Elo đệ quy của sinh viên: 1350
   |-- Tìm bài với Elo độ khó: 1400-1600 (phạm vi ZPD)
   |
6. Trả về bài tập được gợi ý
   |
7. Sinh viên nộp lời giải
   |
8. Cập nhật tất cả các tầng:
   |-- Tầng 1: Cập nhật P(khái niệm) dựa trên thành công/thất bại
   |-- Tầng 2: Cập nhật Elo sinh viên và Elo bài tập
   |-- Tầng 4: Cập nhật mô hình trí nhớ FSRS cho khái niệm này
   |-- Tầng 3: Cập nhật tín hiệu phần thưởng MAB
```

---

## Đóng Góp Mới Của Khóa Luận

1. **Tích hợp đa tầng:** Không hệ thống nào hiện có kết hợp KT + Elo + MAB + FSRS trong kiến trúc thống nhất
2. **Elo giá trị K động cho lập trình:** Ứng dụng đầu tiên của K động vào lĩnh vực lập trình thi đấu
3. **MAB phân cấp với ràng buộc tiền đề:** Các cánh tay MAB được ràng buộc bởi tiền đề đồ thị tri thức
4. **FSRS cho duy trì kỹ năng lập trình:** Ứng dụng đầu tiên của FSRS cho duy trì kỹ năng lập trình (so với thẻ ghi nhớ)
5. **Phản hồi kết hợp thích ứng + LLM:** Kết hợp gợi ý thuật toán với gợi ý phân tầng sinh bởi LLM

---

## Ưu Tiên Triển Khai

| Ưu tiên | Tầng | Kỹ thuật | Độ khó | Tác động |
|---------|------|----------|--------|----------|
| 1 (bắt buộc) | Tầng 2 | Xếp hạng Elo | Thấp | Cao — cho phép ZPD |
| 2 (bắt buộc) | Tầng 1 | BKT (pyBKT) | Thấp-TB | Cao — cho phép theo dõi thành thạo |
| 3 (bắt buộc) | Tầng 3 | MAB Phân Cấp | Trung bình | Cao — logic gợi ý cốt lõi |
| 4 (nên có) | Nền tảng | Đồ Thị Tri Thức | Trung bình | Trung bình — cho phép tiền đề |
| 5 (nên có) | Tầng 4 | FSRS | Thấp | Trung bình — cho phép lập lịch ôn tập |
| 6 (tốt nếu có) | Tầng 5 | LLM + RAG | Cao | Trung bình — nâng cao, không cốt lõi |

---

## Tài Nguyên Mã Nguồn Mở

| Tài nguyên | URL | Mục đích |
|-----------|-----|----------|
| pyBKT | https://github.com/CAHLR/pyBKT | Theo Dõi Kiến Thức Bayesian |
| DKT2 | https://github.com/zyy-2001/DKT2 | Theo Dõi Kiến Thức Sâu |
| pyKT | https://github.com/pykt-team/pykt-toolkit | Bộ công cụ mô hình KT |
| MAB Phân Cấp | https://github.com/b-castleman/hierarchical-mab-tutoring | Gợi ý MAB |
| FSRS | https://github.com/open-spaced-repetition/free-spaced-repetition-scheduler | Lặp lại ngắt quãng |
| Elo-MMR | https://github.com/EbTech/Elo-MMR | Hệ thống xếp hạng |
