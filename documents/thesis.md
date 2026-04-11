# Adaptive Learning Platform for University Programming Courses

**Hệ thống hỗ trợ học tập thích ứng cho môn lập trình tại đại học**

---

**TRƯỜNG ĐẠI HỌC HÀ NỘI — KHOA CÔNG NGHỆ THÔNG TIN**

**ĐỀ CƯƠNG KHÓA LUẬN TỐT NGHIỆP**

---

## A. Thông tin về sinh viên

| Field        | Detail              |
| ------------ | ------------------- |
| Mã sinh viên | 2201040036          |
| Họ tên       | Nguyễn Tuấn Dương   |

## B. Thông tin về giảng viên hướng dẫn

| Field        | Detail                                              |
| ------------ | --------------------------------------------------- |
| Họ tên       | Bùi Quốc Khánh                                      |
| Nơi công tác | Trường Đại Học Hà Nội — Khoa Công Nghệ Thông Tin    |

---

## C. Tên đề tài khóa luận

- **English:** Adaptive Learning Platform for University Programming Courses
- **Vietnamese:** Hệ thống hỗ trợ học tập thích ứng cho môn lập trình tại đại học

---

## D. Lý do lựa chọn đề tài

### 1. Context and Current Situation

The current state of programming education is challenged by many issues in accommodating the varied needs of students within university classes. Emergent research shows that dropout levels within introductory programming courses can be as high as **30% or more**, with students differing considerably in terms of their pre-existing skills, speed of learning, or problem-solving capacity. For classes consisting of 50–100 students, teachers lack the time or resources to offer personalized help or detailed feedback on coding work.

The conventional method of lecturing all students simultaneously does not address the needs of each student. Students who can understand concepts quickly become disengaged while waiting for others, while those who understand less fall further behind. Also, manually grading coding assignment work is time-consuming, resulting in delayed grading, which does not allow the student immediate feedback.

### 2. Research Problem

While existing online coding platforms such as LeetCode, HackerRank, and Coursera offer extensive problem repositories, they exhibit several critical limitations:

- **Static difficulty classification:** Problems are labeled with fixed difficulty levels (easy/medium/hard) that do not adapt to individual learner profiles.
- **Lack of fine-grained skill modeling:** Most systems track overall progress rather than modeling specific competencies (e.g., recursion, dynamic programming, data structures).
- **No closed-loop adaptation:** Feedback from code submissions rarely influences subsequent problem recommendations in real-time.

Furthermore, existing research in adaptive learning for programming has typically focused on isolated components — either automated grading, skill assessment, or recommendation — without integrating them into a unified, feedback-driven system that continuously refines its understanding of learner capabilities.

### 3. Proposed Solution

This thesis proposes the design and development of an **Adaptive Learning Platform for University Programming Courses** that addresses these gaps through a data-driven, personalized approach. The platform integrates three core components into a unified closed-loop system:

#### 3.1. Student Skill Embedding

Maps individual learner performance into dense vector representations of programming skills, capturing fine-grained competencies across multiple dimensions (syntax, algorithms, problem-solving patterns, code quality).

#### 3.2. Intelligent Question Recommendation

Dynamically suggests coding challenges tailored to each student's current mastery level by matching their skill embedding against a problem database.

#### 3.3. Automated Code Assessment

Instantly evaluates code submissions in a secure, sandboxed environment using test cases. Assessment results are fed back into the skill embedding model to continuously refine the learner profile.

#### 3.4. Closed-Loop Feedback Workflow

The system implements a continuous feedback mechanism:

1. Students complete an initial diagnostic test
2. Their performance generates a skill embedding
3. The recommendation engine suggests appropriate problems
4. Each submission is automatically graded
5. Results update the skill embedding in real-time
6. The refined profile influences subsequent recommendations

This adaptive cycle ensures that the learning experience evolves dynamically with student progress, maintaining optimal challenge levels and maximizing engagement.

### 4. Significance and Contributions

#### 4.1. Benefits for Students

- Personalized learning paths adapted to individual skill levels and learning pace
- Optimized challenge difficulty preventing both frustration and boredom
- Transparent skill visualization showing concrete progress across competencies

#### 4.2. Benefits for Instructors

- Reduced grading workload through automated assessment
- Actionable analytics identifying struggling students and common misconceptions
- Data-driven curriculum design based on aggregated performance metrics
- Scalable personalization enabling differentiated instruction in large classes
- Early intervention capability through continuous progress monitoring

#### 4.3. Scientific Contributions

- Integration of skill embedding with adaptive recommendation in a unified system
- Empirical validation of closed-loop adaptive systems in programming education

#### 4.4. Implementation Scope

By implementing and evaluating a functional MVP focused on **Python programming** within a real university course setting, this study seeks to demonstrate how adaptive feedback mechanisms and personalized learning paths can measurably improve students' coding proficiency, reduce time-to-mastery, and increase course completion rates. The findings will inform both educational practice and future research in computer science education technology.

> **In summary**, this research addresses the urgent need for personalization in large-scale programming education by integrating artificial intelligence, automated assessment, and learning science into a unified system capable of continuously adapting to learner capabilities.

---

## E. Đề cương của khóa luận

### Chapter 1: Introduction

- Context & Motivation
- Research Objectives
- Research Questions
- Scope
- Main Contributions
- Thesis Structure

### Chapter 2: Literature Review and Theoretical Foundations

- Intelligent Tutoring Systems
- Knowledge Tracing
- Recommendation Systems
- Auto-Grading Systems
- Explainable AI in Education
- Related Work Summary

### Chapter 3: System Requirements & Analysis

- User Personas
- Functional Requirements
- Non-Functional Requirements
- System Workflow
- Data Model Design
- Use Cases
- System Architecture
- Constraints & Assumptions

### Chapter 4: Design & Implementation

- Skill Embedding Model Design
- Question Recommendation Algorithm Design
- Automated Grading Engine Design
- System Implementation
- Challenges & Mitigation

### Chapter 5: Experimentation & Evaluation

- Experimental Design
- Evaluation Metrics
- Data Analysis Plan
- Expected Results & Discussion
- Ablation Study
- Ethical Considerations

### Chapter 6: Conclusion

- Summary of Contributions
- Key Findings
- Limitations
- Practical Implications
- Final Remarks

### Chapter 7: References

### Appendices (Optional)

---

**Hà Nội, ngày 26 tháng 10 năm 2025**

| Xác nhận của giảng viên hướng dẫn | Sinh viên thực hiện khóa luận |
| ---------------------------------- | ----------------------------- |
| *(Họ tên / chữ ký)*               | Nguyễn Tuấn Dương             |
