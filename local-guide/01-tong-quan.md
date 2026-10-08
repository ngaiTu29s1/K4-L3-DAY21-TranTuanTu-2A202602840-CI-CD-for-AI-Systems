# Local Guide - CI/CD cho AI Systems

## Cách sử dụng

Làm theo đúng thứ tự `Bước 1 -> Bước 2 -> Bước 3`. Mỗi bước chỉ chuyển sang bước
tiếp theo sau khi đã đạt checklist và lưu đủ bằng chứng. Các task gốc nằm tại:

- [tasks/buoc-1.md](../tasks/buoc-1.md)
- [tasks/buoc-2.md](../tasks/buoc-2.md)
- [tasks/buoc-3.md](../tasks/buoc-3.md)

## Chuẩn bị một lần

Từ thư mục gốc repository:

```bash
source .venv/bin/activate
python --version
which python
python -m pip install -r requirements.txt
```

`which python` phải trỏ vào `.venv/bin/python`. Không commit `.venv/`, credential,
file CSV, model hoặc database MLflow; các mục này đã được thêm vào `.gitignore`.

## Bảng tiến độ

| Checkpoint | Trạng thái | Guide | Bằng chứng chính |
|---|---|---|---|
| Bước 1 - Thực nghiệm local | [ ] | [02-buoc-1.md](02-buoc-1.md) | MLflow UI, 3 lần chạy, bộ tham số được chọn |
| Bước 2 - CI/CD | [ ] | [03-buoc-2.md](03-buoc-2.md) | Actions xanh, API `/healthz` và `/score`, cloud storage |
| Bước 3 - Dữ liệu mới | [ ] | [04-buoc-3.md](04-buoc-3.md) | Actions được kích hoạt bởi commit dữ liệu, bảng so sánh |
| Hồ sơ nộp bài | [ ] | `nop-bai/README.md` | 5 ảnh, báo cáo, repo public |

## Quy tắc an toàn

- Không đưa `sa-key.json`, nội dung GitHub Secrets, access key hoặc private key vào
  Git, log hay ảnh chụp.
- Chỉ commit file `.dvc`, không commit các file CSV được DVC quản lý.
- Kiểm tra `git status` trước mỗi commit.
- Dùng F1 của lớp dương làm quality gate; không thay bằng accuracy.
- Nếu pipeline lỗi, ghi lại URL run, job lỗi và log liên quan trước khi sửa.

## Định dạng bằng chứng

Ảnh cần đặt đúng tên trong `nop-bai/anh-chup-man-hinh/`, mỗi ảnh dưới 1 MB:

1. `01-mlflow-ui.png`
2. `02-actions-buoc-2.png`
3. `03-actions-buoc-3.png`
4. `04-curl-api.png`
5. `05-cloud-storage.png`

Giá trị F1, accuracy, URL repo, bucket và VM IP trong báo cáo phải là kết quả thật
của bạn, không dùng số minh họa trong task.
