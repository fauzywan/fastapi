# Na Willa Sentiment API — FastAPI + OOP

Backend siap pakai untuk analisis sentimen ulasan film **Na Willa** menggunakan **TF-IDF + Linear SVM**.

## Arsitektur OOP

- `Ulasan` — objek data ulasan.
- `TextPreprocessor` — cleaning, normalisasi slang, stopword removal, stemming.
- `ModelAnalisis` — memuat TF-IDF dan SVM serta melakukan klasifikasi.
- `HasilAnalisis` — objek hasil prediksi per ulasan.
- `Laporan` — merangkum jumlah dan persentase sentimen.
- `CsvAnalysisService` — pengolahan upload/download CSV.

Alur:

`FastAPI -> Ulasan -> TextPreprocessor -> ModelAnalisis -> HasilAnalisis -> Laporan`

## Menjalankan di Windows

Cara termudah: double-click `run_backend.bat`.

Script akan:
1. Membuat `venv` jika belum ada.
2. Menginstal `requirements.txt`.
3. Menjalankan FastAPI pada port 8000.

Buka:
- API: `http://127.0.0.1:8000`
- Swagger Docs: `http://127.0.0.1:8000/docs`
- Health: `http://127.0.0.1:8000/api/health`

> Disarankan Python 3.13. Model pickle dibuat menggunakan scikit-learn 1.6.1, sehingga `requirements.txt` mengunci versi tersebut untuk mengurangi masalah kompatibilitas model.

## Endpoint

### Analisis satu ulasan
`POST /api/ulasan`

```json
{
  "review_text": "Film Na Willa bagus banget"
}
```

Alias kompatibilitas frontend lama: `POST /api/predict`.

### Analisis CSV
`POST /api/analyze-csv`

Multipart form-data dengan field `file`. CSV harus memiliki kolom `review_text` dan encoding UTF-8.

### Download hasil CSV
`POST /api/download-csv`

Multipart form-data dengan field `file`.

## Model

Runtime utama memakai:
- `models/svm_na_willa_final.pkl`
- `models/tfidf_na_willa_final.pkl`
- `models/slang_dict_final.json`
- `models/stopwords_svm_final.json`
- `models/metadata_model_final.json`

Model CNN tidak diperlukan oleh backend final ini karena inference sistem menggunakan SVM.

## Frontend

Jika frontend React/Vite milikmu berada dalam folder `frontend` yang berdampingan dengan folder backend ini, gunakan `run_with_frontend.bat`. Jika struktur frontend berbeda, ubah nilai `FRONTEND_DIR` di file tersebut.
