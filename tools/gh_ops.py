"""GitHub CLI operations for ml-lab."""
import subprocess
import sys


def run(cmd: list[str], check=True):
    print(f"$ {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.stdout:
        print(result.stdout)
    if result.stderr:
        print(result.stderr, file=sys.stderr)
    if check and result.returncode != 0:
        sys.exit(result.returncode)
    return result


def auth_status():
    run(["gh", "auth", "status"])


def repo_list():
    run(["gh", "repo", "list", "--limit", "50"])


def pr_create(title: str, body: str = ""):
    cmd = ["gh", "pr", "create", "--title", title]
    if body:
        cmd += ["--body", body]
    run(cmd)


def pr_list():
    run(["gh", "pr", "list"])


def issue_create(title: str, body: str = ""):
    cmd = ["gh", "issue", "create", "--title", title]
    if body:
        cmd += ["--body", body]
    run(cmd)


def issue_list():
    run(["gh", "issue", "list"])


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    args = sys.argv[2:]

    match cmd:
        case "status":
            auth_status()
        case "repos":
            repo_list()
        case "pr":
            if len(args) >= 1 and args[0] == "create":
                pr_create(args[1], args[2] if len(args) > 2 else "")
            else:
                pr_list()
        case "issue":
            if len(args) >= 1 and args[0] == "create":
                issue_create(args[1], args[2] if len(args) > 2 else "")
            else:
                issue_list()
        case _:
            print(f"Unknown: {cmd}. Try: status, repos, pr, issue")
