from domain.ulasan import Ulasan


class HasilAnalisis:
    """Objek hasil klasifikasi dari satu Ulasan."""

    def __init__(
        self,
        ulasan: Ulasan,
        processed_text: str,
        sentimen: str,
    ):
        self.ulasan = ulasan
        self.processed_text = processed_text
        self.sentimen = sentimen

    def to_dict(self) -> dict:
        return {
            "review_text": self.ulasan.review_text,
            "processed_text": self.processed_text,
            "predicted_sentiment": self.sentimen,
        }
