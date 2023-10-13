import tkinter as tk
from tkinter import ttk
import tkinter.messagebox as messagebox

class CharacterManager:
    def __init__(self):
        self.character_data = {}

    def validate_entries(self, entries):
        for entry in entries[3:]:
            value = entry.get()
            if not value.isdigit():
                return False
        return True

    def save_character(self, player_index, entries, notes_text):
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
            'Notes': notes_text.get("1.0", tk.END).strip()
        }
        self.character_data[player_index] = char_details

    def create_or_open_character_sheet(self, player_index):
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

        notes_text = tk.Text(character_sheet_window, width=40, height=10)
        notes_text.pack()

        if player_index in self.character_data:
            for i, key in enumerate(core_stats_labels_text):
                entries[i].insert(0, self.character_data[player_index].get(key, ''))
            saved_notes = self.character_data[player_index].get('Notes', '')
            notes_text.delete("1.0", tk.END)
            notes_text.insert("1.0", saved_notes)

        save_button = tk.Button(character_sheet_window, text="Save", command=lambda: self.save_character(player_index, entries, notes_text) if self.validate_entries(entries) else messagebox.showerror("Invalid Input", "Please enter valid numbers for Level, AC, HP, and ability scores."))
        save_button.pack()
