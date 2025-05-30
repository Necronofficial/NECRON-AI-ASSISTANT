import pyttsx3

class TTS:
    def __init__(self):
        self.engine = pyttsx3.init()
        self._set_male_voice()
        self.engine.setProperty('rate', 190)  # Default speed for a natural, fast reply
        self.engine.setProperty('volume', 1.0) # Full volume

    def _set_male_voice(self):
        """Attempts to set a male voice, prioritizing English US voices."""
        voices = self.engine.getProperty('voices')
        male_voice_id = None
        
        # Try to find a male voice explicitly
        for voice in voices:
            # On Windows, names might contain "Zira" (female) or "David" (male)
            # On Linux/macOS, voice.name might indicate gender or specific IDs
            if "male" in voice.name.lower() or "david" in voice.name.lower():
                male_voice_id = voice.id
                break
        
        # If no explicit male voice found, try common English (US) voices and check ID
        if not male_voice_id:
            for voice in voices:
                if "en-us" in voice.id.lower() or "english" in voice.id.lower():
                    # This is a heuristic, not guaranteed to be male
                    # You might need to test which voice IDs sound male on your system
                    male_voice_id = voice.id
                    break

        if male_voice_id:
            self.engine.setProperty('voice', male_voice_id)
            print(f"TTS Module: Using voice: {self.engine.getProperty('voice')}")
        else:
            print("TTS Module: Warning: Could not find a suitable male voice. Using default system voice.")

    def speak(self, text, speed="normal"):
        if text.strip() == "":
            return

        # Adjust speech rate based on requested speed
        if speed == "fast":
            self.engine.setProperty('rate', 250) # Faster rate
        elif speed == "slow":
            self.engine.setProperty('rate', 120) # Slower rate
        else:
            self.engine.setProperty('rate', 190) # Default normal rate

        self.engine.say(text)
        self.engine.runAndWait()
        self.engine.setProperty('rate', 190) # Reset to default after speaking
