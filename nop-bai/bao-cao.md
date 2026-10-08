# Báo Cáo Lab Day 21 - CI/CD cho AI Systems

| | |
|---|---|
| Họ và tên | Trần Tuấn Tú |
| MSSV | 2A202602840 |
| Lớp / Khóa | K4 |
| Repo GitHub | https://github.com/ngaiTu29s1/K4-L3-DAY21-TranTuanTu-2A202602840-CI-CD-for-AI-Systems |
| Ngày nộp | 08/10/2026 |

---

## 1. Bộ Siêu Tham Số Đã Chọn và Lý Do

| Lần chạy | n_estimators | learning_rate | max_depth | f1_score | accuracy |
|---|---|---|---|---|---|
| 1 | 50 | 0.05 | 2 | 0.6051 | 0.8460 |
| 2 | 100 | 0.1 | 3 | 0.7109 | 0.8780 |
| 3 | 200 | 0.1 | 5 | 0.7149 | 0.8740 |

**Bộ siêu tham số đã chọn:** `n_estimators=200`, `learning_rate=0.1`, `max_depth=5`.

**Lý do:** Lần chạy 3 đạt điểm F1 của lớp dương cao nhất (0.7149), vượt qua ngưỡng kiểm định chất lượng 0.65 của bài toán. Dù lần chạy 2 đạt accuracy cao hơn (0.8780 so với 0.8740), sự chênh lệch này khẳng định accuracy cao nhất không đồng nghĩa với khả năng nhận diện người thu nhập cao tốt nhất. Khi số cây quá ít (50 cây) kết hợp tốc độ học thấp (0.05) và độ sâu nông (2), mô hình bị underfitting rõ rệt khiến F1 chỉ đạt 0.6051. Tăng số cây lên 200 và độ sâu cây lên 5 giúp mô hình nắm bắt được các tương tác phi tuyến tính trong tập dữ liệu.

---

## 2. Vì Sao Ngưỡng Chất Lượng Đặt Trên F1 Chứ Không Phải Accuracy

Tập dữ liệu Census Income có phân bố lớp mất cân bằng nghiêm trọng với chỉ 24.8% mẫu thuộc lớp thu nhập cao (>50K USD). Trong điều kiện này, một mô hình tầm thường luôn dự đoán "thu nhập thấp" cho tất cả mọi người vẫn đạt độ chính xác (accuracy) lên tới 75.2%, nhưng hoàn toàn vô giá trị trong thực tế vì F1 của lớp dương bằng 0. Điểm F1 là trung bình điều hòa giữa Precision và Recall, phản ánh chính xác khả năng phát hiện đúng đối tượng mục tiêu mà không bỏ sót hay báo động giả quá mức. Lab này sử dụng trực tiếp F1 cho lớp dương (nhãn 1), không dùng `average="weighted"` hay `average="macro"` vì trọng số từ lớp đa số sẽ kéo chỉ số lên cao một cách giả tạo, làm mất đi ý nghĩa của chốt chặn chất lượng Quality Gate.

---

## 3. Khó Khăn Gặp Phải và Cách Giải Quyết

| Khó khăn | Nguyên nhân | Cách giải quyết |
|---|---|---|
| MLflow lỗi `pkg_resources` và SQLAlchemy | Phiên bản setuptools mới loại bỏ API cũ và SQLAlchemy 2.1 không tương thích với MLflow 2.13.0 | Khóa phiên bản `setuptools<70` và `sqlalchemy<2.1` trong file `requirements.txt` |
| Lỗi unpickle model trên VM | Máy local dùng scikit-learn 1.4.2 trong khi môi trường VM cài đặt phiên bản mới hơn (1.9.1) | Đồng bộ chính xác phiên bản `scikit-learn==1.4.2` trong môi trường ảo của VM |
| Đồng bộ dữ liệu DVC trên GitHub Actions | Runner cần quyền truy cập Cloud Storage nhưng không được để lộ secret credential vào Git | Sử dụng Azure Blob Storage với Connection String bảo mật qua GitHub Secrets và cấu hình DVC remote |

---

## 4. So Sánh Bước 2 và Bước 3

| | f1_score | accuracy |
|---|---|---|
| Bước 2 (chỉ `train_batch1` - 22.361 mẫu) | 0.7149 | 0.8740 |
| Bước 3 (thêm `train_batch2` - 44.722 mẫu) | 0.7354 | 0.8820 |

**Nhận xét:** Khi bổ sung thêm 22.361 mẫu dữ liệu mới, điểm F1 tăng từ 0.7149 lên 0.7354 (+0.0205) và Accuracy tăng từ 0.8740 lên 0.8820 (+0.0080). Dung lượng dữ liệu dồi dào giúp GradientBoosting phân định biên quyết định chuẩn xác hơn ở nhóm thiểu số. Thành công lớn nhất của Bước 3 là chứng minh tính tự động hóa hoàn chỉnh: chỉ cần một thao tác cập nhật con trỏ DVC và git push, hệ thống CI/CD đã tự động kéo dữ liệu mới, huấn luyện lại, vượt qua Quality Gate và triển khai phiên bản mô hình mới lên VM đang phục vụ người dùng.
