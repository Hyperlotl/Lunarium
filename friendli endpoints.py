#1. getting the PAT for friendli.ai
from google.colab import userdata #this part is unique to google colab
token = userdata.get("FRIENDLI_TOKEN") #replace this part with getting the token
print(token)

#2. importing necessary libs
import requests #pip install requests
import json #pip install json
import time  # Import time module for measuring response time

#3. init chat hist (character background)
chat = [
    {"role": "system", "content": (
        "system message goes here ig"
    )}
]

#4. response generation function
def generate_response(conversation = chat,model_choice = "meta-llama-3.1-8b-instruct",serverless = True):
    start_time = time.time()  # Start timing
    if serverless:
      url = "https://api.friendli.ai/serverless/v1/chat/completions"
    else:
      url = "https://api.friendli.ai/dedicated/v1/chat/completions"
    try:
      generated_text = ""
      headers = {
      "Authorization": "Bearer " + token,
      "Content-Type": "application/json"
      }
      payload = {
      "model": model_choice, 
      "messages": conversation,
      "temperature": 0.8,
      "max_tokens": 2048,
      "top_p": 0.8
      }
      response = requests.request("POST", url, json=payload, headers=headers)
      generated_text = response.json()["choices"][0]["message"]["content"]
      print("")#print("✅ Response generated successfully")
    except Exception as e:
        print(f"❌ Error: {e}")
        generated_text = "(Error occurred)"
        
    end_time = time.time()  # End timing
    elapsed_time = end_time - start_time
    print(f"⏳ Response generated in {elapsed_time:.2f} seconds")
    
    return generated_text

print("AI Ready! Begin chatting.")

#5. Chat loop
while True:
    try:
        msg = input("You: ")
        if msg.lower() == "cmd":
            print("Command interface initiated")
            command = input("Enter command: ").lower()
            if command == "clear":
                chat = [{"role": "system", "content": ("You are Luna, a cheerful and adventurous AI who loves helping people solve problems and explore new ideas. She is friendly, curious, and eager to engage in conversation.")}]
            elif command == "hist":
                print("----------------------------------------------------------------------------------------")
                for msg in chat:
                    print(f"{msg['role']}: {msg['content']}\n")
                print("----------------------------------------------------------------------------------------")
            elif command == "crash":
                raise Exception("Crashing")
            elif command == "exit":
                break
        else:
            chat.append({"role": "user", "content": str(msg)})
            chat_reply = generate_response(conversation = chat,model_choice ="lzhdgefmojxs",serverless = False) #change model_choice to the actual endpoint ID if using dedicated endpoints, otherwise, remove and set "serverless" to true
            print(f"Luna: {chat_reply}")
            chat.append({"role": "assistant", "content": str(chat_reply)})
    except KeyboardInterrupt:
        break
