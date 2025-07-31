from dotenv import load_dotenv
import os

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
GITHUB_TOKEN = os.getenv("GITHUB_ACCESS_TOKEN")

print("Loaded GitHub Token:", GITHUB_TOKEN[:4] + "..." + GITHUB_TOKEN[-4:] if GITHUB_TOKEN else "Token not loaded!")
