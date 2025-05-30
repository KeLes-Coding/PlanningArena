"""
This file receives and processes the query.
"""

import copy
import json
import logging
import os
import sys
from plan_generater import plan_generater # Assuming plan_generater.py is in the same directory or PYTHONPATH
import config

def receive_and_process_query(): # Renamed function for clarity
    # Get arguments from the command line
    if len(sys.argv) < 5:
        print("Error: Missing command line arguments. Expected: message_number query_message operational_scenario scenario")
        sys.exit(1)
        
    message_number = sys.argv[1]
    query_message_json = sys.argv[2] # Assuming this is a JSON string, to be parsed if it's complex
    operational_scenario = sys.argv[3]
    scenario_category = sys.argv[4] # Renamed for clarity, as 'scenario' is also a variable name

    # Attempt to parse query_message if it's expected to be more than a simple string
    try:
        # If query_message_json is a simple string and not JSON, this might fail.
        # If it's always a simple string, json.loads isn't needed here.
        # Based on original code, it's concatenated directly, suggesting it's a string.
        query_content = query_message_json # If it's passed as a direct string
        # If it's passed as a JSON string containing the actual query:
        # query_data = json.loads(query_message_json)
        # query_content = query_data.get("query") # or whatever the key is
    except json.JSONDecodeError:
        print(f"Error: query_message (arg 2) is not a valid JSON string: {query_message_json}")
        # Fallback or error handling if query_message is expected to be JSON but isn't
        # For now, assuming it's a direct string as per original concatenation logic
        query_content = query_message_json


    planner_message_system_config = None
    result_message_system_config = None
    message_planner_config = None
    message_result_config = None

    if operational_scenario == "APP":
        planner_message_system_config = config.AGENT_PLANNER_APP
        result_message_system_config = config.AGENT_RESULT_APP
        message_planner_config = config.MESSAGE_PLANNER_APP
        message_result_config = config.MESSAGE_RESULT_APP
    elif operational_scenario == "API":
        planner_message_system_config = config.AGENT_PLANNER_API
        result_message_system_config = config.AGENT_RESULT_API
        if scenario_category == "1_travel":
            message_planner_config = config.MESSAGE_PLANNER_1_travel
            message_result_config = config.MESSAGE_RESULT_1_travel
        elif scenario_category == "2_entertainment":
            message_planner_config = config.MESSAGE_PLANNER_2_entertainment
            message_result_config = config.MESSAGE_RESULT_2_entertainment
        elif scenario_category == "3_shopping":
            message_planner_config = config.MESSAGE_PLANNER_3_shopping
            message_result_config = config.MESSAGE_RESULT_3_shopping
        elif scenario_category == "4_edu":
            message_planner_config = config.MESSAGE_PLANNER_4_edu
            message_result_config = config.MESSAGE_RESULT_4_edu
        elif scenario_category == "5_health":
            message_planner_config = config.MESSAGE_PLANNER_5_health
            message_result_config = config.MESSAGE_RESULT_5_health
        else:
            print(f"Error: Unknown scenario category '{scenario_category}' for API operational scenario.")
            # Initialize to empty lists or handle error appropriately to prevent NoneType issues later
            message_planner_config = [] 
            message_result_config = []
            # sys.exit(1) # Optionally exit if scenario is critical
    else:
        print(f"Error: Unknown operational_scenario '{operational_scenario}'.")
        # Initialize to prevent NoneType issues if execution continues
        message_planner_config = []
        message_result_config = []
        planner_message_system_config = []
        result_message_system_config = []
        # sys.exit(1) # Optionally exit

    # Ensure configs are not None before proceeding
    if message_planner_config is None or not message_planner_config:
        print(f"Error: message_planner_config is not properly initialized for scenario '{scenario_category}'.")
        # Handle error, perhaps by exiting or using a default empty config
        return # or sys.exit(1)

    try:
        # Prepare the message to be sent to the Planner
        # Ensure message_planner_config is a list and has at least one element if [0] is accessed
        if not isinstance(message_planner_config, list) or not message_planner_config:
             print(f"Error: message_planner_config is empty or not a list for scenario '{scenario_category}'.")
             # Handle error appropriately
             return # or sys.exit(1)

        combined_messages_for_planner = copy.deepcopy(message_planner_config[0]) # Assumes it's a string
        combined_messages_for_planner += query_content # Concatenate the query string

        # The original commented-out line suggests combined_messages might be a list of dicts:
        # combined_messages[-1]["content"] += query_message
        # If that's the case, the deepcopy and concatenation logic needs to be adjusted.
        # For now, following the uncommented logic: combined_messages = combined_messages[0] + query_message

        # print(f"Debug: Combined message for planner: {combined_messages_for_planner}") # Optional debug print

        # Ensure other configs are valid before passing to plan_generater
        if message_result_config is None or planner_message_system_config is None or result_message_system_config is None:
            print("Error: One or more system message configurations are None.")
            return # or sys.exit(1)


        executor = plan_generater(
            message_number,
            combined_messages_for_planner,
            query_content, # Pass the processed query content
            message_result_config,
            planner_message_system_config,
            result_message_system_config,
        )
        executor.PlanGenerater() # Assuming this method exists in plan_generater class
        print(f"Program {message_number} executed successfully.")

    except Exception as e:
        # Ensure the directory exists, create if it doesn't
        error_data_path = config.ERROR_DATA
        # It's safer to ensure error_data_path itself exists if it's a base for further subdirectories
        if not os.path.exists(error_data_path):
             os.makedirs(error_data_path, exist_ok=True) # exist_ok=True is helpful

        # Then create the specific message_number directory
        error_log_directory = os.path.join(error_data_path, str(message_number))
        if not os.path.exists(error_log_directory):
            os.makedirs(error_log_directory, exist_ok=True)

        error_file_name = f"{message_number}-error.log"
        error_file_path = os.path.join(error_log_directory, error_file_name)
        
        # Configure logging
        # BasicConfig should ideally be called once. If called multiple times, it might not reconfigure.
        # For simplicity here, it's kept as is, but in larger apps, configure logging at app start.
        logging.basicConfig(
            filename=error_file_path,
            level=logging.DEBUG,
            format="%(asctime)s - %(levelname)s - %(module)s - %(message)s", # Added module for more context
            filemode='a' # Append to log file
        )
        logging.error(
            f"Program execution failed (message_number: {message_number}, query: {query_content[:100]}...): {str(e)}", # Log part of the query for context
            exc_info=True, # This will include the stack trace
        )
        print(f"Program {message_number} execution failed: {str(e)}. Check log at {error_file_path}")

if __name__ == "__main__":
    receive_and_process_query()
