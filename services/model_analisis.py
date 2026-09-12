import pickle
from pathlib import Path

from domain.hasil_analisis import HasilAnalisis
from domain.ulasan import Ulasan
from services.text_preprocessor import TextPreprocessor


class ModelAnalisis:
    """Mengelola TF-IDF + Linear SVM dan menghasilkan HasilAnalisis."""

    def __init__(
        self,
        model_path: Path,
        tfidf_path: Path,
        preprocessor: TextPreprocessor,
    ):
        self.nama_model = "Support Vector Machine"
        self.kode_model = "SVM"
        self.preprocessor = preprocessor
        self.model = self._load_pickle(model_path)
        self.tfidf = self._load_pickle(tfidf_path)

    @staticmethod
    def _load_pickle(path: Path):
        with open(path, "rb") as file:
            return pickle.load(file)

    def analisis(self, ulasan: Ulasan) -> HasilAnalisis:
        if not ulasan.is_valid():
            raise ValueError("review_text wajib diisi")

        processed_text = self.preprocessor.process(ulasan.review_text)
        if not processed_text:
            raise ValueError(
                "review_text tidak memiliki teks yang dapat dianalisis"
            )

        vector = self.tfidf.transform([processed_text])
        sentimen = str(self.model.predict(vector)[0])

        return HasilAnalisis(
            ulasan=ulasan,
            processed_text=processed_text,
            sentimen=sentimen,
        )
