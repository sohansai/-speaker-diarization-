import torch
from pyannote.audio import Pipeline
import os
from datetime import timedelta
from typing import Optional, Dict, Any
from .config import DiarizationConfig
from ..utils.logger import setup_logger

# Setup logger
logger = setup_logger()

class DiarizationPipeline:
    def __init__(self):
        # Initialize pipeline
        self.pipeline = self._initialize_pipeline()
        # Set device
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        if self.pipeline:
            # Move pipeline to device
            self.pipeline.to(self.device)
    
    def _initialize_pipeline(self) -> Optional[Pipeline]:
        try:
            # Load pretrained pipeline
            pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization-3.1", use_auth_token=os.environ.get("HUGGINGFACE_READ_TOKEN"))
            logger.info("Pipeline initialized successfully")
            return pipeline
        except Exception as e:
            logger.error(f"Failed to initialize pipeline: {e}")
            return None

    def process_audio(self, audio_path: str, config: DiarizationConfig) -> Dict[str, Any]:
        if not self.pipeline:
            return {"error": "Pipeline not initialized"}

        try:
            # Build params
            params = self._build_diarization_params(config)
            # Perform diarization
            diarization = self.pipeline(audio_path, **params)
            
            result = {
                "diarization_text": self._format_diarization_output(diarization),
                "segments": self._extract_segments(diarization),
                "statistics": self._calculate_statistics(diarization)
            }
            return result
        except Exception as e:
            logger.error(f"Error processing audio: {e}")
            return {"error": f"Processing failed: {str(e)}"}

    def _build_diarization_params(self, config: DiarizationConfig) -> dict:
        params = {}
        # Set num speakers
        if config.num_speakers > 0:
            params["num_speakers"] = config.num_speakers
        # Set min speakers
        if config.min_speakers > 0:
            params["min_speakers"] = config.min_speakers
        # Set max speakers
        if config.max_speakers > 0:
            params["max_speakers"] = config.max_speakers
        
        return params

    @staticmethod
    def _format_diarization_output(diarization) -> str:
        formatted_output = []
        # Iterate through turns
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            start_time = str(timedelta(seconds=turn.start)).split('.')[0]
            end_time = str(timedelta(seconds=turn.end)).split('.')[0]
            # Append formatted output
            formatted_output.append(f"[{start_time} --> {end_time}] {speaker}")
        return "\n".join(formatted_output)

    @staticmethod
    def _extract_segments(diarization) -> list:
        segments = []
        # Extract segment details
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            segments.append({"start": turn.start, "end": turn.end, "duration": turn.end - turn.start, "speaker": speaker})
        return segments

    @staticmethod
    def _calculate_statistics(diarization) -> dict:
        speakers = set()
        total_duration = 0
        speaker_durations = {}

        # Calculate speaker stats
        for turn, _, speaker in diarization.itertracks(yield_label=True):
            duration = turn.end - turn.start
            speakers.add(speaker)
            total_duration += duration
            speaker_durations[speaker] = speaker_durations.get(speaker, 0) + duration

        return {
            "total_speakers": len(speakers),
            "total_duration": total_duration,
            "speaker_durations": speaker_durations,
            "speaker_percentages": {
                speaker: (duration / total_duration) * 100 
                for speaker, duration in speaker_durations.items()
            }
        }
