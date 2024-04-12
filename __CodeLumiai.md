# << NotebookForgeBeta>> 
## NotebookForgeBeta File Tree

```
NotebookForgeBeta/
    create_jupyter_notebook.py
    README.md
    app.py
    example/
        example01.md
    script/
        activate-notebook-forge.bat
        activate-notebook-forge.sh
    docs/

```

## create_jupyter_notebook.py

```python
import json
import re

def create_jupyter_notebook(markdown_file, output_file):
    with open(markdown_file, 'r', encoding="utf-8") as file:
        markdown_content = file.read()

    cells = []
    chunks = re.split(r'(#+\s.*)', markdown_content)

    for i in range(len(chunks)):
        chunk = chunks[i].strip()
        if chunk:
            if chunk.startswith('#'):
                cells.append({
                    'cell_type': 'markdown',
                    'source': [chunk]
                })
            else:
                code_chunks = re.split(r'```python\n(.*?)```', chunk, flags=re.DOTALL)
                for j in range(len(code_chunks)):
                    if j % 2 == 0 and code_chunks[j].strip():
                        cells.append({
                            'cell_type': 'markdown',
                            'source': code_chunks[j].strip().split('\n')
                        })
                    elif j % 2 == 1:
                        code_lines = code_chunks[j].strip().split('\n')
                        cells.append({
                            'cell_type': 'code',
                            'execution_count': None,
                            'metadata': {},
                            'outputs': [],
                            'source': code_lines
                        })

    notebook = {
        'nbformat': 4,
        'nbformat_minor': 0,
        'metadata': {
            'colab': {
                'provenance': []
            },
            'kernelspec': {
                'name': 'python3',
                'display_name': 'Python 3'
            },
            'language_info': {
                'name': 'python'
            }
        },
        'cells': cells
    }

    with open(output_file, 'w') as file:
        json.dump(notebook, file, indent=2)

if __name__ == '__main__':

    # 使用例
    markdown_file = 'example/example01.md'
    output_file = 'example/example01.ipynb'
    create_jupyter_notebook(markdown_file, output_file)
```

## README.md

```markdown
---
title: NotebookForgeDemo
emoji: 📉
colorFrom: blue
colorTo: pink
sdk: streamlit
sdk_version: 1.33.0
app_file: app.py
pinned: false
license: mit
---

<p align="center">
<img src="https://raw.githubusercontent.com/Sunwood-ai-labs/NotebookForgeBeta/main/docs/NotebookForge_icon.jpg" width="100%">
<br>
<h1 align="center">NotebookForge</h1>

</p>


## Introduction
NotebookForgeは、マークダウンファイルをJupyter Notebookに変換するPythonツールです。主な特徴と利点は以下の通りです。

- マークダウンファイル内のPythonコードブロックを適切なセルタイプ（コードセルまたはマークダウンセル）に自動変換
- 通常のテキストはマークダウンセルに変換
- 生成されたNotebookは指定された出力ファイルに保存
- シンプルで使いやすいインターフェース

NotebookForgeを使用することで、マークダウンファイルで書かれたドキュメントやチュートリアルを簡単にJupyter Notebook形式に変換できます。これにより、対話的な実行環境を提供しつつ、マークダウンの読みやすさと書きやすさを維持できます。

>このリポジトリは[SourceSage](https://github.com/Sunwood-ai-labs/SourceSage)を活用しており、リリースノートやREADME、コミットメッセージの9割は[SourceSage](https://github.com/Sunwood-ai-labs/SourceSage) ＋ [claude.ai](https://claude.ai/)で生成しています。

## Demo
NotebookForgeの使用例として、Cohere APIのClassifyエンドポイントについての解説をマークダウンで書き、Jupyter Notebookに変換しました。

- [example/example01.md](example/example01.md): 変換元のマークダウンファイル
- [example/example01.ipynb](example/example01.ipynb): 変換後のJupyter Notebookファイル

このようにNotebookForgeを使うことで、APIドキュメントやチュートリアルを対話的なNotebook形式で提供できます。



## Updates

- [2024/04/11] [NotebookForge v1.0.0](https://github.com/Sunwood-ai-labs/NotebookForgeBeta/releases/tag/v1.0.0)
  - Streamlitベースのウェブアプリを実装
    - ユーザーフレンドリーなGUIでマークダウンからノートブックへの変換を実行可能に
    - 生成されたノートブックをダウンロードする機能を追加
  - Hugging Faceでのデモアプリをリリース
    - [NotebookForgeDemo](https://huggingface.co/spaces/MakiAi/NotebookForgeDemo)にてアプリを公開
  - ノートブック生成ロジックの最適化
  - ドキュメントの拡充
  - マークダウン解析時のバグを修正

- [2024/04/10] [NotebookForge v0.2.0](https://github.com/Sunwood-ai-labs/NotebookForgeBeta/releases/tag/v0.2.0) 
  - Cohere APIのClassifyエンドポイントについての解説をサンプルに追加
  - READMEファイルを追加し、プロジェクトの概要とツールの使い方を記載 
  - `example`ディレクトリを新設し、サンプルファイルを整理
  - サンプルコードのインデントを修正し可読性を向上


## Getting Started
### インストール
NotebookForgeを使用するには、Python 3.11以上が必要です。以下のコマンドでNotebookForge用のConda環境を作成し、アクティベートします。

	```bash
	conda create -n notebook-forge python=3.11
	conda activate notebook-forge
	```

### 使用方法
1. コードブロックを含むマークダウンファイルを用意します。（例: `example/example01.md`）

2. 以下のコマンドを実行し、マークダウンファイルをJupyter Notebookに変換します。
   ```bash
   python create_jupyter_notebook.py
   ```

3. 変換後のNotebookファイルが生成されます。（例: `example/example01.ipynb`）

### カスタマイズ
`create_jupyter_notebook.py`スクリプトの以下の部分を変更することで、入出力ファイルのパスをカスタマイズできます。

	```python
	markdown_file = 'example/example01.md'
	output_file = 'example/example01.ipynb'
	create_jupyter_notebook(markdown_file, output_file)
	```

## Contributing
NotebookForgeへの貢献を歓迎します。バグ報告、機能要望、プルリクエストをお待ちしております。

## License
NotebookForgeはMITライセンスの下で公開されています。詳細は[LICENSE](LICENSE)ファイルを参照してください。

## Acknowledgements

NotebookForgeの開発にあたり、以下のオープンソースプロジェクトを参考にさせていただきました。

- [Jupyter Notebook](https://jupyter.org/)
- [nbformat](https://github.com/jupyter/nbformat)

```

