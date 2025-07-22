from dotenv import load_dotenv
import os

load_dotenv()

api_key = os.getenv('GEMINI_API_KEY')

# if not api_key:
#     raise ValueError('환경 변수 안됨 다시해')

# import google.genai as genai

# genai.configure(api_key=api_key)

