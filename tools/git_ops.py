"""Git operations for ml-lab."""
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


def status():
    run(["git", "status", "--short"])


def commit(message: str):
    run(["git", "add", "."])
    run(["git", "commit", "-m", message])


def push():
    run(["git", "push"])


def pull():
    run(["git", "pull"])


def branch(name: str):
    run(["git", "checkout", "-b", name])


def merge(name: str):
    run(["git", "checkout", "main"])
    run(["git", "merge", name, "--squash"])
    run(["git", "commit", "-m", f"merge: {name}"])
    run(["git", "branch", "-d", name])


def log(n: int = 10):
    run(["git", "log", "--oneline", "--graph", f"-{n}"])


def undo_last_commit():
    run(["git", "reset", "--soft", "HEAD~1"])


if __name__ == "__main__":
    cmd = sys.argv[1] if len(sys.argv) > 1 else "status"
    args = sys.argv[2:]

    match cmd:
        case "status":
            status()
        case "commit":
            commit(args[0] if args else "update")
        case "push":
            push()
        case "pull":
            pull()
        case "branch":
            branch(args[0])
        case "merge":
            merge(args[0])
        case "log":
            log(int(args[0]) if args else 10)
        case "undo":
            undo_last_commit()
        case _:
            print(f"Unknown: {cmd}. Try: status, commit, push, pull, branch, merge, log, undo")
