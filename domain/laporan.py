from collections import Counter
from datetime import datetime, timezone

from domain.hasil_analisis import HasilAnalisis


class Laporan:
    """Merangkum kumpulan HasilAnalisis menjadi statistik sentimen."""

    LABELS = ("positif", "netral", "negatif")

    def __init__(
        self,
        hasil: list[HasilAnalisis],
        total_data: int | None = None,
        data_duplikat: int = 0,
    ):
        self.hasil = hasil
        self.total_data = total_data if total_data is not None else len(hasil)
        self.data_duplikat = int(data_duplikat)
        self.dibuat_pada = datetime.now(timezone.utc)

    def generate(self) -> dict:
        counts = Counter(
            item.sentimen.lower()
            for item in self.hasil
            if item.sentimen
        )

        total_dianalisis = len(self.hasil)
        ringkasan = {
            "total_data": int(self.total_data),
            "total_dianalisis": int(total_dianalisis),
            "total_tidak_dianalisis": int(self.total_data - total_dianalisis),
            "data_duplikat": self.data_duplikat,
        }

        for label in self.LABELS:
            jumlah = int(counts.get(label, 0))
            ringkasan[label] = jumlah
            ringkasan[f"persentase_{label}"] = (
                round(jumlah / total_dianalisis * 100, 2)
                if total_dianalisis
                else 0
            )

        return ringkasan

    def to_dict(self) -> dict:
        return {
            "dibuat_pada": self.dibuat_pada.isoformat(),
            "ringkasan": self.generate(),
        }
