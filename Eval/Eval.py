import json
import re
import os
import requests
from collections import OrderedDict

# --- LLM Client ---
class LLMClient:
    """
    Uses the requests library for LLM API calls.
    Supports OPENAI and GEMINI modes.
    """
    def __init__(self, model_type="OPENAI",
                 openai_api_key=None, openai_endpoint=None, openai_model=None,
                 gemini_api_key=None, gemini_endpoint=None, gemini_model=None,
                 proxy_address=None): # Added proxy address parameter
        self.model_type = model_type

        # OpenAI Configuration
        self.openai_api_key = openai_api_key
        self.openai_endpoint = openai_endpoint if openai_endpoint else "https://api.openai.com/v1/chat/completions"
        self.openai_model = openai_model if openai_model else "gpt-3.5-turbo"

        # Gemini Configuration
        self.gemini_api_key = gemini_api_key
        self.gemini_endpoint = gemini_endpoint if gemini_endpoint else "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
        self.gemini_model = gemini_model if gemini_model else "gemini-pro"

        # Proxy Settings
        self.proxy_address = proxy_address
        self.proxies = {
            "http": proxy_address,
            "https": proxy_address,
        } if proxy_address else None


    def call_llm(self, prompt):
        """
        Sends an API request to the specified LLM.
        Args:
            prompt (str): The prompt to send to the LLM.
        Returns:
            dict: A JSON response structured as {'Result': True/False, 'Description': 'reason'}.
        """
        headers = {"Content-Type": "application/json"}
        payload = {}
        llm_response_content = ""

        print(f"\n--- Calling LLM ({self.model_type}) for prompt (first 100 chars): {prompt[:100]}... ---")

        try:
            if self.model_type == "OPENAI":
                if not self.openai_api_key:
                    raise ValueError("OpenAI API key is not set.")
                headers["Authorization"] = f"Bearer {self.openai_api_key}"
                payload = {
                    "model": self.openai_model,
                    "messages": [{"role": "user", "content": prompt}],
                    "response_format": {"type": "json_object"}
                }
                response = requests.post(self.openai_endpoint, headers=headers, json=payload, timeout=60, proxies=self.proxies) # Added proxies
                response.raise_for_status()
                llm_output = response.json()
                llm_response_content = llm_output['choices'][0]['message']['content']

            elif self.model_type == "GEMINI":
                if not self.gemini_api_key:
                    raise ValueError("Gemini API key is not set.")
                url_with_key = f"{self.gemini_endpoint}?key={self.gemini_api_key}"
                payload = {
                    "contents": [{"parts": [{"text": prompt}]}]
                }
                response = requests.post(url_with_key, headers=headers, json=payload, timeout=60, proxies=self.proxies) # Added proxies
                response.raise_for_status()
                llm_output = response.json()
                if 'candidates' in llm_output and llm_output['candidates']:
                    llm_response_content = llm_output['candidates'][0]['content']['parts'][0]['text']
                else:
                    raise Exception(f"Gemini API response did not find 'candidates' or content: {llm_output}")

            else:
                return {"Result": False, "Description": f"Unsupported LLM model type: {self.model_type}"}

            try:
                parsed_content = json.loads(llm_response_content)
                if "Result" in parsed_content and "Description" in parsed_content:
                    return parsed_content
                else:
                    return {"Result": False, "Description": f"LLM response did not include expected 'Result' or 'Description' keys: {llm_response_content}"}
            except json.JSONDecodeError:
                return {"Result": False, "Description": f"LLM returned invalid JSON: {llm_response_content}"}

        except requests.exceptions.Timeout:
            print("LLM API request timed out.")
            return {"Result": False, "Description": "LLM API request timed out."}
        except requests.exceptions.ConnectionError:
            print("LLM API connection error.")
            return {"Result": False, "Description": "LLM API connection error."}
        except requests.exceptions.HTTPError as e:
            print(f"LLM API HTTP error: {e.response.status_code} - {e.response.text}")
            return {"Result": False, "Description": f"LLM API HTTP error: {e.response.status_code} - {e.response.text}"}
        except ValueError as e:
            print(f"Configuration error: {e}")
            return {"Result": False, "Description": f"Configuration error: {e}"}
        except Exception as e:
            print(f"An unexpected error occurred during LLM call: {e}")
            return {"Result": False, "Description": f"An unexpected error occurred during LLM call: {e}"}

