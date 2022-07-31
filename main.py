# -*- coding:utf-8 -*-
import os
from git.repo import Repo
import time
import datetime
import shutil

print("-" * 50)
print("now: ", datetime.datetime.now().strftime('%Y-%M-%d %H:%M:%S'))
print("-" * 50)


class AutoDeploy(object):

    def __init__(self):
        self.base_path = os.path.dirname(os.path.abspath(__file__))
        self.repo_path = os.path.join(self.base_path, "repo")
        self.git_url = "https://github.com/zkpgds/docs.git"
        print(self.git_url)
        # 逻辑，检测以下每个分支代码在近5分钟是否有提交， 如果有提交的话， 执行deploy.sh
        self.need_scan_branch = ["v1_cn", "v1_en"# 现货
                                 ]

    def clone_code(self):
        # 拉代码库
        clone_start = time.time()
        if os.path.exists(self.repo_path):
            shutil.rmtree(self.repo_path)
        git_repo = Repo.clone_from(self.git_url, to_path=self.repo_path, branch='master')
        print("clone repo spend: ", (time.time() - clone_start) // 1, "s")
        # 更新代码
        git_repo.git.fetch("--all", '--force')
        os.environ["GH_TOKEN"] = "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"
        return git_repo

    def auto_scan_and_deploy(self):
        base_time = datetime.datetime.now(
            tz=datetime.timezone(datetime.timedelta(hours=8), 'Asia/Shanghai')) - datetime.timedelta(minutes=6)
        git_repo = self.clone_code()
        for branch in self.need_scan_branch:
            git_repo.git.checkout(branch)
            git_repo.git.pull("origin", branch)
            commit_history = list(git_repo.iter_commits(rev=branch))
            latest_commit = commit_history[0]
            print(branch, "last commit", latest_commit.committer.name, latest_commit.committed_datetime)
            if latest_commit.committed_datetime > base_time:
                print(branch, "is update", latest_commit.committer.name, latest_commit.committed_datetime, )
                cmd_str = "cd " + os.path.join(self.base_path, 'repo') + " && bundle install && ./deploy.sh"
                print(cmd_str)
                r = os.system(cmd_str)
                if r != 0:
                    raise Exception("deploy fail")
        print("done~")


auto = AutoDeploy()
auto.auto_scan_and_deploy()
