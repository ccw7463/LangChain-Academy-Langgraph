
# Langgraph

<img src="./public/langgraph.png" alt="made by DALL-E" width="600">


## About The Project

This project provides an opportunity to implement and explore features based on Langgraph. By experimenting with the code, you can develop functionalities tailored to your needs and better understand the capabilities of Langgraph.

For more details, please visit the [Langgraph official documentation](https://www.langchain.com/langgraph) or refer to the `langchain-academy` folder in the project repository.

**Note:** All prompts and test sentences in this project are in Korean.

## Project Structure

The repository is organized as follows:

- `public/` : Contains images used in the README or other documentation.
- `modules/` : Includes various libraries for testing Langgraph functionalities.
- `notebooks/` : Contains Jupyter Notebook files for testing, organized with step-by-step numbering.
- `utils/` : Defines decorators for setting up environment variables and checking the state during graph execution.
- `chat_test.py` : Simple chat test for Langgraph.
- `tool_test.py` : Simple tool test for Langgraph.

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

## Quick Start

You can simply Langgraph test by running the following command.

- type 1) simple chat test : collect user information

    ```bash
    poetry run python chat_test.py
    ```

    ![chat_test](./public/chat_test.png)

- type 2) tool test : perform arithmetic operations

    ```bash
    poetry run python tool_test.py
    ```

    ![tool_test](./public/tool_test.png)
