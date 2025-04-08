# reterm/shell.py

import os
import sys # Required for sys.stderr
from pathlib import Path

def detect_shell() -> str:
    """
    Detect the current shell being used (e.g., zsh or bash).
    Provides a default ('zsh') with a warning to stderr if detection fails.
    """
    shell_path = os.environ.get("SHELL", "")
    if not shell_path:
        # Output warnings to stderr
        print("Warning: SHELL environment variable not set. Assuming zsh history format.", file=sys.stderr)
        return "zsh" # Default assumption

    shell_name = Path(shell_path).name
    if "zsh" in shell_name:
        return "zsh"
    elif "bash" in shell_name:
        return "bash"
    # Add elif for other shells like fish if needed
    else:
        # Output warnings to stderr
        print(f"Warning: Could not reliably detect known shell from '{shell_path}'. Assuming zsh history format.", file=sys.stderr)
        return "zsh" # Default assumption

def get_history_file(shell: str) -> Path:
    """
    Return the path to the history file based on the shell type.
    Considers HISTFILE environment variable for Zsh. Outputs warnings to stderr.
    """
    home = Path.home()
    histfile_path = None

    if shell == "zsh":
        # Check Zsh specific HISTFILE environment variable first
        histfile_env = os.environ.get('HISTFILE')
        if histfile_env:
            # Ensure the path is absolute and expanded (~ handled)
            histfile_path = Path(histfile_env).expanduser()
            if not histfile_path.is_absolute():
                 # Output warnings to stderr
                 print(f"Warning: Zsh HISTFILE ('{histfile_env}') is not absolute. Using default.", file=sys.stderr)
                 histfile_path = None # Fallback to default
        # Default Zsh history file if HISTFILE not set or invalid
        if histfile_path is None:
            histfile_path = home / ".zsh_history"

    elif shell == "bash":
        # Bash might also use HISTFILE, but less commonly configured than zsh
        # Default Bash history file
        histfile_path = home / ".bash_history"

    else:
        # This case should be handled by detect_shell's default,
        # but raise error for unexpected internal state.
        # Errors that stop execution are okay, but informational prints should go to stderr.
        raise ValueError(f"Internal error: Unsupported shell type '{shell}' in get_history_file.")

    return histfile_path
from typing import Optional, List

def get_recent_history(limit: Optional[int] = 200) -> List[str]:
    """
    Read and return the most recent commands from the shell history file.
    If limit is None, return all available history.
    Handles Zsh timestamp format correctly.
    Outputs errors to stderr.
    Returns an empty list if the file is not found or errors occur.
    """
    commands = []
    try:
        shell = detect_shell()
        history_file = get_history_file(shell)

        if not history_file.exists():
            return []

        with open(history_file, "r", encoding="utf-8", errors="ignore") as f:
            lines = f.readlines()

        for line in lines:
            line = line.strip()
            if not line:
                continue

            command = None
            if shell == "zsh" and line.startswith(":") and ";" in line:
                try:
                    parts = line.split(";", 1)
                    if len(parts) > 1:
                        command_part = parts[1].strip()
                        if command_part:
                            command = command_part
                except Exception:
                    pass
            elif not line.startswith(":"):
                command = line

            if command:
                commands.append(command)

    except FileNotFoundError:
        return []
    except Exception as e:
        print(f"Error reading or processing history file {history_file}: {e}", file=sys.stderr)
        return []

    # ✅ 핵심 로직: 전체 반환
    if limit is None or limit <= 0:
        return commands

    return commands[-limit:]


# --- No example usage code below this line ---