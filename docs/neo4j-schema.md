# Schema Neo4j cho Medical GraphRAG

## Nguyên tắc thiết kế

- Label dùng `PascalCase`, relationship dùng `UPPER_SNAKE_CASE`, property dùng `snake_case`.
- Mọi thực thể y khoa đều có label nền `MedicalConcept` và ít nhất một label chuyên biệt.
- `id` là định danh ổn định; không dùng `name` làm khóa vì tên y khoa có thể có nhiều biến thể.
- `code` và `coding_system` dùng để ánh xạ tới hệ thuật ngữ chuẩn như SNOMED CT, ICD-10, RxNorm, ATC hoặc LOINC.
- Quan hệ y khoa phải giữ được bằng chứng nguồn để Agent có thể kiểm chứng và giảm hallucination.
- Schema ban đầu chỉ lưu tri thức tổng quát, không lưu dữ liệu nhận dạng cá nhân hoặc hồ sơ bệnh nhân.

## Node labels

| Label | Mục đích | Thuộc tính chính |
|---|---|---|
| `MedicalConcept` | Label nền cho mọi khái niệm y khoa | `id`, `name`, `normalized_name`, `aliases`, `description`, `code`, `coding_system` |
| `Disease` | Bệnh, rối loạn hoặc tình trạng lâm sàng | Thuộc tính của `MedicalConcept` |
| `Symptom` | Triệu chứng hoặc dấu hiệu | Thuộc tính của `MedicalConcept` |
| `Drug` | Thuốc hoặc hoạt chất | Thuộc tính của `MedicalConcept` |
| `Treatment` | Phác đồ, thủ thuật hoặc liệu pháp không phải thuốc | Thuộc tính của `MedicalConcept` |
| `DiagnosticTest` | Xét nghiệm hoặc kỹ thuật chẩn đoán | Thuộc tính của `MedicalConcept` |
| `Anatomy` | Cơ quan, mô hoặc cấu trúc giải phẫu | Thuộc tính của `MedicalConcept` |
| `RiskFactor` | Yếu tố nguy cơ | Thuộc tính của `MedicalConcept` |
| `Pathogen` | Tác nhân gây bệnh | Thuộc tính của `MedicalConcept` |
| `AdverseEffect` | Phản ứng hoặc tác dụng không mong muốn | Thuộc tính của `MedicalConcept` |
| `PatientGroup` | Nhóm đối tượng như trẻ em, thai phụ hoặc người cao tuổi | Thuộc tính của `MedicalConcept` |
| `Document` | Tài liệu nguồn, hướng dẫn hoặc bài báo | `id`, `title`, `source_type`, `source_url`, `publisher`, `publication_date`, `language`, `checksum`, `ingested_at` |
| `Chunk` | Đoạn văn dùng cho RAG và embedding | `id`, `document_id`, `position`, `text`, `token_count`, `embedding` |

Một node có thể mang nhiều label khi phù hợp, ví dụ `(:MedicalConcept:Symptom:AdverseEffect)`.

## Relationships

| Relationship | Node nguồn | Node đích | Ý nghĩa |
|---|---|---|---|
| `HAS_CHUNK` | `Document` | `Chunk` | Tài liệu chứa đoạn văn |
| `MENTIONS` | `Chunk` | `MedicalConcept` | Đoạn văn nhắc tới thực thể |
| `HAS_SYMPTOM` | `Disease` | `Symptom` | Bệnh có triệu chứng hoặc dấu hiệu |
| `HAS_RISK_FACTOR` | `Disease` | `RiskFactor` | Bệnh có yếu tố nguy cơ |
| `CAUSED_BY` | `Disease` | `Pathogen` hoặc `MedicalConcept` | Nguyên nhân hoặc tác nhân gây bệnh |
| `AFFECTS` | `Disease` | `Anatomy` | Bệnh ảnh hưởng cấu trúc giải phẫu |
| `DIAGNOSTIC_FOR` | `DiagnosticTest` | `Disease` | Xét nghiệm hỗ trợ chẩn đoán bệnh |
| `TREATS` | `Drug` hoặc `Treatment` | `Disease` | Thuốc hoặc liệu pháp điều trị bệnh |
| `RECOMMENDED_FOR` | `Drug` hoặc `Treatment` | `Disease` hoặc `PatientGroup` | Khuyến nghị cho bệnh hoặc nhóm đối tượng |
| `CONTRAINDICATED_FOR` | `Drug` hoặc `Treatment` | `Disease` hoặc `PatientGroup` | Chống chỉ định |
| `CAUSES_ADVERSE_EFFECT` | `Drug` hoặc `Treatment` | `AdverseEffect` | Gây tác dụng không mong muốn |
| `INTERACTS_WITH` | `Drug` | `Drug` | Tương tác thuốc |
| `COMORBID_WITH` | `Disease` | `Disease` | Hai bệnh thường đồng mắc |
| `IS_A` | `MedicalConcept` | `MedicalConcept` | Quan hệ phân cấp khái niệm |
| `PART_OF` | `Anatomy` | `Anatomy` | Quan hệ thành phần giải phẫu |
| `ASSOCIATED_WITH` | `MedicalConcept` | `MedicalConcept` | Liên hệ tổng quát khi chưa đủ bằng chứng cho loại cụ thể |

Không lưu đồng thời hai quan hệ nghịch đảo như `TREATS` và `TREATED_BY`. Khi truy vấn có thể dùng cạnh không định hướng nếu cần. Với `INTERACTS_WITH` và `COMORBID_WITH`, chỉ lưu một cạnh theo thứ tự tăng dần của `id` để tránh trùng lặp.

## Thuộc tính bằng chứng

Các relationship y khoa được trích xuất nên có:

| Property | Kiểu | Ý nghĩa |
|---|---|---|
| `confidence` | `Float` từ 0 đến 1 | Độ tin cậy của bước trích xuất |
| `assertion` | `String` | `affirmed`, `negated` hoặc `uncertain` |
| `evidence_chunk_ids` | `List<String>` | Các `Chunk.id` làm bằng chứng |
| `extraction_method` | `String` | Model hoặc quy tắc đã tạo quan hệ |
| `created_at` | ISO 8601 UTC | Thời điểm tạo |

`MENTIONS` có thể dùng thêm `start_char`, `end_char` và `confidence` để lưu vị trí thực thể trong đoạn văn.

## Constraint và index

Module `graphrag_med_agent.schema` tạo constraint duy nhất cho `MedicalConcept.id`, `Document.id`, `Chunk.id`; index cho tên chuẩn hóa, mã thuật ngữ, checksum và vị trí chunk; cùng full-text index cho tên thực thể và nội dung chunk.

Vector index chưa được tạo ở bước này vì số chiều phải khớp embedding model. Index này sẽ được thêm sau khi chọn model embedding để tránh khóa schema vào một cấu hình sai.

## Khởi tạo schema và kiểm tra kết nối

Chạy từ thư mục gốc của dự án bằng PowerShell:

```powershell
$env:PYTHONPATH = "src"
.\.venv\Scripts\python.exe -m graphrag_med_agent.schema
.\.venv\Scripts\python.exe -m graphrag_med_agent.database
```

Các lệnh không in username, password hoặc API key ra terminal.
