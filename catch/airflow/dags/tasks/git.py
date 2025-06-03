def git_clone(repo, branch, clone_dir):
    import os
    import shutil
    import subprocess

    # git clone 빈 디렉토리만 허용 (과거 데이터 지우기)
    if os.path.isdir(clone_dir):
        shutil.rmtree(clone_dir)
    os.makedirs(clone_dir, exist_ok=True)

    cmd = f"git clone --depth 1 --branch {branch} {repo} {clone_dir}"
    print(f">>> git clone cmd: {cmd}")

    res = subprocess.run(cmd.split(), capture_output=True, text=True)
    if res.returncode != 0:
        raise Exception(f"git clone error. {res}")
    else:
        print(f"git clone success")
