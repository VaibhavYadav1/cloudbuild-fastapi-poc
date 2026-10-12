# Cloud Build POC (FastAPI)

A tiny FastAPI service built, tested and deployed by Google Cloud Build.

**Pipeline:** pytest -> docker build -> push to Artifact Registry -> deploy to Cloud Run

## Project layout

```
app/main.py          FastAPI app with one endpoint: GET /
tests/test_main.py   Unit test run by Cloud Build
Dockerfile           Container image definition
cloudbuild.yaml      Cloud Build pipeline
requirements.txt     Python dependencies
```

## Run locally

```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
# open http://127.0.0.1:8000  (docs at /docs)
python -m pytest
```

## One-time GCP setup

```bash
export PROJECT_ID=<your-project-id>
export REGION=asia-south1
gcloud config set project $PROJECT_ID

gcloud services enable cloudbuild.googleapis.com artifactregistry.googleapis.com run.googleapis.com

gcloud artifacts repositories create poc-repo \
  --repository-format=docker --location=$REGION

PROJECT_NUMBER=$(gcloud projects describe $PROJECT_ID --format='value(projectNumber)')
CB_SA="${PROJECT_NUMBER}-compute@developer.gserviceaccount.com"

for ROLE in roles/run.admin roles/iam.serviceAccountUser \
            roles/artifactregistry.writer roles/logging.logWriter \
            roles/storage.objectAdmin; do
  gcloud projects add-iam-policy-binding $PROJECT_ID \
    --member="serviceAccount:$CB_SA" --role=$ROLE
done
```

## Build manually

```bash
gcloud builds submit --config cloudbuild.yaml .
```

## Automatic deploy on every push to `main`

Console -> Cloud Build -> Triggers -> Create trigger:
- Source: connect this GitHub repo
- Event: Push to a branch, `^main$`
- Configuration: `cloudbuild.yaml`

Now every push to `main` runs the pipeline and updates the live service.
