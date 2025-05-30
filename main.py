import os
import threading
import time
import queue
import random
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Import modules from the 'modules' package
from modules.stt_module import STT
from modules.tts_module import TTS
from modules.decision_maker_module import DecisionMaker
from modules.automation_module import AutomationHandler
from modules.chat_memory_module import init_db, save_chat, get_chat_history, get_user_name_from_voice_sample, set_user_automation_permission, get_user_automation_permission
from modules.image_generation_module import ImageGenerator # Even if placeholder for now

# Import UI module if using a GUI
# from ui.siriraj_ui import SIRIRAJ_UI
# from PyQt5.QtWidgets import QApplication # Only if using PyQt5

# --- Configuration ---
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
ASSISTANT_NAME = "Siriraj"
USERNAME = "Sir" # Default, can be personalized later

# --- Global Queues for Multitasking ---
task_queue = queue.Queue() # To hold tasks for processing
response_queue = queue.Queue() # To hold responses for TTS/UI display

# --- Main SIRIRAJ AI Logic ---
class SIRIRAJ:
    def __init__(self):
        init_db() # Initialize the database
        self.stt_engine = STT()
        self.tts_engine = TTS()
        self.decision_maker = DecisionMaker(GROQ_API_KEY, ASSISTANT_NAME, USERNAME)
        self.automation_handler = AutomationHandler(self.tts_engine, get_user_automation_permission, set_user_automation_permission)
        self.image_generator = ImageGenerator() # Initialize image generation
        self.is_speaking = False
        self.mic_on = True # Tracks microphone state
        self.speaker_on = True # Tracks speaker state (for voice output)
        self.user_name = USERNAME # Current recognized user

        # Responses for long output
        self.long_responses = [
            "The rest of the result has been printed to the chat screen, kindly check it out sir.",
            "The rest of the text is now on the chat screen, sir, please check it.",
            "You can see the rest of the text on the chat screen, sir.",
            "The remaining part of the text is now on the chat screen, sir.",
            "Sir, you'll find more text on the chat screen for you to see.",
            "The rest of the answer is now on the chat screen, sir.",
            "Sir, please look at the chat screen, the rest of the answer is there.",
            "You'll find the complete answer on the chat screen, sir.",
            "The next part of the text is on the chat screen, sir.",
            "Sir, please check the chat screen for more information.",
            "There's more text on the chat screen for you, sir.",
            "The chat screen has the rest of the text, sir.",
            "There's more to see on the chat screen, sir, please look.",
            "Sir, the chat screen holds the continuation of the text.",
            "You'll find the complete answer on the chat screen, kindly check it out sir.",
            "Please review the chat screen for the rest of the text, sir.",
            "Sir, look at the chat screen for the complete answer."
        ]
        self.current_query = "" # To store the current query for chat history

    def _handle_response(self, response_text, speed="normal"):
        save_chat(self.current_query, response_text) # Save interaction
        if len(response_text) > 500: # Example: If response is too long
            short_response = response_text[:200] + "..."
            long_response_message = random.choice(self.long_responses)
            if self.speaker_on:
                self.tts_engine.speak(f"{short_response} {long_response_message}", speed=speed)
            # In a real UI, you'd send the full response_text to update the chat display
            print(f"UI_DISPLAY (Full): {response_text}")
        else:
            if self.speaker_on:
                self.tts_engine.speak(response_text, speed=speed)
            print(f"UI_DISPLAY: {response_text}")

    def process_query(self, query):
        if not query.strip():
            return

        self.current_query = query # Store current query for saving chat history

        # Basic Emotion recognition (can be expanded)
        lower_query = query.lower()
        if any(word in lower_query for word in ["sad", "unhappy", "depressed"]):
            self.tts_engine.speak(f"I sense you might be feeling down, {self.user_name}. Is there anything I can do to help?", speed="slow")
        elif any(word in lower_query for word in ["happy", "great", "wonderful"]):
            self.tts_engine.speak(f"That's wonderful to hear, {self.user_name}!", speed="fast")

        # Get decision from the Decision Maker
        decision_output = self.decision_maker.decide_query_type(query)

        # Extract decision type and actual query from the decision output
        try:
            parts = decision_output.split(' ', 1)
            decision_type = parts[0].strip()
            actual_query = parts[1].strip() if len(parts) > 1 else ""
        except IndexError:
            decision_type = "general" # Fallback
            actual_query = query

        # Handle multiple automation tasks in one go
        if "," in actual_query and decision_type in ["open", "close", "play", "generate image", "system", "content", "google search", "Youtube"]:
            self.tts_engine.speak("Performing multiple tasks simultaneously, Sir.")
            tasks = decision_output.split(', ')
            for task in tasks:
                task_parts = task.split(' ', 1)
                task_type = task_parts[0].strip()
                task_query = task_parts[1].strip() if len(task_parts) > 1 else ""
                task_queue.put((task_type, task_query, self.user_name))
        else:
            task_queue.put((decision_type, actual_query, self.user_name))

    def process_tasks(self):
        while True:
            if not task_queue.empty():
                decision_type, actual_query, current_user = task_queue.get()
                print(f"Processing task: Type='{decision_type}', Query='{actual_query}'")

                if decision_type == "general":
                    response = self.decision_maker.get_llm_response(actual_query, get_chat_history)
                    self._handle_response(response, speed="fast")
                elif decision_type == "realtime":
                    response = self.decision_maker.get_realtime_response(actual_query)
                    self._handle_response(response, speed="fast")
                elif decision_type == "generate image":
                    image_result = self.image_generator.generate_image(actual_query)
                    if image_result:
                        self.tts_engine.speak(f"Image for '{actual_query}' has been generated, Sir. Please check the chat screen.", speed="fast")
                        print(f"UI_DISPLAY (Image Path): {image_result}") # Simulate UI update
                    else:
                        self.tts_engine.speak(f"Sorry, I couldn't generate an image for '{actual_query}' right now.", speed="slow")
                elif decision_type in ["open", "close", "play", "reminder", "system", "content", "google search", "Youtube"]:
                    self.automation_handler.perform_automation_task(decision_type, actual_query, current_user, self.tts_engine, self.decision_maker, self.image_generator)
                elif decision_type == "exit":
                    self.tts_engine.speak("Goodbye, Sir. Have a great day!")
                    print("Exiting SIRIRAJ.")
                    os._exit(0)
                else:
                    response = "I am not sure how to handle that query, Sir. Could you please rephrase?"
                    self._handle_response(response, speed="slow")
            time.sleep(0.1) # Prevent busy-waiting

    def start(self):
        self.tts_engine.speak(f"Hello, I am {ASSISTANT_NAME}. How can I assist you today, {self.user_name}?")

        # Start a separate thread for processing tasks
        task_processor_thread = threading.Thread(target=self.process_tasks)
        task_processor_thread.daemon = True
        task_processor_thread.start()

        # Main loop for listening (or UI input)
        # For demonstration, we'll use console input.
        # In a real UI, this would be triggered by mic input or text input events.
        print(f"\n{ASSISTANT_NAME}: Listening for your query...")
        while True:
            try:
                if self.mic_on:
                    # This will be blocking until user speaks, or needs to be in a separate thread
                    print("Listening... (Type 'exit' to quit)")
                    query = self.stt_engine.listen_and_transcribe_realtime() # This should return text
                    if query:
                        print(f"You (Voice): {query}")
                        # Simulate user recognition (complex, requires advanced models)
                        # self.user_name = get_user_name_from_voice_sample(audio_data_of_query) # Pass raw audio if STT provides it
                        self.process_query(query)
                else:
                    text_input = input("You (text input): ")
                    if text_input.lower() == 'exit':
                        self.process_query("exit") # Send exit command
                    else:
                        self.process_query(text_input)
            except KeyboardInterrupt:
                print("\nSiriraj: Exiting initiated by user.")
                self.tts_engine.speak("Exiting, Sir. Have a good day.")
                sys.exit(0) # Clean exit

if __name__ == "__main__":
    siriraj_instance = Siriraj()
    siriraj_instance.start()
