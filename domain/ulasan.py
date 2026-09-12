class Ulasan:
    """Objek domain yang mewakili satu ulasan film."""

    def __init__(self, review_text: str):
        self.review_text = str(review_text).strip()

    def is_valid(self) -> bool:
        return bool(self.review_text)

    def to_dict(self) -> dict:
        return {"review_text": self.review_text}
