from src.models.property.detected_food import DetectedFood


class AIService:
    def __init__(self, db_service):
        self._db_service = db_service

    async def scan_image(self, image) -> list[DetectedFood]:
        pass

