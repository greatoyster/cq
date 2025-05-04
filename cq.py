# command_queue.py
import asyncio
from collections import deque
import shlex
from pathlib import Path
from textual.app import App, ComposeResult
from textual.containers import Container
from textual.widgets import Header, Footer, Log, ListView, ListItem, Label, Static, Input
from textual.message import Message
from textual.reactive import reactive

# CSS content embedded directly
CSS_CONTENT = """
/* command_queue.css */
Screen {
    layout: grid;
    grid-size: 2 1;
    grid-gutter: 0 0;
    /* height: 100%; */
}

#left-pane {
    column-span: 1;
    border: round $accent;
}

#right-pane {
    column-span: 1;
    border: round $accent;
    display: block; /* Ensure children stack vertically */
}

Log {
    height: 1fr;
    border-bottom: dashed $accent;
}

#queue-list {
    height: 2fr; /* Takes up remaining space */
    border-bottom: hidden $accent;
}

#command-input {
    height: 1fr; /* Fixed height for the input */
    border: none;
    border-top: thick $accent; /* Add border only at the top */
}
"""

class CommandExecutor(Static):
    """A non-visual widget to manage and execute commands."""

    command_queue = reactive(deque())
    is_running = reactive(False)

    class CommandFinished(Message):
        """Posted when a command finishes execution."""
        def __init__(self, stdout: str, stderr: str, return_code: int, command: str) -> None:
            self.stdout = stdout
            self.stderr = stderr
            self.return_code = return_code
            self.command = command
            super().__init__()

    class QueueUpdated(Message):
        """Posted when the queue is modified."""
        pass

    def add_command(self, command: str):
        """Add a command to the queue."""
        new_queue = self.command_queue.copy()
        new_queue.append(command)
        self.command_queue = new_queue
        self.post_message(self.QueueUpdated())
        self.set_timer(0.1, self.run_next_command) # Try to run immediately if idle

    async def run_command(self, command: str):
        """Execute a single command."""
        self.is_running = True
        log_widget = self.app.query_one(Log)
        log_widget.write_line(f"$ {command}")
        try:
            # Use asyncio.create_subprocess_shell for shell execution
            process = await asyncio.create_subprocess_shell(
                command,
                stdout=asyncio.subprocess.PIPE,
                stderr=asyncio.subprocess.PIPE
            )
            stdout, stderr = await process.communicate()
            stdout_str = stdout.decode().strip()
            stderr_str = stderr.decode().strip()
            return_code = process.returncode

            if stdout_str:
                log_widget.write_line(stdout_str)
            if stderr_str:
                log_widget.write_line(f"Error: {stderr_str}")
            log_widget.write_line(f"[Command '{command}' finished with code {return_code}]")

            self.post_message(self.CommandFinished(stdout_str, stderr_str, return_code, command))

        except Exception as e:
            log_widget.write_line(f"Execution Error for '{command}': {e}")
            self.post_message(self.CommandFinished("", str(e), -1, command))
        finally:
            self.is_running = False
            # Remove the completed command from the reactive queue
            new_queue = self.command_queue.copy()
            if new_queue and new_queue[0] == command:
                new_queue.popleft()
                self.command_queue = new_queue
            self.post_message(self.QueueUpdated())
            self.set_timer(0.1, self.run_next_command) # Try to run the next one

    def run_next_command(self):
        """Run the next command in the queue if available and not already running."""
        if self.command_queue and not self.is_running:
            command_to_run = self.command_queue[0] # Peek, don't pop yet
            asyncio.create_task(self.run_command(command_to_run))

class CommandQueueApp(App):
    """A Textual app with a terminal view and command queue."""

    # Use the embedded CSS content
    CSS = CSS_CONTENT
    BINDINGS = [("q", "quit", "Quit")]

    def compose(self) -> ComposeResult:
        self.executor = CommandExecutor(id="executor") # Add the executor
        yield Header()
        # Yield panes directly to the Screen grid
        yield Log(highlight=True, id="left-pane")
        yield Container(
             Label("Command Queue"),
             ListView(id="queue-list"),
             Input(placeholder="Enter command and press Enter", id="command-input"),
             id="right-pane"
        )
        yield self.executor # Add it to the DOM (though it's not visible)


    def on_mount(self) -> None:
        """Called when the app is mounted."""
        self.query_one(Input).focus()
        self.update_queue_display() # Initial display

    async def on_input_submitted(self, event: Input.Submitted) -> None:
        """Handle submission from the input widget."""
        command = event.value
        input_widget = event.control
        if command:
            self.executor.add_command(command)
            input_widget.clear()

    def on_command_executor_queue_updated(self, event: CommandExecutor.QueueUpdated) -> None:
        """Update the list view when the queue changes."""
        self.update_queue_display()

    def update_queue_display(self):
        """Refresh the ListView based on the current command queue."""
        list_view = self.query_one("#queue-list", ListView)
        list_view.clear() # Clear existing items
        for command in self.executor.command_queue:
             # Display command; could add more details later if needed
            list_view.append(ListItem(Label(f"- {command}")))


def main():
    """Runs the CommandQueueApp."""
    app = CommandQueueApp()
    app.run()

if __name__ == "__main__":
    main()