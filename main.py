
#!/usr/bin/env python3
import os
import re
import time
from agent_engine import GitHubAgent

def main():
    # التحقق من وجود مفتاح API
    api_key = os.getenv("LLM_API_KEY")
    if not api_key:
        print("Error: LLM_API_KEY not found. Please add it to GitHub Secrets.")
        return

    # استخدام نموذج أحدث وأكثر استقراراً
    agent = GitHubAgent(api_key=api_key, model="llama-3.3-70b-versatile")
    print("--- GitHub Autonomous Agent Started ---")

    # قراءة الكود الحالي لـ main.py و agent_engine.py
    try:
        main_code = agent.read_file("main.py")
        engine_code = agent.read_file("agent_engine.py")
    except Exception as e:
        print(f"Error reading source files: {e}")
        return # الخروج إذا فشلت قراءة الملفات

    # صياغة طلب للنموذج لتحسين main.py أو agent_engine.py
    prompt = f"""
You are an autonomous self-improving GitHub Agent. 
Your goal is to identify ONE specific logic improvement, bug fix, or feature enhancement in your own source code (either main.py or agent_engine.py) and provide the FULL updated code for that file.

CURRENT MAIN CODE (main.py):
{main_code}

CURRENT ENGINE CODE (agent_engine.py):
{engine_code}

TASK:
1. Analyze the current code in main.py and agent_engine.py.
2. Identify ONE specific, actionable improvement (e.g., optimize a function, fix a potential bug, add a small useful feature, improve error handling).
3. Provide the FULL updated code for the file you chose to improve. Ensure the code is complete and syntactically correct.

RESPONSE FORMAT:
You MUST start your response with the filename in a code block, like this:

```main.py
(full updated code here)
```

OR

```agent_engine.py
(full updated code here)
```

Do not provide explanations outside the code block. If no improvement is needed or possible at this moment, respond with "NO_IMPROVEMENT_NEEDED".
"""

    print(f"Consulting {agent.model} via Groq for self-improvement...")
    response = agent.improved_query_with_validation(prompt) # استخدام الدالة الجديدة للاستعلام

    # معالجة الاستجابة
    if response:
        if response.startswith("Error:") or response == "Invalid response from the AI provider.":
            print(f"AI Provider returned an error or invalid response: {response}")
        elif response == "NO_IMPROVEMENT_NEEDED":
            print("AI indicated no improvement needed at this time.")
        else:
            # البحث عن كتلة برمجية تبدأ بـ main.py أو agent_engine.py
            match = re.search(r"```(?:python|)\s*(main\.py|agent_engine\.py)\s*\n(.*?)\n```", response, re.DOTALL | re.IGNORECASE)
            
            if match:
                filename = match.group(1).strip().lower()
                new_code = match.group(2).strip()
                
                if filename in ["main.py", "agent_engine.py"]:
                    print(f"Applying improvement to {filename}...")
                    agent.improved_self_improve_with_validation(new_code, filename)
                else:
                    print(f"AI suggested an invalid filename: {filename}")
            else:
                print("No valid code block found in the AI response.")
    else:
        print("No response received from the AI.")
    
    print("--- Agent Task Completed ---")

if __name__ == "__main__":
    main()
    
