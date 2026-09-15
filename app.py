import os
from google import genai

# ১. API Key দিয়ে Gemini ক্লায়েন্ট ইনিশিয়াল করুন
# (এখানে আপনার আসল API Key বসিয়ে দিন)
API_KEY = "YOUR_GEMINI_API_KEY" 
client = genai.Client(api_key=API_KEY)

print("--- Gemini 2.5 Flash Testing Tool ---")
print("Type 'exit' or 'quit' to stop the app.\n")

# ২. একটি লুপ চালানো হচ্ছে যেন আপনি বারবার প্রম্পট দিয়ে টেস্ট করতে পারেন
while True:
    user_prompt = input("You: ")
    
    if user_prompt.lower() in ['exit', 'quit']:
        print("Exiting app. Goodbye!")
        break
        
    if not user_prompt.strip():
        continue
        
    try:
        print("Gemini is thinking...")
        
        # ৩. Gemini 2.5 Flash মডেলে রিকোয়েস্ট পাঠানো
        response = client.models.generate_content(
            model='gemini-2.5-flash', # মডেলের নাম
            contents=user_prompt     # আপনার প্রম্পট
        )
        
        # ৪. আউটপুট প্রিন্ট করা
        print(f"\nGemini: {response.text}\n")
        print("-" * 40)
        
    except Exception as e:
        print(f"An error occurred: {e}\n")
