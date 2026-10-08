from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import joblib
import os
from pathlib import Path

app = FastAPI(title="Adult Income Classifier")

ARTIFACT_BUCKET = os.environ.get("ARTIFACT_BUCKET", "income-artifacts")
MODEL_KEY = "artifacts/current/model.joblib"
MODEL_PATH = os.path.expanduser("~/models/model.joblib")


def download_model():
    """
    Tai file model.joblib tu cloud storage ve may khi server khoi dong.
    Ho tro ca Azure Blob Storage va Google Cloud Storage.
    """
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)

    # 1. Thu voi Azure Blob Storage
    azure_conn = os.environ.get("AZURE_STORAGE_CONNECTION_STRING") or os.environ.get("STORAGE_CREDENTIALS")
    if azure_conn and "EndpointSuffix=" in azure_conn:
        try:
            from azure.storage.blob import BlobServiceClient
            service_client = BlobServiceClient.from_connection_string(azure_conn)
            blob_client = service_client.get_blob_client(container=ARTIFACT_BUCKET, blob=MODEL_KEY)
            with open(MODEL_PATH, "wb") as f:
                data = blob_client.download_blob()
                data.readinto(f)
            print("Model da duoc tai xuong tu Azure Blob Storage.")
            return
        except Exception as e:
            print(f"Loi tai tu Azure Blob: {e}")

    # 2. Thu voi Google Cloud Storage
    if os.environ.get("GOOGLE_APPLICATION_CREDENTIALS") or os.environ.get("STORAGE_CREDENTIALS"):
        try:
            from google.cloud import storage
            client = storage.Client()
            bucket = client.bucket(ARTIFACT_BUCKET)
            blob = bucket.blob(MODEL_KEY)
            blob.download_to_filename(MODEL_PATH)
            print("Model da duoc tai xuong tu Google Cloud Storage.")
            return
        except Exception as e:
            print(f"Loi tai tu GCS: {e}")

    print("Khong the tai model tu Cloud Storage hoac chua co cau hinh.")


# Tai model khi khoi dong neu chua co hoac khi service duoc reload
try:
    download_model()
except Exception as e:
    print(f"Download model exception: {e}")

if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
else:
    model = None


class ScoreRequest(BaseModel):
    features: list[float]


@app.get("/healthz")
def healthz():
    """
    Endpoint kiem tra suc khoe server.
    GitHub Actions goi endpoint nay sau khi deploy de xac nhan server dang chay.
    """
    global model
    if model is None and os.path.exists(MODEL_PATH):
        try:
            model = joblib.load(MODEL_PATH)
        except Exception:
            pass
    return {"status": "ok"}


@app.post("/score")
def score(req: ScoreRequest):
    """
    Endpoint suy luan chinh.

    Dau vao : JSON {"features": [f1, f2, ..., f10]}
    Dau ra  : JSON {"prediction": <0|1>, "label": <"thu_nhap_thap"|"thu_nhap_cao">}
    """
    global model
    if model is None:
        if os.path.exists(MODEL_PATH):
            model = joblib.load(MODEL_PATH)
        else:
            raise HTTPException(status_code=503, detail="Model is not loaded")

    if len(req.features) != 10:
        raise HTTPException(
            status_code=400,
            detail="Expected 10 features (adult income)"
        )

    pred = int(model.predict([req.features])[0])
    label = "thu_nhap_cao" if pred == 1 else "thu_nhap_thap"

    return {"prediction": pred, "label": label}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8080)
