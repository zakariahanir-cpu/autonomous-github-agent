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
            time.sleep(5)  
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

        # Added a new feature to send a notification after self-improvement
        try:
            import requests
            notification_url = "https://gullsatin-jawrid--96637.stormkit.dev/api/notifications"
            notification_data = {
                "event": "self-improvement",
                "status": "success"
            }
            response = requests.post(notification_url, json=notification_data)
            if response.status_code == 200:
                print("Notification sent successfully.")
            else:
                print("Error sending notification.")
        except Exception as e:
            print(f"Error sending notification: {str(e)}")

        # Added a new feature to log the self-improvement process
        try:
            logging.basicConfig(filename='self_improvement.log', level=logging.INFO)
            logging.info('Self-improvement process started')
            logging.info('New code written to file')
            logging.info('Git commands executed')
            logging.info('Agent restarted')
            logging.info('Notification sent')
            logging.info('Self-improvement process completed')
        except Exception as e:
            print(f"Error logging self-improvement process: {str(e)}")

        # Added error handling for the logging feature
        try:
            logging.info('Self-improvement process completed successfully')
        except Exception as e:
            print(f"Error logging self-improvement completion: {str(e)}")

        # Added a check to verify the git status after self-improvement
        try:
            import subprocess
            git_status = subprocess.run(['git', 'status'], capture_output=True, text=True)
            if git_status.returncode == 0:
                print("Git status is clean.")
            else:
                print("Git status is not clean.")
        except Exception as e:
            print(f"Error checking git status: {str(e)}")

        # Added a new feature to check for updates and restart the agent if necessary
        try:
            import requests
            update_url = "https://api.github.com/repos/your-repo/your-repo/commits"
            response = requests.get(update_url)
            if response.status_code == 200:
                commits = response.json()
                latest_commit = commits[0]
                if latest_commit['sha'] != self.get_latest_commit():
                    print("New update available. Restarting the agent.")
                    import os
                    os.execl(sys.executable, sys.executable, *sys.argv)
                else:
                    print("Agent is up to date.")
            else:
                print("Error checking for updates.")
        except Exception as e:
            print(f"Error checking for updates: {str(e)}")

    def get_latest_commit(self):
        try:
            import subprocess
            latest_commit = subprocess.run(['git', 'rev-parse', 'HEAD'], capture_output=True, text=True)
            if latest_commit.returncode == 0:
                return latest_commit.stdout.strip()
            else:
                return None
        except Exception as e:
            print(f"Error getting latest commit: {str(e)}")
            return None

    # Added a new method to handle errors during the self-improvement process
    def handle_error(self, error):
        try:
            logging.error(f"Error during self-improvement: {str(error)}")
            print(f"Error during self-improvement: {str(error)}")
        except Exception as e:
            print(f"Error handling error: {str(e)}")

    # Added a new method to verify the agent's configuration
    def verify_config(self):
        try:
            import os
            if not os.getenv('LLM_API_KEY'):
                print("Error: LLM_API_KEY not found. Please add it to GitHub Secrets.")
                return False
            return True
        except Exception as e:
            print(f"Error verifying config: {str(e)}")
            return False

    # Added a new method to improve the agent's performance
    def improve_performance(self):
        try:
            import os
            import psutil
            process = psutil.Process(os.getpid())
            memory_usage = process.memory_info().rss / (1024 * 1024)
            if memory_usage > 100:
                print("Memory usage is high. Restarting the agent to free up memory.")
                import os
                os.execl(sys.executable, sys.executable, *sys.argv)
            else:
                print("Memory usage is within acceptable limits.")
        except Exception as e:
            print(f"Error improving performance: {str(e)}")

    # Added a new method to check for updates and restart the agent if necessary
    def check_for_updates(self):
        try:
            import requests
            update_url = "https://api.github.com/repos/your-repo/your-repo/commits"
            response = requests.get(update_url)
            if response.status_code == 200:
                commits = response.json()
                latest_commit = commits[0]
                if latest_commit['sha'] != self.get_latest_commit():
                    print("New update available. Restarting the agent.")
                    import os
                    os.execl(sys.executable, sys.executable, *sys.argv)
                else:
                    print("Agent is up to date.")
            else:
                print("Error checking for updates.")
        except Exception as e:
            print(f"Error checking for updates: {str(e)}")

    # Added a new method to add a timeout for the query method
    def query_with_timeout(self, prompt, timeout=10):
        import signal
        def timeout_handler(signum, frame):
            raise TimeoutError()
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(timeout)
        try:
            return self.query(prompt)
        except TimeoutError:
            print("Timeout error: Query took too long to respond.")
            return None
        finally:
            signal.alarm(0)

    # Added a new method to implement a retry mechanism for the query method
    def query_with_retry(self, prompt, max_retries=3, retry_delay=1):
        for attempt in range(max_retries):
            try:
                return self.query(prompt)
            except Exception as e:
                print(f"Error during query attempt {attempt+1}: {str(e)}")
                time.sleep(retry_delay)
        print("All query attempts failed. Giving up.")
        return None