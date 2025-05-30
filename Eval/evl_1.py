import json
import re
import os
import requests
from collections import OrderedDict

# --- LLM 客户端 ---
class LLMClient:
    """
    使用 requests 库进行 LLM API 调用。
    支持 OPENAI 和 GEMINI 模式。
    """
    def __init__(self, model_type="OPENAI",
                 openai_api_key=None, openai_endpoint=None, openai_model=None,
                 gemini_api_key=None, gemini_endpoint=None, gemini_model=None,
                 proxy_address=None): # 新增代理地址参数
        self.model_type = model_type

        # OpenAI 配置
        self.openai_api_key = openai_api_key
        self.openai_endpoint = openai_endpoint if openai_endpoint else "https://api.openai.com/v1/chat/completions"
        self.openai_model = openai_model if openai_model else "gpt-3.5-turbo"

        # Gemini 配置
        self.gemini_api_key = gemini_api_key
        self.gemini_endpoint = gemini_endpoint if gemini_endpoint else "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
        self.gemini_model = gemini_model if gemini_model else "gemini-pro"

        # 代理设置
        self.proxy_address = proxy_address
        self.proxies = {
            "http": proxy_address,
            "https": proxy_address,
        } if proxy_address else None


    def call_llm(self, prompt):
        """
        向指定的 LLM 发送 API 请求。
        Args:
            prompt (str): 发送给 LLM 的提示词。
        Returns:
            dict: 结构为 {'Result': True/False, 'Description': '理由'} 的 JSON 响应。
        """
        headers = {"Content-Type": "application/json"}
        payload = {}
        llm_response_content = ""

        print(f"\n--- Calling LLM ({self.model_type}) for prompt (first 100 chars): {prompt[:100]}... ---")

        try:
            if self.model_type == "OPENAI":
                if not self.openai_api_key:
                    raise ValueError("OpenAI API 密钥未设置。")
                headers["Authorization"] = f"Bearer {self.openai_api_key}"
                payload = {
                    "model": self.openai_model,
                    "messages": [{"role": "user", "content": prompt}],
                    "response_format": {"type": "json_object"}
                }
                response = requests.post(self.openai_endpoint, headers=headers, json=payload, timeout=60, proxies=self.proxies) # 加入 proxies
                response.raise_for_status()
                llm_output = response.json()
                llm_response_content = llm_output['choices'][0]['message']['content']

            elif self.model_type == "GEMINI":
                if not self.gemini_api_key:
                    raise ValueError("Gemini API 密钥未设置。")
                url_with_key = f"{self.gemini_endpoint}?key={self.gemini_api_key}"
                payload = {
                    "contents": [{"parts": [{"text": prompt}]}]
                }
                response = requests.post(url_with_key, headers=headers, json=payload, timeout=60, proxies=self.proxies) # 加入 proxies
                response.raise_for_status()
                llm_output = response.json()
                if 'candidates' in llm_output and llm_output['candidates']:
                    llm_response_content = llm_output['candidates'][0]['content']['parts'][0]['text']
                else:
                    raise Exception(f"Gemini API 响应中未找到 'candidates' 或内容: {llm_output}")

            else:
                return {"Result": False, "Description": f"不支持的 LLM 模型类型: {self.model_type}"}

            try:
                parsed_content = json.loads(llm_response_content)
                if "Result" in parsed_content and "Description" in parsed_content:
                    return parsed_content
                else:
                    return {"Result": False, "Description": f"LLM 响应未包含预期的 'Result' 或 'Description' 键: {llm_response_content}"}
            except json.JSONDecodeError:
                return {"Result": False, "Description": f"LLM 返回了无效的 JSON: {llm_response_content}"}

        except requests.exceptions.Timeout:
            print("LLM API 请求超时。")
            return {"Result": False, "Description": "LLM API 请求超时。"}
        except requests.exceptions.ConnectionError:
            print("LLM API 连接错误。")
            return {"Result": False, "Description": "LLM API 连接错误。"}
        except requests.exceptions.HTTPError as e:
            print(f"LLM API HTTP 错误: {e.response.status_code} - {e.response.text}")
            return {"Result": False, "Description": f"LLM API HTTP 错误: {e.response.status_code} - {e.response.text}"}
        except ValueError as e:
            print(f"配置错误: {e}")
            return {"Result": False, "Description": f"配置错误: {e}"}
        except Exception as e:
            print(f"LLM 调用期间发生意外错误: {e}")
            return {"Result": False, "Description": f"LLM 调用期间发生意外错误: {e}"}

