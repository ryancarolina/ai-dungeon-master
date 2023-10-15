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






openai.api_key = Config.API_KEY
character_manager = CharacterManager()
simple_session_manager = SimpleSessionManager()
speech_queue = queue.Queue()
engine = pyttsx3.init()

# Create the main window
window = tk.Tk()
window.title("Gauntlets and Goblins")

# Explicitly set the Tkinter window size
window_width = 900  # You can set this to any value you want
window_height = 700  # You can set this to any value you want
window.geometry(f"{window_width}x{window_height}")

# Load the startup graphic
startup_image = PhotoImage(file="ggTitle.png")

# Calculate aspect ratios
window_aspect = window_width / window_height
image_aspect = startup_image.width() / startup_image.height()

# Determine the zoom factors
if window_aspect > image_aspect:
    # Window is wider than image
    zoom_factor = window_width / startup_image.width()
else:
    # Window is taller than image
    zoom_factor = window_height / startup_image.height()

# Use the zoom factor to resize the image
startup_image = startup_image.zoom(int(round(zoom_factor)), int(round(zoom_factor)))

# Create the label and place the image
startup_label = tk.Label(window, image=startup_image)
startup_label.place(x=0, y=0, relwidth=1, relheight=1)  # Cover the whole window

# Set a minimum window size (width x height)
window.minsize(800, 600)

# Set background color to a dark gray to resemble dungeon tiles
window.configure(bg='#2E2E2E')

# Define a custom font
custom_font = tkFont.Font(family="Helvetica", size=12)

# Create a frame to hold the text area and the scrollbar
text_frame = tk.Frame(window)
text_frame.grid(column=0, row=0, padx=10, pady=10, sticky='nsew')

# Create a scrollable text display area
text_area = tk.Text(text_frame, wrap=tk.WORD, bg='#2E2E2E', fg='#FFFFFF', font=custom_font)
text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

# Create a scrollbar and attach it to text_area
scrollbar = tk.Scrollbar(text_frame, command=text_area.yview)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
text_area['yscrollcommand'] = scrollbar.set

# Create a multi-line text input field
input_field = tk.Text(window, width=40, height=4, bg='#2E2E2E', fg='#FFFFFF', font=custom_font)
input_field.grid(column=0, row=1, padx=10, pady=10, sticky='w')

# Create a Submit button
submit_button = tk.Button(window, text="Submit", command=lambda: handle_entry(None), bg='#2E2E2E', fg='#FFFFFF', font=custom_font)
submit_button.grid(column=0, row=2, padx=10, pady=10, sticky='w')

# Define text tags for coloring
text_area.tag_config('player_tag', foreground='green')
text_area.tag_config('dm_tag', foreground='yellow')

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

# Function to handle text entry
def handle_entry(event):
    user_text = input_field.get("1.0", tk.END).strip()  # Get text from input_field
    input_field.delete("1.0", tk.END)  # Clear the input_field
    text_area.insert(tk.END, "Player: ", 'player_tag')  # colored "Player:"
    text_area.insert(tk.END, f"{user_text}\n\n")  # user's message

    if not simple_session_manager.session_exists():
        simple_session_manager.start_session()
        simple_session_manager.add_milestone()

    if user_text == '!clearsession':
        simple_session_manager.clear_session()
        simple_session_manager.start_session()  # Start a new session immediately
        acknowledgment = "Session cleared. New session started."
        text_area.insert(tk.END, "DM: ", 'dm_tag')
        text_area.insert(tk.END, f"{acknowledgment}\n\n")
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
        text_area.insert(tk.END, "GM: ", 'dm_tag')  # colored "DM:"
        text_area.insert(tk.END, f"{acknowledgment}\n\n")  # acknowledgment message
        return  # Exit early as no further processing is needed
    else:
        # Get only the relevant messages since the last milestone
        relevant_messages = simple_session_manager.get_messages_since_last_milestone()

        if relevant_messages:
            try:
                chat = openai.ChatCompletion.create(model="gpt-4", messages=relevant_messages)
                dm_response = chat.choices[0].message.content

                if "_____________________" in dm_response:  # or any other identifier for ASCII art
                    dm_response = "[SKIP_TTS]" + dm_response

                simple_session_manager.add_message({"role": "assistant", "content": dm_response})

                text_area.insert(tk.END, "GM: ", 'dm_tag')  # colored "DM:"
                text_area.insert(tk.END, f"{dm_response}\n\n")  # DM's message

                text_area.see(tk.END)
                speech_queue.put(dm_response)

            except Exception as e:
                text_area.insert(tk.END, f"An error occurred: {e}\n")
        else:
            text_area.insert(tk.END, "No messages to process.\n")
            
# Function to handle text entry and keep the startup image
def handle_entry_and_keep_image(event):
    handle_entry(event)

# Bind the Enter key
input_field.bind("<Return>", handle_entry_and_keep_image)

# Use the instance to create or open character sheets
for i in range(6):
    button = tk.Button(window, text=f"Player {i + 1} Character Sheet", command=lambda i=i: character_manager.create_or_open_character_sheet(i), bg='#2E2E2E', fg='#FFFFFF', font=custom_font)
    button.grid(column=0, row=i + 3, padx=10, pady=10, sticky='w')

# Set weight and minimum size for rows and columns
window.grid_rowconfigure(0, weight=1, minsize=200)  # Text frame
window.grid_rowconfigure(1, weight=0, minsize=100)  # Input field
window.grid_rowconfigure(2, weight=0, minsize=50)  # Submit button

# Set weight and minimum size for the rows containing the buttons
for i in range(3, 9):  # Loop through the rows where buttons are placed (3 to 8)
    window.grid_rowconfigure(i, weight=0, minsize=50)

# Set weight for the column
window.grid_columnconfigure(0, weight=1)

# Run the Tkinter event loop
window.mainloop()