# --- Evaluation Agents (Keep unchanged) ---
class EvaluationAgent:
    def __init__(self, name):
        self.name = name

    def evaluate(self, *args, **kwargs):
        raise NotImplementedError("Subclasses must implement the 'evaluate' method'")

    def _format_response(self, result, reason):
        return {"Result": result, "Description": reason}

class TaskSuccessAgent(EvaluationAgent):
    def __init__(self):
        super().__init__("TaskSuccessAgent")

    def evaluate(self, query, global_thought, steps_data):
        if not (query and global_thought and query in global_thought):
            return self._format_response(False, "Query and GlobalThought do not align perfectly.")

        total_steps_declared = steps_data[0]['OrderSteps']['TotalSteps'] if steps_data and steps_data[0].get('OrderSteps') else 0
        actual_steps = len(steps_data)
        if total_steps_declared != actual_steps:
            return self._format_response(False, f"Declared total steps ({total_steps_declared}) does not match actual steps ({actual_steps}).")

        for step in steps_data:
            step_detail = step.get('OrderSteps', {}).get('StepDetail', {})
            step_number = step_detail.get('StepNumber')
            description = step_detail.get('Description')
            results = step_detail.get('Results')

            if not description:
                return self._format_response(False, f"Step {step_number}: Description is missing.")
            if results and isinstance(results, dict) and 'status' in results and results['status'] is not True:
                return self._format_response(False, f"Step {step_number}: Results indicate failure (status is not True).")

        return self._format_response(True, "All steps appear to be successful and align with the overall task.")

class DependencyCheckAgent(EvaluationAgent):
    def __init__(self):
        super().__init__("DependencyCheckAgent")

    def evaluate(self, query, steps_data):
        step_actions = [s.get('OrderSteps', {}).get('StepDetail', {}).get('Action', '') for s in steps_data]

        paris_location_converted = False
        hotel_search_done = False
        weather_check_done = False

        for i, action in enumerate(step_actions):
            if "BookingLocationToLatLong" in action and "Paris" in action:
                paris_location_converted = True
            elif "BookingCOM" in action:
                hotel_search_done = True
                if not paris_location_converted:
                    return self._format_response(False, f"Step {i+1}: Hotel search performed before Paris location conversion.")
            elif "OpenWeather" in action:
                weather_check_done = True
                if not paris_location_converted:
                    return self._format_response(False, f"Step {i+1}: Weather check performed before Paris location conversion.")

        if "find a hotel" in query.lower() and not hotel_search_done:
            return self._format_response(False, "Query includes 'find a hotel' but no hotel search step was found.")
        if "check the weather forecast" in query.lower() and not weather_check_done:
            return self._format_response(False, "Query includes 'check the weather forecast' but no weather check step was found.")

        return self._format_response(True, "Dependencies appear to be satisfied based on the sequence of steps.")

class RedundantStepsAgent(EvaluationAgent):
    def __init__(self, llm_client):
        super().__init__("RedundantStepsAgent")
        self.llm_client = llm_client

    def evaluate(self, query, steps_data):
        step_descriptions = [s.get('OrderSteps', {}).get('StepDetail', {}).get('Description', '') for s in steps_data]
        prompt = (f"Given the main query: '{query}', and the following sequence of steps: "
                  f"{', '.join(filter(None, step_descriptions))}. Are there any redundant steps? " # filter(None, ...) to remove empty descriptions
                  "Respond with a JSON object in the format: {'Result': True/False, 'Description': 'brief reason'}.")
        llm_response = self.llm_client.call_llm(prompt)
        return self._format_response(llm_response.get('Result', False), llm_response.get('Description', 'LLM did not return a valid response for RedundantStepsAgent.'))


