# << CodeLumia>> 
## CodeLumia File Tree

```
CodeLumia/
    .SourceSageignore
    app.py
    CodeLumia.md
    docker-compose.yml
    Dockerfile
    README.md
    requirements.txt
    docs/
        language_map.json
        page_front.md
        SourceSageDocs.md
    modules/
        file_operations.py
        git_operations.py
        markdown_operations.py

```

## .SourceSageignore

```
.git
__pycache__
LICENSE
output.md
assets
Style-Bert-VITS2
output
streamlit
SourceSage.md
data
.gitignore
.SourceSageignore
*.png
Changelog
SourceSageAssets
SourceSageAssetsDemo
__pycache__
.pyc
**/__pycache__/**
modules\__pycache__
.svg
sourcesage.egg-info
.pytest_cache
dist
build

.gitattributes
.CodeLumiaignore
tmp
.CodeLumiaignore
```

## app.py

```python
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

```

## CodeLumia.md

```markdown
# << CodeLumia>> 
## CodeLumia File Tree

	```
	CodeLumia/
	    app.py
	    README.md
	    docs/
	        SourceSageDocs.md
	
	```

## app.py

	```python
	# sample code 
	
	import streamlit as st
	
	x = st.slider('Select a value')
	st.write(x, 'squared is', x * x)
	```

## README.md

	```markdown
	---
	title: CodeLumia
	emoji: 📚
	colorFrom: purple
	colorTo: blue
	sdk: streamlit
	sdk_version: 1.33.0
	app_file: app.py
	pinned: false
	license: mit
	---
	
	
	<p align="center">
	<img src="https://media.githubusercontent.com/media/Sunwood-ai-labs/CodeLumia/main/docs/CodeLumia_icon.png" width="50%">
	<br>
	<h1 align="center">CodeLumia</h1>
	<h3 align="center">
	  ～Learn to Code, Step by Step～
	
	[![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/MakiAi/CodeLumia)[![](https://img.shields.io/github/stars/Sunwood-ai-labs/CodeLumia)](https://github.com/Sunwood-ai-labs/CodeLumia)[![](https://img.shields.io/github/last-commit/Sunwood-ai-labs/CodeLumia)](https://github.com/Sunwood-ai-labs/CodeLumia)[![](https://img.shields.io/github/languages/top/Sunwood-ai-labs/CodeLumia)](https://github.com/Sunwood-ai-labs/CodeLumia)
	
	</h3>
	
	</p>
	
	
	```

## docs/SourceSageDocs.md

	```markdown
	# SourceSageDocs
	
		```bash
		
		sourcesage --repository CodeLumia --owner Sunwood-ai-labs
		```
	```


```

## docker-compose.yml

```yaml
version: '3'

services:
  app:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - .:/app
```

## Dockerfile

```
FROM python:3.12-slim

WORKDIR /app

RUN apt-get update && \
    apt-get install -y git && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py"]
```

## README.md

```markdown
---
title: CodeLumia
emoji: 📚
colorFrom: purple
colorTo: blue
sdk: docker
app_port: 8501
app_file: app.py
pinned: false
license: mit
---


<p align="center">
<img src="https://media.githubusercontent.com/media/Sunwood-ai-labs/CodeLumia/main/docs/CodeLumia_icon.png" width="50%">
<br>
<h1 align="center">CodeLumia</h1>
<h3 align="center">
  ～Learn to Code, Step by Step～

[![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/MakiAi/CodeLumia)[![](https://img.shields.io/github/stars/Sunwood-ai-labs/CodeLumia)](https://github.com/Sunwood-ai-labs/CodeLumia)[![](https://img.shields.io/github/last-commit/Sunwood-ai-labs/CodeLumia)](https://github.com/Sunwood-ai-labs/CodeLumia)[![](https://img.shields.io/github/languages/top/Sunwood-ai-labs/CodeLumia)](https://github.com/Sunwood-ai-labs/CodeLumia)

</h3>

</p>


## 🚀 はじめに


CodeLumiaへようこそ！CodeLumiaは、GitHubリポジトリのソースコードを分析し、包括的なマークダウン形式のドキュメントを自動生成するツールです。プロジェクトの構造、依存関係、設定などを簡単に理解できるようになります。

CodeLumiaは、開発者がコードベースをすばやく把握し、プロジェクトに効率的に貢献できるようにすることを目的としています。新しいチームメンバーのオンボーディングを容易にし、コードの保守性を向上させます。

>[!TIP]
>このリポジトリは[SourceSage](https://github.com/Sunwood-ai-labs/SourceSage)を活用しており、リリースノートやREADME、コミットメッセージの9割は[SourceSage](https://github.com/Sunwood-ai-labs/SourceSage) ＋ [claude.ai](https://claude.ai/)で生成しています。

### 主な特徴:

- GitHubリポジトリの自動分析
- マークダウン形式のドキュメント生成
- ファイルとディレクトリの無視パターンのカスタマイズ
- わかりやすいStreamlitユーザーインターフェース

CodeLumiaを使用して、プロジェクトのドキュメンテーションを強化し、チームのコラボレーションを促進しましょう。ぜひお試しください！


## デモアプリ

[![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/OFA-Sys/OFA-Image_Caption)



### 前提条件

- Docker
- Docker Compose

### インストール

1. リポジトリをクローンします:
   ```bash
   git clone https://github.com/Sunwood-ai-labs/CodeLumia.git
   cd CodeLumia
   ```

2. Dockerコンテナをビルドして実行します:
   ```bash
   docker-compose up --build
   ```

3. ブラウザで `http://localhost:8501` にアクセスしてアプリケーションを開きます。

## 📖 使い方

1. 分析したいGitHubリポジトリのURLをテキスト入力フィールドに入力します。
2. アプリケーションがリポジトリをクローンし、ファイルを処理して、マークダウンのドキュメントファイルを生成します。
3. 生成されたドキュメントがStreamlitアプリに表示されます。
4. "Download Markdown File"リンクをクリックして、マークダウンファイルをダウンロードできます。

>[!TIP]
>Full Textのところからクリップボードにコピーすることもできます


## 🔧 設定

- `.CodeLumiaignore`ファイルには、ドキュメント生成プロセス中に無視する特定のファイルとディレクトリのパターンが含まれています。これらのパターンは、Streamlitアプリのサイドバーで編集できます。

## 📂 プロジェクト構造

	```
	CodeLumia/
	├─ .github/
	│  └─ workflows/
	│     └─ run.yaml
	├─ docs/
	│  ├─ language_map.json
	│  ├─ page_front.md
	│  └─ SourceSageDocs.md
	├─ modules/
	│  ├─ file_operations.py
	│  ├─ git_operations.py
	│  └─ markdown_operations.py
	├─ app.py
	├─ CodeLumia.md
	├─ docker-compose.yml
	├─ Dockerfile
	├─ README.md
	└─ requirements.txt
	```

## 🤝 コントリビューション

コントリビューションは大歓迎です！問題を見つけたり、改善のための提案がある場合は、issueを開くかプルリクエストを送ってください。

## 📄 ライセンス

このプロジェクトは[MITライセンス](LICENSE)の下で公開されています。
	```
```

## requirements.txt

```plaintext
streamlit
```

## docs/language_map.json

```json
{
    ".py": "python",
    ".js": "javascript",
    ".java": "java",
    ".c": "c",
    ".cpp": "cpp",
    ".cs": "csharp",
    ".go": "go",
    ".php": "php",
    ".rb": "ruby",
    ".rs": "rust",
    ".ts": "typescript",
    ".html": "html",
    ".css": "css",
    ".json": "json",
    ".xml": "xml",
    ".yml": "yaml",
    ".yaml": "yaml",
    ".md": "markdown",
    ".txt": "plaintext",
    ".sh": "bash",
    ".sql": "sql",
    "Dockerfile": "dockerfile",
    ".dockerfile": "dockerfile",
    "docker-compose.yml": "yaml",
    "docker-compose.yaml": "yaml"
}
```

## docs/page_front.md

```markdown
<p align="center">
<img src="https://media.githubusercontent.com/media/Sunwood-ai-labs/CodeLumia/main/docs/CodeLumia_icon.png" width="40%">
<br>
<h1 align="center">CodeLumia</h1>
<h3 align="center">
  ～Learn to Code, Step by Step～

[![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/OFA-Sys/OFA-Image_Caption)[![](https://img.shields.io/github/stars/Sunwood-ai-labs/CodeLumia)](https://github.com/Sunwood-ai-labs/CodeLumia)[![](https://img.shields.io/github/last-commit/Sunwood-ai-labs/CodeLumia)](https://github.com/Sunwood-ai-labs/CodeLumia)[![](https://img.shields.io/github/languages/top/Sunwood-ai-labs/CodeLumia)](https://github.com/Sunwood-ai-labs/CodeLumia)

</h3>

</p>

```

## docs/SourceSageDocs.md

```markdown
# SourceSageDocs

	```bash
	
	sourcesage --repository CodeLumia --owner Sunwood-ai-labs
	```
```

## modules/file_operations.py

```python
import os
import fnmatch

def get_file_tree(repo_path, ignore_patterns):
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
    return file_tree

def process_files(repo_path, ignore_patterns):
    file_contents = []
    for root, dirs, files in os.walk(repo_path):
        # .gitignoreに一致するディレクトリを無視
        dirs[:] = [d for d in dirs if not any(fnmatch.fnmatch(d, pattern) for pattern in ignore_patterns)]
        for file in files:
            # .gitignoreに一致するファイルを無視
            if not any(fnmatch.fnmatch(file, pattern) for pattern in ignore_patterns):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    file_contents.append((file_path.replace(f'{repo_path}/', ''), content))
    return file_contents
```

## modules/git_operations.py

```python
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
```

## modules/markdown_operations.py

```python
import json
from modules.file_operations import get_file_tree, process_files
import os

def create_markdown_content(repo_name, file_tree, repo_path, ignore_patterns):
    markdown_content = f"# << {repo_name}>> \n## {repo_name} File Tree\n\n```\n{file_tree}\n```\n\n"

    # 拡張子と言語のマッピングを読み込む
    with open("docs/language_map.json", "r") as f:
        language_map = json.load(f)

    file_contents = process_files(repo_path, ignore_patterns)
    for file_path, content in file_contents:
        _, file_extension = os.path.splitext(file_path)
        language = language_map.get(file_extension, "")
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
        markdown_content += f"## {file_path}\n\n```{language}\n{content}\n```\n\n"

    return markdown_content

def save_markdown_file(repo_name, markdown_content):
    with open(f"{repo_name}.md", "w", encoding="utf-8") as f:
        f.write(markdown_content)
```

