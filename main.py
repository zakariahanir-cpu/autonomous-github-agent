#!/usr/bin/env python3

import os

from agent_engine import GitHubAgent



def main():
  
    api_key = os.getenv('LLM_API_KEY')
  
    if not api_key:
      
        print("Error: LLM_API_KEY not found. Please add it to GitHub Secrets.")
      
        return
      


    agent = GitHubAgent(api_key=api_key, model="llama3-70b-8192")
  
    print("--- GitHub Autonomous Agent Started ---")
  


    main_code = agent.read_file('main.py')
  
    engine_code = agent.read_file('agent_engine.py')
  


    prompt = f"""
    
    You are an autonomous self-improving GitHub Agent powered by Llama 3 70B.
    
    Review your own source code below and identify ONE specific improvement.
    

    
    CURRENT MAIN CODE:
    
    {main_code}
    

    
    CURRENT ENGINE CODE:
    
    {engine_code}
    

    
    Provide the FULL updated code for the file you chose to improve. 
    
    Format your response as follows:
    
    ```filename
    
    (full code here)
    
    ```
    
    """
  


    print("Consulting Llama 3 70B via Groq...")
  
    response = agent.query(prompt)
  


    if response and "```" in response:
      
        try:
          
            parts = response.split("```")
          
            content = parts[1].strip()
          
            lines = content.split("\n")
          
            filename = lines[0].strip()
          
            new_code = "\n".join(lines[1:]).strip()
          


            if filename in ['main.py', 'agent_engine.py']:
              
                print(f"Applying improvement to {filename}...")
              
                agent.self_improve(new_code, filename)
              
            else:
              
                print(f"Invalid filename: {filename}")
              
        except Exception as e:
          
            print(f"Error: {e}")
          
    else:
      
        print("No improvement suggested.")
      


    print("--- Agent Task Completed ---")
  


if __name__ == "__main__":
  
    main()












































