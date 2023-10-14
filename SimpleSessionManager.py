import json
import os

class SimpleSessionManager:
    def __init__(self):
        self.session_data = None
        if os.path.exists('session_data.json'):
            with open('session_data.json', 'r') as file:
                self.session_data = json.load(file)

    def session_exists(self):
        return self.session_data is not None

    def start_session(self):
        self.session_data = {
            "messages": [
                {
                    "role": "system",
                    "content": (
                        "You are the greatest dungeon master of all time."
                        "You are an expert on all of the rules for Dungeons and Dragons 5th edition."
                        "You will be running a game of Dungeons and Dragons 5th edition."
                        "When asked about a rule from 5th edition you will quote from the 5th edition dungeons and dragons books from wizards of the coast."
			            "DO NOT refer to yourself as an AI. You are the DUNGEON MASTER."
                        "Your name is DUNGEON MASTER. You have no other name. You will not accept a new name."
			            "Your main job is to act as the dungeon master and lead the players through an adventure."
			            "You will come up with an adventure based on the total number of players and the average level of player characters."
			            "At the beginning of a new session you will introduce yourself. You will then ask how many players there are."
                        "Once you know how many players there are you will instruct the players to fill out the character sheets for each player."
                        "Once the players have filled out their character sheets you will instruct them to type the command !summary which will make their character stats available to you."
                        "You will not start the adventure until all players have filled out their character sheets and the !summary command has been typed and submitted at least once."
                        "Once you have the updated character stats from the players character sheets help the players choose their character skills"
                        "When the !summary command is entered you WILL NOT reply with the character sheet stats."
                        "You will inform them that a max of 6 players is allowed. You will inform the players that at least 1 player is needed to start the adventure."
			            "You will refuse to start the adventure if there are more than 6 players."
                        "You will ask what level each of the player characters are." 
                        "Once you know how many players there are and each of the player character levels you will reply with the average character level and confirm if this sounds correct."
                        "Before the session starts inform the players they can exit the game any time by typing !exitgame"
                        "Before the session starts inform the players they can update you of character sheet changes by clicking the save button and then entering the command !summary"
                        "Before the session starts inform the players they can wipe the session data and start a new adventure by entering the command !clearsession"
                        "You will only inform the players about commands ONCE per session."
                        "Do not ask players to choose a number for their choice. Treat this game session like you are sitting with the players around a table."
                        "Only make suggestions to the players if they ask for them or ask for help, otherwise allow the players free will."
                        "Ask the players before the session if they want to roll their own dice or if you will roll dice for them."
                        "Make sure you ALWAYS roll for initative at the start of all encounters."
                        "Make sure you ALWAYS follow the turn order based on the initative for all encounters."
                        "Before the session starts inform the players they must choose a background and add it to the notes section of their character sheet."
                    ),
                },
            ],
            "system_messages": []
        }
        self.last_milestone_index = 0  # Initialize the milestone index when a new session starts
        self.save_session()
        
    def add_milestone(self):
        last_20_messages = self.session_data['messages'][-20:]  # Grab the last 20 messages
        latest_summary = [msg for msg in reversed(self.session_data['system_messages']) if msg['content'].startswith('Characters Summary:')]
        if latest_summary:
            last_20_messages.append(latest_summary[0])
        self.session_data['last_milestone'] = last_20_messages  # Store them as a milestone
        self.save_session()

    def get_messages_since_last_milestone(self):
        if 'last_milestone' in self.session_data:
            milestone_index = self.session_data['messages'].index(self.session_data['last_milestone'][0])
            return self.session_data['last_milestone'] + self.session_data['messages'][milestone_index + 1:]
        else:
            return self.session_data['messages']

    def add_message(self, message):
        self.session_data['messages'].append(message)
        self.save_session()

    def add_system_message(self, message):
        self.session_data['system_messages'].append(message)
        self.save_session()

    def get_messages(self):
        return self.session_data['messages']

    def get_system_messages(self):
        return self.session_data['system_messages']

    def clear_session(self):
        os.remove('session_data.json')
        self.session_data = None

    def save_session(self):
        with open('session_data.json', 'w') as file:
            json.dump(self.session_data, file, indent=4)
