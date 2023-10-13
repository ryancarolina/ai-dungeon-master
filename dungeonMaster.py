import openai
import config
import tkinter as tk
from tkinter import scrolledtext  # for scrollable text field


openai.api_key = config.API_KEY

messages = [ {"role": "system", "content": 
			"You are the greatest dungeon master of all time."
			"You are an expert on all of the rules for Dungeons and Dragons 5th edition."
			"When asked about a rule from 5th edition you will quote from the 5th edition dungeons and dragons books from wizards of the coast."
			"You WILL NOT refer to yourself as an AI. You are the DUNGEON MASTER."
			"Your main job is to act as the dungeon master and lead the players through an adventure."
			"You will come up with an adventure based on the total number of players and the average level of player characters."
			"At the beginning of a new session you will introduce yourself. You will then ask how many players there are."
			"You will ask what level each of the player characters are." 
            "Once you know how many players there are and each of the player character levels you will reply with the average character level and confirm if this sounds correct."
            "Before the session starts inform the players they can exit the game any time by typing !exitgame"
			} ] 

# Create the main window
window = tk.Tk()
window.title("Dungeon Master")

# Set a minimum window size (width x height)
window.minsize(400, 300)

# Create a scrollable text display area
text_area = scrolledtext.ScrolledText(window, wrap=tk.WORD)
text_area.grid(column=0, row=0, padx=10, pady=10, sticky='nsew')

# Make the text area span the entire window
window.grid_columnconfigure(0, weight=1)
window.grid_rowconfigure(0, weight=1)

# Create a multi-line text input field
input_field = tk.Text(window, width=40, height=4)
input_field.grid(column=0, row=1, padx=10, pady=10, sticky='w')

# Function to handle text entry
def handle_entry(event):
    user_text = input_field.get("1.0", tk.END).strip()  # Get text from input_field
    input_field.delete("1.0", tk.END)  # Clear the input_field
    text_area.insert(tk.END, f"Player: {user_text}\n")
    
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
    text_area.insert(tk.END, f"DM: {dm_response}\n")
    
    # Add the DM's reply to the messages list
    messages.append({"role": "assistant", "content": dm_response})

# Bind the Enter key to the handle_entry function
# Note: You may want to create a "Submit" button or use a different event binding,
# as the Enter key will create a new line in the Text widget by default.
input_field.bind("<Return>", handle_entry)

# Run the Tkinter event loop
window.mainloop()
