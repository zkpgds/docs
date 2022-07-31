# -*- coding:utf-8 -*-
import argparse
import os
import time
import datetime
import shutil

from github import Github

print("-" * 50)
print("now: ", datetime.datetime.now().strftime('%Y-%M-%d %H:%M:%S'))
print("-" * 50)

def __init__(self):
    self.base_path = os.path.dirname(os.path.abspath(__file__))

def get_me(user):
    return user.get_user().login


def login(token):
    return Github(token)


def get_repo(user: Github, repo: str):
    return user.get_repo(repo)


def main(token, repo_name):
    print("===============")
    print(token)
    print(repo_name)
    print("===================")
    user = login(token)
    me = get_me(user)
    repo = get_repo(user, repo_name)
#     cmd_str = "cd " + os.path.join(os.path.dirname(os.path.abspath(__file__)), 'repo') + " && bundle install && ./deploy.sh"
#     print(cmd_str)
#     r = os.system(cmd_str)
#     if r != 0:
#         raise Exception("deploy fail")
#     print("done~")
    print(repo.name)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("github_token", help="github_token")
    parser.add_argument("repo_name", help="repo_name")
    options = parser.parse_args()
    main(options.github_token, options.repo_name)
