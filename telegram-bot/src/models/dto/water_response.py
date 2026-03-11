from dataclasses import dataclass

@dataclass
class WaterResponseDTO:
    day: str = None
    drunk_water: int = None