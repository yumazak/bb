import subprocess


def get_diff(target: str) -> str:
    result = subprocess.run(
        ["git", "diff", "-w", "--ignore-blank-lines", "-U0", target],
        capture_output=True,
        text=True,
    )
    return result.stdout
