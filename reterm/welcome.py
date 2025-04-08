from rich.console import Console
from rich.panel import Panel
from rich.text import Text

console = Console()

def print_welcome():
    ascii_art = Text(r"""
 ___   ___   _____   ___   ___   __ __    __    _ 
| _ \ | __| |_   _| | __| | _ \ |  V  |  /  \  | |
| v / | _|    | |   | _|  | v / | \_/ | | /\ | | |
|_|_\ |___|   |_|   |___| |_|_\ |_| |_| |_||_| |_|
""", style="bold blue")

    subtitle = "[bold green]reTermAI[/bold green] - Smart command assistant for your terminal 🧠💻"

    usage_panel = Panel.fit(
        """[bold white]Available Commands[/bold white]
[cyan]reterm suggest[/cyan]               Get AI-powered command suggestions
[cyan]reterm match [keyword][/cyan]        Search your shell history for similar commands

[bold white]Options[/bold white]
[green]--limit, -l[/green]                Number of history lines to analyze (default: 200)
[green]--provider, -p[/green]             LLM to use (openai or gemini)

[bold white]Examples[/bold white]
[magenta]reterm suggest[/magenta]                         Suggest based on recent history (default 200 lines)
[magenta]reterm suggest -l 300[/magenta]                 Analyze last 300 commands
[magenta]reterm suggest -p gemini[/magenta]              Use Gemini LLM for suggestions
[magenta]reterm match docker[/magenta]                   Find all past commands related to "docker"
[magenta]reterm match build -l 10[/magenta]              Show last 10 commands matching "build"

[i]Tip: Type 0 to cancel command execution when prompted[/i]""",
        title="📘 reTermAI Help",
        border_style="bright_blue"
    )

    console.print(ascii_art)
    console.print(subtitle, justify="center")
    console.print(usage_panel)
