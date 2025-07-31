import streamlit as st
from openai import OpenAI
from config import get_openai_key, get_github_token
from agent.tools.github_reader import get_github_issue, get_readme
from agent.tools.code_writer import generate_code_from_issue

st.set_page_config(page_title="🤖 HyperCoder", layout="wide")

st.markdown("<h1 style='text-align: center; color: #4CAF50;'>🤖 HyperCoder</h1>", unsafe_allow_html=True)

# Load API keys
openai_key = get_openai_key()
github_token = get_github_token()

if not openai_key or not github_token:
    st.error("❌ API keys are missing! Please check your config.py file.")
    st.stop()

client = OpenAI(api_key=openai_key)

def summarize_text(text):
    response = client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": f"Summarize this:\n\n{text}"}]
    )
    return response.choices[0].message.content.strip()

def full_app():
    repo_url = st.text_input("Enter GitHub Issue URL:")
    if repo_url:
        try:
            issue = get_github_issue(repo_url, github_token)
            st.subheader("🔍 Issue Summary")
            st.write(issue.get("title", "No title found"))
            st.write(issue.get("body", "No body found"))

            summary = summarize_text(issue.get("body", ""))
            st.subheader("🧠 AI Summary")
            st.write(summary)

            st.subheader("💡 Generated Code")
            generated_code = generate_code_from_issue(issue.get("body", ""))
            st.code(generated_code, language='python')

        except Exception as e:
            st.error(f"❌ Error: {str(e)}")

if __name__ == "__main__":
    full_app()
