import json
import re

from openai import OpenAI
import os
import sys

sys.path.append("..") # Assuming this relative path is correct for the execution environment
import config # Assuming config.py is in the parent directory or Python path

os.environ["HTTP_PROXY"] = config.HTTP_PROXY
# Initialize OpenAI client
client = OpenAI(api_key=config.API_KEY, base_url=config.BASE_URL)
GlobalModel = config.GLOBAL_MODEL


class Agent:
    def __init__(self, name):
        self.name = name
        self.messages = []

    def clean_json_string(self, json_str):
        # Use regular expressions to remove redundant ```json and ``` markers
        cleaned_str = re.sub(r"```json\s*", "", json_str)
        cleaned_str = re.sub(r"```\s*", "", cleaned_str)
        return cleaned_str


# Define agent class
class Agent_Planner(Agent):
    def __init__(self, name, message_number, message_system):
        super().__init__(name) # Call to superclass constructor
        message_number_int = int(message_number) # Renamed to avoid confusion if message_number is reused
        
        user_data_path_prefix = "" # Base path for user data files
        user_file_index = 0
        user_info = {} # Default to empty dict

        # Determine user data file path based on message_number_int
        if message_number_int <= 3600:
            user_data_path_prefix = "user/user_TheFour_1" # Assuming this path exists
            user_file_index = (message_number_int - 1) // 180 + 1
        elif message_number_int < 4500: # Consistent with original logic
            user_data_path_prefix = "user/user_DAG_1" # Assuming this path exists
            user_file_index = (message_number_int - 3601) // 30 + 1
        
        if user_data_path_prefix and user_file_index > 0:
            user_file_path = f"{user_data_path_prefix}/user_{user_file_index}.json"
            try:
                with open(
                    user_file_path,
                    "r",
                    encoding="utf-8",
                ) as file:
                    user = json.load(file)
                    user_info = user.get("userInfo", {}) # Get userInfo, default to empty dict
            except FileNotFoundError:
                print(f"Warning: User data file not found at {user_file_path} for Agent_Planner")
            except json.JSONDecodeError:
                 print(f"Warning: Could not decode JSON from {user_file_path} for Agent_Planner")
        
        print(f"User_File_Index: {user_file_index}, Message_Number: {message_number_int}, UserInfo_Keys: {list(user_info.keys())}") # Example print, adjust as needed

        self.messages.append(
            {
                "role": "system",
                "content": f"{message_system[0]}", # Assuming message_system is a list/tuple with at least one element
            }
        )
        # print(f"message_system: {message_system}")

    def interact(self, message):
        # Add user input to the message list
        self.messages.append({"role": "user", "content": message})

        # Call OpenAI API to get response
        response = client.chat.completions.create(
            model=GlobalModel,
            # model="qwen-plus", # Example of an alternative model
            messages=self.messages,
            temperature=0,
            # response_format={"type": "json_object"}, # If JSON mode is desired and supported
        )

        # Get and return AI's response
        ai_response = response.choices[0].message
        # print()
        # print(ai_response.content)
        # print()
        self.messages.append(ai_response) # Add AI's response to maintain conversation history
        # print(self.clean_json_string(ai_response.content))
        return self.clean_json_string(ai_response.content)


# Define agent class
class Agent_Result(Agent):
    def __init__(self, name, message_system):
        super().__init__(name) # Call to superclass constructor
        self.messages.append(
            {
                "role": "system",
                "content": f"{message_system[0]}", # Assuming message_system is a list/tuple
            }
        )
        # print(f"Result_message_system: {message_system}")

    def interact(self, message):
        # Add user input to the message list
        self.messages.append({"role": "user", "content": message})

        # Call OpenAI API to get response
        response = client.chat.completions.create(
            model=GlobalModel, messages=self.messages, temperature=0
        )

        # Get and return AI's response
        ai_response = response.choices[0].message
        # print(ai_response.content)
        self.messages.append(ai_response) # Add AI's response
        # print(self.clean_json_string(ai_response.content))
        return self.clean_json_string(ai_response.content)
