import os
import streamlit as st
import fnmatch
import shutil
import time
import json
import base64

# .gitignoreのパターンを読み込む
ignore_patterns = []
if os.path.exists(".CodeLumiaignore"):
    with open(".CodeLumiaignore", "r") as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith("#"):
                ignore_patterns.append(line)

# docs\page_front.mdファイルの内容を読み込む
if os.path.exists("docs/page_front.md"):
    with open("docs/page_front.md", "r", encoding="utf-8") as f:
        page_front_content = f.read()
        
        st.markdown(page_front_content, unsafe_allow_html=True)

# リポジトリのURLを入力するテキストボックス
repo_url = st.text_input("リポジトリのURL:")

# .gitignoreのパターンを編集するサイドバー
st.sidebar.title(".gitignore Patterns")
ignore_patterns = st.sidebar.text_area("Enter patterns (one per line):", value="\n".join(ignore_patterns), height=600).split("\n")

if repo_url:
    # tmpフォルダを削除
    if os.path.exists("tmp"):
        shutil.rmtree("tmp")

    # tmpフォルダを作成
    os.makedirs("tmp")

    # リポジトリのクローン
    repo_name = repo_url.split("/")[-1].split(".")[0]
    repo_path = f"tmp/{repo_name}"
    if os.path.exists(repo_path):
        shutil.rmtree(repo_path)
    os.system(f"git clone {repo_url} {repo_path}")

    # 一時的な遅延を追加
    time.sleep(1)

    # リポジトリのファイルツリーを取得
    file_tree = ""
    for root, dirs, files in os.walk(repo_path):
        # .gitignoreに一致するディレクトリを無視
        dirs[:] = [d for d in dirs if not any(fnmatch.fnmatch(d, pattern) for pattern in ignore_patterns)]
        
        level = root.replace(repo_path, "").count(os.sep)
        indent = " " * 4 * (level)
        file_tree += f"{indent}{os.path.basename(root)}/\n"
        subindent = " " * 4 * (level + 1)
        for f in files:
            # .gitignoreに一致するファイルを無視
            if not any(fnmatch.fnmatch(f, pattern) for pattern in ignore_patterns):
                file_tree += f"{subindent}{f}\n"

    # マークダウンファイルを結合
    markdown_content = f"# << {repo_name}>> \n## {repo_name} File Tree\n\n```\n{file_tree}\n```\n\n"

    # 拡張子と言語のマッピングを読み込む
    with open("docs/language_map.json", "r") as f:
        language_map = json.load(f)

    for root, dirs, files in os.walk(repo_path):
        # .gitignoreに一致するディレクトリを無視
        dirs[:] = [d for d in dirs if not any(fnmatch.fnmatch(d, pattern) for pattern in ignore_patterns)]
        for file in files:
            # .gitignoreに一致するファイルを無視
            if not any(fnmatch.fnmatch(file, pattern) for pattern in ignore_patterns):
                file_path = os.path.join(root, file)
                _, file_extension = os.path.splitext(file)
                language = language_map.get(file_extension, "")
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    # コードブロック内のコードブロックの範囲の全行の先頭に2つのスペースを入れる
                    lines = content.split("\n")
                    modified_lines = []
                    inside_code_block = False
                    for line in lines:
                        if line.startswith("```"):
                            inside_code_block = not inside_code_block
                            modified_lines.append("\t" + line)
                        else:
                            if inside_code_block:
                                modified_lines.append("\t" + line)
                            else:
                                modified_lines.append(line)
                    content = "\n".join(modified_lines)
                    # コードブロックの中のバッククォートをエスケープ
                    markdown_content += f"## {file_path.replace(f'{repo_path}/', '')}\n\n```{language}\n{content}\n```\n\n"

    # マークダウンファイルを保存
    with open(f"{repo_name}.md", "w", encoding="utf-8") as f:
        f.write(markdown_content)

    # Streamlitアプリケーションの構築
    st.markdown(markdown_content, unsafe_allow_html=True)

    # ダウンロードリンクの作成
    st.markdown(f'<a href="data:text/markdown;base64,{base64.b64encode(markdown_content.encode("utf-8")).decode("utf-8")}" download="{repo_name}.md">Download Markdown File</a>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("# Full Text")
    st.code(markdown_content)