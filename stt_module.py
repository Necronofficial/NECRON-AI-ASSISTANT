import speech_recognition as sr
import time

class STT:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        # You can adjust these for better performance or specific environments
        # self.recognizer.energy_threshold = 300 # Adjust if too sensitive or not sensitive enough
        # self.recognizer.pause_threshold = 0.8 # Seconds of non-speaking audio before a phrase is considered complete

    def listen_and_transcribe_realtime(self):
        with sr.Microphone() as source:
            self.recognizer.adjust_for_ambient_noise(source, duration=1) # Adjust for noise once
            print("STT Module: Listening...")
            try:
                audio = self.recognizer.listen(source, timeout=5, phrase_time_limit=5) # Listen for a phrase
                print("STT Module: Processing audio...")
                # Using Google Web Speech API (online) for simplicity.
                # For offline, use Vosk or Whisper (more setup required).
                text = self.recognizer.recognize_google(audio, language="en-IN") # You can specify language
                print(f"STT Module: Transcribed: {text}")
                return text
            except sr.WaitTimeoutError:
                print("STT Module: No speech detected within timeout.")
                return ""
            except sr.UnknownValueError:
                print("STT Module: Could not understand audio.")
                return ""
            except sr.RequestError as e:
                print(f"STT Module: Could not request results from Google Speech Recognition service; {e}")
                return ""

# Note: For Vosk or Whisper, the implementation would be more complex,
# involving downloading models and potentially handling audio streams directly.
# Example for Vosk (conceptual, requires Vosk model download):
# from vosk import Model, KaldiRecognizer
# import sounddevice as sd
# import queue
# class STT_Vosk:
#     def __init__(self, model_path="path/to/vosk-model-en-us-0.22"):
#         self.model = Model(model_path)
#         self.q = queue.Queue()
#         self.recognizer = KaldiRecognizer(self.model, 16000) # Sample rate
#     def callback(self, indata, frames, time, status):
#         self.q.put(bytes(indata))
#     def listen_and_transcribe_realtime(self):
#         with sd.RawInputStream(samplerate=16000, blocksize=8000,
#                                dtype='int16', channels=1,
#                                callback=self.callback):
#             while True:
#                 data = self.q.get()
#                 if self.recognizer.AcceptWaveform(data):
#                     result = json.loads(self.recognizer.Result())
#                     text = result.get('text', '')
#                     if text:
#                         return text
