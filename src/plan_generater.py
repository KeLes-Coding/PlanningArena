"""
PLAN Generator
"""

import copy
import json
import os
from Agent.agents import Agent_Planner, Agent_Result # Assuming Agent.agents is a valid import
import config # Assuming config is a valid import
from openpyxl import load_workbook # Assuming openpyxl is installed and used

class plan_generater:
    def __init__(
        self,
        message_number,
        query,
        query_message,
        message_Result,
        planner_message_system,
        result_message_system,
    ):
        # Receive 0_query number
        self.message_number = message_number
        # 0_query
        self.query = query
        self.query_message = query_message
        self.message_result = message_Result
        self.planner_message_system = planner_message_system
        self.result_message_system = result_message_system

        self.message_planner = []
        self.message_results = []
        self.message_total = []

    # Agent Initialization
    def AgentInit(self):
        agents = [
            Agent_Planner("Planner", self.message_number, self.planner_message_system),
            Agent_Result("Result", self.result_message_system),
        ]
        return agents

    """
        Information Processing Module
    """

    # Planner Printer
    def PlannerJsonPrinter(self, json_data):
        formatted_json = {
            "GlobalThought": json_data["GlobalThought"],
            "OrderSteps": {
                "TotalSteps": json_data["OrderSteps"]["TotalSteps"],
                "StepDetail": {
                    "StepNumber": json_data["OrderSteps"]["StepDetail"]["StepNumber"],
                    "Description": json_data["OrderSteps"]["StepDetail"]["Description"],
                    "Action": json_data["OrderSteps"]["StepDetail"]["Action"],
                },
            },
        }
        self.message_planner.append(formatted_json)
        return formatted_json

    # Result Printer
    def ResultJsonPrinter(self, json_data):
        formatted_json = {
            "OrderSteps": {
                # "TotalSteps": json_data["OrderSteps"]["TotalSteps"],
                "StepDetail": {
                    "StepNumber": json_data["OrderSteps"]["StepDetail"]["StepNumber"],
                    "Description": json_data["OrderSteps"]["StepDetail"]["Description"],
                    "Action": json_data["OrderSteps"]["StepDetail"]["Action"],
                    "Results": json_data["OrderSteps"]["StepDetail"]["Results"],
                },
            },
        }
        self.message_results.append(formatted_json)

        # Append "Results" to "OrderSteps" with the same StepNumber to form the message_total for that StepNumber
        messages_total = copy.deepcopy(self.message_planner[-1])
        messages_total["OrderSteps"]["StepDetail"]["Results"] = json_data["OrderSteps"][
            "StepDetail"
        ]["Results"]
        self.message_total.append(messages_total)
        return formatted_json

    """
        File Saving Module
    """

    # File save function
    def message_save(self):
        self.message_planner_save()
        self.message_results_save()
        self.message_total_save()
        print("File saved successfully!")

    # Save message_planner to file
    def message_planner_save(self):
        # Ensure the directory exists, create it if it does not
        json_data_path = config.JSON_DATA # Assuming config.JSON_DATA is the correct path
        directory = f"{json_data_path}/{self.message_number}"
        if not os.path.exists(directory):
            os.makedirs(directory)

        file_name = self.message_number + "-message_planner.json"
        file_path = os.path.join(directory, file_name)

        data = {"MessageNumber": self.message_number, "Query": self.query_message}

        formatted_planner = []
        formatted_planner.append(data)
        for json_str in self.message_planner:
            formatted_planner.append(json_str)
        with open(file_path, "w", encoding="utf-8") as json_file: # Added encoding for consistency
            json.dump(formatted_planner, json_file, indent=4, ensure_ascii=False) # ensure_ascii=False for non-ASCII if any in data

    # Save message_results to file
    def message_results_save(self):
        # Ensure the directory exists, create it if it does not
        json_data_path = config.JSON_DATA
        directory = f"{json_data_path}/{self.message_number}"
        if not os.path.exists(directory):
            os.makedirs(directory)

        file_name = self.message_number + "-message_results.json"
        file_path = os.path.join(directory, file_name)

        data = {"MessageNumber": self.message_number, "Query": self.query_message}

        formatted_results = []
        formatted_results.append(data)
        for json_str in self.message_results:
            formatted_results.append(json_str)
        with open(file_path, "w", encoding="utf-8") as json_file: # Added encoding
            json.dump(formatted_results, json_file, indent=4, ensure_ascii=False) # ensure_ascii=False

    # Save message_total to file
    def message_total_save(self):
        # Ensure the directory exists, create it if it does not
        json_data_path = config.JSON_DATA
        directory = f"{json_data_path}/{self.message_number}"
        directory_2 = f"{json_data_path}/message_total"
        if not os.path.exists(directory):
            os.makedirs(directory)
        if not os.path.exists(directory_2):
            os.makedirs(directory_2)
        file_name = self.message_number + "-message_total.json"
        file_path = os.path.join(directory, file_name)
        file_path_2 = os.path.join(directory_2, file_name)

        data = {"MessageNumber": self.message_number, "Query": self.query_message}

        formatted_total = []
        formatted_total.append(data)
        for json_str in self.message_total:
            formatted_total.append(json_str)
        with open(file_path, "w", encoding="utf-8") as json_file: # Added encoding
            json.dump(formatted_total, json_file, indent=4, ensure_ascii=False) # ensure_ascii=False
        with open(file_path_2, "w", encoding="utf-8") as json_file: # Added encoding
            json.dump(formatted_total, json_file, indent=4, ensure_ascii=False) # ensure_ascii=False

    """
        Dialog Generation Module
    """

    # Dialog generator
    def PlanGenerater(self):
        # agents initialization
        agents = self.AgentInit()
        message_number_int = int(self.message_number) # Renamed to avoid conflict if message_number is reused
        
        user_data_path_prefix = "" # Base path for user data files
        user_file_index = 0
        
        if message_number_int <= 3600:
            user_data_path_prefix = "user_TheFour_1" # Assuming this path exists
            user_file_index = (message_number_int - 1) // 180 + 1
        elif message_number_int < 4500: # Corrected condition from original code logic
            user_data_path_prefix = "user_DAG_1" # Assuming this path exists
            user_file_index = (message_number_int - 3601) // 30 + 1
        
        user_info = {} # Default to empty dict if file not found or other issues
        if user_data_path_prefix and user_file_index > 0:
            user_file_path = f"{user_data_path_prefix}/user_{user_file_index}.json"
            try:
                with open(user_file_path, "r", encoding="utf-8") as file:
                    user = json.load(file)
                    user_info = user.get("userInfo", {}) # Get userInfo, default to empty dict
            except FileNotFoundError:
                print(f"Warning: User data file not found at {user_file_path}")
            except json.JSONDecodeError:
                print(f"Warning: Could not decode JSON from {user_file_path}")


        # The first Agent (Planner) gets the query and starts the first step of planning
        # print(f"User Info:\n{user_info}\nQuery:{self.query}")
        ai_response_str = agents[0].interact(f"User Info:\n{user_info}\nQuery:{self.query}")
        
        try:
            json_data = json.loads(ai_response_str)
        except json.JSONDecodeError:
            print(f"Error: Planner initial response is not valid JSON: {ai_response_str}")
            return # Exit if initial plan is not valid

        TotalSteps = json_data.get("OrderSteps", {}).get("TotalSteps")
        if TotalSteps is None:
            print(f"Error: Could not determine TotalSteps from Planner response: {json_data}")
            return # Exit if TotalSteps is not found

        print(f"Total steps: {TotalSteps}")
        ai_response_json_printed = self.PlannerJsonPrinter(json_data) # Renamed to avoid confusion
        print(f"{agents[0].name}:")
        print(json.dumps(ai_response_json_printed, indent=4, ensure_ascii=False))

        current_ai_response_str = ai_response_str # Keep track of the current response string

        # Start conversation between agents:
        while True:
            # The current agent's response serves as the input for the next agent
            next_agent = agents[1] # This will alternate between Result and Planner after agents.reverse()

            try:
                current_ai_response_json = json.loads(current_ai_response_str)
            except json.JSONDecodeError:
                print(f"Error: Could not parse current AI response to JSON: {current_ai_response_str}")
                break # Exit loop if response is not valid JSON

            # Divide roles based on next_agent.name
            if next_agent.name == "Planner":
                # When the role is Planner, transmit the Results of the previous agent (Result) to the Planner
                ai_response_Results = current_ai_response_json.get("OrderSteps", {}).get("StepDetail", {}).get("Results")
                ai_response_step = current_ai_response_json.get("OrderSteps", {}).get("StepDetail", {}).get("StepNumber")

                if ai_response_Results is None or ai_response_step is None:
                    print(f"Error: Missing 'Results' or 'StepNumber' in Result's response: {current_ai_response_json}")
                    break 
                
                next_input = f"The execution result of step {ai_response_step} is:\n {ai_response_Results}\n Next, proceed to step {int(ai_response_step) + 1}"
                print(f"Input for Planner: {next_input}")
                current_ai_response_str = next_agent.interact(next_input)
                # Print the current agent's response
                try:
                    parsed_planner_response = json.loads(current_ai_response_str)
                    ai_response_json_printed = self.PlannerJsonPrinter(parsed_planner_response)
                    print(f"{next_agent.name}:")
                    print(json.dumps(ai_response_json_printed, indent=4, ensure_ascii=False))
                except json.JSONDecodeError:
                    print(f"Error: Planner response is not valid JSON: {current_ai_response_str}")
                    break


            elif next_agent.name == "Result":
                # When the role is Result, transmit the Action of the previous agent (Planner) to Result
                ai_response_Action = current_ai_response_json.get("OrderSteps", {}).get("StepDetail", {}).get("Action")
                ai_response_step = current_ai_response_json.get("OrderSteps", {}).get("StepDetail", {}).get("StepNumber")

                if ai_response_Action is None or ai_response_step is None:
                    print(f"Error: Missing 'Action' or 'StepNumber' in Planner's response: {current_ai_response_json}")
                    break

                # Use Results as input for the next agent (Result agent)
                if ai_response_step == 1:
                    user_input_for_result = f"{ai_response_Action}\n Next, proceed to step {ai_response_step}'s result"
                    # Ensure self.message_result is a list and has at least one element
                    if self.message_result and isinstance(self.message_result, list):
                         next_input = self.message_result[0] + user_input_for_result
                    else:
                        print("Warning: self.message_result is not properly initialized or empty. Using action only.")
                        next_input = user_input_for_result
                else:
                    next_input = f"The execution Action of step {ai_response_step} is:\n {ai_response_Action}\n Next, proceed to step {ai_response_step}'s result"
                
                print(f"Input for Result: {next_input}")
                current_ai_response_str = next_agent.interact(next_input)
                
                # Print the current agent's response
                # Use regular expressions to match if there are ```json and ``` before and after (original comment)
                # The actual parsing should handle this, but if the output is non-JSON text with JSON embedded, it needs pre-processing.
                # For now, assuming interact returns a clean JSON string or a string that json.loads can handle.
                try:
                    parsed_result_response = json.loads(current_ai_response_str)
                    ai_response_json_printed = self.ResultJsonPrinter(parsed_result_response)
                    print(f"{next_agent.name}:")
                    print(json.dumps(ai_response_json_printed, indent=4, ensure_ascii=False))
                except json.JSONDecodeError:
                    print(f"Error: Result response is not valid JSON: {current_ai_response_str}")
                    break
                
                # After getting the Result's Response, get its StepNumber. If StepNumber = TotalSteps, exit the loop
                # Re-parse because ResultJsonPrinter might not return the full structure needed for step_number check
                try:
                    step_check_json = json.loads(current_ai_response_str) 
                    step_number = step_check_json.get("OrderSteps", {}).get("StepDetail", {}).get("StepNumber")
                    if step_number is None:
                        print(f"Error: Could not determine StepNumber from Result's response for loop check: {step_check_json}")
                        break
                    
                    if step_number == TotalSteps:
                        print("Generation finished!")
                        self.message_save()
                        break
                except json.JSONDecodeError:
                    print(f"Error: Could not parse Result response for step check: {current_ai_response_str}")
                    break


            # Switch agent
            agents.reverse()
