#automation_module.py

import os
import subprocess
import platform
import pyautogui
import time # For delays in automation actions
import webbrowser

class AutomationHandler:
    def __init__(self, tts_engine, get_permission_func, set_permission_func):
        self.tts = tts_engine
        self.os_type = platform.system() # 'Windows', 'Linux', 'Darwin' (macOS)
        self.get_automation_permission = get_permission_func
        self.set_automation_permission = set_permission_func

    def _check_and_request_permission(self, user_name):
        permission_granted = self.get_automation_permission(user_name)
        if not permission_granted:
            self.tts.speak(f"Sir, you have not granted me full automation control. Would you like to enable it now? This will allow me to perform tasks like opening applications, setting reminders, and controlling system settings for you. Please type 'yes' or 'no' in the chat to grant permission.", speed="slow")
            # In a real UI, this would show a prompt. For console, we need input.
            print("SIRIRAJ: Please type 'yes' or 'no' in the chat to grant automation permission.")
            # This is a blocking input for demonstration. In UI, it would be an event handler.
            # You'll need to pass the user's response back to this module or handle it in main.py
            # For simplicity in this structure, we'll assume a 'yes' if not explicitly set.
            # A better way would be to have UI button callbacks that call set_automation_permission.
            # For now, we'll simulate it or default to false.
            # Example of getting input (would block execution):
            # response = input("Grant automation permission? (yes/no): ").lower()
            # if response == 'yes':
            #     self.set_automation_permission(user_name, True)
            #     self.tts.speak("Thank you, Sir! Automation control granted.", speed="fast")
            #     return True
            # else:
            #     self.tts.speak("Understood, Sir. I cannot perform this automation without permission.", speed="slow")
            #     return False
            
            # Defaulting to False if not explicitly set by user. UI would manage this.
            return False 
        return True


    def _open_application(self, app_name, user_name):
        if not self._check_and_request_permission(user_name):
            return

        print(f"Automation: Attempting to open '{app_name}' on {self.os_type}")
        self.tts.speak(f"Opening {app_name}, Sir.", speed="fast")

        try:
            if self.os_type == "Windows":
                # Try opening as a process, then as a shell command
                try:
                    subprocess.Popen(app_name, shell=False) # Try direct executable name
                except FileNotFoundError:
                    subprocess.Popen(f"start {app_name}", shell=True) # Try Windows 'start' command
                except Exception:
                    # Fallback for common apps
                    if "chrome" in app_name.lower(): webbrowser.open("chrome://newtab")
                    elif "firefox" in app_name.lower(): webbrowser.open("about:home")
                    elif "notepad" in app_name.lower(): subprocess.Popen("notepad.exe", shell=False)
                    elif "facebook" in app_name.lower(): webbrowser.open("https://www.facebook.com")
                    elif "instagram" in app_name.lower(): webbrowser.open("https://www.instagram.com")
                    else:
                        raise Exception("Generic open failed")

            elif self.os_type == "Darwin": # macOS
                subprocess.Popen(['open', '-a', app_name])
            elif self.os_type == "Linux":
                subprocess.Popen([app_name.lower().replace(" ", "")]) # Try common executable names (e.g., 'firefox', 'gnome-terminal')
            else:
                self.tts.speak(f"I cannot perform this action on your operating system ({self.os_type}) yet, Sir.", speed="slow")
                return

            self.tts.speak(f"{app_name} opened successfully, Sir.", speed="fast")
        except Exception as e:
            self.tts.speak(f"Sorry, I couldn't open {app_name}. Error: {e}", speed="slow")
            print(f"Automation Error: Could not open {app_name}: {e}")

    def _close_application(self, app_name, user_name):
        if not self._check_and_request_permission(user_name):
            return

        self.tts.speak(f"Attempting to close {app_name}, Sir. This feature is under development for robust cross-platform closing.", speed="slow")
        # Closing applications reliably across OS is complex.
        # On Windows: taskkill /f /im process_name.exe
        # On Linux/macOS: killall process_name
        # pyautogui.hotkey('alt', 'f4') can close active window, but not specific app in background.
        print(f"Automation: Closing '{app_name}' (placeholder)")

    def _play_song(self, song_name, user_name):
        if not self._check_and_request_permission(user_name):
            return

        self.tts.speak(f"Searching for '{song_name}' on YouTube and playing, Sir.", speed="fast")
        webbrowser.open(f"https://www.youtube.com/results?search_query={song_name}")
        # For more direct playback, you'd need YouTube Data API or other music service APIs
        # and potentially a media player integration.

    def _set_reminder(self, reminder_data, user_name):
        if not self._check_and_request_permission(user_name):
            return

        # Parse reminder_data (e.g., "9:00pm 25th june business meeting")
        # This requires robust date/time parsing. Example:
        # from datetime import datetime
        # try:
        #     # Example simple parsing, needs more advanced NLP for flexible inputs
        #     parts = reminder_data.split(' for ', 1)
        #     time_date_str = parts[0].strip()
        #     message = parts[1].strip() if len(parts) > 1 else "Reminder"
        #     # Assuming '9:00pm 25th june' -> '2025-06-25 21:00:00'
        #     # This parsing logic is complex and needs libraries like 'dateparser' or custom regex
        #     self.tts.speak(f"Reminder set for {time_date_str} for: {message}. I will notify you, Sir.", speed="fast")
        #     print(f"Automation: Reminder set for {time_date_str} for {message}")
        # except Exception as e:
        #     self.tts.speak(f"Sorry, I couldn't set the reminder. Please provide the time and date clearly.", speed="slow")
        #     print(f"Automation Error: Reminder parsing failed: {e}")
        self.tts.speak(f"Reminder for {reminder_data} acknowledged, Sir. (Detailed parsing and scheduling needed)", speed="fast")

    def _system_task(self, task_name, user_name):
        if not self._check_and_request_permission(user_name):
            return

        print(f"Automation: Performing system task: {task_name}")
        if "mute" in task_name.lower():
            self.tts.speak("Muting system audio, Sir.", speed="fast")
            # pyautogui.press('volumemute') # This usually works
        elif "unmute" in task_name.lower():
            self.tts.speak("Unmuting system audio, Sir.", speed="fast")
            # pyautogui.press('volumemute') # Toggling mute
        elif "volume up" in task_name.lower() or "increase volume" in task_name.lower():
            self.tts.speak("Increasing volume, Sir.", speed="fast")
            for _ in range(5): # Press volume up key multiple times
                pyautogui.press('volumeup')
                time.sleep(0.1)
        elif "volume down" in task_name.lower() or "decrease volume" in task_name.lower():
            self.tts.speak("Decreasing volume, Sir.", speed="fast")
            for _ in range(5): # Press volume down key multiple times
                pyautogui.press('volumedown')
                time.sleep(0.1)
        else:
            self.tts.speak(f"I don't recognize the system task: {task_name}, Sir.", speed="slow")

    def _write_content(self, topic, user_name, decision_maker_instance):
        if not self._check_and_request_permission(user_name):
            return
        self.tts.speak(f"I can help you write content about '{topic}', Sir. Please provide more details or let me generate a draft.", speed="fast")
        print(f"Automation: Generating content for '{topic}'")
        
        # Use the LLM to generate content
        generated_text = decision_maker_instance.get_llm_response(f"Write a detailed piece of content about {topic}. Make it professional and comprehensive.", lambda x: []) # Pass a dummy chat history func
        
        self.tts.speak(f"I have generated content about {topic}, Sir. It has been printed to the chat screen.", speed="fast")
        print(f"Generated Content for '{topic}':\n{generated_text}")
        
        # Optionally, automate opening notepad and pasting (OS-specific and complex)
        # if self.os_type == "Windows":
        #     subprocess.Popen("notepad.exe")
        #     time.sleep(2) # Give time for notepad to open
        #     pyautogui.typewrite(generated_text)


    def _Google Search(self, topic, user_name):
        if not self._check_and_request_permission(user_name):
            return
        self.tts.speak(f"Searching Google for '{topic}', Sir. Opening your default browser now.", speed="fast")
        webbrowser.open(f"https://www.google.com/search?q={topic}")

    def _Youtube(self, topic, user_name):
        if not self._check_and_request_permission(user_name):
            return
        self.tts.speak(f"Searching YouTube for '{topic}', Sir. Opening your default browser now.", speed="fast")
        webbrowser.open(f"https://www.youtube.com/results?search_query={topic}")
    
    # New: Automate Instagram/Facebook Post (Highly complex and requires APIs or advanced UI automation)
    def _post_on_social_media(self, platform_name, account_name, text_content, style, image_path=None, user_name=None):
        if not self._check_and_request_permission(user_name):
            return
        self.tts.speak(f"Automating a post on {platform_name} for account {account_name}, Sir. This is a very advanced feature and requires specific API integrations or complex UI automation, which I am still learning to perform reliably.", speed="slow")
        print(f"Automation: Attempting to post on {platform_name}. Content: '{text_content}', Style: '{style}'")
        # This would involve:
        # 1. Using a social media API (e.g., Instagram Graph API, Facebook Graph API - requires developer setup, app review, etc.)
        # 2. Or, highly complex pyautogui scripting to navigate browser, login, paste text, upload image.
        # This is generally outside the scope of a basic AI assistant and requires dedicated development.

    def perform_automation_task(self, decision_type, query_data, user_name, tts_engine, decision_maker_instance, image_generator_instance):
        # The main entry point for automation tasks
        
        # Handle the specific social media posting request
        if "post" in decision_type and ("instagram" in query_data.lower() or "facebook" in query_data.lower()):
            # This is a very complex request. We need to parse: platform, account, content, style, image
            # The decision_maker might only give "content (topic)" or "open (instagram)" for this initially.
            # A more sophisticated decision_maker would need to parse this intent specifically.
            self.tts.speak("Sir, performing social media posting is a very advanced automation. I can try to open the platform for you, but direct posting requires specific permissions and API integrations which are highly complex.", speed="slow")
            if "instagram" in query_data.lower():
                self._open_application("instagram", user_name)
            elif "facebook" in query_data.lower():
                self._open_application("facebook", user_name)
            return

        if decision_type == "open":
            self._open_application(query_data, user_name)
        elif decision_type == "close":
            self._close_application(query_data, user_name)
        elif decision_type == "play":
            self._play_song(query_data, user_name)
        elif decision_type == "generate image":
            # This task is handled by image_generation_module directly in main.py, not here.
            # This ensures images are generated and then their paths are sent to UI.
            # If this automation module is called for generate image, it will be a fallback.
            self.tts.speak("Image generation is being handled by the dedicated image generator, Sir.", speed="normal")
            image_generator_instance.generate_image(query_data) # Ensure this call is valid
        elif decision_type == "reminder":
            self._set_reminder(query_data, user_name)
        elif decision_type == "system":
            self._system_task(query_data, user_name)
        elif decision_type == "content":
            self._write_content(query_data, user_name, decision_maker_instance)
        elif decision_type == "google search":
            self._Google Search(query_data, user_name)
        elif decision_type == "Youtube":
            self._Youtube(query_data, user_name)
        else:
            self.tts.speak("I don't know how to perform this automation task yet, Sir.", speed="slow")
