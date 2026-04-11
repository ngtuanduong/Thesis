# Phân Tích Hệ Thống Gợi Ý Hiện Tại

## Tổng Quan Kiến Trúc

Hệ thống hiện tại sử dụng phương pháp **Lọc Dựa Trên Nội Dung (Content-Based Filtering)** với **nhúng Sentence Transformer** và **độ tương đồng cosine qua pgvector**.

```
Người dùng giải bài tập
    -> Các tag được trích xuất từ bài đã giải (ví dụ: "array", "hash-table")
    -> Mỗi tag được nhúng qua all-MiniLM-L6-v2 (vector 384 chiều)
    -> Có trọng số theo độ khó (DỄ=1, TRUNG BÌNH=2, KHÓ=3)
    -> Chuẩn hóa về khoảng 0-1
    -> Tất cả vector kỹ năng được lấy trung bình thành một vector hồ sơ duy nhất
    -> Tính độ tương đồng cosine với vector nhúng của bài tập
    -> Trả về Top-N bài tập chưa giải có độ tương đồng cao nhất
```

## Kỹ Thuật Được Sử Dụng

| Khía cạnh | Phương pháp hiện tại |
|-----------|---------------------|
| Mô hình nhúng | all-MiniLM-L6-v2 (Sentence Transformers) |
| Số chiều vector | 384 |
| Độ đo tương đồng | Khoảng cách cosine (toán tử `<=>` của pgvector) |
| Biểu diễn người dùng | Trung bình các vector nhúng tag kỹ năng |
| Biểu diễn bài tập | Nhúng `tiêu đề + mô tả + tag` |
| Tính điểm kỹ năng | Tổng có trọng số theo độ khó, chuẩn hóa theo giá trị lớn nhất |
| Khởi động lạnh | Dự phòng: bài tập mới nhất chưa giải |

## Các Điểm Yếu Nghiêm Trọng

### 1. Không Có Theo Dõi Kiến Thức (Knowledge Tracing)
Hệ thống không mô hình hóa những gì sinh viên **thực sự biết**. Nó chỉ theo dõi các tag mà sinh viên đã giải bài. Giải một bài DỄ về "mảng" cho cùng tín hiệu với việc thành thạo hoàn toàn về mảng.

### 2. Không Có Hiệu Chuẩn Độ Khó
Không có cơ chế đánh giá liệu một bài tập quá dễ hay quá khó cho một sinh viên cụ thể. Hệ thống gợi ý bài **tương tự** với những gì bạn đã làm, chứ không phải bài ở **mức độ khó phù hợp** để học tập.

### 3. Không Có Vùng Phát Triển Gần Nhất (ZPD)
Hệ thống gợi ý các bài tập tương đồng nhất với hồ sơ người dùng. Điều này có nghĩa là nó gợi ý thêm những gì bạn đã biết, thay vì các bài tập đẩy bạn vào vùng học tập phát triển.

### 4. Không Có Mô Hình Quên
Nếu sinh viên học "đệ quy" 3 tháng trước nhưng không luyện tập kể từ đó, hệ thống vẫn coi kỹ năng đó đã thành thạo. Không có sự suy giảm hay lặp lại ngắt quãng.

### 5. Tổng Hợp Kỹ Năng Thô Sơ
Lấy trung bình tất cả vector nhúng kỹ năng thành một vector duy nhất sẽ mất thông tin về mức độ kỹ năng riêng lẻ. Một sinh viên yếu về "đồ thị" nhưng giỏi về "mảng" sẽ có vector hỗn hợp không thể hiện chính xác cả hai.

### 6. Không Cân Bằng Khám Phá - Khai Thác
Hệ thống luôn khai thác (gợi ý tương tự nhất). Không bao giờ khám phá xem sinh viên có thể hưởng lợi từ một chủ đề hoàn toàn mới mà họ chưa thử hay không.

### 7. Không Nhận Biết Tiền Đề
Hệ thống không biết rằng "quy hoạch động" yêu cầu hiểu "đệ quy" trước. Nó có thể gợi ý bài DP cho sinh viên chưa thành thạo đệ quy.

### 8. Chỉ Có Kết Quả Nhị Phân
Hệ thống chỉ sử dụng CHẤP NHẬN/không-CHẤP NHẬN. Không xem xét:
- Bao nhiêu lần thử trước khi thành công
- Sinh viên mất bao lâu
- Những lỗi nào họ mắc phải
- Liệu họ có cần gợi ý không

## Kết Luận

Phương pháp hiện tại là một **hệ thống gợi ý dựa trên nội dung cơ bản** — cùng kỹ thuật được sử dụng trong các hệ thống gợi ý sản phẩm đơn giản (ví dụ: "người mua X cũng mua Y"). Nó **không phù hợp cho gợi ý giáo dục** vì thiếu trí tuệ sư phạm. Nó không mô hình hóa việc học, quên, độ khó, hay mối quan hệ tiền đề.

Đối với một khóa luận, phương pháp này được coi là **lỗi thời và thiếu tính mới**. Cộng đồng khai phá dữ liệu giáo dục đã vượt qua lọc dựa trên nội dung từ nhiều năm trước.
