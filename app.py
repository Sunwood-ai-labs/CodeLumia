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
# st.markdown("[Full Text](#full-text)")

# .gitignoreのパターンを編集するサイドバー
st.sidebar.title(".CodeLumiaignore Patterns")
ignore_patterns = st.sidebar.text_area("Enter patterns (one per line):", value="\n".join(ignore_patterns), height=300).split("\n")
tmp_dir = st.sidebar.text_input('tmp_dir', './tmp')
# 探索の最大深度を入力するテキストボックス
max_depth = st.sidebar.number_input("探索の最大深度:", min_value=1, value=1, step=1)

preview_markdown = st.sidebar.checkbox('preview markdown', value=False)
preview_plaintext = st.sidebar.checkbox('preview plaintext', value=False)

if st.button("CodeLumia Run ...", type="primary"):
    if repo_url:
        repo_name = repo_url.split("/")[-1].split(".")[0]
        with st.status("Scaning repository...", expanded=False):
            st.write("clone repository...")
            repo_path = clone_repository(repo_url, repo_name, tmp_dir=tmp_dir)
            st.write("get file tree...")
            file_tree = get_file_tree(repo_path, ignore_patterns, max_depth)
            st.write("create markdown content...")
            markdown_content = create_markdown_content(repo_name, file_tree, repo_path, ignore_patterns, max_depth)

        # マークダウンファイルを保存
        save_markdown_file(repo_name, markdown_content)

        # Streamlitアプリケーションの構築
        if(preview_markdown):
            st.markdown(markdown_content, unsafe_allow_html=True)

        # ダウンロードリンクの作成
        st.markdown(f'<div align="center"><a href="data:text/markdown;base64,{base64.b64encode(markdown_content.encode("utf-8")).decode("utf-8")}" download="{repo_name}.md">Download Markdown File</a></div>', unsafe_allow_html=True)

        st.markdown("---")
        if(preview_plaintext):
            st.markdown("# Full Text")
            st.code(markdown_content)