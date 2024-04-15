
import os
import fnmatch

def get_file_tree(repo_path, ignore_patterns, max_depth):
    file_tree = ""
    for root, dirs, files in os.walk(repo_path):
        # .gitignoreに一致するディレクトリを無視
        dirs[:] = [d for d in dirs if not any(fnmatch.fnmatch(d, pattern) for pattern in ignore_patterns)]
        
        level = root.replace(repo_path, "/").count(os.sep)
        # print(f"------------------------- max_depth : {max_depth}")
        # print(f"dirs1:{dirs}")
        # print(f"level:{level}")
        # print(f"files:{files}")
        if level > max_depth:
            continue
        
        indent = " " * 4 * (level)
        file_tree += f"{indent}{os.path.basename(root)}/\n"

        subindent = " " * 4 * (level + 1)
        for f in files:
            # .gitignoreに一致するファイルを無視
            if not any(fnmatch.fnmatch(f, pattern) for pattern in ignore_patterns):
                file_tree += f"{subindent}{f}\n"
    return file_tree

def process_files(repo_path, ignore_patterns, max_depth):
    file_contents = []
    for root, dirs, files in os.walk(repo_path):
        # .gitignoreに一致するディレクトリを無視
        dirs[:] = [d for d in dirs if not any(fnmatch.fnmatch(d, pattern) for pattern in ignore_patterns)]
        
        level = root.replace(repo_path, "/").count(os.sep)
        if level > max_depth:
            continue
        
        for file in files:
            # .gitignoreに一致するファイルを無視
            if not any(fnmatch.fnmatch(file, pattern) for pattern in ignore_patterns):
                file_path = os.path.join(root, file)
                with open(file_path, "r", encoding="utf-8", errors="ignore") as f:
                    content = f.read()
                    file_contents.append((file_path.replace(f'{repo_path}/', ''), content))
    return file_contents

if __name__ == "__main__": 

    repo_path = "tmp/DeepSeek-Math"
    # .gitignoreのパターンを読み込む
    ignore_patterns = []
    if os.path.exists(".CodeLumiaignore"):
        with open(".CodeLumiaignore", "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    ignore_patterns.append(line)
    max_depth = 1
    file_tree = get_file_tree(repo_path, ignore_patterns, max_depth)
    print(file_tree)
