import tkinter as tk
import tkinter.font as tkFont


class UiManager:

    def __init__(self, window, handle_entry_logic_callback):
        self.handle_entry_logic_callback = handle_entry_logic_callback
        print(f"Debug: handle_entry_logic_callback is {self.handle_entry_logic_callback}")
        self.window = window

        # Call the function to get the values
        self.custom_font, self.bg_color, self.fg_color = self.define_custom_font_and_colors()

        # Load the startup graphic
        self.startup_image = tk.PhotoImage(file="art/ggTitle.png")

        # Create the label and place the image
        self.startup_label = tk.Label(window, image=self.startup_image)
        self.startup_label.place(x=0, y=0, relwidth=1, relheight=1)  # Cover the whole window

        # Set a minimum window size (width x height)
        window.minsize(800, 600)

        # Set background color
        window.configure(bg=self.bg_color)

        # Create a frame to hold the text area and the scrollbar
        self.text_frame = tk.Frame(window, bg=self.bg_color)
        self.text_frame.grid(column=0, row=0, padx=10, pady=10, sticky='nsew')

        # Create a scrollable text display area
        self.text_area = tk.Text(self.text_frame, wrap=tk.WORD, bg=self.bg_color, fg=self.fg_color, font=self.custom_font)
        self.text_area.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Create a scrollbar and attach it to text_area
        self.scrollbar = tk.Scrollbar(self.text_frame, command=self.text_area.yview, bg=self.bg_color)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create a multi-line text input field
        self.input_field = tk.Text(self.window, width=40, height=4, bg=self.bg_color, fg=self.fg_color, font=self.custom_font)
        self.input_field.grid(column=0, row=1, padx=10, pady=10, sticky='w')
        
        # Bind the Enter key to handle_entry method
        self.input_field.bind("<Return>", lambda event, self=self: self.handle_entry(event, self.handle_entry_logic_callback))


        # Create a Submit button
        self.submit_button = tk.Button(window, text="Submit", command=lambda: self.handle_entry(None, self.handle_entry_logic_callback), bg=self.bg_color, fg=self.fg_color, font=self.custom_font)

        self.submit_button.grid(column=0, row=2, padx=10, pady=10, sticky='w')

        # Define text tags for coloring
        self.text_area.tag_config('player_tag', foreground='green')
        self.text_area.tag_config('dm_tag', foreground='yellow')

        # ... Other initialization code ...

    # Define custom font and colors
    def define_custom_font_and_colors(self):
        custom_font = tkFont.Font(family="Helvetica", size=12)
        bg_color = '#2E2E2E'
        fg_color = '#FFFFFF'
        return custom_font, bg_color, fg_color
    
    def initialize_window(self, width, height):
        self.window.geometry(f"{width}x{height}")
        self.window.minsize(800, 600)
        self.window.title("Gauntlets and Goblins")

    def display_text(self, text, tag=None):
        if tag:
            self.text_area.insert(tk.END, text, tag)
        else:
            self.text_area.insert(tk.END, text)
            
    def handle_entry(self, event, callback):
        print("handle_entry is called")  # Debugging line
        print(f"Event Info: {event}")  # Debugging line
        user_text = self.input_field.get("1.0", tk.END).strip()
        print(f"User Text: {user_text}")  # Debugging line
        self.input_field.delete("1.0", tk.END)
        callback(user_text)


        
    def add_character_buttons(self, num_buttons, callback):
        for i in range(num_buttons):
            button = tk.Button(self.window, text=f"P {i + 1} Character", command=lambda i=i: callback(i), bg=self.bg_color, fg=self.fg_color, font=self.custom_font)
            button.grid(column=0, row=i + 3, padx=10, pady=10, sticky='w')
            
    def display_dm_message(self, message, tag='dm_tag'):
        self.text_area.insert(tk.END, "GM: ", tag)
        self.text_area.insert(tk.END, f"{message}\n\n")
        
    def add_character_buttons_and_configure_grid(self, num_buttons, callback):
        # Use the instance to create or open character sheets
        self.add_character_buttons(num_buttons, callback)

        # Set weight and minimum size for rows and columns
        self.window.grid_rowconfigure(0, weight=1, minsize=200)  # Text frame
        self.window.grid_rowconfigure(1, weight=0, minsize=100)  # Input field
        self.window.grid_rowconfigure(2, weight=0, minsize=50)  # Submit button

        # Set weight and minimum size for the rows containing the buttons
        for i in range(3, num_buttons + 3):  # Loop through the rows where buttons are placed
            self.window.grid_rowconfigure(i, weight=0, minsize=50)

        # Set weight for the column
        self.window.grid_columnconfigure(0, weight=1)
        


