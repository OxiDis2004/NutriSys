from asyncio import Queue

# from dynamic_det import detector


class AIService:
    def __init__(self, db_service):
        self._db_service = db_service
        # self.detector = detector()
        self.queue = Queue()

    # async def scan_image(self, image: UploadFile) -> list[DetectedFood]:
    #     image_bytes = await image.read()
    #     return self.detector(image_bytes)
