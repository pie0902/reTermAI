import typer
from typer import Exit
import logging
import os
import sys
import subprocess
from reterm.welcome import print_welcome
from reterm.shell import get_recent_history
from reterm.llm import get_llm
from reterm.config import load_api_key

# Suppress gRPC and Google SDK logs
os.environ['GRPC_VERBOSITY'] = 'NONE'
log_level = logging.ERROR
logging.getLogger('grpc').setLevel(log_level)
logging.getLogger('google.api_core').setLevel(log_level)
logging.getLogger('google.auth').setLevel(log_level)

app = typer.Typer(
    help="Reterm AI: Get AI-powered suggestions based on your command history.",
    add_completion=False
)

CONFIG_PATH = os.path.expanduser("~/.reterm_config")

# 웰컴 메시지 초기 실행 로직을 별도 함수로 분리
def check_and_show_welcome():
    """최초 실행 시 웰컴 메시지를 보여주고 설정 파일을 생성."""
    if not os.path.exists(CONFIG_PATH):
        print_welcome()
        with open(CONFIG_PATH, "w") as f:
            f.write("welcome_shown=true\n")

@app.command("welcome")
def show_welcome():
    """Show the welcome banner manually."""
    print_welcome()

@app.command()
def suggest(
    history_limit: int = typer.Option(
        300,
        "--history-limit",
        "-hl",
        help="How many recent commands to read from history.",
        min=1,
    ),
    context_limit: int = typer.Option(
        20,
        "--context-limit",
        "-cl",
        "-l",
        help="How many of those commands to feed into the LLM.",
        min=1,
    ),
    provider: str = typer.Option(
        "gemini",
        "--provider",
        "-p",
        help="LLM provider to use (e.g., 'openai', 'gemini')."
    )
):
    """Analyze your shell history and get AI-based command suggestions."""
    check_and_show_welcome()  # 모든 명령어 실행 전 웰컴 확인
    try:
        api_key = load_api_key(provider)
        if not api_key:
            typer.echo(f"❌ Error: API key for provider '{provider}' not found or is empty.", err=True)
            typer.echo("👉 Please check your .env file or environment variables.", err=True)
            typer.echo("🧩 Tip: You can choose the provider using '--provider gemini' or '--provider openai'", err=True)
            raise Exit(code=1)

        full_history = get_recent_history(limit=history_limit)
        if not full_history:
            typer.echo("✅ No command history found.", err=True)
            raise Exit(code=0)

        history_for_llm = full_history[-context_limit:]
        llm = get_llm(provider, api_key)

        typer.echo(f"⏳ Analyzing {len(history_for_llm)} commands using {provider}...", err=True)
        suggestions = llm.suggest(history_for_llm)

        filtered_suggestions = []
        if suggestions:
            for cmd in suggestions:
                if (cmd and isinstance(cmd, str) and " " in cmd.strip() and
                        not cmd.lower().strip().startswith(("there are no", "i cannot")) and
                        len(cmd.strip().split()) > 1):
                    filtered_suggestions.append(cmd.strip())

        if not filtered_suggestions:
            typer.echo("✅ No suitable suggestions found.", err=True)
            raise Exit(code=0)

        typer.echo("\n💡 Suggested commands:", err=True)
        for i, cmd in enumerate(filtered_suggestions, 1):
            typer.echo(f"{i}. {cmd}", err=True)

        try:
            choice_str = typer.prompt("\nEnter the number of the command to run (or 0 to cancel)")
            choice = int(choice_str)
        except ValueError:
            typer.echo("⚠️ Invalid input. Please enter a number.", err=True)
            raise Exit(code=1)

        if choice == 0:
            typer.echo("❌ Cancelled.", err=True)
            raise Exit(code=0)
        elif 1 <= choice <= len(filtered_suggestions):
            cmd_to_run = filtered_suggestions[choice - 1]
            typer.echo(f"\n🚀 Running: {cmd_to_run}\n", err=True)

            user_shell = os.environ.get("SHELL") or "/bin/sh"
            try:
                subprocess.run(
                    cmd_to_run,
                    shell=True,
                    check=True,
                    executable=user_shell,
                )
                raise Exit(code=0)
            except subprocess.CalledProcessError as cpe:
                typer.echo(f"⚠️ Command failed with exit code {cpe.returncode}.", err=True)
                raise Exit(code=cpe.returncode)
            except FileNotFoundError:
                typer.echo(f"⚠️ Command not found: maybe '{cmd_to_run.split()[0]}' is not in your PATH.", err=True)
                raise Exit(code=127)
        else:
            typer.echo("⚠️ Invalid selection number.", err=True)
            raise Exit(code=1)

    except Exit as e:
        raise e
    except FileNotFoundError as fnf_err:
        typer.echo(f"❌ Error: File not found - {fnf_err}", err=True)
        raise Exit(code=1)
    except NotImplementedError as ni_err:
        typer.echo(f"❌ Error: {ni_err}", err=True)
        raise Exit(code=1)
    except Exception as e:
        typer.echo(f"\n❌ Unexpected error: {e}", err=True)
        raise Exit(code=1)

@app.command()
def match(
    query: str = typer.Argument(..., help="Keyword or partial command to search in history."),
    limit: int = typer.Option(5, "--limit", "-l", help="Maximum number of matching commands to display.")
):
    """Search your full command history for matches to the given keyword or phrase."""
    check_and_show_welcome()  # 모든 명령어 실행 전 웰컴 확인
    try:
        history = get_recent_history(limit=None)
        matches = [cmd for cmd in history if query.lower() in cmd.lower()]

        if not matches:
            typer.echo(f"😕 No commands found matching: '{query}'", err=True)
            raise Exit()

        typer.echo(f"\n🔍 Commands related to '{query}':", err=True)
        for i, cmd in enumerate(matches[-limit:], 1):
            typer.echo(f"{i}. {cmd}", err=True)

        choice_str = typer.prompt("\nEnter the number of the command to run (or 0 to cancel)")
        choice = int(choice_str)

        if choice == 0:
            typer.echo("❌ Cancelled.", err=True)
            raise Exit(code=0)
        elif 1 <= choice <= len(matches):
            cmd_to_run = matches[-limit:][choice - 1]
            typer.echo(f"\n🚀 Running: {cmd_to_run}\n", err=True)
            subprocess.run(cmd_to_run, shell=True)
            raise Exit(code=0)
        else:
            typer.echo("⚠️ Invalid selection.", err=True)
            raise Exit(code=1)

    except Exit:
        raise
    except Exception as e:
        typer.echo(f"❌ Error: {e}", err=True)
        raise Exit(code=1)

if __name__ == "__main__":
    app()