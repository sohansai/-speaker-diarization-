import gradio as gr
from typing import Tuple, Any, Dict
from ..core.pipeline import DiarizationPipeline
from ..core.processor import AudioProcessor
from ..core.config import DiarizationConfig
from ..utils.logger import setup_logger
import os

logger = setup_logger()
logger.setLevel("CRITICAL")

def process_audio_file(audio: str, num_speakers: int, min_speakers: int, max_speakers: int, min_duration: float, handle_overlap: bool, diarization_pipeline: DiarizationPipeline,   audio_processor: AudioProcessor) -> Tuple[str, Any, dict]:
    try:
        temp_audio = audio_processor.save_audio(audio)
        
        config = DiarizationConfig(
            num_speakers=num_speakers,
            min_speakers=min_speakers,
            max_speakers=max_speakers,
            min_duration=min_duration,
            handle_overlap=handle_overlap
        )
        
        result = diarization_pipeline.process_audio(temp_audio, config)
        
        if "error" in result:
            return result["error"], None, {}
        
        labels_path = audio_processor.generate_labels(result)
        
        return (result["diarization_text"], labels_path, result["statistics"])
    except Exception as e:
        logger.error(f"Error in process_audio_file: {e}")
        return f"Error processing audio: {str(e)}", None, {}
    finally:
        if 'temp_audio' in locals():
            try:
                os.remove(temp_audio)
            except Exception as e:
                logger.error(f"Error removing temporary file: {e}")

def create_gradio_interface() -> gr.Blocks:
    diarization_pipeline = DiarizationPipeline()
    audio_processor = AudioProcessor()

    with gr.Blocks() as demo:
        gr.HTML("""
        <div style="display: flex; justify-content: center; align-items: center; flex-direction: column; font-family: Arial, sans-serif; line-height: 1.6; text-align: center; margin: 20px;">
            <h1 style="color: var(--primary-color, #4CAF50);">🗣️ Enhanced Speaker Diarization 3.1 🗣️</h1>

            <p style="font-size: 16px; max-width: 800px;">
                Upload an audio file to identify and separate different speakers using <b>pyannote.audio</b>, a state-of-the-art speaker diarization toolkit.
            </p>

            <hr style="border: 1px solid #ddd; width: 80%;">

            <h2 style="color: var(--secondary-color, #2196F3);">🎯 Features</h2>
            <ul style="list-style: none; padding: 0; text-align: left; max-width: 800px;">
                <li>
                    <span style="color: var(--bullet-color, #4CAF50);">●</span>
                    <b>Automatic Speaker Detection:</b> Automatically identify and label different speakers in your audio file without any prior information.
                </li>
                <li>
                    <span style="color: var(--bullet-color, #4CAF50);">●</span>
                    <b>Custom Speaker Count Configuration:</b> Specify the exact number of speakers, or set a range (minimum and maximum) for more control over the diarization process.
                </li>
                <li>
                    <span style="color: var(--bullet-color, #4CAF50);">●</span>
                    <b>Detailed Statistics and Analysis:</b> Comprehensive insights into the audio, including:
                    <ul style="list-style-type: disc; margin-left: 20px;">
                        <li>Total number of speakers.</li>
                        <li>Duration of each speaker's segments.</li>
                        <li>Percentage of speaking time for each speaker.</li>
                    </ul>
                </li>
                <li>
                    <span style="color: var(--bullet-color, #4CAF50);">●</span>
                    <b>DAW-Compatible Label Export:</b> Export speaker diarization results as label files for Digital Audio Workstations (DAWs).
                </li>
                <li>
                    <span style="color: var(--bullet-color, #4CAF50);">●</span>
                    <b>Real-Time Processing:</b> Process audio files efficiently with optional GPU acceleration.
                </li>
                <li>
                    <span style="color: var(--bullet-color, #4CAF50);">●</span>
                    <b>User-Friendly Interface:</b> An intuitive and easy-to-use design for both beginners and professionals.
                </li>
            </ul>

            <hr style="border: 1px solid #ddd; width: 80%;">

            <h2 style="color: var(--secondary-color, #2196F3);">📋 How to Use</h2>
            <ol style="text-align: left; max-width: 800px;">
                <li><b>Upload Audio File:</b> Click the "Upload Audio File" button to select your audio file (formats: WAV, MP3, etc.).</li>
                <li><b>Configure Settings (Optional):</b> Adjust parameters:
                    <ul>
                        <li>Number of Speakers: Set the exact number if known (otherwise leave as 0).</li>
                        <li>Minimum/Maximum Speakers: Define a range for speaker count (set to 0 if unknown).</li>
                        <li>Minimum Segment Duration: Adjust the minimum duration for speaker segments (default: 0.5 seconds).</li>
                        <li>Handle Speaker Overlap: Enable for overlapping speech segments.</li>
                    </ul>
                </li>
                <li><b>Process Audio:</b> Click the "Process Audio" button to start.</li>
                <li><b>View Results:</b> Access:
                    <ul>
                        <li>Diarization Output: Speaker-separated timeline in text format.</li>
                        <li>Analysis Statistics: Detailed speaker statistics and speaking times.</li>
                        <li>Download DAW Labels: Get a label file for DAWs.</li>
                    </ul>
                </li>
            </ol>

            <hr style="border: 1px solid #ddd; width: 80%;">

            <h2 style="color: var(--secondary-color, #F44336);">⚠️ Limitations</h2>
            <ul style="list-style: none; padding: 0; text-align: left; max-width: 800px;">
                <li>
                    <span style="color: var(--bullet-color, #FF5722);">●</span>
                    Performance depends on audio quality and background noise.
                </li>
                <li>
                    <span style="color: var(--bullet-color, #FF5722);">●</span>
                    Very long audio files may require significant processing time or resources.
                </li>
            </ul>

            <p style="font-size: 12px; color: #999;">
                <b>Note:</b> Ensure you have the necessary rights to process uploaded audio files. This tool is for educational, research, and professional use.
            </p>
        </div>
        """)

        with gr.Row():
            audio_input = gr.Audio(type="filepath", label="Upload Audio File")

        with gr.Row():
            with gr.Column():
                num_speakers = gr.Number(
                    label="Number of Speakers",
                    value=0,
                    info="Set the exact number if known, otherwise leave as 0"
                )
                min_speakers = gr.Number(
                    label="Minimum Speakers",
                    value=0,
                    info="Optional lower bound (leave as 0 if unknown)"
                )
                max_speakers = gr.Number(
                    label="Maximum Speakers",
                    value=0,
                    info="Optional upper bound (leave as 0 if unknown)"
                )

            with gr.Column():
                min_duration = gr.Slider(
                    minimum=0.1,
                    maximum=2.0,
                    value=0.5,
                    label="Minimum Segment Duration (seconds)"
                )
                handle_overlap = gr.Checkbox(
                    label="Handle Speaker Overlap",
                    value=True
                )

        process_button = gr.Button("Process Audio")
        
        with gr.Row():
            diarization_output = gr.Textbox(
                label="Diarization Output",
                lines=10
            )
            statistics_output = gr.JSON(
                label="Analysis Statistics"
            )
        
        label_file = gr.File(label="Download DAW Labels")

        process_button.click(
            fn=process_audio_file,
            inputs=[
                audio_input,
                num_speakers,
                min_speakers,
                max_speakers,
                min_duration,
                handle_overlap,
                gr.State(diarization_pipeline),  # Pass the pipeline as a state
                gr.State(audio_processor)  # Pass the processor as a state
            ],
            outputs=[
                diarization_output,
                label_file,
                statistics_output
            ]
        )

    return demo
