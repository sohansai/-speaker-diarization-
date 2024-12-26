import tempfile  
from pathlib import Path  
import os  
from typing import Optional, Dict, Any  
from ..utils.logger import setup_logger

logger = setup_logger()  # Initialize logger

class AudioProcessor:
    @staticmethod
    def save_audio(audio_file: str) -> str:
        try:
            temp_dir = tempfile.mkdtemp()  # Create temp directory
            temp_path = Path(temp_dir) / "temp_audio.wav"  # Temp file path
            
            with open(audio_file, "rb") as src, open(temp_path, "wb") as dst:
                dst.write(src.read())  # Copy audio content
            
            return str(temp_path)

        except Exception as e:
            logger.error(f"Error saving audio: {e}") 
            raise

    @staticmethod
    def generate_labels(diarization_result: Dict[str, Any], output_path: str = "labels.txt") -> Optional[str]:
        try:
            if "segments" not in diarization_result:  # Check for segments
                return None  # No segments found

            with open(output_path, "w") as f:
                for segment in diarization_result["segments"]:  # Write segments
                    f.write(f"{segment['start']:.3f}\t{segment['end']:.3f}\t{segment['speaker']}\n")
            
            return output_path  # Return path to labels
        except Exception as e:
            logger.error(f"Error generating labels: {e}")
            return None 
