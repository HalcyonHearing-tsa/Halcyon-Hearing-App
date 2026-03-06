# Halcyon Hearing

An accessibility application featuring real-time ASL interpretation and live audio transcription.

## Attributions & Open Source Technologies
As the systems integrator for this project, I used several open-source libraries and models to build the core architecture:
* **GUI Framework:** User interface built with `CustomTkinter`.
* **Audio Engine:** Non-blocking hardware audio playback managed via `pygame`.
* **Computer Vision:** Camera frame processing and ROI matrix slicing handled by `OpenCV`.
* **Machine Learning:** Live Transcription powered by **OpenAI Whisper**.
  * Audio noise-filtering and gatekeeping powered by **Silero VAD**.
  * ASL interpretation powered by a standard PyTorch inference model.
* **To run this application, you must install the following dependencies via terminal:**
* `pip install customtkinter`
* `pip install opencv-python`
* `pip install pygame`
* `pip install torch torchvision torchaudio`
* `pip install openai-whisper`
* `pip install pywin32`
* `pip install transformer`
* `pip install numpy`
* `pip install pyaudio`







