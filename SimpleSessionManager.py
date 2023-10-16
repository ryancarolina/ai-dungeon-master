import json
import os
import openai
import Config

class SimpleSessionManager:
    SOME_LIMIT = 700
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
                "You are the Gauntlet Master (GM) for a Gauntlets and Goblins (G&G) game. Follow all rules as if it were D&D 5th edition, but refer to the game as G&G."
                "Don't refer to yourself as an AI, only as the GM. You won't accept a new name."
                "Start each session by introducing yourself and asking for the number and levels of players. Max 6 players allowed."
                "Instruct players to fill out character sheets and submit via !summary before starting. Help them choose skills based on their stats."
                "You won't display the character stats when !summary is entered."
                "Players can exit anytime with !exitgame, update character sheets with !summary, or start anew with !clearsession. Inform them of these commands once per session."
                "Run the game as if you're at a physical table, no number-based choices. Ask players about dice rolling preferences."
                "Always roll for initiative and follow turn order in encounters."
                "Players must choose a background for their characters."
                "Use ascii art for maps and battle diagrams, prepend with [SKIP_TTS]."
                "Replace any mention of 'Dungeons and Dragons' or 'D&D' with 'Gauntlets and Goblins' or 'G&G'."
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
        last_15_messages = self.session_data['messages'][-15:]  # Grab the last 15 messages
        latest_summary = [msg for msg in reversed(self.session_data['system_messages']) if msg['content'].startswith('Characters Summary:')]
    
        if latest_summary:
            last_15_messages.append(latest_summary[0])
            # Ensure this latest_summary message also exists in 'messages'
            if latest_summary[0] not in self.session_data['messages']:
                self.session_data['messages'].append(latest_summary[0])
        
        self.session_data['last_milestone'] = last_15_messages  # Store them as a milestone
    
        self.last_milestone_index = len(self.session_data['messages']) - 15  # Update the index
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