class MissingStepsAgent(EvaluationAgent):
    def __init__(self, llm_client):
        super().__init__("MissingStepsAgent")
        self.llm_client = llm_client

    def evaluate(self, query, steps_data):
        step_descriptions = [s.get('OrderSteps', {}).get('StepDetail', {}).get('Description', '') for s in steps_data]
        prompt = (f"Given the main query: '{query}', and the following sequence of steps: "
                  f"{', '.join(filter(None, step_descriptions))}. Are there any crucial steps missing to fully achieve the query? "
                  "Respond with a JSON object in the format: {'Result': True/False, 'Description': 'brief reason'}.")
        llm_response = self.llm_client.call_llm(prompt)
        return self._format_response(llm_response.get('Result', False), llm_response.get('Description', 'LLM did not return a valid response for MissingStepsAgent.'))


class FictitiousMisusedParametersAgent(EvaluationAgent):
    def __init__(self, llm_client):
        super().__init__("FictitiousMisusedParametersAgent")
        self.llm_client = llm_client

    def evaluate(self, steps_data):
        for step in steps_data:
            step_detail = step.get('OrderSteps', {}).get('StepDetail', {})
            step_number = step_detail.get('StepNumber')
            action_str = step_detail.get('Action', '')

            match = re.match(r"(\w+)\((.*)\)", action_str)
            if not match:
                # If action_str is empty or doesn't match, it's not necessarily an error for this agent,
                # but we might log it or handle it depending on strictness. For now, skip.
                continue

            tool_name = match.group(1)
            params_str = match.group(2)

            prompt = (f"Given the tool '{tool_name}' and its parameters '{params_str}', "
                      "do these parameters seem fictitious or misused for a typical use case of this tool? "
                      "Respond with a JSON object in the format: {'Result': True/False, 'Description': 'brief reason'}.")
            llm_response = self.llm_client.call_llm(prompt)
            # This agent should return True if a fictitious/misused parameter IS found.
            # So, if LLM says Result:True (meaning "yes, it seems fictitious"), this agent's overall result for this step is True.
            if llm_response.get('Result') is True:
                return self._format_response(True, f"Step {step_number}: {llm_response.get('Description', 'LLM indicated fictitious/misused parameter but provided no description.')}")

        return self._format_response(False, "No fictitious or misused parameters detected by LLM.")

class FictitiousToolAgent(EvaluationAgent):
    def __init__(self):
        super().__init__("FictitiousToolAgent")

    def evaluate(self, steps_data, tool_list):
        for step in steps_data:
            step_detail = step.get('OrderSteps', {}).get('StepDetail', {})
            step_number = step_detail.get('StepNumber')
            action_str = step_detail.get('Action', '')


            match = re.match(r"(\w+)\(", action_str)
            if not match:
                # If action_str is empty or doesn't match, skip.
                continue
            tool_name = match.group(1)

            if tool_name not in tool_list:
                return self._format_response(True, f"Step {step_number}: Tool '{tool_name}' is fictitious or not in the allowed list.")

        return self._format_response(False, "No fictitious tools detected.")

class OperationalSpaceErrorAgent(EvaluationAgent):
    def __init__(self, llm_client):
        super().__init__("OperationalSpaceErrorAgent")
        self.llm_client = llm_client

    def evaluate(self, steps_data):
        for step in steps_data:
            step_detail = step.get('OrderSteps', {}).get('StepDetail', {})
            step_number = step_detail.get('StepNumber')
            action_str = step_detail.get('Action', '')
            results = step_detail.get('Results')


            if results and isinstance(results, dict) and 'status' in results and results['status'] is not True:
                # This indicates a direct failure reported by the tool itself.
                return self._format_response(True, f"Step {step_number}: Action '{action_str}' failed with status '{results.get('status')}', indicating a potential operational error reported by the tool.")

            # If no direct failure, ask LLM
            prompt = (f"Given the action '{action_str}' and its results: {json.dumps(results)}. "
                      "Does this indicate an operational space error within an application context (e.g., trying to use a tool in a way it's not designed for, even if it doesn't explicitly fail)? "
                      "Respond with a JSON object in the format: {'Result': True/False, 'Description': 'brief reason'}.")
            llm_response = self.llm_client.call_llm(prompt)
            if llm_response.get('Result') is True:
                return self._format_response(True, f"Step {step_number}: {llm_response.get('Description', 'LLM indicated operational space error but provided no description.')}")

        return self._format_response(False, "No operational space errors detected by LLM or direct tool failure.")

