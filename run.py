"""
Program entry point
"""

import json
import os
import subprocess
import sys
import time

import src.config as config
import pandas as pd

# --- Read and process CSV file ---
# Replace with the actual path to your CSV file if different
csv_file_path = "dataSet_example.csv"
try:
    # Attempt to read with utf-8 encoding, common for CSVs with varied characters.
    # If you know the specific encoding (e.g., 'latin1', 'iso-8859-1'), use that.
    df = pd.read_csv(csv_file_path, encoding="utf-8")
except FileNotFoundError:
    print(f"Error: The file {csv_file_path} was not found.")
    sys.exit(1) # Exit if the data file is crucial and not found
except Exception as e:
    print(f"Error reading CSV file {csv_file_path}: {e}")
    sys.exit(1)


messages_list = []
# Extract data from 'Operational Scenario', 'Scenario', 'Task ID', and 'Query-en' columns
# Ensure these column names exactly match your CSV file header
required_columns = ["Operational Scenario", "Scenario", "Task ID", "Query-en"]
missing_columns = [col for col in required_columns if col not in df.columns]

if missing_columns:
    print(f"Error: The CSV file is missing the following required columns: {', '.join(missing_columns)}")
    sys.exit(1)

for index, row in df.iterrows():
    operational_scenario = row["Operational Scenario"]
    scenario = row["Scenario"]
    task_id = row["Task ID"]
    query_en = row["Query-en"] # Assuming Query-en is not PII
    messages_list.append((operational_scenario, scenario, task_id, query_en))

Operational_Scenarios = [item[0] for item in messages_list]
Scenarios = [item[1] for item in messages_list]
Task_IDs = [item[2] for item in messages_list] # Changed variable name for clarity
Queries_en = [item[3] for item in messages_list] # Changed variable name for clarity

# Renaming for consistency if these are used later, though they seem to be immediately repacked
operational_scenario_messages = []
scenario_messages = []
task_id_messages = [] # Changed variable name
query_messages = [] # Changed variable name

for op_scenario, scen, task_id_val, query_val in zip(
    Operational_Scenarios, Scenarios, Task_IDs, Queries_en
):
    operational_scenario_messages.append(op_scenario)
    scenario_messages.append(scen)
    task_id_messages.append(task_id_val)
    query_messages.append(query_val)

# List to store all subprocesses
processes = []
process_counter = 0 # Renamed for clarity

def start_terminal(program_path, task_id_arg, message_arg, operational_scenario_arg, scenario_arg):
    global process_counter
    process_counter += 1

    # Convert message to JSON string
    message_json = json.dumps(message_arg)

    # Get Python interpreter path from the current virtual environment
    python_executable = sys.executable

    # Run the target program using the Python interpreter from the virtual environment
    # Ensure program_path, task_id_arg, etc. are correctly passed
    try:
        process = subprocess.Popen(
            [
                python_executable,
                program_path,
                str(task_id_arg), # Make sure this is the intended argument
                message_json,
                str(operational_scenario_arg),
                str(scenario_arg),
            ],
            shell=False, # shell=False is generally safer
            stdout=subprocess.PIPE, # Capture stdout
            stderr=subprocess.PIPE  # Capture stderr
        )
        processes.append(process) # Add to list to wait for it later if not handled by process_counter logic
    except FileNotFoundError:
        print(f"Error: The program path '{program_path}' was not found.")
        return # Or handle error appropriately
    except Exception as e:
        print(f"Error starting subprocess for task {task_id_arg}: {e}")
        return


    # Original logic: wait for every 4th process. This might not be what's intended
    # if tasks are independent. If they must run in batches of 4, this is okay.
    # Consider if all processes should be started first, then all waited upon.
    if process_counter % 4 == 0: # Wait after every 4 processes are started
        # This will only wait for the *last* process started in the batch of 4,
        # if `processes` list is not used for waiting.
        # To wait for all 4, you'd need to manage the `processes` list more carefully here.
        # For now, sticking to original logic of communicating with the current `process`.
        stdout, stderr = process.communicate() # This waits for the current process

        # Check process exit code
        if process.returncode == 0:
            print(f"Program {program_path} executed successfully for task ID {task_id_arg}.")
            # print(f"Output:\n{stdout.decode()}") # Optionally print stdout
        else:
            print(
                f"Error occurred while executing {program_path} for task ID {task_id_arg}:"
            )
            if stderr:
                print(f"Error details:\n{stderr.decode()}")
            else:
                print("No error details on stderr.")
        # process_counter = 0 # Resetting here means only every 4th process triggers this block fully.
                           # If the goal is batches, this reset might be too soon or too late.
                           # If the goal is to limit concurrent processes, a different mechanism is needed.

def main():
    # Record start time
    start_time = time.time()
    
    # Assuming config.QUERY_RECEIVE is correctly set up in your config file
    # and is expected to be in English.
    program_path = config.QUERY_RECEIVE 
    if not os.path.exists(program_path):
        print(f"Error: query_receive program path not found: {program_path}")
        return

    # Iterate and start processes
    # Using the repacked variable names for clarity
    for op_scen, scen, task_id_val, query_val in zip(
        operational_scenario_messages, scenario_messages, task_id_messages, query_messages
    ):
        start_terminal(program_path, task_id_val, query_val, op_scen, scen)

    # Wait for any remaining subprocesses to complete
    # This loop is crucial if not all processes are handled by the process_counter % 4 logic
    for i, process in enumerate(processes):
        if process.poll() is None: # Check if process is still running
            print(f"Waiting for process {i+1} (Task ID: {task_id_messages[i] if i < len(task_id_messages) else 'N/A'}) to complete...")
            try:
                stdout, stderr = process.communicate() # Wait for this specific process
                if process.returncode == 0:
                    print(f"Process {i+1} (Task ID: {task_id_messages[i] if i < len(task_id_messages) else 'N/A'}) finished successfully.")
                else:
                    print(f"Process {i+1} (Task ID: {task_id_messages[i] if i < len(task_id_messages) else 'N/A'}) finished with error code {process.returncode}.")
                    if stderr:
                        print(f"Error details:\n{stderr.decode()}")
            except Exception as e:
                print(f"Exception while waiting for process {i+1}: {e}")


    # Record end time
    end_time = time.time()
    # Calculate and print execution time
    execution_time = end_time - start_time
    print(f"Total execution time: {execution_time:.4f} seconds")


if __name__ == "__main__":
    # Print configuration information (assuming config.GLOBAL_MODEL is relevant)
    print(f"Model: {config.GLOBAL_MODEL}\n")
    process_counter = 0 # Initialize counter here, as it's global in start_terminal
    main()
