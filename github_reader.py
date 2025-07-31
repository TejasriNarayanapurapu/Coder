import requests
from config import GITHUB_TOKEN

def get_headers():
    return {"Authorization": f"token {GITHUB_TOKEN}"}

def get_github_issue(owner, repo, issue_number):
    url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}"
    response = requests.get(url, headers=get_headers())
    if response.status_code == 200:
        return response.json()
    return {"title": "Issue not found", "body": "Check repository or issue number."}

def get_readme(owner, repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/readme"
    response = requests.get(url, headers=get_headers())
    if response.status_code == 200:
        import base64
        content = response.json().get("content", "")
        return base64.b64decode(content).decode("utf-8")
    return "README not found."
