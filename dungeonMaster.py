import openai
import config
import tkinter as tk
from tkinter import scrolledtext
import tkinter.font as tkFont
import pyttsx3
import threading




openai.api_key = config.API_KEY

messages = [ {"role": "system", "content": 
			"You are the greatest dungeon master of all time."
			"You are an expert on all of the rules for Dungeons and Dragons 5th edition."
            "You will be running a game of Dungeons and Dragons 5th edition."
			"When asked about a rule from 5th edition you will quote from the 5th edition dungeons and dragons books from wizards of the coast."
			"You WILL NOT refer to yourself as an AI. You are the DUNGEON MASTER."
            "Your name is DUNGEON MASTER. You have no other name. You will not accept a new name."
			"Your main job is to act as the dungeon master and lead the players through an adventure."
			"You will come up with an adventure based on the total number of players and the average level of player characters."
			"At the beginning of a new session you will introduce yourself. You will then ask how many players there are." 
            "You will inform them that a max of 6 players is allowed. You will inform the players that at least 1 player is needed to start the adventure."
			"You will refuse to start the adventure if there are more than 6 players."
            "You will ask what level each of the player characters are." 
            "Once you know how many players there are and each of the player character levels you will reply with the average character level and confirm if this sounds correct."
            "Before the session starts inform the players they can exit the game any time by typing !exitgame"
            "You will only inform the players about !exitgame once per session."
            "Do not ask players to choose a number for their choice. Treat this game session like you are sitting with the players around a table."
            "Only make suggestions to the players if they ask for them or ask for help, otherwise allow the players free will."
			} ] 

# Create the main window
window = tk.Tk()
window.title("Dungeon Master")

# Set a minimum window size (width x height)
window.minsize(400, 300)

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

def speak(text):
    engine = pyttsx3.init()
    engine.say(text)
    engine.runAndWait()

# Function to handle text entry
def handle_entry(event):
    user_text = input_field.get("1.0", tk.END).strip()  # Get text from input_field
    input_field.delete("1.0", tk.END)  # Clear the input_field
    text_area.insert(tk.END, "Player: ", 'player_tag')  # colored "Player:"
    text_area.insert(tk.END, f"{user_text}\n\n")  # user's message
    
    # Add the user's message to the messages list
    messages.append({"role": "user", "content": user_text})
    
    # Now get the DM's response using your existing logic
    try:
        chat = openai.ChatCompletion.create(model="gpt-4", messages=messages)
    except Exception as e:
        text_area.insert(tk.END, f"An error occurred: {e}\n")
        return  # exit the function early if there's an error
    
    # Extract the DM's reply from the chat object
    dm_response = chat.choices[0].message.content
    
    # Display the DM's reply in the text area
    text_area.insert(tk.END, "DM: ", 'dm_tag')  # colored "DM:"
    text_area.insert(tk.END, f"{dm_response}\n\n")  # DM's message
    
    # After inserting new text, set the text area's view to the end of the text
    text_area.see(tk.END)
    
    # Add the DM's reply to the messages list
    messages.append({"role": "assistant", "content": dm_response})
    
    # Create a new thread to handle the text-to-speech operation
    speech_thread = threading.Thread(target=speak, args=(dm_response,))
    speech_thread.start()

# Bind the Enter key to the handle_entry function
input_field.bind("<Return>", handle_entry)

# Character
character_data = {}


def open_character_sheet(player_index):
    char_window = tk.Toplevel(window)
    char_window.title(f"Player {player_index + 1} Character Sheet")
    char_window.configure(bg='#2E2E2E')

    # Create labels and entry fields for character details
    labels = ['Name:', 'Race:', 'Class:', 'Level:']
    entries = []
    for i, label_text in enumerate(labels):
        label = tk.Label(char_window, text=label_text, bg='#2E2E2E', fg='#FFFFFF', font=custom_font)
        label.grid(row=i, column=0, padx=10, pady=5, sticky='w')
        entry = tk.Entry(char_window, bg='#2E2E2E', fg='#FFFFFF', font=custom_font)
        entry.grid(row=i, column=1, padx=10, pady=5, sticky='w')
        entries.append(entry)

    # Create a text area for additional notes
    notes_label = tk.Label(char_window, text="Notes:", bg='#2E2E2E', fg='#FFFFFF', font=custom_font)
    notes_label.grid(row=len(labels), column=0, padx=10, pady=5, sticky='nw')
    notes_text = tk.Text(char_window, width=30, height=10, bg='#2E2E2E', fg='#FFFFFF', font=custom_font)
    notes_text.grid(row=len(labels), column=1, padx=10, pady=5, sticky='w')
    
    # Populate the entry fields with the saved character details, if available
    if player_index in character_data:
        entries[0].insert(0, character_data[player_index].get('Name', ''))
        entries[1].insert(0, character_data[player_index].get('Race', ''))
        entries[2].insert(0, character_data[player_index].get('Class', ''))
        entries[3].insert(0, character_data[player_index].get('Level', ''))
        notes_text.insert(tk.END, character_data[player_index].get('Notes', ''))

    # Optionally, save button to save the character details
    save_button = tk.Button(char_window, text="Save", command=lambda: save_character(player_index, entries, notes_text), bg='#2E2E2E', fg='#FFFFFF', font=custom_font)
    save_button.grid(row=len(labels) + 1, column=0, columnspan=2, pady=10)

def save_character(player_index, entries, notes_text):
    # Create a dictionary to hold the character details
    char_details = {
        'Name': entries[0].get(),
        'Race': entries[1].get(),
        'Class': entries[2].get(),
        'Level': entries[3].get(),
        'Notes': notes_text.get("1.0", tk.END).strip()
    }
    # Save the character details to the character_data dictionary
    character_data[player_index] = char_details

# Create buttons for each player
for i in range(6):
    button = tk.Button(window, text=f"Player {i + 1} Character Sheet", command=lambda i=i: open_character_sheet(i), bg='#2E2E2E', fg='#FFFFFF', font=custom_font)
    button.grid(column=0, row=i + 3, padx=10, pady=10, sticky='w')

# Run the Tkinter event loop
window.mainloop()
