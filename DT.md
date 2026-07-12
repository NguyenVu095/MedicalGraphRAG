Đề tài: Tăng cường độ tin cậy và tri thức y khoa chuyên sâu cho Tác nhân thông minh thông qua tích hợp Đồ thị tri thức (Knowledge Graph) và Cơ chế RAG (Enhancing Reliability and Specialized Medical Knowledge for Intelligent Agents via Knowledge Graph Integration and RAG Mechanisms)



Gemini AI đề xuất hướng đi:



1\. Nội dung lý thuyết (Theoretical Content)

\- Nghiên cứu tổng quan về kiến trúc và cơ chế hoạt động của Tác nhân thông minh (AI Agents) và Mô hình ngôn ngữ lớn (LLMs).

\- Tìm hiểu sâu về cơ chế RAG (Retrieval-Augmented Generation): Quy trình từ tiền xử lý dữ liệu, định dạng nhúng (Embedding), lưu trữ Vector Database đến truy xuất dữ liệu.

\- Nghiên cứu về Đồ thị tri thức (Knowledge Graph): Cách biểu diễn dữ liệu dưới dạng thực thể (Entities), thuộc tính (Attributes) và mối quan hệ (Relations).

\- Nghiên cứu phương pháp kết hợp GraphRAG: Cách tích hợp Đồ thị tri thức vào luồng RAG để tối ưu hóa khả năng truy vấn logic và ngữ cảnh sâu.

\- Tìm hiểu về chuẩn dữ liệu và các thách thức về độ tin cậy trong y khoa chuyên sâu (tránh hiện tượng AI "báo lỗi" hoặc ảo tưởng thông tin - Hallucination).



2\. Nội dung thực hành (Practical/Implementation Content)

\- Khảo sát, thu thập và làm sạch tài liệu/dữ liệu mẫu thuộc lĩnh vực Y khoa chuyên sâu.

\- Thiết lập môi trường lập trình (Python) và cài đặt các thư viện, framework hỗ trợ (ví dụ: LangChain, LlamaIndex, hoặc GraphRAG của Microsoft).

\- Thực hành xây dựng và chuẩn hóa Đồ thị tri thức từ tập dữ liệu y khoa thu được sử dụng các hệ quản trị cơ sở dữ liệu đồ thị (như Neo4j) hoặc cơ sở dữ liệu Vector.

\- Triển khai thử nghiệm (PoC - Proof of Concept) hệ thống Agent tích hợp cơ chế GraphRAG để truy vấn và trả lời các câu hỏi y khoa.

\- Đánh giá, đo lường độ chính xác và độ tin cậy của câu trả lời từ Tác nhân thông minh dựa trên tập câu hỏi thử nghiệm.

\- Tổng hợp kết quả, viết báo cáo thực tập và chuẩn bị tài liệu bàn giao sản phẩm.



Phần công việc của tôi:

* Thiết lập cấu trúc dự án (Python, Git), nghiên cứu Neo4j \& GraphRAG.
* Thiết kế Schema cho Graph. Viết code trích xuất thực thể để đẩy vào Neo4j.
* Viết code kết nối GraphRAG và xây dựng AI Agent
* Tối ưu prompt, xử lý logic để giảm Hallucination khi Agent trả lời.
* Viết chương: Kiến trúc Agent, GraphRAG, Neo4j, kết quả thực nghiệm.