## app.py

```python
import streamlit as st
from create_jupyter_notebook import create_jupyter_notebook
import base64

def download_notebook(notebook_file):
    with open(notebook_file, 'rb') as file:
        notebook_data = file.read()
    b64 = base64.b64encode(notebook_data).decode()
    href = f'<a href="data:application/octet-stream;base64,{b64}" download="{notebook_file}">ノートブックをダウンロード</a>'
    return href

def main():

    st.markdown('''
    
<p align="center">
<img src="https://raw.githubusercontent.com/Sunwood-ai-labs/NotebookForgeBeta/main/docs/NotebookForge_icon.jpg" width="50%">
<br>
<h1 align="center">NotebookForge</h1>
<h3 align="center">～Markdown to Jupyter Notebook Converter～</h3>

</p>

    ''', unsafe_allow_html=True)
    markdown_content = st.text_area('Markdownファイルの内容を貼り付けてください', height=400)
    
    if st.button('変換'):
        if markdown_content.strip():
            with open('temp_markdown.md', 'w', encoding='utf-8') as file:
                file.write(markdown_content)
            
            output_file = 'output_notebook.ipynb'
            create_jupyter_notebook('temp_markdown.md', output_file)
            
            st.success('ノートブックが生成されました。')
            st.markdown(download_notebook(output_file), unsafe_allow_html=True)
        else:
            st.warning('Markdownファイルの内容を入力してください。')

if __name__ == '__main__':
    main()
```

## example/example01.md

```markdown
# Cohere APIのClassifyエンドポイントとは

Classifyエンドポイントは、テキストを事前に定義されたクラス（カテゴリ）に分類するための機能です。いくつかの例を使って、生成モデルからクラス分類器を作成します。内部的には、few-shot分類プロンプトを構築し、それを使って入力テキストを分類します。

## Classifyエンドポイントの使用例

顧客サポートチケットの分類に使えます。例えば、保険会社に届く顧客メールを以下の4つのタイプに自動分類できます。

- 保険証券の詳細を探す
- アカウント設定の変更
- 保険金請求と状況確認
- 保険の解約

これにより、サポートチームは手動で情報を分析してルーティングする手間を省けます。

## Classifyエンドポイントの使い方

### 1. Cohere SDKのインストール

まず、Cohere SDKをインストールします。

	```bash
	pip install cohere
	```

### 2. Cohere clientの設定

次に、Cohere clientを設定します。

	```python
	import cohere
	co = cohere.Client(api_key)
	```

### 3. 学習用の例の追加

学習用の例を追加します。各例はテキストとそれに対応するラベル（クラス）で構成されます。各クラスに最低2つの例が必要です。

	```python
	from cohere.responses.classify import Example
	
	examples=[
	  Example("保険証券はどこで見つけられますか？", "保険証券の詳細を探す"),
	  Example("保険証券のコピーをダウンロードする方法は？", "保険証券の詳細を探す"),
	  ...
	]
	```

### 4. 分類対象テキストの追加

分類したいテキストを入力として追加します。

	```python
	inputs=["パスワードを変更したいのですが",
	        "私の保険で処方薬はカバーされていますか？"
	        ]
	```

### 5. Classifyエンドポイントの呼び出し

Classifyエンドポイントを呼び出して分類します。モデルのタイプを指定します（デフォルトはlarge）。

	```python
	response = co.classify(
	    model='large',
	    inputs=inputs,
	    examples=examples)
	
	print(response.classifications)
	```

## レスポンスの例

	```json
	{
	  "results": [
	    {
	      "text": "パスワードを変更したいのですが",
	      "prediction": "アカウント設定の変更",
	      "confidence": 0.82,
	      ...
	    },
	    {
	      "text":  "私の保険で処方薬はカバーされていますか？",
	      "prediction": "保険証券の詳細を探す",
	      "confidence": 0.75,
	      ...
	    }
	  ]
	}
	```

以上が、Cohere APIのClassifyエンドポイントの概要と基本的な使い方です。テキスト分類タスクを手軽に実装できる便利な機能といえるでしょう。
```

## script/activate-notebook-forge.bat

```
conda activate notebook-forge
```

## script/activate-notebook-forge.sh

```bash
#!/bin/bash
conda activate notebook-forge
```

