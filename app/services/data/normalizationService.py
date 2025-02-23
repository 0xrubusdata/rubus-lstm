from sqlmodel import Session
from app.utils.normalizer import Normalizer
from app.models import NormalizedData, DataPoint
import numpy as np

class NormalizationService:
    @staticmethod
    def normalize_data(data_points: list[DataPoint], session: Session):
        raw_prices = np.array([dp.adjusted_close for dp in data_points])
        scaler = Normalizer()
        normalized_prices = scaler.fit_transform(raw_prices)

        normalized_data = []
        for dp, norm_value in zip(data_points, normalized_prices):
            nd = NormalizedData(
                dataset_id=None,
                data_point_id=dp.id,
                normalized_value=float(norm_value)
            )
            session.add(nd)
            normalized_data.append(nd)
        session.commit()

        return {
            "scaler": scaler,
            "normalized_values": normalized_prices,
            "normalized_data": normalized_data
        }

normalization_service = NormalizationService()