# --- 评估代理 (保持不变) ---
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

        total_steps_declared = steps_data[0]['OrderSteps']['TotalSteps'] if steps_data else 0
        actual_steps = len(steps_data)
        if total_steps_declared != actual_steps:
            return self._format_response(False, f"Declared total steps ({total_steps_declared}) does not match actual steps ({actual_steps}).")

        for step in steps_data:
            step_number = step['OrderSteps']['StepDetail']['StepNumber']
            description = step['OrderSteps']['StepDetail']['Description']
            results = step['OrderSteps']['StepDetail']['Results']

            if not description:
                return self._format_response(False, f"Step {step_number}: Description is missing.")
            if results and isinstance(results, dict) and 'status' in results and results['status'] is not True:
                return self._format_response(False, f"Step {step_number}: Results indicate failure (status is not True).")

        return self._format_response(True, "All steps appear to be successful and align with the overall task.")

class DependencyCheckAgent(EvaluationAgent):
    def __init__(self):
        super().__init__("DependencyCheckAgent")

    def evaluate(self, query, steps_data):
        step_actions = [s['OrderSteps']['StepDetail']['Action'] for s in steps_data]

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
        step_descriptions = [s['OrderSteps']['StepDetail']['Description'] for s in steps_data]
        prompt = (f"Given the main query: '{query}', and the following sequence of steps: "
                  f"{', '.join(step_descriptions)}. Are there any redundant steps? "
                  "Respond with a JSON object in the format: {'Result': True/False, 'Description': 'brief reason'}.")
        llm_response = self.llm_client.call_llm(prompt)
        return self._format_response(llm_response['Result'], llm_response['Description'])

class MissingStepsAgent(EvaluationAgent):
    def __init__(self, llm_client):
        super().__init__("MissingStepsAgent")
        self.llm_client = llm_client

    def evaluate(self, query, steps_data):
        step_descriptions = [s['OrderSteps']['StepDetail']['Description'] for s in steps_data]
        prompt = (f"Given the main query: '{query}', and the following sequence of steps: "
                  f"{', '.join(step_descriptions)}. Are there any crucial steps missing to fully achieve the query? "
                  "Respond with a JSON object in the format: {'Result': True/False, 'Description': 'brief reason'}.")
        llm_response = self.llm_client.call_llm(prompt)
        return self._format_response(llm_response['Result'], llm_response['Description'])

class FictitiousMisusedParametersAgent(EvaluationAgent):
    def __init__(self, llm_client):
        super().__init__("FictitiousMisusedParametersAgent")
        self.llm_client = llm_client

    def evaluate(self, steps_data):
        for step in steps_data:
            step_number = step['OrderSteps']['StepDetail']['StepNumber']
            action_str = step['OrderSteps']['StepDetail']['Action']

            match = re.match(r"(\w+)\((.*)\)", action_str)
            if not match:
                return self._format_response(False, f"Step {step_number}: Could not parse action string: {action_str}")

            tool_name = match.group(1)
            params_str = match.group(2)

            prompt = (f"Given the tool '{tool_name}' and its parameters '{params_str}', "
                      "do these parameters seem fictitious or misused for a typical use case of this tool? "
                      "Respond with a JSON object in the format: {'Result': True/False, 'Description': 'brief reason'}.")
            llm_response = self.llm_client.call_llm(prompt)
            if llm_response['Result'] is True:
                return self._format_response(True, f"Step {step_number}: {llm_response['Description']}")

        return self._format_response(False, "No fictitious or misused parameters detected.")

