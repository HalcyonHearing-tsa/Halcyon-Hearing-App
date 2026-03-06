import whisper
import numpy as np
import pyaudio
import threading
import torch

class Transcription():
    def __init__(self):
        
        self.audio_model = whisper.load_model("base")
        self.stop_event = threading.Event()
        
        
    def helperTranscription(self,callback_function):
        self.callback = callback_function
        self.thread = threading.Thread(target=self.live_transcription,daemon=True)
        self.thread.start()
        self.stop_event.clear()
        self.start_Trans = False
    
    def live_transcription(self):
        """Reads user input as raw audio tensor, using Silvero VAD creates a confidence threshold of 0.5 
        to filter background noice, any value greater is passed as a balid speech to the Whisper transcription model. """
        
        model, utils = torch.hub.load(repo_or_dir='snakers4/silero-vad',
                              model='silero_vad',
                              force_reload=False)
        (get_speech_timestamps, _, read_audio, VADIterator, _) = utils


        #Configuration for PyAudio
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 16000
        CHUNK = 512
        
        self.speech_buffer = []
        is_speaking = False

        p = pyaudio.PyAudio()
        stream = p.open(format=FORMAT, channels=CHANNELS,
                        rate=RATE, input=True,
                        frames_per_buffer=CHUNK)
        

        while not self.stop_event.is_set():

            
            audio_chunk = stream.read(CHUNK, exception_on_overflow=False)
            
            audio_int16 = np.frombuffer(audio_chunk, np.int16)
            #Normalizes the 16-bit integer audio into a 32-bit float for the AI model
            audio_float32 = audio_int16.astype(np.float32) / 32768.0
            
            new_confidence = model(torch.from_numpy(audio_float32), 16000).item()

            if new_confidence > 0.5:
                if not is_speaking:
                    is_speaking = True
                self.speech_buffer.append(audio_int16)
            if self.stop_event.is_set():
                if is_speaking:
                    self.speech_buffer.append(audio_int16)
                    if self.start_Trans:
                        is_speaking = False
                        
                        full_audio_data = np.concatenate(self.speech_buffer)
                        self.speech_buffer = [] 
                        
                        audio_np = full_audio_data.astype(np.float32) / 32768.0
                        
                        
                        result = self.audio_model.transcribe(audio_np, fp16=torch.cuda.is_available())
                        text = result['text'].strip()
                        
                        
                        if text and len(text) > 1:
                            self.callback(f"Transcript: {result['text']}\n")
                            self.start_Trans = False
                        
                          
                        else:
                            self.callback(f"Transcript: ...\n")
                            self.start_Trans = False
                break
                        
            
        stream.stop_stream()
        stream.close()
        p.terminate()
        
        
    def transcription(self,filename):
        audio=self.audio_model.transcribe(filename)
        return audio