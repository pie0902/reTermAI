# reTermAI

💡 A terminal command recommender powered by AI and your own shell history.

---

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

### Suggest AI-powered command recommendations:

```bash
reterm suggest
```

Options:

- `--limit, -l` — number of recent commands to analyze (default: 200)
- `--provider, -p` — choose from `"openai"` or `"gemini"`

---

### Match commands by keyword:

```bash
reterm match docker
```

Options:

- `--limit, -l` — max results to display (default: 5)

---

## 🔐 Configuration

Create a `.env` file in your project or home directory:

```env
OPENAI_API_KEY=sk-xxxxxxxxxxxxxxxxxxxxx
GOOGLE_API_KEY=your-gemini-api-key
```

A `.env.example` is also included for reference.

---

## 📂 Project Structure

```bash
reterm/
├── cli.py          # Main CLI interface
├── llm.py          # LLM integration (OpenAI, Gemini)
├── shell.py        # Shell history detection and parsing
├── config.py       # API key loader
```

---

## 🧑‍💻 Contributing

We welcome contributions! Fork the repo, create a feature branch, and open a pull request.

```bash
git checkout -b feat/your-feature
```

Feel free to open issues or suggest enhancements!

---

## 📄 License

Apache License 2.0
