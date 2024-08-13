# Gauntlets and Goblins

Gauntlets and Goblins is an interactive text-based role-playing game with a graphical user interface. It uses OpenAI's GPT-4 model to generate dynamic responses, creating an immersive gaming experience.

## Features

- Text-based role-playing game with AI-driven responses
- Character management system
- Advanced session management to track game progress
- Graphical user interface built with Tkinter
- Text-to-speech functionality for game responses
- Special commands for session management and character summaries

### Session Management System

- Persistent session storage using JSON files
- Milestone system for managing conversation context
- Token management to control conversation size
- Automatic summarization of older messages using GPT-3.5-turbo
- Separate handling of system messages and character summaries

## Requirements

- Python 3.x
- OpenAI API key
- Required Python packages:
  - openai
  - tkinter
  - pyttsx3
  - json
  - os
  - threading

## Installation

1. Clone this repository:
   ```
   git clone https://github.com/yourusername/gauntlets-and-goblins.git
   ```

2. Navigate to the project directory:
   ```
   cd gauntlets-and-goblins
   ```

3. Install the required packages:
   ```
   pip install -r requirements.txt
   ```

4. Create a `Config.py` file in the project root and add your OpenAI API key:
   ```python
   API_KEY = "your_openai_api_key_here"
   ```

## Usage

Run the game by executing the main script:

```
python main.py
```

### Game Commands

- `/clearsession`: Clears the current session and starts a new one
- `/summary`: Displays a summary of the current characters

## Game World

- The game is set in Nethercroft, an underground labyrinth with 100 floors
- Players start in the town of Ebonvale on the first floor
- Each floor has increasingly difficult monsters and a floor boss
- The game world has dark gothic horror tones

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Disclaimer

This project uses OpenAI's GPT-4 and GPT-3.5-turbo models and requires an API key. Please ensure you comply with OpenAI's use-case policy and terms of service.
