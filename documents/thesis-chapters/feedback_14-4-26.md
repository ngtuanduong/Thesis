Có vài vấn đề em cân nhắc nhé:

1. Abstract đang nói quá tay so với phần em chứng minh được.
Em viết như thể hệ thống đã được thiết kế, triển khai và đánh giá rất đầy đủ, nhưng phần evaluation hiện chưa đủ mạnh để đỡ các claim đó. Nếu kết quả thực nghiệm chưa thật sự complete, phải hạ giọng xuống “pilot evaluation” hoặc “preliminary evaluation”. Ví dụ Abstract nói rất mạnh về architecture, experiment, metrics, contribution; nhưng nếu sang Chapter 5 mà chủ yếu vẫn là design thí nghiệm, chưa có bảng kết quả rõ ràng, thì người đọc sẽ thấy lệch giữa lời hứa và bằng chứng.

2. Em đang ôm quá nhiều đóng góp trong một khóa luận đại học.
BKT, Dynamic Elo, H-MAB, FSRS, knowledge graph, LLM hints, sandbox, full-stack, experiment — mỗi cái đã là một phần lớn. Hội đồng sẽ hỏi: “Đóng góp chính xác của em là gì?” Nếu em trả lời quá nhiều ý, bài sẽ loãng.

Cách sửa: chốt lại 2 ý chính thôi:

xây dựng một nền tảng adaptive learning tích hợp nhiều cơ chế
đánh giá pilot ban đầu trên sinh viên
LLM nên hạ xuống phần bổ sung, không nên để thành trục chính.

3. Objectives, RQ và Contributions chưa khớp nhau hoàn toàn.
Hiện em viết RQ2 hỏi hiệu quả của H-MAB, RQ3 hỏi hiệu quả của FSRS, nhưng thiết kế thực nghiệm lại thay đổi nhiều thành phần cùng lúc. Như vậy em không thể kết luận riêng từng thành phần mạnh như đang viết.

Ví dụ dễ thấy: nếu nhóm thực nghiệm bật cả adaptive system, còn control tắt adaptive features, thì kết quả tốt hơn chưa chắc là do riêng H-MAB hay riêng FSRS. Chỗ này phải viết trung thực hơn.

4. Chapter 5 là phần cần sửa mạnh nhất.
Hiện cảm giác giống “kế hoạch đánh giá” hơn là “kết quả nghiên cứu”.
Người chấm cần thấy ngay các thứ sau:

có bao nhiêu sinh viên tham gia thực tế
mỗi nhóm bao nhiêu người
pre-test/post-test ra sao
bảng kết quả chính
biểu đồ hoặc số liệu so sánh
kết luận cho từng RQ

Nói thẳng: nếu Chapter 5 chưa có số liệu thật, thì phải đổi tên chương và đổi giọng viết. Không được viết như thể đã chứng minh xong.

5. Có chỗ em dùng ngôn ngữ kiểu “marketing học thuật”.
Các cụm như “first integrated”, “fully unified”, “novel contribution”, “addresses the gap” xuất hiện dày sẽ làm bài nghe mạnh miệng hơn dữ liệu em có.

Cách sửa: thay bằng kiểu viết an toàn hơn:

“this thesis proposes…”
“preliminary evidence suggests…”
“within the scope of this pilot study…”
Viết như vậy trưởng thành hơn và khó bị bắt bẻ hơn.

6. Introduction và literature review bị dài và lặp ý.
Nhiều luận điểm lặp lại: programming khó, lớp học đông, cần cá nhân hóa, platform hiện tại chưa adaptive. Nói 1–2 lần là đủ. Lặp quá nhiều làm người đọc mệt và có cảm giác kéo dài để tạo độ hoành tráng.

Cách sửa: cắt bớt 15–20% phần mô tả lặp, giữ lại ý nào thật sự phục vụ research gap.

7. LLM đang được đưa vào hơi nhiều so với vai trò thực tế.
Trong thesis em nói Layer 5 là optional, nhưng cách viết vẫn làm nó trông như một đóng góp lớn. Đây là điểm dễ bị hỏi xoáy vì LLM kéo theo chuyện hallucination, đánh giá hint, chi phí, độ tin cậy.

Cách sửa: giữ LLM ở mức “optional extension” hoặc “future enhancement”. Đừng để nó làm loãng contribution chính.

8. Phần hình thức đang có lỗi rất dễ mất điểm.
Ngay đầu thesis vẫn còn “Declaration of Originality (Pending)” và “Acknowledgements (Pending)”. Đây là lỗi rất cơ bản, nhìn vào là thấy bản chưa hoàn thiện.

Yêu cầu: xóa toàn bộ dấu vết “Pending”, rà lại numbering, caption, tense, thuật ngữ, và bảo đảm hình/bảng nào đưa vào cũng được phân tích trong nội dung.

9. Em cần thêm một mục ‘Threats to Validity’.
Đây là chỗ giúp bài trông chững hơn.

Em nên tự nói thẳng các hạn chế sau:

sample nhỏ
chỉ ở một trường
thời gian can thiệp ngắn
nhiều thành phần thay đổi cùng lúc
một số metric phụ thuộc vào chính mô hình của hệ thống
Viết ra không làm bài yếu đi, ngược lại làm bài đáng tin hơn.

10. Thứ tự sửa ưu tiên như sau:

sửa Chapter 5 trước
rồi sửa Abstract/Introduction cho khớp với bằng chứng thực có
rồi chỉnh RQ/Contributions cho logic
cuối cùng mới rút gọn văn phong và rà lỗi trình bày

Tóm lại: bài này không yếu, nhưng đang bị “tham”. Em không cần chứng minh mọi thứ. Em chỉ cần làm rõ: em đã xây được gì, đánh giá được gì thật, và giới hạn của kết quả nằm ở đâu.