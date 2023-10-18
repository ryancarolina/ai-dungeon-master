import openai
import Config
import tkinter as tk
import tkinter.font as tkFont
import tkinter.messagebox as messagebox 
import pyttsx3
import threading
import queue
from CharacterManager import CharacterManager
from SimpleSessionManager import SimpleSessionManager
from tkinter import PhotoImage
from UiManager import UiManager







openai.api_key = Config.API_KEY
character_manager = CharacterManager()
simple_session_manager = SimpleSessionManager()
speech_queue = queue.Queue()
engine = pyttsx3.init()

# Create the main window
window = tk.Tk()
window.title("Gauntlets and Goblins")

def handle_entry_logic(user_text):
    print("handle_entry_logic is called")
    print(f"Inside handle_entry_logic, user_text: {user_text}")
    ui_manager.display_text("Player: ", 'player_tag')
    ui_manager.display_text(f"{user_text}\n\n")  # user's message
    
    if not simple_session_manager.session_exists():
        simple_session_manager.start_session()
        simple_session_manager.add_milestone()
    
    if user_text == '!clearsession':
        simple_session_manager.clear_session()
        simple_session_manager.start_session()  # Start a new session immediately
        acknowledgment = "Session cleared. New session started."
        ui_manager.display_dm_message(acknowledgment)
        return  # Exit early as there's no further processing needed

    # Add the user's message to the session data
    simple_session_manager.add_message({"role": "user", "content": user_text})

    if user_text == '!summary':
        summary_data = character_manager.get_summary_data()
        formatted_summary = f"Characters Summary: {summary_data}"
        simple_session_manager.add_system_message({"role": "system", "content": formatted_summary})
        simple_session_manager.add_milestone()

        # Acknowledge the summary command without contacting the AI DM
        acknowledgment = "Summary data updated."
        ui_manager.display_dm_message(acknowledgment)
        return  # Exit early as no further processing is needed
    else:
        # Get only the relevant messages since the last milestone
        relevant_messages = simple_session_manager.get_messages_since_last_milestone()

        if relevant_messages:
            try:
                chat = openai.ChatCompletion.create(model="gpt-4", messages=relevant_messages, max_tokens=100)
                dm_response = chat.choices[0].message.content
                if "_____________________" in dm_response:  # or any other identifier for ASCII art
                    dm_response = "[SKIP_TTS]" + dm_response
                simple_session_manager.add_message({"role": "assistant", "content": dm_response})
                ui_manager.display_dm_message(dm_response)
                ui_manager.text_area.see(tk.END)
                speech_queue.put(dm_response)
            except Exception as e:
                ui_manager.text_area.insert(tk.END, f"An error occurred: {e}\n")
        else:
            ui_manager.text_area.insert(tk.END, "No messages to process.\n")
            
def speak():
    while True:
        text = speech_queue.get()  # Get text from the queue
        if text == "STOP":
            break  # Exit the loop if the text is "STOP"
        if text.startswith("[SKIP_TTS]"):
            continue  # Skip this iteration, don't read this text
        engine.say(text)
        engine.runAndWait()
        
speech_thread = threading.Thread(target=speak)
speech_thread.start()

ui_manager = UiManager(window, handle_entry_logic)

ui_manager.initialize_window(900, 700)

ui_manager.add_character_buttons_and_configure_grid(6, character_manager.create_or_open_character_sheet)

# Run the Tkinter event loop
window.mainloop()

