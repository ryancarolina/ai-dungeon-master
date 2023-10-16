import json
import os
from tkinter import PhotoImage
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox
from tkinter import filedialog
from InventoryManager import InventoryManager


class CharacterManager:
    skills_labels_text = [
            "Acrobatics (Dex)", "Animal Handling (Wis)", "Arcana (Int)", 
            "Athletics (Str)", "Deception (Cha)", "History (Int)", 
            "Insight (Wis)", "Intimidation (Cha)", "Investigation (Int)", 
            "Medicine (Wis)", "Nature (Int)", "Perception (Wis)", 
            "Performance (Cha)", "Persuasion (Cha)", "Religion (Int)", 
            "Sleight of Hand (Dex)", "Stealth (Dex)", "Survival (Wis)"
        ]
    
    def __init__(self):
        self.character_data = {}
        self.inventory_managers = {}
        self.load_character_data()
        
    def save_character_data(self):
        try:
            with open('data/character_data.json', 'w') as file:
                json.dump(self.character_data, file, indent=4)
            print("Data saved successfully")  # Debugging line
            print(os.path.abspath('data/character_data.json'))
        except Exception as e:
            print(f"Error saving character data: {e}")

    def load_character_data(self):
        try:
            if os.path.exists('data/character_data.json'):
                with open('data/character_data.json', 'r') as file:
                    self.character_data = json.load(file)
                print(f"Data loaded successfully: {self.character_data}")  # Debugging line
                print(os.path.abspath('data/character_data.json'))
        except Exception as e:
            print(f"Error loading character_data: {e}")

    def validate_entries(self, entries):
        for entry in entries[3:]:
            value = entry.get()
            if not value.isdigit():
                print(f"Invalid value: {value}")  # Debugging line
                return False
        return True

    def save_character(self, player_index, entries, skills_entries, notes_text, image_path):
        char_details = {
            'Name': entries[0].get(),
            'Race': entries[1].get(),
            'Class': entries[2].get(),
            'Level': entries[3].get(),
            'AC': entries[4].get(),
            'HP': entries[5].get(),
            'Strength': entries[6].get(),
            'Dexterity': entries[7].get(),
            'Constitution': entries[8].get(),
            'Intelligence': entries[9].get(),
            'Wisdom': entries[10].get(),
            'Charisma': entries[11].get(),
            'Skills': {skill_label: entry.get() for skill_label, entry in zip(self.skills_labels_text, skills_entries)},
            'Notes': notes_text.get("1.0", tk.END).strip(),
            'Image': image_path,
            'Inventory': self.inventory_managers[player_index].to_json()
        }
        print(f"Saving data for player {player_index}: {char_details}")  # Debugging line
        self.character_data[str(player_index)] = char_details
        self.save_character_data()
        
    def update_inventory_display(self, player_index, listbox):
        listbox.delete(0, tk.END)  # Clear the listbox
        for category, items in self.inventory_managers[player_index].inventory.items():
            for item_name, quantity in items.items():
                listbox.insert(tk.END, f"{category}: {item_name} (x{quantity})")

    def create_or_open_character_sheet(self, player_index):
        if player_index not in self.inventory_managers:
            self.inventory_managers[player_index] = InventoryManager()
            
        self.load_character_data()

        # Convert player_index to string for consistency with JSON data
        player_index_str = str(player_index)

        character_sheet_window = tk.Toplevel()
        character_sheet_window.configure(bg='#2E2E2E')
        character_sheet_window.title(f"Character Sheet {player_index + 1}")

        notebook = ttk.Notebook(character_sheet_window)
        notebook.pack(fill=tk.BOTH, expand=True)

        core_stats_frame = tk.Frame(notebook, bg='#2E2E2E')
        notebook.add(core_stats_frame, text="Core Stats")

        core_stats_labels_text = ["Name", "Race", "Class", "Level", "AC", "HP", "Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]

        # Load and display the character portrait image
        original_portrait_image = PhotoImage(file="art/femaleElfBlonde.png")  # Replace with your image path
        portrait_image = original_portrait_image.subsample(4, 4)  # Reduce size by half as an example
        portrait_label = tk.Label(core_stats_frame, image=portrait_image, bg='#2E2E2E')
        portrait_label.photo = portrait_image  # Keep a reference to avoid garbage collection
        portrait_label.grid(row=0, column=2, rowspan=len(core_stats_labels_text))  # Adjust grid position

        current_image_path = "art/femaleElfBlonde.png"  # Initialize with your default image path
        
        # Function to open file dialog and update portrait
        def update_portrait():
            nonlocal current_image_path
            file_path = filedialog.askopenfilename(filetypes=[("PNG files", "*.png")])
            if file_path:
                new_image = PhotoImage(file=file_path)
                new_image = new_image.subsample(4, 4)  # Resize the image
                portrait_label.configure(image=new_image)
                portrait_label.photo = new_image
                current_image_path = file_path
                self.save_character(player_index, entries, skills_entries, notes_text, file_path)  # Save the new image path

        # Add button to update portrait
        update_button = tk.Button(core_stats_frame, text="Update Portrait", command=update_portrait, bg='#2E2E2E', fg='#FFFFFF')
        update_button.grid(row=0, column=3)  # Adjust grid position

        entries = []
        for i, text in enumerate(core_stats_labels_text):
            tk.Label(core_stats_frame, text=f"{text}:", bg='#2E2E2E', fg='#FFFFFF').grid(row=i, column=0, sticky='e')
            entry = tk.Entry(core_stats_frame, bg='#2E2E2E', fg='#FFFFFF', insertbackground='white')
            entry.grid(row=i, column=1)
            entries.append(entry)


        skills_frame = tk.Frame(notebook, bg='#2E2E2E')
        notebook.add(skills_frame, text="Skills")

        skills_entries = []  # Local variable to hold Entry widgets for skills
        for i, text in enumerate(self.skills_labels_text):
            tk.Label(skills_frame, text=f"{text}:", bg='#2E2E2E', fg='#FFFFFF').grid(row=i, column=0, sticky='e')
            entry = tk.Entry(skills_frame, bg='#2E2E2E', fg='#FFFFFF', insertbackground='white')
            entry.grid(row=i, column=1)
            skills_entries.append(entry)  # Keep track of entry fields for later use


        notes_text = tk.Text(character_sheet_window, width=40, height=10)
        notes_text.pack()

        # Use player_index_str when checking if it's a key in self.character_data
        if player_index_str in self.character_data:
            for i, key in enumerate(core_stats_labels_text):
                entries[i].insert(0, self.character_data[player_index_str].get(key, ''))
            saved_notes = self.character_data[player_index_str].get('Notes', '')
            notes_text.delete("1.0", tk.END)
            notes_text.insert("1.0", saved_notes)
            
            # Also use player_index_str when accessing data in self.character_data
            skills_data = self.character_data[player_index_str].get('Skills', {})
            for i, skill_label in enumerate(self.skills_labels_text):
                skills_entries[i].insert(0, skills_data.get(skill_label, ''))
                
            # Load saved portrait if available
            saved_image_path = self.character_data[player_index_str].get('Image', "art/femaleElfBlonde.png")  # Replace with your default image path
            saved_image = PhotoImage(file=saved_image_path)
            saved_image = saved_image.subsample(4, 4)  # Resize the image
            portrait_label.configure(image=saved_image)
            portrait_label.photo = saved_image
            
            self.inventory_managers[player_index].from_json(self.character_data[player_index_str].get('Inventory', {}))
            
            # Create a new frame for the inventory and add it to the notebook
            inventory_frame = tk.Frame(notebook, bg='#2E2E2E')
            notebook.add(inventory_frame, text="Inventory")
            
            # Create a Listbox for the inventory items
            inventory_listbox = tk.Listbox(inventory_frame, bg='#2E2E2E', fg='#FFFFFF')
            inventory_listbox.grid(row=0, column=0, rowspan=4, columnspan=2)
            # Populate the Listbox with current inventory items
            self.update_inventory_display(player_index, inventory_listbox)

            # Add buttons for adding removing items from inventory
            add_button = tk.Button(inventory_frame, text="Add Item", command=lambda: self.add_item(player_index, inventory_listbox), bg='#2E2E2E', fg='#FFFFFF')
            add_button.grid(row=4, column=0)

            remove_button = tk.Button(inventory_frame, text="Remove Item", command=lambda: self.remove_item(player_index, inventory_listbox), bg='#2E2E2E', fg='#FFFFFF')
            remove_button.grid(row=4, column=1)


        save_button = tk.Button(character_sheet_window, text="Save", command=lambda: self.save_character(player_index, entries, skills_entries, notes_text, current_image_path) if self.validate_entries(entries) else messagebox.showerror("Invalid Input", "Please enter valid numbers for Level, AC, HP, and ability scores."))
        save_button.pack()
        
    def add_item(self, player_index, inventory_listbox):
        # Create a new window for adding items
        add_item_window = tk.Toplevel()
        add_item_window.title("Add Item")

        # Predefined categories
        categories = ["Weapons", "Armor", "Items", "Currency"]

        # Create Tkinter StringVar to hold selected category
        selected_category = tk.StringVar()
        selected_category.set(categories[0])  # Default value

        # Add widgets to enter item details
        tk.Label(add_item_window, text="Category: ").grid(row=0, column=0)
        tk.OptionMenu(add_item_window, selected_category, *categories).grid(row=0, column=1)

        tk.Label(add_item_window, text="Item Name: ").grid(row=1, column=0)
        item_name_entry = tk.Entry(add_item_window)
        item_name_entry.grid(row=1, column=1)

        tk.Label(add_item_window, text="Quantity: ").grid(row=2, column=0)
        quantity_entry = tk.Entry(add_item_window)
        quantity_entry.grid(row=2, column=1)

        def submit_item():
            category = selected_category.get().strip()
            item_name = item_name_entry.get().strip()
            quantity = quantity_entry.get().strip()

            if not category or not item_name or not quantity.isdigit():
                tk.messagebox.showerror("Invalid Input", "Please enter valid details.")
                return

            self.inventory_managers[player_index].add_item(category, item_name, int(quantity))
            add_item_window.destroy()
            tk.messagebox.showinfo("Success", "Item added successfully.")
            self.update_inventory_display(player_index, inventory_listbox)

        tk.Button(add_item_window, text="Submit", command=submit_item).grid(row=3, columnspan=2)
        self.update_inventory_display(player_index, inventory_listbox)

    def remove_item(self, player_index, inventory_listbox):
        # Create a new window for removing items
        remove_item_window = tk.Toplevel()
        remove_item_window.title("Remove Item")
        
        # Predefined categories
        categories = ["Weapons", "Armor", "Items", "Currency"]
        
        # Create Tkinter StringVar to hold selected category
        selected_category = tk.StringVar()
        selected_category.set(categories[0])  # Default value
    
        # Add widgets to enter item details
        tk.Label(remove_item_window, text="Category: ").grid(row=0, column=0)
        tk.OptionMenu(remove_item_window, selected_category, *categories).grid(row=0, column=1)
    
        tk.Label(remove_item_window, text="Item Name: ").grid(row=1, column=0)
        item_name_entry = tk.Entry(remove_item_window)
        item_name_entry.grid(row=1, column=1)
    
        tk.Label(remove_item_window, text="Quantity: ").grid(row=2, column=0)
        quantity_entry = tk.Entry(remove_item_window)
        quantity_entry.grid(row=2, column=1)
    
        def submit_item():
            category = category_entry.get().strip()
            item_name = item_name_entry.get().strip()
            quantity = quantity_entry.get().strip()
        
            if not category or not item_name or not quantity.isdigit():
                tk.messagebox.showerror("Invalid Input", "Please enter valid details.")
                return

            self.inventory_managers[player_index].remove_item(category, item_name, int(quantity))  # Updated
            remove_item_window.destroy()
            tk.messagebox.showinfo("Success", "Item removed successfully.")
        tk.Button(remove_item_window, text="Submit", command=submit_item).grid(row=3, columnspan=2)
        self.update_inventory_display(player_index, inventory_listbox)
            
        
    def get_summary_data(self):
        self.load_character_data()    
        summary = {}
        for player_index, char_data in self.character_data.items():
            # Convert player_index to int, then add 1, and finally convert it back to str for concatenation
            summary[f"Player {str(int(player_index) + 1)}"] = char_data
        return summary

