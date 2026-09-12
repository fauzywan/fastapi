import json
from io import BytesIO
from pathlib import Path

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse, StreamingResponse
from pydantic import BaseModel, Field

from domain.ulasan import Ulasan
from services.csv_analysis_service import CsvAnalysisService
from services.model_analisis import ModelAnalisis
from services.text_preprocessor import TextPreprocessor


# =========================================================
# PATH
# =========================================================
BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "models"
METADATA_PATH = MODEL_DIR / "metadata_model_final.json"


# =========================================================
# FASTAPI
# =========================================================
app = FastAPI(
    title="Na Willa Sentiment API",
    description=(
        "Backend FastAPI berbasis OOP untuk analisis sentimen ulasan "
        "film Na Willa menggunakan TF-IDF + SVM."
    ),
    version="1.0.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://127.0.0.1:5173",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# =========================================================
# OBJECT OOP / DEPENDENCY
# =========================================================
preprocessor = TextPreprocessor(
    slang_path=MODEL_DIR / "slang_dict_final.json",
    stopwords_path=MODEL_DIR / "stopwords_svm_final.json",
)

model_analisis = ModelAnalisis(
    model_path=MODEL_DIR / "svm_na_willa_final.pkl",
    tfidf_path=MODEL_DIR / "tfidf_na_willa_final.pkl",
    preprocessor=preprocessor,
)

csv_service = CsvAnalysisService(model_analisis=model_analisis)


# =========================================================
# REQUEST SCHEMA
# =========================================================
class UlasanRequest(BaseModel):
    review_text: str = Field(
        ...,
        min_length=1,
        examples=["Film Na Willa bagus banget"],
    )


# =========================================================
# HELPER
# =========================================================
def load_metadata() -> dict:
    if not METADATA_PATH.exists():
        return {}
    with open(METADATA_PATH, "r", encoding="utf-8") as file:
        return json.load(file)


def model_information() -> dict:
    metadata = load_metadata()
    svm = metadata.get("svm", {})
    metrics = metadata.get("hasil_test", {}).get("svm", {})
    return {
        "name": model_analisis.nama_model,
        "code": model_analisis.kode_model,
        "configuration": {
            "C": svm.get("C"),
            "ngram_range": svm.get("ngram_range"),
            "min_df": svm.get("min_df"),
            "jumlah_fitur": svm.get("jumlah_fitur"),
        },
        "metrics": metrics,
    }


def error_response(message: str, status_code: int = 400) -> JSONResponse:
    return JSONResponse(
        status_code=status_code,
        content={"success": False, "message": message},
    )


# =========================================================
# ROUTES
# =========================================================
@app.get("/")
def root():
    return {
        "success": True,
        "message": "Na Willa Sentiment API",
        "docs": "/docs",
    }


@app.get("/api/health")
def health():
    return {
        "success": True,
        "message": "Backend FastAPI berjalan",
        "model": model_information(),
    }


@app.post("/api/ulasan")
def analisis_ulasan(data: UlasanRequest):
    """Endpoint OOP untuk menganalisis satu objek Ulasan."""
    try:
        hasil = model_analisis.analisis(Ulasan(data.review_text))
        return {
            "success": True,
            "data": hasil.to_dict(),
        }
    except ValueError as error:
        return error_response(str(error))
    except Exception as error:
        return error_response(f"Terjadi kesalahan: {error}", 500)


@app.post("/api/predict")
def predict(data: UlasanRequest):
    """Alias kompatibel dengan response endpoint Flask sebelumnya."""
    try:
        hasil = model_analisis.analisis(Ulasan(data.review_text))
        hasil_dict = hasil.to_dict()
        return {
            "success": True,
            "review_text": hasil_dict["review_text"],
            "processed_text": hasil_dict["processed_text"],
            "predicted_sentiment": hasil_dict["predicted_sentiment"],
        }
    except ValueError as error:
        return error_response(str(error))
    except Exception as error:
        return error_response(f"Terjadi kesalahan: {error}", 500)


@app.post("/api/analyze-csv")
async def analyze_csv(file: UploadFile = File(...)):
    try:
        content = await file.read()
        dataframe = csv_service.read_csv(file.filename or "", content)
        classified, _hasil, laporan = csv_service.analyze_dataframe(dataframe)
        visible = csv_service.public_dataframe(classified)

        return {
            "success": True,
            "filename": file.filename,
            "analyzed_at": laporan.dibuat_pada.isoformat(),
            "model": model_information(),
            "laporan": laporan.to_dict(),
            "summary": laporan.generate(),
            "reviews": csv_service.dataframe_to_records(visible),
        }
    except ValueError as error:
        return error_response(str(error))
    except Exception as error:
        return error_response(f"Terjadi kesalahan: {error}", 500)


@app.post("/api/download-csv")
async def download_csv(file: UploadFile = File(...)):
    try:
        content = await file.read()
        dataframe = csv_service.read_csv(file.filename or "", content)
        classified, _hasil, _laporan = csv_service.analyze_dataframe(dataframe)
        csv_bytes = csv_service.to_csv_bytes(classified)

        original_name = Path(file.filename or "hasil").stem
        headers = {
            "Content-Disposition": (
                f'attachment; filename="{original_name}_hasil_sentimen.csv"'
            )
        }
        return StreamingResponse(
            BytesIO(csv_bytes),
            media_type="text/csv; charset=utf-8",
            headers=headers,
        )
    except ValueError as error:
        return error_response(str(error))
    except Exception as error:
        return error_response(f"Terjadi kesalahan: {error}", 500)
