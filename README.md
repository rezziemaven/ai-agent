# Noodle: AI Coding Agent

![Noodle Banner](images/banner-yellow.jpg)

Meet **Noodle**, your helpful AI coding agent!

Noodle can perform tasks within a specified working directory, as well as answer general questions. It has access to the following tools:

- List content of files and directories for a given directory
- Read file contents
- Execute Python files with optional arguments
- Write or overwrite files with provided content

The working directory is set in a `config.py` file. The agent does not have access to the working directory for security reasons.

## Features

- Switch between [Ollama](https://github.com/ollama/ollama-python) and [Gemini](https://github.com/googleapis/python-genai) SDKs for the best of both worlds (agent uses Ollama by default)
- Use tools for listing directory contents, reading files, writing files, and executing Python scripts
- Log user prompt, function calls with provided arguments, and token usage in 'verbose' mode
- Set your working directory, add additional SDKs, and configure system prompt, models used, and other settings (see [Configuration](#configuration) for more information)

## Getting started

1. Ensure you have the following installed on your computer:

    1.  `uv`: Python package manager
    2. `python3`: Version 3.14 is required.
    3. `Ollama` GUI and CLI (download [here](https://ollama.com/download))
2. Clone this repository locally.
3. Enter the root of the repository using `cd noodle-ai-agent`.
4. Copy the  `.env.example` file using `cp .env.example .env`, then add your Gemini and (optionally) Ollama API keys (the key is only required if using a cloud model). You can get the Gemini API Key from [Google AI Studio](https://aistudio.google.com/api-keys) and the Ollama API Key from [the Ollama settings page](https://ollama.com/settings/keys) (note: you will need to be logged in first or create a new account).
5. Run `uv run main.py` from the root of the repository to install the packages and set up the virtual environment. If successful, you should see example usage instructions printed to the console.
6. Use the demo calculator project, located in the `demo/` folder, to test out the features of the agent before using it with your own projects. Here are some sample prompts to try out:

    1. "What are the contents of root?"
    2. "What are the contents of the calculator directory?"
    3. "What are the contents of lorem.txt?"
    4. "Write 'wait, this isn\'t lorem' to lorem.txt"
    5. "Create a new file, 'more/morelorem.txt', with some sample lorem ipsum text"
    6. "Create a new README.md file in the calculator folder with the contents '# Calculator'"
    7. "Run the calculator tests file"
    8. "Add a README.md with # Hello World to /tmp" (should result in an error message)
    9. "Run nonexistent.py" (should result in an error message)
    10. Test fixing a bug:
        a. In the `calculator.py` file, change the `precedence` of the `+` operator to '3'.
        b. Run the calculator app with a test calculation, eg.:

        ```bash
        uv run calculator/main.py "3 + 7 * 2"
        ```

        The correct result should be 17, but because we've introduced a bug, it will return 20.
        c. Run Noodle with the prompt "Fix the bug: 3 + 7 * 2 shouldn't be 20" (It should correctly identify the bug and fix the file).

## Usage

```bash
  uv run main.py "<user_prompt>" [-s | --sdk=sdk-name] [--verbose]
```

- **user_prompt**: Message to send to the model
- **-s, --sdk**: Optional argument that when set, uses the SDK chosen. Uses the `ollama` SDK by default. The current acceptable values are:
  - `genai`: Uses the `genai` sdk
- **--verbose**: Optional flag that when set,  returns the response with a verbose output. The verbose flag reports on token usage and function calls with provided arguments.

Example usage:

```bash
  uv run main.py "Why is the sky blue? Respond with two lines max." -s=genai --verbose
```

## Stack

- `python3` (version 3.14 required)
- `uv` (required): package manager
- `ollama` CLI (required)
- `ollama`: Python version of [Ollama](https://github.com/ollama/ollama-python) SDK
- `genai`: Python version of [Google Gemini](https://github.com/googleapis/python-genai) SDK
- `venv`: Project virtual environment

## Configuration

Noodle can be configured in the following ways:

**`config.py`**
The main config file. Here you can modify the models to use with Gemini or Ollama, the system prompt to use (imported from `prompts.py`), the working directory (initially set to `demo/`) and more.

**`prompts.py`**
This file contains two prompts: `test_system_prompt` and `system_prompt`. The system prompt is the base set of instructions given to the model which it should carry out no matter what. To demonstrate how it works, feel free to change the `SYSTEM_PROMPT` variable in `config.py` to `test_symptom_prompt` and see what happens!

As you work, you may need to modify the `system_prompt` over time. It is recommended to make your instructions as explicit as possible to avoid any unintended side effects. You can try using other models like Claude or ChatGPT to assist you with customising your agent as you see fit.

**Adding SDKs**
While Noodle initially features support for both Google Gemini and Ollama, you can add additional SDKs of your choice, such as OpenAI or OpenRouter, albeit manually. If this is necessary, please do the following:

1. Locate the documentation for your chosen SDK to aid in setup.
2. Use one of the existing SDK files in the `sdks/` folder for reference. You may like to duplicate one of the files as a starting point.
3. Add schema or make modifications to each function in the `functions/` folder, again using the existing schema/ functions there for reference.
4. Import the sdk file into `main.py`, then add the sdk name to the `available_sdks` list and call the function in the `generate_response` function.

## License

This project uses the [MIT license](/LICENSE.md).
