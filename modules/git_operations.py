import os
import shutil
import time

import os
import shutil
from git import Repo
import time

def clone_repository(repo_url, repo_name, tmp_dir="./tmp"):
    # tmpフォルダを削除
    # if os.path.exists(tmp_dir):
    #     shutil.rmtree(tmp_dir)

    # tmpフォルダを作成
    os.makedirs(tmp_dir, exist_ok=True)

    # リポジトリのクローン
    repo_path = os.path.join(tmp_dir, repo_name)
    if os.path.exists(repo_path):
        shutil.rmtree(repo_path)
    Repo.clone_from(repo_url, repo_path)

    # 一時的な遅延を追加
    time.sleep(1)

    return repo_path

if __name__ == "__main__": 
    repo_url = "https://github.com/deepseek-ai/DeepSeek-Math"
    repo_name = repo_url.split("/")[-1].split(".")[0]
    tmp_dir = "./tmp"  # 必要に応じてtmpディレクトリを指定
    clone_repository(repo_url, repo_name, tmp_dir)