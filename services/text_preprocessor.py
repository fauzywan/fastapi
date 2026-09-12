import json
import re
from pathlib import Path

from Sastrawi.Stemmer.StemmerFactory import StemmerFactory


class TextPreprocessor:
    """Preprocessing SVM sesuai pipeline penelitian."""

    def __init__(self, slang_path: Path, stopwords_path: Path):
        self.slang_dict = self._load_json(slang_path)
        self.stop_words = set(self._load_json(stopwords_path))
        self.stemmer = StemmerFactory().create_stemmer()

    @staticmethod
    def _load_json(path: Path):
        with open(path, "r", encoding="utf-8") as file:
            return json.load(file)

    def preprocessing_umum(self, text: str) -> list[str]:
        text = re.sub(r"https?://\S+|www\.\S+", " ", str(text))
        text = re.sub(r"<.*?>", " ", text)
        text = text.lower()
        text = re.sub(r"[^\w\s]", " ", text, flags=re.UNICODE)
        text = re.sub(r"[\d_]+", " ", text)
        text = re.sub(r"\s+", " ", text).strip()
        return [self.slang_dict.get(token, token) for token in text.split()]

    def preprocessing_svm(self, tokens: list[str]) -> str:
        filtered = [token for token in tokens if token not in self.stop_words]
        return " ".join(self.stemmer.stem(token) for token in filtered).strip()

    def process(self, text: str) -> str:
        return self.preprocessing_svm(self.preprocessing_umum(text))
