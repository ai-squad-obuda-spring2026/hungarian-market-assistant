# test_key.py
import os
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv('DEEPSEEK_API_KEY')

if api_key:
    print("✅ API key loaded successfully!")
    print(f"First 10 chars: {api_key[:10]}...")
    print(f"Length: {len(api_key)} characters")
else:
    print("❌ No API key found!")
