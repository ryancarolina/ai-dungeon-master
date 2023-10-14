import json
import os
import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox

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
        self.load_character_data()
        
    def save_character_data(self):
        try:
            with open('character_data.json', 'w') as file:
                json.dump(self.character_data, file, indent=4)
            print("Data saved successfully")  # Debugging line
            print(os.path.abspath('character_data.json'))
        except Exception as e:
            print(f"Error saving character data: {e}")

    def load_character_data(self):
        try:
            if os.path.exists('character_data.json'):
                with open('character_data.json', 'r') as file:
                    self.character_data = json.load(file)
                print(f"Data loaded successfully: {self.character_data}")  # Debugging line
                print(os.path.abspath('character_data.json'))
        except Exception as e:
            print(f"Error loading character_data: {e}")

    def validate_entries(self, entries):
        for entry in entries[3:]:
            value = entry.get()
            if not value.isdigit():
                print(f"Invalid value: {value}")  # Debugging line
                return False
        return True

    def save_character(self, player_index, entries, skills_entries, notes_text):
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
            'Notes': notes_text.get("1.0", tk.END).strip()
        }
        print(f"Saving data for player {player_index}: {char_details}")  # Debugging line
        self.character_data[str(player_index)] = char_details
        self.save_character_data()

    def create_or_open_character_sheet(self, player_index):
        self.load_character_data()        

        # Convert player_index to string for consistency with JSON data
        player_index_str = str(player_index)

        character_sheet_window = tk.Toplevel()
        character_sheet_window.title(f"Character Sheet {player_index + 1}")

        notebook = ttk.Notebook(character_sheet_window)
        notebook.pack(fill=tk.BOTH, expand=True)

        core_stats_frame = ttk.Frame(notebook)
        notebook.add(core_stats_frame, text="Core Stats")

        core_stats_labels_text = ["Name", "Race", "Class", "Level", "AC", "HP", "Strength", "Dexterity", "Constitution", "Intelligence", "Wisdom", "Charisma"]
        entries = []
        for i, text in enumerate(core_stats_labels_text):
            tk.Label(core_stats_frame, text=f"{text}:").grid(row=i, column=0, sticky='e')
            entry = tk.Entry(core_stats_frame)
            entry.grid(row=i, column=1)
            entries.append(entry)

        skills_frame = ttk.Frame(notebook)
        notebook.add(skills_frame, text="Skills")

        skills_entries = []  # Local variable to hold Entry widgets for skills
        for i, text in enumerate(self.skills_labels_text):
            tk.Label(skills_frame, text=f"{text}:").grid(row=i, column=0, sticky='e')
            entry = tk.Entry(skills_frame)
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

        save_button = tk.Button(character_sheet_window, text="Save", command=lambda: self.save_character(player_index, entries, skills_entries, notes_text) if self.validate_entries(entries) else messagebox.showerror("Invalid Input", "Please enter valid numbers for Level, AC, HP, and ability scores."))
        save_button.pack()
        
    def get_summary_data(self):
        self.load_character_data()    
        summary = {}
        for player_index, char_data in self.character_data.items():
            # Convert player_index to int, then add 1, and finally convert it back to str for concatenation
            summary[f"Player {str(int(player_index) + 1)}"] = char_data
        return summary

