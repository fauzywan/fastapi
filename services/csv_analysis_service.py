from io import BytesIO

import pandas as pd

from domain.laporan import Laporan
from domain.ulasan import Ulasan
from services.model_analisis import ModelAnalisis


class CsvAnalysisService:
    """Membaca CSV, menganalisis banyak Ulasan, dan membuat Laporan."""

    PRIVATE_COLUMNS = {"reviewer", "review_url"}
    MAX_FILE_SIZE = 10 * 1024 * 1024

    def __init__(self, model_analisis: ModelAnalisis):
        self.model_analisis = model_analisis

    def read_csv(self, filename: str, content: bytes) -> pd.DataFrame:
        if not filename or not filename.lower().endswith(".csv"):
            raise ValueError("File harus berformat CSV")

        if len(content) > self.MAX_FILE_SIZE:
            raise ValueError("Ukuran file melebihi batas maksimum 10 MB")

        try:
            dataframe = pd.read_csv(BytesIO(content), encoding="utf-8-sig")
        except UnicodeDecodeError as exc:
            raise ValueError("Encoding CSV harus UTF-8") from exc
        except Exception as exc:
            raise ValueError(f"File CSV tidak dapat dibaca: {exc}") from exc

        if dataframe.empty:
            raise ValueError("Dataset kosong")
        if "review_text" not in dataframe.columns:
            raise ValueError("Kolom review_text tidak ditemukan")

        return dataframe

    def analyze_dataframe(self, dataframe: pd.DataFrame):
        result_dataframe = dataframe.copy()
        result_dataframe["processed_text"] = None
        result_dataframe["predicted_sentiment"] = None

        hasil_analisis = []
        for index, value in result_dataframe["review_text"].items():
            if pd.isna(value) or not str(value).strip():
                continue

            try:
                hasil = self.model_analisis.analisis(Ulasan(str(value)))
            except ValueError:
                continue

            hasil_analisis.append(hasil)
            result_dataframe.at[index, "processed_text"] = hasil.processed_text
            result_dataframe.at[index, "predicted_sentiment"] = hasil.sentimen

        duplicate_count = int(
            result_dataframe["review_text"].astype(str).duplicated().sum()
        )
        laporan = Laporan(
            hasil_analisis,
            total_data=len(result_dataframe),
            data_duplikat=duplicate_count,
        )
        return result_dataframe, hasil_analisis, laporan

    def public_dataframe(self, dataframe: pd.DataFrame) -> pd.DataFrame:
        private = [
            column
            for column in dataframe.columns
            if column.lower() in self.PRIVATE_COLUMNS
        ]
        return dataframe.drop(columns=private, errors="ignore")

    @staticmethod
    def dataframe_to_records(dataframe: pd.DataFrame) -> list[dict]:
        safe = dataframe.astype(object).where(pd.notnull(dataframe), None)
        return safe.to_dict(orient="records")

    def to_csv_bytes(self, dataframe: pd.DataFrame) -> bytes:
        visible = self.public_dataframe(dataframe)
        csv_data = visible.to_csv(index=False, encoding="utf-8-sig")
        return csv_data.encode("utf-8-sig")
