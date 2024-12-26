# Speaker Diarization

This project provides a user-friendly interface for speaker diarization using the `pyannote.audio` toolkit. It allows you to upload an audio file, identify speakers, and export the results in a DAW-compatible format.

## Features
- Automatic Speaker Detection
- Custom Speaker Count Configuration
- Detailed Statistics and Analysis
- DAW-Compatible Label Export
- Real-Time Processing

## Prerequisites
Before running the project, ensure you have the following installed:

1. **Python 3.8 or higher**
2. **pip** (Python package manager)
3. **Git** (optional, for cloning the repository)

## Installation

### 1. Clone the Repository
```bash
git clone https://github.com/sohansai/speaker-diarization.git
cd speaker-diarization
```
### 2. Create a Virtual Environment

To isolate the project dependencies, create a virtual environment:
```bash
python -m venv venv
```

### 3. Activate the Virtual Environment

Activate the virtual environment based on your operating system:

-   **Windows:**
```bash
    venv\Scripts\activate
```
-   **macOS/Linux:**
```bash
    source venv/bin/activate
```
### 4. Install Dependencies

Install the required Python packages using the `requirements.txt` file:
```bash
pip install -r requirements.txt
```

### 5. Set Up Hugging Face Token

The project uses the `pyannote/speaker-diarization-3.1` model, which requires a Hugging Face token.

1.  Create a Hugging Face account if you don't have one: [Hugging Face](https://huggingface.co/).

2.  Generate a read token from your Hugging Face account settings.

3.  Set the token as an environment variable:

    -   **Windows:**
        ```bash
        set HUGGINGFACE_READ_TOKEN=your_token_here
        ```
    -   **macOS/Linux:**
        ```bash
        export HUGGINGFACE_READ_TOKEN=your_token_here
        ```
Running the Application
-----------------------

### 1. Start the Application

Run the following command to start the Gradio interface:
```bash
python app.py
```
### 2\. Access the Interface

After running the Gradio app with `python app.py`, Gradio will usually display the URL directly in your terminal or command prompt. You should see something like:
```bash
http://127.0.0.1:7860
```
### 3. Use the Interface

-   **Upload Audio File:** Click the "Upload Audio File" button to select your audio file (supported formats: WAV, MP3, etc.).

-   **Configure Settings (Optional):**

    -   **Number of Speakers:** Set the exact number of speakers if known (otherwise leave as 0).

    -   **Minimum/Maximum Speakers:** Define a range for the number of speakers (set to 0 if unknown).

    -   **Minimum Segment Duration:** Adjust the minimum duration for speaker segments (default: 0.5 seconds).

    -   **Handle Speaker Overlap:** Enable this option to handle overlapping speech segments.

-   **Process Audio:** Click the "Process Audio" button to start the diarization process.

-   **View Results:**

    -   **Diarization Output:** See the speaker-separated timeline in text format.

    -   **Analysis Statistics:** View detailed statistics about the speakers and their speaking times.

    -   **Download DAW Labels:** Download the label file for use in your DAW.

Project Structure
-----------------

```bash

speaker-diarization/
├── app/                     # Main application package
│   ├── __init__.py          # Initializes the app package
│   ├── core/                # Core functionality of the application
│   │   ├── __init__.py      # Initializes the core package
│   │   ├── pipeline.py      # Handles the speaker diarization pipeline logic
│   │   ├── processor.py     # Manages audio processing utilities
│   │   └── config.py        # Configuration settings for diarization
│   ├── ui/                  # User interface components
│   │   ├── __init__.py      # Initializes the ui package
│   │   └── interface.py     # Gradio interface setup and logic
│   └── utils/               # Utility functions and helpers
│       ├── __init__.py      # Initializes the utils package
│       └── logger.py        # Logging configuration and utilities
├── app.py                   # Main entry point for the application
├── requirements.txt         # Lists all Python dependencies for the project
├── README.md                # Project documentation and setup instructions
└── .env                     # Environment variables (Hugging Face token)
```
Troubleshooting
---------------

-   **GPU Support:** Ensure you have CUDA installed if you want to use GPU acceleration.

-   **Long Audio Files:** For very long audio files, consider using a machine with a GPU for faster processing.

-   **Hugging Face Token:** Ensure the token is correctly set as an environment variable.

License
-------

This project is licensed under the MIT License. See the [LICENSE](https://github.com/sohansai/speaker-diarization/blob/main/LICENSE) file for details.

Acknowledgments
---------------

-   [pyannote.audio](https://github.com/pyannote/pyannote-audio) for the speaker diarization model.

-   [Gradio](https://gradio.app/) for the user interface.

* * * * *

**Note:** This project is for educational and research purposes. Ensure you have the necessary rights to process and analyze the uploaded audio files.