class TimeReasoningErrorAgent(EvaluationAgent):
    def __init__(self, llm_client):
        super().__init__("TimeReasoningErrorAgent")
        self.llm_client = llm_client

    def evaluate(self, steps_data, time_groundtruth, enable_agent=False):
        if not enable_agent:
            return self._format_response(False, "Time Reasoning Error Agent is disabled.")

        for step in steps_data:
            step_detail = step.get('OrderSteps', {}).get('StepDetail', {})
            step_number = step_detail.get('StepNumber')
            action_str = step_detail.get('Action', '')


            dates_found = {}
            # Regex to find key-value pairs like 'some_date': 'YYYY-MM-DD'
            date_matches = re.findall(r"['\"](\w+_date)['\"]:\s*['\"](\d{4}-\d{2}-\d{2})['\"]", action_str)
            for key, value in date_matches:
                dates_found[key] = value

            if dates_found:
                prompt = (f"Given the action '{action_str}' with extracted dates {dates_found}, "
                          f"and the time ground truth {time_groundtruth}. "
                          "Are there any time reasoning errors (e.g., illogical dates, conflicts with ground truth)? "
                          "Respond with a JSON object in the format: {'Result': True/False, 'Description': 'brief reason'}.")
                llm_response = self.llm_client.call_llm(prompt)
                if llm_response.get('Result') is True:
                    return self._format_response(True, f"Step {step_number}: {llm_response.get('Description', 'LLM indicated time reasoning error but provided no description.')}")

        return self._format_response(False, "No time reasoning errors detected by LLM.")

class MultiAgentEvaluationSystem:
    """
    Coordinates the multi-agent evaluation system.
    """
    def __init__(self, llm_model_type="OPENAI",
                 openai_api_key=None, openai_endpoint=None, openai_model=None,
                 gemini_api_key=None, gemini_endpoint=None, gemini_model=None,
                 proxy_address=None): # Added proxy address parameter
        # Instantiate LLM client, passing all configuration parameters
        self.llm_client = LLMClient(model_type=llm_model_type,
                                    openai_api_key=openai_api_key,
                                    openai_endpoint=openai_endpoint,
                                    openai_model=openai_model,
                                    gemini_api_key=gemini_api_key,
                                    gemini_endpoint=gemini_endpoint,
                                    gemini_model=gemini_model,
                                    proxy_address=proxy_address) # Pass proxy address
        self.agents = OrderedDict()
        self._initialize_agents()

    def _initialize_agents(self):
        """Initializes all agents."""
        self.agents["TaskSuccessAgent"] = TaskSuccessAgent()
        self.agents["DependencyCheckAgent"] = DependencyCheckAgent()
        self.agents["RedundantStepsAgent"] = RedundantStepsAgent(self.llm_client)
        self.agents["MissingStepsAgent"] = MissingStepsAgent(self.llm_client)
        self.agents["FictitiousMisusedParametersAgent"] = FictitiousMisusedParametersAgent(self.llm_client)
        self.agents["FictitiousToolAgent"] = FictitiousToolAgent()
        self.agents["OperationalSpaceErrorAgent"] = OperationalSpaceErrorAgent(self.llm_client)
        self.agents["TimeReasoningErrorAgent"] = TimeReasoningErrorAgent(self.llm_client)

    def evaluate_json_data(self, json_data, tool_list, time_groundtruth, enable_time_agent=False):
        """
        Evaluates parsed JSON data using all agents.
        Args:
            json_data (list): Parsed JSON data.
            tool_list (list): Ground truth list of valid tool names.
            time_groundtruth (dict): Ground truth for time-related data.
            enable_time_agent (bool): Whether to enable the time reasoning error agent.
        Returns:
            tuple: (results_only_json, results_with_reasons_json, all_agents_passed_for_this_file)
        """
        full_results = OrderedDict()
        results_only = OrderedDict()
        all_agents_passed_for_this_file = True

        # Safely extract query, global_thought, and steps_data
        query = ""
        if json_data and isinstance(json_data, list) and len(json_data) > 0 and isinstance(json_data[0], dict):
            query = json_data[0].get('Query', "")
        
        global_thought = ""
        if json_data and isinstance(json_data, list) and len(json_data) > 1 and isinstance(json_data[1], dict):
            global_thought = json_data[1].get('GlobalThought', "")
            
        steps_data = []
        if json_data and isinstance(json_data, list):
            steps_data = [d for d in json_data if isinstance(d, dict) and 'OrderSteps' in d]


        # Helper function to process agent results
        def process_agent_result(agent_name, agent_result):
            nonlocal all_agents_passed_for_this_file
            full_results[agent_name] = agent_result
            results_only[agent_name] = agent_result.get('Result', False) # Default to False if 'Result' key is missing
            if not agent_result.get('Result', False):
                all_agents_passed_for_this_file = False

        # Evaluate with each agent
        process_agent_result(self.agents["TaskSuccessAgent"].name, self.agents["TaskSuccessAgent"].evaluate(query, global_thought, steps_data))
        process_agent_result(self.agents["DependencyCheckAgent"].name, self.agents["DependencyCheckAgent"].evaluate(query, steps_data))
        process_agent_result(self.agents["RedundantStepsAgent"].name, self.agents["RedundantStepsAgent"].evaluate(query, steps_data))
        process_agent_result(self.agents["MissingStepsAgent"].name, self.agents["MissingStepsAgent"].evaluate(query, steps_data))
        process_agent_result(self.agents["FictitiousMisusedParametersAgent"].name, self.agents["FictitiousMisusedParametersAgent"].evaluate(steps_data))
        process_agent_result(self.agents["FictitiousToolAgent"].name, self.agents["FictitiousToolAgent"].evaluate(steps_data, tool_list))
        process_agent_result(self.agents["OperationalSpaceErrorAgent"].name, self.agents["OperationalSpaceErrorAgent"].evaluate(steps_data))
        
        time_reasoning_result = self.agents["TimeReasoningErrorAgent"].evaluate(steps_data, time_groundtruth, enable_agent=enable_time_agent)
        full_results[self.agents["TimeReasoningErrorAgent"].name] = time_reasoning_result
        results_only[self.agents["TimeReasoningErrorAgent"].name] = time_reasoning_result.get('Result', False)
        if enable_time_agent and not time_reasoning_result.get('Result', False): # Only impacts overall success if enabled
            all_agents_passed_for_this_file = False


        return json.dumps(results_only, indent=4, ensure_ascii=False), \
               json.dumps(full_results, indent=4, ensure_ascii=False), \
               all_agents_passed_for_this_file

