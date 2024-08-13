# Gauntlets and Goblins

Gauntlets and Goblins is an interactive text-based role-playing game with a graphical user interface. It uses OpenAI's GPT-4 model to generate dynamic responses, creating an immersive gaming experience.

## Features

- Text-based role-playing game with AI-driven responses
- Character management system
- Session management to track game progress
- Graphical user interface built with Tkinter
- Text-to-speech functionality for game responses
- Special commands for session management and character summaries

## Requirements

- Python 3.x
- OpenAI API key
- Required Python packages:
  - openai
  - tkinter
  - pyttsx3

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

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

[Add your chosen license here]

## Disclaimer

This project uses OpenAI's GPT-4 model and requires an API key. Please ensure you comply with OpenAI's use-case policy and terms of service.