class FictitiousToolAgent(EvaluationAgent):
    def __init__(self):
        super().__init__("FictitiousToolAgent")

    def evaluate(self, steps_data, tool_list):
        for step in steps_data:
            step_number = step['OrderSteps']['StepDetail']['StepNumber']
            action_str = step['OrderSteps']['StepDetail']['Action']

            match = re.match(r"(\w+)\(", action_str)
            if not match:
                return self._format_response(False, f"Step {step_number}: Could not parse tool name from action string: {action_str}")
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
            step_number = step['OrderSteps']['StepDetail']['StepNumber']
            action_str = step['OrderSteps']['StepDetail']['Action']
            results = step['OrderSteps']['StepDetail']['Results']

            if results and isinstance(results, dict) and 'status' in results and results['status'] is not True:
                return self._format_response(True, f"Step {step_number}: Action '{action_str}' failed with status '{results.get('status')}', indicating a potential operational error.")

            prompt = (f"Given the action '{action_str}' and its results: {json.dumps(results)}. "
                      "Does this indicate an operational space error within an application context? "
                      "Respond with a JSON object in the format: {'Result': True/False, 'Description': 'brief reason'}.")
            llm_response = self.llm_client.call_llm(prompt)
            if llm_response['Result'] is True:
                return self._format_response(True, f"Step {step_number}: {llm_response['Description']}")

        return self._format_response(False, "No operational space errors detected.")

class TimeReasoningErrorAgent(EvaluationAgent):
    def __init__(self, llm_client):
        super().__init__("TimeReasoningErrorAgent")
        self.llm_client = llm_client

    def evaluate(self, steps_data, time_groundtruth, enable_agent=False):
        if not enable_agent:
            return self._format_response(False, "Time Reasoning Error Agent is disabled.")

        for step in steps_data:
            step_number = step['OrderSteps']['StepDetail']['StepNumber']
            action_str = step['OrderSteps']['StepDetail']['Action']

            dates_found = {}
            date_matches = re.findall(r"'(\w+_date)': '(\d{4}-\d{2}-\d{2})'", action_str)
            for key, value in date_matches:
                dates_found[key] = value

            if dates_found:
                prompt = (f"Given the action '{action_str}' with dates {dates_found}, "
                          f"and the time ground truth {time_groundtruth}. "
                          "Are there any time reasoning errors (e.g., illogical dates, conflicts with ground truth)? "
                          "Respond with a JSON object in the format: {'Result': True/False, 'Description': 'brief reason'}.")
                llm_response = self.llm_client.call_llm(prompt)
                if llm_response['Result'] is True:
                    return self._format_response(True, f"Step {step_number}: {llm_response['Description']}")

        return self._format_response(False, "No time reasoning errors detected.")

