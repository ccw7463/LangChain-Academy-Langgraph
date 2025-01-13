
# Langchain Academy - Langgraph

## Getting Started


### Installation
_Using `poetry` for Python project dependency management and package distribution._

1. Download the poetry tool
```bash
curl -sSL https://install.python-poetry.org | python3.11 -
```

2. Add poetry to the PATH environment variable.
```bash
export PATH="$HOME/.local/bin:$PATH"
```

3. Verify that poetry is installed and recognized correctly.
```bash
poetry --version
```

4. Configure a virtual environment for each project.
```bash
poetry config virtualenvs.in-project true
```

5. Install dependencies

```bash
poetry install
```