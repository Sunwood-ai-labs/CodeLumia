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