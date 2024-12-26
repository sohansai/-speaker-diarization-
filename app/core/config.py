from dataclasses import dataclass

@dataclass
class DiarizationConfig:
    # Configuration class for diarization parameters
    num_speakers: int = 0
    min_speakers: int = 0
    max_speakers: int = 0
    min_duration: float = 0.5
    handle_overlap: bool = True