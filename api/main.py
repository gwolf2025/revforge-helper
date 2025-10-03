import os
from fastapi import FastAPI, UploadFile, File, Form, Header, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from api.schemas import *
from api.utils import ris_bib_parser, dedup, ranker, exports, storage

API_KEY = os.environ.get("HELPER_API_KEY", "")

app = FastAPI(title="RevForge Helper API", version="0.1.0")

origins = [os.environ.get("CORS_ORIGIN", "*")]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"]
)

def check_key(x_api_key: str | None):
    if API_KEY and x_api_key != API_KEY:
        raise HTTPException(status_code=401, detail="Invalid API key")

@app.get("/health")
async def health(): return {"ok": True}

@app.post("/import", response_model=ImportOut)
async def import_files(
    project_id: str = Form(...),
    files: list[UploadFile] = File(...),
    x_api_key: str | None = Header(default=None, alias="X-API-KEY")
):
    check_key(x_api_key)
    saved_paths = storage.save_originals(project_id, files)
    records = ris_bib_parser.strict_parse(files)
    enriched = await ris_bib_parser.enrich_metadata(records)
    counts = ris_bib_parser.persist_records(project_id, enriched)
    return ImportOut(project_id=project_id, saved_files=saved_paths, counts=counts)

@app.post("/dedup", response_model=DedupOut)
async def run_dedup(payload: DedupIn, x_api_key: str | None = Header(default=None, alias="X-API-KEY")):
    check_key(x_api_key)
    summary, merge_log, duplicates_csv = dedup.run(project_id=payload.project_id, threshold=payload.threshold)
    paths = storage.save_dedup_artifacts(payload.project_id, merge_log, duplicates_csv)
    return DedupOut(summary=summary, artifacts=paths)

@app.post("/rerank", response_model=RerankOut)
async def rerank(payload: RerankIn, x_api_key: str | None = Header(default=None, alias="X-API-KEY")):
    check_key(x_api_key)
    order = ranker.rerank(payload.project_id)
    return RerankOut(order=order)

@app.post("/export", response_model=ExportOut)
async def export_bundle(payload: ExportIn, x_api_key: str | None = Header(default=None, alias="X-API-KEY")):
    check_key(x_api_key)
    zip_path, files = exports.build_bundle(payload.project_id, payload.include_individual_files)
    return ExportOut(zip_path=zip_path, files=files)
