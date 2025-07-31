import streamlit as st
import openai
from config import OPENAI_API_KEY
from github_reader import get_github_issue, get_readme

openai.api_key = OPENAI_API_KEY

def login():
    st.title("🔐 HyperCoder Access")
    access_code = st.text_input("Enter your access code", type="password")

    if 'login_error' not in st.session_state:
        st.session_state['login_error'] = False

    def authenticate():
        if access_code == "HyperCoder2025!":
            st.session_state['authenticated'] = True
            st.session_state['login_error'] = False
        else:
            st.session_state['login_error'] = True

    st.button("Submit", on_click=authenticate)

    if st.session_state.get('login_error', False):
        st.error("Invalid access code")

def limited_view():
    st.title("HyperCoder - Limited Demo")
    st.write("This is a demo version. Buy access to unlock full features!")

def summarize_text(text):
    if not text:
        return "No content to summarize."
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "user", "content": f"Summarize this:\n\n{text}"}]
    )
    return response.choices[0].message["content"]

def full_app():
    st.title("🧠 HyperCoder – AI Engineer-in-a-Box")

    owner = st.text_input("GitHub Owner (e.g., 'openai')")
    repo = st.text_input("Repo (e.g., 'gpt-2')")
    issue_number = st.number_input("Issue Number", step=1)

    if st.button("Read Issue"):
        issue = get_github_issue(owner, repo, issue_number)
        readme = get_readme(owner, repo)

        st.subheader("🪵 Issue Content")
        st.markdown(f"### 📝 Title: {issue.get('title', 'N/A')}")
        labels = issue.get("labels", [])
        if labels:
            label_names = [label['name'] for label in labels]
            st.markdown(f"🏷️ Labels: {', '.join(label_names)}")
        else:
            st.markdown("🏷️ Labels: None")

        st.write(issue.get("body", "Not found"))
        st.subheader("🧠 Summary of Issue")
        summary = summarize_text(issue.get("body", ""))
        st.write(summary)

        st.subheader("📘 README")
        st.code(readme)

if 'authenticated' not in st.session_state:
    login()
elif st.session_state['authenticated']:
    full_app()
else:
    limited_view()
