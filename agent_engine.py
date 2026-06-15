import os

import requests

import json

import subprocess



class GitHubAgent:
  
    def __init__(self, api_key, model="llama3-70b-8192", endpoint=None):
      
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
          
            "temperature": 0.5
          
        }
      
        try:
          
            response = requests.post(self.endpoint, headers=headers, json=data)
          
            response.raise_for_status()
          
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
          
            'git commit -m "Self-improvement: Agent updated its own code via Groq Llama 3 70B"',
          
            'git push'
          
        ]
      


        results = []
      
        for cmd in commands:
          
            results.append(self.execute_command(cmd))
          
   


























































