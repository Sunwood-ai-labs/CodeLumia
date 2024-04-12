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