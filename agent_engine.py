import os
import requests
import json
import subprocess
import sys
import importlib
import time
import logging

class GitHubAgent:
    def __init__(self, api_key, model="llama-3.3-70b-versatile", endpoint=None):
        self.api_key = api_key
        self.model = model
        self.endpoint = endpoint or "https://api.groq.com/openai/v1/chat/completions"
        self.error_handling()

    def query(self, prompt, system_prompt="You are an autonomous self-improving GitHub Agent."):
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        data = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt}
            ],
            "temperature": 0.2 
        }
        try:
            response = requests.post(self.endpoint, headers=headers, json=data, timeout=10)
            if response.status_code != 200:
                error_details = response.json() if response.headers.get('Content-Type') == 'application/json' else response.text
                return f"Error: {response.status_code} {response.reason} - {error_details}"
            return response.json()['choices'][0]['message']['content']
        except Exception as e:
            return f"Error: {str(e)}"

    def read_file(self, path):
        try:
            with open(path, 'r', encoding='utf-8') as f:
                return f.read()
        except Exception as e:
            return f"Error reading file: {str(e)}"

    def write_file(self, path, content):
        try:
            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)
            return f"File {path} written successfully."
        except Exception as e:
            return f"Error writing file: {str(e)}"

    def execute_command(self, command):
        try:
            result = subprocess.run(command, shell=True, capture_output=True, text=True)
            return {
                "stdout": result.stdout,
                "stderr": result.stderr,
                "returncode": result.returncode
            }
        except Exception as e:
            return {"error": str(e)}

    def self_improve(self, new_code, file_path='main.py'):
        self.write_file(file_path, new_code)

        commands = [
            'git config --global user.name "GitHub Agent"',
            'git config --global user.email "agent@github.com"',
            f'git add {file_path}',
            'git commit -m "Self-improvement: Agent updated its own code via Groq LLM"',
            'git push'
        ]

        for cmd in commands:
            res = self.execute_command(cmd)
            if res.get('returncode') != 0:
                print(f"Command failed: {cmd}\nError: {res.get('stderr') or res.get('error')}")
            else:
                print(f"Command executed successfully: {cmd}")
                if 'stdout' in res:
                    print(f"Output: {res['stdout']}")

        try:
            importlib.reload(sys.modules[__name__])
        except Exception as e:
            print(f"Error reloading agent's code: {str(e)}")
        
        try:
            import os
            os.execl(sys.executable, sys.executable, *sys.argv)
        except Exception as e:
            print(f"Error restarting agent: {str(e)}")

        # Added a check to ensure the agent is still functioning after self-improvement
        try:
            import os
            import psutil
            process = psutil.Process(os.getpid())
            memory_usage = process.memory_info().rss / (1024 * 1024)
            cpu_usage = process.cpu_percent()
            if memory_usage > 100 or cpu_usage > 90:
                print("Agent is experiencing high resource usage after self-improvement. Restarting the agent to prevent crashes.")
                import os
                os.execl(sys.executable, sys.executable, *sys.argv)
            else:
                print("Agent is functioning within acceptable resource limits after self-improvement.")
        except Exception as e:
            print(f"Error checking agent status after self-improvement: {str(e)}")

    def error_handling(self):
        try:
            import logging
            logging.basicConfig(filename='error.log', level=logging.ERROR)
        except Exception as e:
            print(f"Error setting up error handling: {str(e)}")

    def validate_api_key(self):
        try:
            response = requests.get(f"https://api.groq.com/openai/v1/chat/completions", headers={"Authorization": f"Bearer {self.api_key}"})
            if response.status_code == 200:
                return True
            else:
                return False
        except Exception as e:
            print(f"Error validating API key: {str(e)}")
            return False

    def validate_response(self, response):
        if response is None:
            return False
        if isinstance(response, str) and response.startswith("Error:"):
            return False
        return True

    def validate_agent_status(self):
        try:
            import os
            import psutil
            process = psutil.Process(os.getpid())
            memory_usage = process.memory_info().rss / (1024 * 1024)
            cpu_usage = process.cpu_percent()
            if memory_usage > 100 or cpu_usage > 90:
                print("Agent is experiencing high resource usage. Restarting the agent to prevent crashes.")
                import os
                os.execl(sys.executable, sys.executable, *sys.argv)
            else:
                print("Agent is functioning within acceptable resource limits.")
        except Exception as e:
            print(f"Error validating agent status: {str(e)}")

    def check_for_updates(self):
        try:
            import requests
            response = requests.get("https://api.github.com/repos/your-repo/your-repo/releases/latest")
            if response.status_code == 200:
                latest_release = response.json()
                current_version = "1.0"  # Replace with your current version
                if latest_release["tag_name"] != current_version:
                    print("Update available. Downloading latest release...")
                    # Download and install the latest release
                else:
                    print("Agent is up-to-date.")
            else:
                print("Error checking for updates.")
        except Exception as e:
            print(f"Error checking for updates: {str(e)}")

    def handle_rate_limit(self, response):
        if 'rate limit' in str(response).lower():
            print("Rate limit exceeded. Waiting for 1 hour before retrying...")
            import time
            time.sleep(3600)
            return self.query(response)
        return response

    def retry_query(self, prompt, max_retries=3):
        retries = 0
        while retries < max_retries:
            response = self.query(prompt)
            if self.validate_response(response):
                return response
            retries += 1
            print(f"Query failed. Retrying... ({retries}/{max_retries})")
        return None

    def query_with_retry(self, prompt):
        return self.retry_query(prompt)

    def exponential_backoff(self, prompt, max_retries=5, initial_delay=1):
        delay = initial_delay
        for _ in range(max_retries):
            response = self.query(prompt)
            if self.validate_response(response):
                return response
            print(f"Query failed. Retrying in {delay} seconds...")
            time.sleep(delay)
            delay *= 2
        return None

    def query_with_exponential_backoff(self, prompt):
        return self.exponential_backoff(prompt)

    def get_agent_status(self):
        try:
            import os
            import psutil
            process = psutil.Process(os.getpid())
            memory_usage = process.memory_info().rss / (1024 * 1024)
            cpu_usage = process.cpu_percent()
            return {
                "memory_usage": memory_usage,
                "cpu_usage": cpu_usage
            }
        except Exception as e:
            print(f"Error getting agent status: {str(e)}")
            return None

    def rate_limit_protection(self):
        import time
        while True:
            response = self.query("Test query to check rate limit")
            if 'rate limit' in str(response).lower():
                print("Rate limit exceeded. Waiting for 1 hour before retrying...")
                time.sleep(3600)
            else:
                break

    def improved_query(self, prompt):
        try:
            response = self.query_with_retry(prompt)
            if response:
                return response
            else:
                return self.query_with_exponential_backoff(prompt)
        except Exception as e:
            print(f"Error in improved query: {str(e)}")
            return None

    def improved_self_improve(self, new_code, file_path='main.py'):
        self.write_file(file_path, new_code)

        commands = [
            'git config --global user.name "GitHub Agent"',
            'git config --global user.email "agent@github.com"',
            f'git add {file_path}',
            'git commit -m "Self-improvement: Agent updated its own code via Groq LLM"',
            'git push'
        ]

        for cmd in commands:
            res = self.execute_command(cmd)
            if res.get('returncode') != 0:
                print(f"Command failed: {cmd}\nError: {res.get('stderr') or res.get('error')}")
            else:
                print(f"Command executed successfully: {cmd}")
                if 'stdout' in res:
                    print(f"Output: {res['stdout']}")

        try:
            importlib.reload(sys.modules[__name__])
        except Exception as e:
            print(f"Error reloading agent's code: {str(e)}")
        
        try:
            import os
            os.execl(sys.executable, sys.executable, *sys.argv)
        except Exception as e:
            print(f"Error restarting agent: {str(e)}")

        # Added a check to ensure the agent is still functioning after self-improvement
        try:
            import os
            import psutil
            process = psutil.Process(os.getpid())
            memory_usage = process.memory_info().rss / (1024 * 1024)
            cpu_usage = process.cpu_percent()
            if memory_usage > 100 or cpu_usage > 90:
                print("Agent is experiencing high resource usage after self-improvement. Restarting the agent to prevent crashes.")
                import os
                os.execl(sys.executable, sys.executable, *sys.argv)
            else:
                print("Agent is functioning within acceptable resource limits after self-improvement.")
        except Exception as e:
            print(f"Error checking agent status after self-improvement: {str(e)}")

    def validate_file_path(self, file_path):
        if file_path in ['main.py', 'agent_engine.py']:
            return True
        else:
            return False

    def improved_self_improve_with_validation(self, new_code, file_path='main.py'):
        if self.validate_file_path(file_path):
            self.improved_self_improve(new_code, file_path)
        else:
            print(f"Invalid file path: {file_path}")
            
    def improved_query_with_validation(self, prompt):
        response = self.improved_query(prompt)
        if self.validate_response(response):
            return response
        else:
            print(f"Invalid response from the AI provider: {response}")
            return None
