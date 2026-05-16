from asyncio import Queue

from dynamic_det import detector, DetectorModul
from fastapi import UploadFile

from src.services.db_service import DBService


class AIService:
    def __init__(self, db_service: DBService):
        self._db_service: DBService = db_service
        self.detector: DetectorModul = detector()
        self.queue = Queue()

    async def scan_image(self, image: UploadFile) -> list[str]:
        image_bytes = await image.read()
        return [detection.name for detection in self.detector.predict(image_bytes)]
