```
 ___   ___   _____   ___   ___   __ __    __    _
| _ \ | __| |_   _| | __| | _ \ |  V  |  /  \  | |
| v / | _|    | |   | _|  | v / | \_/ | | /\ | | |
|_|_\ |___|   |_|   |___| |_|_\ |_| |_| |_||_| |_|

[reTermAI] Smart command assistant for your terminal 🧠💻
```

---

![Image](https://github.com/user-attachments/assets/0de4a2b5-2167-4fe0-bc6c-764cc76ff435)

# reTermAI

💡 A terminal command recommender powered by AI and your own shell history.

## Demo GIF

## ![demo](docs/demo.gif)

## ✨ Features

- 🔍 Recommends relevant terminal commands based on your past history using OpenAI or Gemini
- 🧠 Supports intelligent matching by keyword or partial input
- ⚡ Easy to install via pip
- 🐚 Supports `zsh` and `bash` shell history
- 🔐 API keys managed via `.env`

---

## 📦 Installation

```bash
pip install reterm-ai
```

> Or, for local development:

```bash
git clone https://github.com/pie0902/reTermAI.git
cd reTermAI
pip install -e .
```

---

## ⚙️ Usage

### 🔮 AI-powered command suggestions:

```bash
reterm suggest
```

Options:

| Option                 | Description                                          |
| ---------------------- | ---------------------------------------------------- |
| `--history-limit, -hl` | Number of recent commands to read (default: 300)     |
| `--context-limit, -cl` | How many commands to feed into the LLM (default: 20) |
| `--provider, -p`       | LLM to use (`openai` or `gemini`)                    |

Examples:

```bash
reterm suggest -p gemini

reterm suggest --history-limit 500 --context-limit 30
# Basic suggestion
reterm suggest

# Suggest using Gemini and 50 recent commands
reterm suggest -hl 50 -p gemini

# Suggest using OpenAI and 30 context commands
reterm suggest --provider openai --context-limit 30

# Search for past docker commands
reterm match docker

# Show up to 10 matching commands
reterm match docker -l 10

```

---

### 🔎 Match past commands by keyword:

```bash
reterm match docker
```

Options:

| Option        | Description                                         |
| ------------- | --------------------------------------------------- |
| `--limit, -l` | Max number of matching results to show (default: 5) |

---

## 🔐 Configuration

Add a `.env` file in your home or project directory:

```env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxx
GOOGLE_API_KEY=your-gemini-api-key
```

| Key              | Used for                              |
| ---------------- | ------------------------------------- |
| `OPENAI_API_KEY` | Required if using `--provider openai` |
| `GOOGLE_API_KEY` | Required if using `--provider gemini` |

You can also refer to the included `.env.example`.

---

## 📂 Project Structure

```bash
reterm/
├── cli.py          # Main CLI interface
├── llm.py          # LLM integration (OpenAI, Gemini)
├── shell.py        # Shell history detection and parsing
├── config.py       # API key loader
├── welcome.py      # ASCII and help panel
```

---

## 🧑‍💻 Contributing

We welcome contributions! Fork the repo, create a feature branch, and open a pull request.

```bash
git checkout -b feat/your-feature
```

Optional ideas:

- Add support for `fish` shell
- Add model options (e.g. `gpt-4o`, `gemini-pro`)
- Improve LLM prompt formatting

---

## 📄 License

Apache License 2.0
