import openai
import config
import tkinter as tk
from tkinter import scrolledtext
import tkinter.font as tkFont


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

# Bind the Enter key to the handle_entry function
input_field.bind("<Return>", handle_entry)

# Run the Tkinter event loop
window.mainloop()
