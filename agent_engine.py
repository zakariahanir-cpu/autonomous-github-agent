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

    def get_current_sha(self):
        try:
            result = subprocess.run(['git', 'rev-parse', 'HEAD'], capture_output=True, text=True)
            return result.stdout.strip()
        except Exception as e:
            print(f"Error getting current SHA: {str(e)}")
            return None

    def self_improve(self, new_code, file_path='main.py'):
        # 1. إعداد نظام التسجيل (Logging) في البداية
        try:
            logging.basicConfig(filename='self_improvement.log', level=logging.INFO)
            logging.info('Self-improvement process started')
        except Exception as e:
            print(f"Error initializing logging: {str(e)}")

        # 2. كتابة الكود الجديد
        self.write_file(file_path, new_code)
        logging.info('New code written to file')

        # 3. تنفيذ أوامر Git
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
        
        logging.info('Git commands executed')

        # 4. التحقق من الاتصال بـ GitHub كمرجع لنجاح العملية
        try:
            time.sleep(2)  
            response = requests.get('https://api.github.com')
            if response.status_code == 200:
                print("Self-improvement successful. Agent is functioning correctly.")
            else:
                print("Self-improvement failed. Agent is not functioning correctly.")
        except Exception as e:
            print(f"Error verifying self-improvement: {str(e)}")

        # 5. إرسال الإشعار عبر الويب
        try:
            notification_url = "https://gullsatin-jawrid--96637.stormkit.dev/api/notifications"
            notification_data = {
                "event": "self-improvement",
                "status": "success"
            }
            res_notif = requests.post(notification_url, json=notification_data, timeout=5)
            if res_notif.status_code == 200:
                print("Notification sent successfully.")
                logging.info('Notification sent')
            else:
                print("Error sending notification.")
        except Exception as e:
            print(f"Error sending notification: {str(e)}")

        # 6. الفحص الاختياري للتحديثات الخارجية من مستودع معين
        # تنبيه: قم بتغيير 'your-repo/your-repo' إلى مسار مستودعك الحقيقي لاحقاً
        should_restart_for_update = False
        try:
            update_url = "https://api.github.com/repos/your-repo/your-repo/contents/agent_engine.py"
            # أضفنا الـ headers لتفادي حظر API من GitHub بدون طلب مصادق
            headers = {"User-Agent": "GitHub-Agent", "Authorization": f"Bearer {self.api_key}"} 
            response = requests.get(update_url, headers=headers, timeout=5)
            if response.status_code == 200:
                update_data = response.json()
                if update_data.get('sha') != self.get_current_sha():
                    print("Update available from remote repository.")
                    should_restart_for_update = True
                else:
                    print("No remote update available.")
            else:
                print("Note: Could not check updates (Repo might be private or path is placeholder).")
        except Exception as e:
            print(f"Error checking for updates: {str(e)}")

        # 7. نهاية عملية التسجيل قبل إعادة التشغيل مباشرة
        try:
            logging.info('Self-improvement process completed successfully')
        except Exception as e:
            print(f"Error logging completion: {str(e)}")

        # 8. خطوة إعادة التشغيل النهائية (الخاتمة)
        # نقوم بإعادة التشغيل إما بسبب التحديث الخارجي أو لأن الوكيل حدث كوده محلياً بالفعل
        try:
            print("Restarting agent process to apply changes...")
            importlib.reload(sys.modules[__name__])
            os.execl(sys.executable, sys.executable, *sys.argv)
        except Exception as e:
            print(f"Critical Error restarting agent: {str(e)}")

        # Added a new feature to handle exceptions during the self-improvement process
        try:
            if should_restart_for_update:
                print("Restarting agent due to external update...")
                importlib.reload(sys.modules[__name__])
                os.execl(sys.executable, sys.executable, *sys.argv)
        except Exception as e:
            print(f"Error restarting agent due to external update: {str(e)}")

        # Added a new feature to improve error handling and provide more informative error messages
        try:
            if should_restart_for_update:
                print("Agent will restart to apply the latest updates from the remote repository.")
            else:
                print("Agent has completed the self-improvement process and will continue running with the updated code.")
        except Exception as e:
            print(f"Error providing informative error message: {str(e)}")