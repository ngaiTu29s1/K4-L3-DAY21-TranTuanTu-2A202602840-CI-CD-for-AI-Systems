# Checkpoint 3 - Huấn luyện liên tục với dữ liệu mới

## Mục tiêu đạt được

Thay đổi dữ liệu, cập nhật con trỏ DVC, rồi để một lần `git push` kích hoạt lại
toàn bộ pipeline mà không sửa thủ công trên VM.

## 1. Bổ sung batch dữ liệu

Đảm bảo đang ở commit đã hoàn thành Bước 2, sau đó chạy:

```bash
source .venv/bin/activate
python append_batch.py
wc -l data/train_batch1.csv
```

Kết quả tham khảo: từ 22.361 lên 44.722 mẫu, tương đương 44.723 dòng gồm header.

## 2. Cập nhật DVC trước khi push Git

Thứ tự bắt buộc:

```bash
dvc add data/train_batch1.csv
export GOOGLE_APPLICATION_CREDENTIALS=sa-key.json
dvc push
git add data/train_batch1.csv.dvc
git commit -m "data: bổ sung 22361 mẫu dữ liệu mới (train_batch2)"
git push origin main
```

Phải chạy `dvc push` trước `git push`; nếu không, Actions có thể bắt đầu trước khi
object dữ liệu mới tồn tại trên remote. Không `git add` file CSV.

## 3. Theo dõi pipeline

Trong GitHub Actions, xác nhận run được tạo bởi commit dữ liệu và bốn job chạy theo
đúng thứ tự. Train phải pull dataset mới, upload model mới; quality gate vẫn phải
kiểm tra `f1_score >= 0.65`; release phải restart service và pass health check.

Nếu run không xuất hiện, kiểm tra:

```bash
git log --name-only -1
git status --short
```

File thay đổi chính phải là `data/train_batch1.csv.dvc`. Nếu `dvc pull` lỗi, kiểm
tra remote, quyền bucket và việc `dvc push` đã hoàn tất.

## 4. Kiểm tra model mới và so sánh

```bash
curl -f "http://$VM_IP:8080/healthz"
curl -X POST "http://$VM_IP:8080/score" \
  -H "Content-Type: application/json" \
  -d '{"features":[28,2,14,2,11,0,1,0,0,45]}'
```

Tải `outputs/report.json` từ artifacts của run Bước 2 và Bước 3, rồi điền số thật
vào mục 3.6 của [tasks/buoc-3.md](../tasks/buoc-3.md) và mục 4 của
`nop-bai/bao-cao.md`. Không mặc định rằng thêm dữ liệu luôn làm F1 tăng.

## Checklist hoàn tất

- [ ] Commit kích hoạt pipeline là commit dữ liệu.
- [ ] Cả bốn jobs của run Bước 3 đều xanh.
- [ ] VM đang phục vụ model mới và API trả lời thành công.
- [ ] Đã điền bảng so sánh F1/accuracy Bước 2 và Bước 3.
- [ ] Đã chụp `03-actions-buoc-3.png`.
- [ ] Đã cập nhật `nop-bai/bao-cao.md` và kiểm tra không quá 1 trang A4.
- [ ] Đã kiểm tra repo public, đủ 5 ảnh và mở URL ở chế độ ẩn danh.