# --- Main Execution ---
if __name__ == "__main__":
    # --- Configure LLM Parameters ---
    # IMPORTANT: Replace with your actual API keys and preferred endpoints/models!
    # In a production environment, it's highly recommended to use environment variables
    # or other secure methods to manage API keys.

    # For OpenAI
    OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "YOUR_OPENAI_API_KEY_HERE") # Read from env var or use placeholder
    OPENAI_ENDPOINT = os.environ.get("OPENAI_ENDPOINT", "YOUR_OPENAI_ENDPOINT_HERE") # e.g., "https://api.openai.com/v1/chat/completions"
    OPENAI_MODEL = os.environ.get("OPENAI_MODEL", "gpt-3.5-turbo") # e.g., "gpt-4", "gpt-3.5-turbo"

    # For Gemini
    GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "YOUR_GEMINI_API_KEY_HERE")
    GEMINI_ENDPOINT = os.environ.get("GEMINI_ENDPOINT", "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent")
    GEMINI_MODEL = os.environ.get("GEMINI_MODEL", "gemini-pro") # e.g., "gemini-pro", "gemini-1.5-pro-latest"

    # --- Proxy Settings ---
    # Example: "http://127.0.0.1:7890" or "socks5://127.0.0.1:1080"
    # Set to None if no proxy is needed.
    PROXY_ADDRESS = os.environ.get("PROXY_ADDRESS", None) 

    # --- File and Directory Configuration ---
    input_directory = './Task' # Directory containing input JSON files
    output_directory = 'evaluation_results' # Directory to save evaluation results

    # Create output directory if it doesn't exist
    os.makedirs(output_directory, exist_ok=True)

    # --- Ground Truth Configuration ---
    valid_tools = []
    tool_list_file = 'tool_list.json' # Name of the JSON file for valid tools

    try:
        with open(tool_list_file, 'r', encoding='utf-8') as f:
            valid_tools = json.load(f)
        if not isinstance(valid_tools, list):
            print(f"Warning: Content of '{tool_list_file}' is not a list. Using empty tool list.")
            valid_tools = []
        print(f"Successfully loaded {len(valid_tools)} tools from '{tool_list_file}'.")
    except FileNotFoundError:
        print(f"Warning: '{tool_list_file}' not found. Using empty tool list. Please create this file with a list of valid tool names.")
        valid_tools = []
    except json.JSONDecodeError:
        print(f"Warning: Could not decode JSON from '{tool_list_file}'. Using empty tool list.")
        valid_tools = []
    except Exception as e:
        print(f"An error occurred while loading '{tool_list_file}': {e}. Using empty tool list.")
        valid_tools = []


    time_gt = None # Placeholder for time ground truth, configure as needed

    # --- Initialize Evaluation System ---
    # Set your desired LLM model type (default is "OPENAI")
    # Ensure the corresponding API key, endpoint, and model name are correctly set above.
    
    # Default to OpenAI, but you can change this logic
    LLM_PROVIDER_TO_USE = os.environ.get("LLM_PROVIDER", "OPENAI").upper() 

    if LLM_PROVIDER_TO_USE == "GEMINI":
        print("Initializing evaluation system with GEMINI LLM.")
        eval_system = MultiAgentEvaluationSystem(llm_model_type="GEMINI",
                                             gemini_api_key=GEMINI_API_KEY,
                                             gemini_endpoint=GEMINI_ENDPOINT,
                                             gemini_model=GEMINI_MODEL,
                                             proxy_address=PROXY_ADDRESS)
    else: # Default to OpenAI
        print("Initializing evaluation system with OPENAI LLM.")
        eval_system = MultiAgentEvaluationSystem(llm_model_type="OPENAI",
                                             openai_api_key=OPENAI_API_KEY,
                                             openai_endpoint=OPENAI_ENDPOINT,
                                             openai_model=OPENAI_MODEL,
                                             proxy_address=PROXY_ADDRESS)


    overall_evaluation_success = True # Tracks if all evaluations for all files passed

    # Iterate through files in the input directory
    for filename in os.listdir(input_directory):
        if re.match(r'\d+-message_total\.json', filename): # Process files matching the pattern
            file_path = os.path.join(input_directory, filename)
            file_prefix = filename.split('-')[0] # Extract prefix for output filenames

            print(f"\n--- Processing file: {filename} ---")
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except FileNotFoundError:
                print(f"Error: File not found {file_path}")
                continue
            except json.JSONDecodeError:
                print(f"Error: Could not decode JSON from {file_path}")
                continue
            except Exception as e:
                print(f"An unknown error occurred while processing file {filename}: {e}")
                continue

            # Run evaluation for the current file's data
            # enable_time_agent is set to False by default
            results_only_json_str, results_with_reasons_json_str, file_evaluation_success = \
                eval_system.evaluate_json_data(data, valid_tools, time_gt, enable_time_agent=False)

            # Update overall success status
            if not file_evaluation_success:
                overall_evaluation_success = False

            # Save results to files in the output directory
            results_only_file = os.path.join(output_directory, f"{file_prefix}-results_only.json")
            results_with_reasons_file = os.path.join(output_directory, f"{file_prefix}-results_with_reasons.json")

            try:
                with open(results_only_file, 'w', encoding='utf-8') as f:
                    f.write(results_only_json_str)
                print(f"Evaluation results (True/False only) saved to {results_only_file}")

                with open(results_with_reasons_file, 'w', encoding='utf-8') as f:
                    f.write(results_with_reasons_json_str)
                print(f"Evaluation results (with reasons) saved to {results_with_reasons_file}")
            except IOError as e:
                print(f"Error writing results to file for {filename}: {e}")


    print("\n--- Final Evaluation Summary ---")
    if not os.listdir(input_directory):
        print("No files found in the input directory to evaluate.")
    elif overall_evaluation_success:
        print("All metrics for all processed files passed successfully!")
    else:
        print("One or more metrics failed for one or more files. Please check the detailed reports in the output directory.")

