import requests
from github import Github
from github import Auth
from github.GithubException import UnknownObjectException
import datetime
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))
from src.utils.config_loader import load_setting




def get_repo():
    setting = load_setting()
    token = setting["github"].get("token")
    if not token:
        raise ValueError("GitHub token is missing in settings.yaml")
    auth = Auth.Token(token)
    g = Github(auth=auth)
    return g.get_user().get_repo(setting["github"].get("repo_name"))


def get_zen_quotes():
    response = requests.get('https://zenquotes.io/api/random/')
    data = response.json()[0]
    return(data)

def commit_quote(repo, file_path='quotes.md'):
    try:
        file = repo.get_contents(file_path)
        # content = file.decoded_content.decode()
        sha = file.sha
        file_exists = True
        current_content = file.decoded_content.decode()
    except UnknownObjectException:
        sha = None
        file_exists = False
        current_content = ""
    new_quote = get_zen_quotes()
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    new_content = f"{current_content}\n\n> \"{new_quote['q']}\"\n\n— {new_quote['a']}\n\n Added on : {timestamp}\n\n --- \n"
    commit_message = f"Updated Quotes with gitfather bot at {datetime.datetime.now()}"
    if file_exists:
        repo.update_file(
            path=file_path,
            message=commit_message,
            content=new_content,
            sha=sha,
            branch="main"
        )
    else:
        repo.create_file(
            path=file_path,
            message=commit_message,
            content=new_content,
            branch="main"
        )
    from src.bot.bot import notify_user
    import asyncio
    asyncio.run(notify_user(msg="A new commit made by the Dom gitfather to family archive"))
    print(commit_message)
    return(new_quote,commit_message)



if __name__ == "__main__":
    repo = get_repo()
    commit_quote(repo)



# def commit_quote(repo, file_path='quotes.md'):
#     try:
#         file = repo.get_contents(file_path)
#         # content = file.decoded_content.decode()
#         sha = file.sha
#         file_exists = True
#     except UnknownObjectException:
#         sha = None
#         file_exists = False
#     new_content = get_zen_quotes()
#     commit_message = f"Updated Quotes with gitfather bot at {datetime.datetime.now()}"
#     if file_exists:
#         repo.update_file(
#             path=file_path,
#             message=commit_message,
#             content=new_content,
#             sha=sha,
#             branch="main"
#         )
#     else:
#         repo.create_file(
#             path=file_path,
#             message=commit_message,
#             content=new_content,
#             branch="main"
#         )