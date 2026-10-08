# Checkpoint 1 - Thực nghiệm local và MLflow

## Mục tiêu đạt được

- Tạo đủ `data/train_batch1.csv`, `data/holdout.csv`, `data/train_batch2.csv`.
- Hoàn thiện TODO trong `src/train.py` và `tests/test_train.py`.
- Chạy test thành công.
- Chạy ít nhất 3 bộ siêu tham số khác nhau và so sánh trên MLflow.
- Chọn bộ có `f1_score` tốt nhất, không chọn chỉ dựa trên accuracy.

## 1. Khởi tạo dữ liệu và MLflow

```bash
source .venv/bin/activate
python prepare_data.py
ls -lh data/
export MLFLOW_TRACKING_URI=sqlite:///mlflow.db
export MLFLOW_ARTIFACT_ROOT=./mlartifacts
```

Kết quả mong đợi: ba file CSV; `holdout.csv` có 500 mẫu; hai batch train có
22.361 mẫu theo task gốc. Nếu khác, ghi lại số thực tế để dùng trong báo cáo.

## 2. Hoàn thiện code

Trong `src/train.py`, thực hiện lần lượt:

1. Đọc hai CSV bằng `pd.read_csv`.
2. Tách `X` bằng cách bỏ `target`, lấy `y` từ `target`.
3. Mở `mlflow.start_run()`.
4. Log `params`, train `GradientBoostingClassifier(**params, random_state=42)`.
5. Tính `f1_score(y_eval, preds)` và `accuracy_score(y_eval, preds)`.
6. Log hai metric và model vào MLflow.
7. Ghi `outputs/report.json` và `models/model.joblib`.
8. Trả về `f1` kiểu `float`.

Trong `tests/test_train.py`, hoàn thiện fixture dữ liệu ngẫu nhiên và ba test
được đánh dấu TODO. Sau đó chạy:

```bash
pytest -v
```

Đạt khi toàn bộ test pass, có `outputs/report.json` và `models/model.joblib`.

## 3. Chạy tối thiểu 3 thí nghiệm

Mỗi lần sửa `params.yaml` rồi chạy:

```bash
python src/train.py
```

Gợi ý ba bộ có tính so sánh:

```yaml
# Lần 1
n_estimators: 100
learning_rate: 0.1
max_depth: 3
```

```yaml
# Lần 2
n_estimators: 50
learning_rate: 0.05
max_depth: 2
```

```yaml
# Lần 3
n_estimators: 200
learning_rate: 0.1
max_depth: 5
```

Vào MLflow UI để ghi lại `n_estimators`, `learning_rate`, `max_depth`,
`f1_score` và `accuracy` của từng run. Chọn run có F1 cao nhất và giữ bộ tham
số đó trong `params.yaml`.

## Checklist chuyển Bước 2

- [ ] `pytest -v` pass.
- [ ] Có ít nhất 3 run trong MLflow.
- [ ] Đã ghi số liệu thật vào `nop-bai/bao-cao.md`, mục 1.
- [ ] Đã giải thích vì sao dùng F1 của lớp dương, không dùng weighted/macro.
- [ ] Đã chụp `01-mlflow-ui.png`.
- [ ] `git status` không cho thấy credential, CSV, model hay database local.
