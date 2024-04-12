import os
import shutil
import time

def clone_repository(repo_url, repo_name):
    # tmpフォルダを削除
    if os.path.exists("tmp"):
        shutil.rmtree("tmp")

    # tmpフォルダを作成
    os.makedirs("tmp")

    # リポジトリのクローン
    repo_path = f"tmp/{repo_name}"
    if os.path.exists(repo_path):
        shutil.rmtree(repo_path)
    os.system(f"git clone {repo_url} {repo_path}")

    # 一時的な遅延を追加
    time.sleep(1)

    return repo_path