class MultiAgentEvaluationSystem:
    """
    协调多代理评估系统。
    """
    def __init__(self, llm_model_type="OPENAI",
                 openai_api_key=None, openai_endpoint=None, openai_model=None,
                 gemini_api_key=None, gemini_endpoint=None, gemini_model=None,
                 proxy_address=None): # 新增代理地址参数
        # 实例化 LLM 客户端，并传入所有配置参数
        self.llm_client = LLMClient(model_type=llm_model_type,
                                    openai_api_key=openai_api_key,
                                    openai_endpoint=openai_endpoint,
                                    openai_model=openai_model,
                                    gemini_api_key=gemini_api_key,
                                    gemini_endpoint=gemini_endpoint,
                                    gemini_model=gemini_model,
                                    proxy_address=proxy_address) # 传递代理地址
        self.agents = OrderedDict()
        self._initialize_agents()

    def _initialize_agents(self):
        """初始化所有代理。"""
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
        使用所有代理评估解析后的 JSON 数据。
        Args:
            json_data (list): 解析后的 JSON 数据。
            tool_list (list): 有效工具名称的地面真值列表。
            time_groundtruth (dict): 时间相关数据的地面真值。
            enable_time_agent (bool): 是否启用时间推理错误代理。
        Returns:
            tuple: (results_only_json, results_with_reasons_json, all_agents_passed_for_this_file)
        """
        full_results = OrderedDict()
        results_only = OrderedDict()
        all_agents_passed_for_this_file = True

        query = json_data[0]['Query'] if json_data and 'Query' in json_data[0] else ""
        global_thought = json_data[1]['GlobalThought'] if len(json_data) > 1 and 'GlobalThought' in json_data[1] else ""
        steps_data = [d for d in json_data if 'OrderSteps' in d]

        task_success_result = self.agents["TaskSuccessAgent"].evaluate(query, global_thought, steps_data)
        full_results[self.agents["TaskSuccessAgent"].name] = task_success_result
        results_only[self.agents["TaskSuccessAgent"].name] = task_success_result['Result']
        if not task_success_result['Result']: all_agents_passed_for_this_file = False

        dependency_check_result = self.agents["DependencyCheckAgent"].evaluate(query, steps_data)
        full_results[self.agents["DependencyCheckAgent"].name] = dependency_check_result
        results_only[self.agents["DependencyCheckAgent"].name] = dependency_check_result['Result']
        if not dependency_check_result['Result']: all_agents_passed_for_this_file = False

        redundant_steps_result = self.agents["RedundantStepsAgent"].evaluate(query, steps_data)
        full_results[self.agents["RedundantStepsAgent"].name] = redundant_steps_result
        results_only[self.agents["RedundantStepsAgent"].name] = redundant_steps_result['Result']
        if not redundant_steps_result['Result']: all_agents_passed_for_this_file = False

        missing_steps_result = self.agents["MissingStepsAgent"].evaluate(query, steps_data)
        full_results[self.agents["MissingStepsAgent"].name] = missing_steps_result
        results_only[self.agents["MissingStepsAgent"].name] = missing_steps_result['Result']
        if not missing_steps_result['Result']: all_agents_passed_for_this_file = False

        fictitious_params_result = self.agents["FictitiousMisusedParametersAgent"].evaluate(steps_data)
        full_results[self.agents["FictitiousMisusedParametersAgent"].name] = fictitious_params_result
        results_only[self.agents["FictitiousMisusedParametersAgent"].name] = fictitious_params_result['Result']
        if not fictitious_params_result['Result']: all_agents_passed_for_this_file = False

        fictitious_tool_result = self.agents["FictitiousToolAgent"].evaluate(steps_data, tool_list)
        full_results[self.agents["FictitiousToolAgent"].name] = fictitious_tool_result
        results_only[self.agents["FictitiousToolAgent"].name] = fictitious_tool_result['Result']
        if not fictitious_tool_result['Result']: all_agents_passed_for_this_file = False

        operational_error_result = self.agents["OperationalSpaceErrorAgent"].evaluate(steps_data)
        full_results[self.agents["OperationalSpaceErrorAgent"].name] = operational_error_result
        results_only[self.agents["OperationalSpaceErrorAgent"].name] = operational_error_result['Result']
        if not operational_error_result['Result']: all_agents_passed_for_this_file = False

        time_reasoning_result = self.agents["TimeReasoningErrorAgent"].evaluate(steps_data, time_groundtruth, enable_agent=enable_time_agent)
        full_results[self.agents["TimeReasoningErrorAgent"].name] = time_reasoning_result
        results_only[self.agents["TimeReasoningErrorAgent"].name] = time_reasoning_result['Result']
        if enable_time_agent and not time_reasoning_result['Result']: all_agents_passed_for_this_file = False

        return json.dumps(results_only, indent=4, ensure_ascii=False), \
               json.dumps(full_results, indent=4, ensure_ascii=False), \
               all_agents_passed_for_this_file

# --- 主执行 ---
if __name__ == "__main__":
    # --- 配置 LLM 参数 ---
    # 请务必替换为您的真实 API 密钥！
    # 在生产环境中，建议使用环境变量或其他安全方式管理密钥。
    OPENAI_API_KEY = "sk-3f16802c73d549d391e7f708cece3ab3" # <<<<<<< 替换您的 OpenAI API 密钥
    OPENAI_ENDPOINT = "https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions" # OpenAI API 端点
    OPENAI_MODEL = "qwen-max-2025-01-25" # OpenAI 模型名称，例如 "gpt-4", "gpt-3.5-turbo"

    GEMINI_API_KEY = "YOUR_GEMINI_API_KEY" # <<<<<<< 替换您的 Gemini API 密钥
    GEMINI_ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"
    GEMINI_MODEL = "gemini-pro" # Gemini 模型名称，例如 "gemini-pro", "gemini-1.5-pro-latest"

    # --- 代理设置 ---
    PROXY_ADDRESS = "127.0.0.1:7890" # 您的代理地址，例如 "http://127.0.0.1:7890" 或 "socks5://user:pass@host:port"

    # --- 文件和目录配置 ---
    input_directory = './Task' # 更改为您的 JSON 文件目录路径，例如 'json_files/'
    output_directory = 'evaluation_results'

    # 创建输出目录（如果不存在）
    os.makedirs(output_directory, exist_ok=True)

    # --- 地面真值配置 ---
    valid_tools = []
    time_gt = None
    # --- 初始化评估系统 ---
    # 设置您希望使用的 LLM 模型类型 (默认是 OPENAI)
    eval_system = MultiAgentEvaluationSystem(llm_model_type="OPENAI",
                                             openai_api_key=OPENAI_API_KEY,
                                             openai_endpoint=OPENAI_ENDPOINT,
                                             openai_model=OPENAI_MODEL,
                                             proxy_address=PROXY_ADDRESS) # 传递代理地址

    # 如果您想使用 Gemini，请取消注释下面的行并注释上面的 OpenAI 初始化
    # eval_system = MultiAgentEvaluationSystem(llm_model_type="GEMINI",
    #                                          gemini_api_key=GEMINI_API_KEY,
    #                                          gemini_endpoint=GEMINI_ENDPOINT,
    #                                          gemini_model=GEMINI_MODEL,
    #                                          proxy_address=PROXY_ADDRESS) # 传递代理地址


    overall_evaluation_success = True # 跟踪所有文件所有评估是否都通过

    # 遍历输入目录中的文件
    for filename in os.listdir(input_directory):
        if re.match(r'\d+-message_total\.json', filename):
            file_path = os.path.join(input_directory, filename)
            file_prefix = filename.split('-')[0]

            print(f"\n--- 正在处理文件: {filename} ---")
            try:
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
            except FileNotFoundError:
                print(f"错误: 未找到文件 {file_path}")
                continue
            except json.JSONDecodeError:
                print(f"错误: 无法从 {file_path} 解码 JSON")
                continue
            except Exception as e:
                print(f"处理文件 {filename} 时发生未知错误: {e}")
                continue

            # 运行当前文件的评估
            # enable_time_agent 默认设置为 False
            results_only_json_str, results_with_reasons_json_str, file_evaluation_success = \
                eval_system.evaluate_json_data(data, valid_tools, time_gt, enable_time_agent=False)

            # 更新整体成功状态
            if not file_evaluation_success:
                overall_evaluation_success = False

            # 将结果保存到输出目录中的文件
            results_only_file = os.path.join(output_directory, f"{file_prefix}-results_only.json")
            results_with_reasons_file = os.path.join(output_directory, f"{file_prefix}-results_with_reasons.json")

            with open(results_only_file, 'w', encoding='utf-8') as f:
                f.write(results_only_json_str)
            print(f"评估结果 (仅 True/False) 已保存到 {results_only_file}")

            with open(results_with_reasons_file, 'w', encoding='utf-8') as f:
                f.write(results_with_reasons_json_str)
            print(f"评估结果 (带理由) 已保存到 {results_with_reasons_file}")

    print("\n--- 最终评估结果 ---")
    print(f"所有文件中的所有指标是否全部正确: {overall_evaluation_success}")
