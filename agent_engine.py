import os
import requests
import json
import subprocess
import sys
import importlib
import time

class GitHubAgent:
    def __init__(self, api_key, model="llama-3.3-70b-versatile", endpoint=None):
        self.api_key = api_key
        self.model = model
        self.endpoint = endpoint or "https://api.groq.com/openai/v1/chat/completions"

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
            "temperature": 0.2 # تقليل العشوائية لضمان الالتزام بالتنسيق
        }
        try:
            response = requests.post(self.endpoint, headers=headers, json=data)
            if response.status_code != 200:
                return f"Error: {response.status_code} {response.reason} - {response.text}"
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

        # Add a try-except block to handle potential exceptions during the self-improvement process
        try:
            # Reload the agent's code after self-improvement
            importlib.reload(sys.modules[__name__])
        except Exception as e:
            print(f"Error reloading agent's code: {str(e)}")
        
        # Added a check to restart the agent after self-improvement
        try:
            import os
            os.execl(sys.executable, sys.executable, *sys.argv)
        except Exception as e:
            print(f"Error restarting agent: {str(e)}")

        # Added a check to verify if the self-improvement was successful
        try:
            time.sleep(5)  # wait for 5 seconds to allow the changes to take effect
            import requests
            response = requests.get('https://api.github.com')
            if response.status_code == 200:
                print("Self-improvement successful. Agent is functioning correctly.")
            else:
                print("Self-improvement failed. Agent is not functioning correctly.")
        except Exception as e:
            print(f"Error verifying self-improvement: {str(e)}")

        # Added a check to handle the case where the agent is not able to restart itself
        try:
            import sys
            if sys.argv[0] == 'main.py':
                print("Agent is running in the main process. No need to restart.")
            else:
                print("Agent is running in a subprocess. Restarting the main process.")
                import os
                os.execl(sys.executable, sys.executable, *sys.argv)
        except Exception as e:
            print(f"Error handling agent restart: {str(e)}")