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

[![Hugging Face Spaces](https://img.shields.io/badge/%F0%9F%A4%97%20Hugging%20Face-Spaces-blue)](https://huggingface.co/spaces/OFA-Sys/OFA-Image_Caption)[![](https://img.shields.io/github/stars/Sunwood-ai-labs/CodeLumia)](https://github.com/Sunwood-ai-labs/CodeLumia)[![](https://img.shields.io/github/last-commit/Sunwood-ai-labs/CodeLumia)](https://github.com/Sunwood-ai-labs/CodeLumia)[![](https://img.shields.io/github/languages/top/Sunwood-ai-labs/CodeLumia)](https://github.com/Sunwood-ai-labs/CodeLumia)

</h3>

</p>


## 🚀 はじめに

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