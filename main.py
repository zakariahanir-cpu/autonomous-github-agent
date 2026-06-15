#!/usr/bin/env python3
import os
import re
from agent_engine import GitHubAgent

def main():
    # التحقق من وجود مفتاح API
    api_key = os.getenv('LLM_API_KEY')
    if not api_key:
        print("Error: LLM_API_KEY not found. Please add it to GitHub Secrets.")
        return

    # استخدام نموذج أحدث وأكثر استقراراً
    # النماذج الموصى بها: llama-3.3-70b-versatile أو llama-3.1-70b-versatile
    agent = GitHubAgent(api_key=api_key, model="llama-3.3-70b-versatile")
    print("--- GitHub Autonomous Agent Started ---")

    # قراءة الكود الحالي
    try:
        main_code = agent.read_file('main.py')
        engine_code = agent.read_file('agent_engine.py')
    except Exception as e:
        print(f"Error reading source files: {e}")
        return

    # صياغة طلب أكثر دقة للنموذج
    prompt = f"""
You are an autonomous self-improving GitHub Agent. 
Your goal is to improve your own source code.

CURRENT MAIN CODE (main.py):
{main_code}

CURRENT ENGINE CODE (agent_engine.py):
{engine_code}

TASK:
1. Identify ONE specific logic improvement, bug fix, or feature enhancement.
2. Provide the FULL updated code for the file you chose to improve.

RESPONSE FORMAT:
You MUST start your response with the filename in a code block, like this:

```main.py
(full updated code here)
```

OR

```agent_engine.py
(full updated code here)
```

Do not provide explanations outside the code block.
"""

    print(f"Consulting {agent.model} via Groq...")
    response = agent.query(prompt)

    # معالجة الاستجابة
    if response:
        if response.startswith("Error:"):
            print(f"AI Provider returned an error: {response}")
            return

        # البحث عن أي كتلة برمجية تبدأ بـ main.py أو agent_engine.py
        match = re.search(r"```(?:python|)\s*(main\.py|agent_engine\.py)\s*\n(.*?)\n```", response, re.DOTALL | re.IGNORECASE)
        
        if match:
            filename = match.group(1).strip().lower()
            new_code = match.group(2).strip()
            
            if filename in ['main.py', 'agent_engine.py']:
                print(f"Applying improvement to {filename}...")
                agent.self_improve(new_code, filename)
            else:
                print(f"AI suggested an invalid filename: {filename}")
        else:
            if "```" in response:
                print("Response format was slightly off, attempting manual extraction...")
                parts = response.split("```")
                content = parts[1].strip()
                lines = content.split("\n")
                
                first_line = lines[0].lower()
                if "agent_engine" in first_line or "class githubagent" in content.lower():
                    filename = "agent_engine.py"
                    new_code = "\n".join(lines[1:]) if "py" in first_line else content
                else:
                    filename = "main.py"
                    new_code = "\n".join(lines[1:]) if "py" in first_line else content
                
                print(f"Applying suspected improvement to {filename}...")
                agent.self_improve(new_code.strip(), filename)
            else:
                print("No valid code block found in the AI response.")
    else:
        print("No response received from the AI.")

    print("--- Agent Task Completed ---")

if __name__ == "__main__":
    main()
    
