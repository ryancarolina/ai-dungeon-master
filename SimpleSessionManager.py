import json
import os
import openai
import Config

class SimpleSessionManager:
    SOME_LIMIT = 1000
    openai.api_key = Config.API_KEY
    def __init__(self):
        self.session_data = None
        if os.path.exists('session_data.json'):
            with open('session_data.json', 'r') as file:
                self.session_data = json.load(file)

    def session_exists(self):
        return self.session_data is not None
        
    def start_session(self):
        initial_system_message = {
            "role": "system",
            "content": (
                "You are the greatest dungeon master of all time. You will make each session tough but fair!"
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
                "You will inform them that a max of 6 players is allowed."
		        "You will refuse to start the adventure if there are more than 6 players."
                "You will ask what level each of the player characters are." 
                "Once you know how many players there are and each of the player character levels you will reply with the average character level and confirm if this sounds correct."
                "Before the session starts inform the players they can exit the game any time by typing !exitgame"
                "Before the session starts inform the players they can update you of character sheet changes by clicking the save button and then entering the command !summary"
                "Before the session starts inform the players they can wipe the session data and start a new adventure by entering the command !clearsession"
                "You will only inform the players about commands ONCE per session."
                "Do not ask players to choose a number for their choice. Treat this game session like you are sitting with the players around a table."
                "Ask the players before the session if they want to roll their own dice or if you will roll dice for them."
                "Make sure you ALWAYS roll for initative at the start of all encounters."
                "Make sure you ALWAYS follow the turn order based on the initative for all encounters."
                "Before the session starts inform the players they must choose a background and add it to the notes section of their character sheet."
                "You will use ascii art to draw out simple maps for the players. When you use ascii art you prepend it with [SKIP_TTS]" 
                "You will use ascii art to draw out simple diagrams to show the location of monsters and the players during battle. WHEN YOU USE ASCII ART YOU WILL PREPEND IT WITH [SKIP_TTS]"
            ),
        }

        self.session_data = {
            "messages": [initial_system_message],
            "system_messages": [],
            "last_milestone": [initial_system_message]  # Initialize last_milestone with the initial system message
        }

        self.last_milestone_index = 0  # Initialize the milestone index when a new session starts
        self.save_session()
        assert self.session_data['last_milestone'] == self.session_data['messages'][:len(self.session_data['last_milestone'])]
        
    def get_token_count(self):
        total_tokens = 0
        for message in self.session_data['messages']:
            content = message['content']
            # Naively count tokens by splitting the string by spaces
            tokens = content.split(' ')
            total_tokens += len(tokens)
        return total_tokens

    def add_milestone(self):
        last_10_messages = self.session_data['messages'][-10:]  # Grab the last 10 messages
        latest_summary = [msg for msg in reversed(self.session_data['system_messages']) if msg['content'].startswith('Characters Summary:')]
    
        if latest_summary:
            last_10_messages.append(latest_summary[0])
            # Ensure this latest_summary message also exists in 'messages'
            if latest_summary[0] not in self.session_data['messages']:
                self.session_data['messages'].append(latest_summary[0])
        
        self.session_data['last_milestone'] = last_10_messages  # Store them as a milestone
    
        # Update your assertions here to ensure that 'last_milestone' is consistent with 'messages'
        #if len(self.session_data['messages']) >= 10:
            #assert set(self.session_data['last_milestone']).issubset(set(self.session_data['messages'][-10:]))
    
        self.last_milestone_index = len(self.session_data['messages']) - 10  # Update the index
        self.save_session()

    def get_messages_since_last_milestone(self):
        try:
            milestone_index = self.session_data['messages'].index(self.session_data['last_milestone'][0])
            return self.session_data['last_milestone'] + self.session_data['messages'][milestone_index + 1:]
        except ValueError as e:
            print(f"An error occurred: {e}")
            print(f"Debug Info: last_milestone[0] = {self.session_data['last_milestone'][0]}")
            print(f"Debug Info: messages = {self.session_data['messages']}")
            return []
        
    def add_message(self, message):
        print("Debug: add_message is called.")  # Debug statement 1
        self.session_data['messages'].append(message)
        print(f"Debug: Message added: {message}")  # Debug statement 2

        # Check token count after adding the message
        current_token_count = self.get_token_count()
        print(f"Debug: Current token count: {current_token_count}")  # Debug statement 3

        if current_token_count > self.SOME_LIMIT:
            print("Debug: Token limit exceeded. Summarizing...")  # Debug statement 4
            oldest_messages = self.get_oldest_messages()
            summarized_message = self.summarize(oldest_messages)
            self.replace_oldest_messages_with_summary(summarized_message)

        self.save_session()
        print("Debug: Session saved.")  # Debug statement 5
        
        #if len(self.session_data['messages']) >= 10:
            #assert self.session_data['last_milestone'] == self.session_data['messages'][-10:]

        #assert self.session_data['last_milestone'] == self.session_data['messages'][-10:]

    def add_system_message(self, message):
        self.session_data['system_messages'].append(message)
        self.save_session()

    def get_messages(self):
        return self.session_data['messages']

    def get_system_messages(self):
        return self.session_data['system_messages']

    def clear_session(self):
        if os.path.exists('session_data.json'):
            os.remove('session_data.json')
        self.session_data = None

    def save_session(self):
        #print("Debug: self.session_data['last_milestone']:", self.session_data['last_milestone'])
        #print("Debug: self.session_data['messages'][-10:]:", self.session_data['messages'][-10:])
        
        #if len(self.session_data['messages']) >= 10:
            #assert self.session_data['last_milestone'] == self.session_data['messages'][-10:]

        #assert self.session_data['last_milestone'] == self.session_data['messages'][-10:]

        with open('session_data.json', 'w') as file:
            json.dump(self.session_data, file, indent=4)
            
    def get_oldest_messages(self, num_messages=5):
        return self.session_data['messages'][:num_messages]

    def replace_oldest_messages_with_summary(self, summarized_message, num_messages=5):
        # Remove the oldest messages from both 'messages' and 'last_milestone'
        del self.session_data['messages'][:num_messages]
        self.session_data['last_milestone'] = [m for m in self.session_data['last_milestone'] if m not in self.session_data['messages'][:num_messages]]
    
        # Add the summarized message to the beginning of 'messages'
        summary_message = {"role": "system", "content": summarized_message}
        self.session_data['messages'].insert(0, summary_message)
    
        # If the summarized message is supposed to be part of the 'last_milestone',
        # you can add it there as well.
        self.session_data['last_milestone'].insert(0, summary_message)
    
        # Since we've made changes, save the session data.
        self.save_session()
        
    def summarize(self, messages):
        # Convert the list of message dictionaries to a single string
        prompt = " ".join([msg['content'] for msg in messages])
    
        # Initialize retry count and maximum retries
        retry_count = 0
        max_retries = 3
    
        while retry_count < max_retries:
            try:
                # Make the API call to get the summary
                chat = openai.ChatCompletion.create(
                    model="gpt-3.5-turbo",
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a helpful assistant whos job is to summarize. When you summarize it will be clear and concise."
                        },
                        {
                            "role": "user",
                            "content": f"Please summarize the following conversation: {prompt}"
                        }
                    ],
                    max_tokens=100  # Limit the response to 100 tokens
                )
                # Extract the generated summary text from the API response
                summary_text = chat.choices[0].message['content'].strip()
                return summary_text

            except Exception as e:
                print(f"An error occurred: {e}")
                retry_count += 1
                print(f"Retrying... {retry_count}")
            
        return "Error in summarization, could not summarize after multiple attempts."





