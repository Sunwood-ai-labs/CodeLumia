# main.py
import os
import streamlit as st
import base64
from modules.git_operations import clone_repository
from modules.file_operations import get_file_tree, process_files
from modules.markdown_operations import create_markdown_content, save_markdown_file

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

st.markdown("---")
# リポジトリのURLを入力するテキストボックス
repo_url = st.text_input("リポジトリのURL:")
st.markdown("---")

# .gitignoreのパターンを編集するサイドバー
st.sidebar.title(".gitignore Patterns")
ignore_patterns = st.sidebar.text_area("Enter patterns (one per line):", value="\n".join(ignore_patterns), height=600).split("\n")

if repo_url:
    repo_name = repo_url.split("/")[-1].split(".")[0]
    repo_path = clone_repository(repo_url, repo_name)

    file_tree = get_file_tree(repo_path, ignore_patterns)
    markdown_content = create_markdown_content(repo_name, file_tree, repo_path, ignore_patterns)

    # マークダウンファイルを保存
    save_markdown_file(repo_name, markdown_content)

    # Streamlitアプリケーションの構築
    st.markdown(markdown_content, unsafe_allow_html=True)

    # ダウンロードリンクの作成
    st.markdown(f'<a href="data:text/markdown;base64,{base64.b64encode(markdown_content.encode("utf-8")).decode("utf-8")}" download="{repo_name}.md">Download Markdown File</a>', unsafe_allow_html=True)

    st.markdown("---")
    st.markdown("# Full Text")
    st.code(markdown_content)