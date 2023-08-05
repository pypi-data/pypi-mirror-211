from dataclasses import dataclass


@dataclass
class UULE_A:
    latitude: float
    longitude: float
    role: int
    provenance: int
    timestamp: int
    radius: float
