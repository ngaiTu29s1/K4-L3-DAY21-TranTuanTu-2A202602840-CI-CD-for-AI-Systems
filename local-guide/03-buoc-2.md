# Checkpoint 2 - Pipeline CI/CD và serving

## Mục tiêu đạt được

Hoàn thiện `src/serve.py` và `.github/workflows/cicd.yml` để bốn job chạy theo
chuỗi `Unit Test -> Train -> Quality Gate -> Release`.

## 1. Chuẩn bị cloud (GCP mặc định)

Tạo bucket, service account chỉ có quyền `roles/storage.objectAdmin`, key local
và VM theo [tasks/buoc-2.md](../tasks/buoc-2.md). Lưu các giá trị sau ở nơi an toàn,
không ghi vào file tracked:

```text
PROJECT=...
BUCKET=...
VM_IP=...
```

Thiết lập DVC và đẩy dữ liệu:

```bash
dvc init
dvc remote add -d labstore gs://$BUCKET/dvc
dvc remote modify labstore credentialpath sa-key.json
dvc add data/train_batch1.csv data/holdout.csv data/train_batch2.csv
git add data/*.dvc .gitignore .dvc/config
git commit -m "feat: track datasets with DVC"
export GOOGLE_APPLICATION_CREDENTIALS=sa-key.json
dvc push
```

Chỉ commit file `.dvc` và cấu hình DVC cần thiết; xác nhận CSV vẫn bị ignore.

## 2. Hoàn thiện serving

Trong `src/serve.py`:

- Tạo `storage.Client()`, lấy bucket/blob và tải model vào `MODEL_PATH`.
- Đảm bảo thư mục `~/models` tồn tại trước khi tải nếu cần.
- `/healthz` trả `{"status": "ok"}`.
- `/score` từ chối input khác 10 feature bằng HTTP 400.
- Dùng `model.predict([req.features])`, trả `prediction` kiểu int và label tương ứng.

Kiểm tra syntax và test local bằng một model đã có cùng schema. Khi chạy server,
cần đặt `ARTIFACT_BUCKET` và credential đúng:

```bash
export ARTIFACT_BUCKET="$BUCKET"
export GOOGLE_APPLICATION_CREDENTIALS="$PWD/sa-key.json"
python src/serve.py
```

## 3. Hoàn thiện GitHub Actions

Trong `.github/workflows/cicd.yml`:

1. Unit Test: `pytest -v tests/`.
2. Authenticate: ghi secret credential vào file tạm và set biến môi trường.
3. Pull đúng các dữ liệu cần thiết bằng `dvc pull`.
4. Đọc `outputs/report.json`, ghi `f1` vào `$GITHUB_OUTPUT`.
5. Upload `models/model.joblib` lên `gs://<ARTIFACT_BUCKET>/artifacts/current/model.joblib`.
6. Quality Gate: fail rõ ràng nếu F1 `< 0.65`.
7. Release: restart `income-api`, retry/check `curl /healthz`.

Tạo GitHub Secrets theo đúng tên workflow dùng: credential storage, bucket, host,
user và SSH key. Không dán giá trị secret vào workflow.

## 4. Kích hoạt và kiểm tra

```bash
git add src/serve.py .github/workflows/cicd.yml
git commit -m "feat: complete CI/CD pipeline and serving"
git push origin main
```

Vào GitHub Actions, đợi cả bốn job xanh. Sau đó kiểm tra:

```bash
curl -f "http://$VM_IP:8080/healthz"
curl -X POST "http://$VM_IP:8080/score" \
  -H "Content-Type: application/json" \
  -d '{"features":[28,2,14,2,11,0,1,0,0,45]}'
```

## Checklist chuyển Bước 3

- [ ] DVC remote đã có đủ object dữ liệu.
- [ ] Bốn jobs Actions đều xanh.
- [ ] Quality gate dùng F1 và ngưỡng `0.65`.
- [ ] `/healthz` trả status ok; `/score` trả prediction/label.
- [ ] Đã chụp `02-actions-buoc-2.png`, `04-curl-api.png`, `05-cloud-storage.png`.
- [ ] Đã lưu F1/accuracy từ artifact report cho mục so sánh Bước 3.
