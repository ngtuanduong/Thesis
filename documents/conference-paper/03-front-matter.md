# Front Matter

<!-- TITLE_VI_BEGIN -->
NỀN TẢNG HỌC TẬP THÍCH ỨNG CHO CÁC MÔN LẬP TRÌNH BẬC ĐẠI HỌC: TÍCH HỢP TRUY VẾT TRI THỨC BAYES, XẾP HẠNG ELO, BANDIT ĐA CÁNH TAY VÀ LỊCH LẶP LẠI CÁCH QUÃNG FSRS
<!-- TITLE_VI_END -->

<!-- TITLE_EN_BEGIN -->
AN ADAPTIVE LEARNING PLATFORM FOR UNIVERSITY PROGRAMMING COURSES: INTEGRATING BAYESIAN KNOWLEDGE TRACING, ELO RATING, MULTI-ARMED BANDITS, AND FSRS
<!-- TITLE_EN_END -->

<!-- AUTHORS_BEGIN -->
Nguyễn Tuấn Dương
Lớp 1C22, Khoa Công Nghệ Thông Tin
Email: ntduongvbhp@gmail.com

Giáo viên hướng dẫn: ThS. Bùi Quốc Khánh
<!-- AUTHORS_END -->

<!-- ABSTRACT_VI_BEGIN -->
**Tóm tắt:** Các môn lập trình đại học có tỉ lệ rớt 30–40% do mâu thuẫn giữa tính cá nhân hoá của kỹ năng lập trình và giảng dạy đại trà. Nền tảng trực tuyến hiện có kho bài tập phong phú nhưng dừng ở độ khó tĩnh, thiếu cơ chế thích ứng khép kín. Bốn kỹ thuật — Truy vết tri thức Bayes (BKT), xếp hạng Elo, bandit đa cánh tay (MAB) và lặp lại cách quãng FSRS — được nghiên cứu riêng lẻ, song chưa tích hợp đồng thời cho giáo dục lập trình. Bài báo đề xuất nền tảng học tập thích ứng năm lớp trên đồ thị tri thức 28 khái niệm, kèm phản hồi Socratic tuỳ chọn. Mỗi lần nộp mã nguồn, hệ thống cập nhật bất đồng bộ bốn lớp. Đóng góp: (i) kiến trúc tích hợp đầu tiên cho giáo dục lập trình; (ii) bandit phân cấp theo điều kiện tiên quyết BKT; (iii) lần đầu áp dụng FSRS cho lập trình qua ánh xạ nộp bài sang mức ôn tập. Bài báo là công trình triển khai kèm giao thức đánh giá thí điểm đã đăng ký trước; thực nghiệm chưa tiến hành.
<!-- ABSTRACT_VI_END -->

<!-- KEYWORDS_VI_BEGIN -->
**Từ khoá:** Bandit đa cánh tay; Giáo dục lập trình; Học tập thích ứng; Lặp lại cách quãng; Truy vết tri thức Bayes.
<!-- KEYWORDS_VI_END -->

<!-- ABSTRACT_EN_BEGIN -->
**Abstract:** Introductory programming courses worldwide report failure rates of 30–40%, driven by a persistent mismatch between the individualized, practice-intensive nature of programming skill acquisition and the uniform delivery model of large-class instruction. Existing online coding platforms provide extensive problem libraries but rely on static difficulty classifications and offer no closed-loop mechanism for learner adaptation. Individual adaptive techniques — Bayesian Knowledge Tracing (BKT), Elo rating, Multi-Armed Bandits (MAB), and the Free Spaced Repetition Scheduler (FSRS) — have each been studied in isolation, but no prior system integrates them for programming education. This paper presents a five-layer adaptive platform unified by a knowledge graph of 28 programming concepts, complemented by an optional large-language-model-based Socratic feedback layer. A closed-loop pipeline triggers asynchronous updates to all four adaptive layers on every code submission. The paper contributes (i) the first integrated adaptive architecture combining all four techniques for programming; (ii) a prerequisite-constrained hierarchical bandit with BKT-based mastery gating; and (iii) the first application of FSRS to programming skill retention through a novel code-submission-to-rating mapping. This paper should be read as an implementation paper accompanied by a pre-registered pilot evaluation protocol, not as a completed classroom study.
<!-- ABSTRACT_EN_END -->

<!-- KEYWORDS_EN_BEGIN -->
**Keywords:** Adaptive learning; Bayesian knowledge tracing; Multi-armed bandit; Programming education; Spaced repetition.
<!-- KEYWORDS_EN_END -->
