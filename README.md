# Command Queue App

A simple TUI application built with Textual for managing and executing shell commands sequentially.

## Features

- **Interactive TUI:** Uses the Textual framework for a rich terminal interface.
- **Command Input:** Enter shell commands to add them to the execution queue.
- **Command Queue:** View the list of commands waiting to be executed.
- **Output Log:** See the real-time output (stdout, stderr) and exit status of executed commands.
- **Sequential Execution:** Commands are run one after another in the order they were added.

## Installation

1.  **Clone the repository (or ensure you have the source code).**
2.  **Navigate to the project directory:**
    ```bash
    cd /path/to/cq
    ```
3.  **Install using pip:**
    ```bash
    pip install .
    ```
    This will install the application and its dependencies (`textual`, `rich`).

## Usage

After installation, you can run the application from your terminal:

```bash
cq
```

This will launch the TUI. Enter commands in the input field at the bottom right and press Enter to add them to the queue. The application will automatically execute the commands sequentially.

Press `Ctrl+C` or `q` to quit.

## Dependencies

- Python 3.7+
- [Textual](https://github.com/Textualize/textual)
- [Rich](https://github.com/Textualize/rich)
