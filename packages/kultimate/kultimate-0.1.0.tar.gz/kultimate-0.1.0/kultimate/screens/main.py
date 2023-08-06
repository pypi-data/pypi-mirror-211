###### Import Textual
from textual.app import ComposeResult
from textual.screen import Screen
from textual.widgets import Footer, Header


class Main(Screen):
    """Main Screen of application"""

    DEFAULT_CSS = """
    Main {
        background: $primary-background-darken-1;
    }
    """
    BINDINGS = [
        ("q", "app.quit", "Quit"),
    ]

    def compose(self) -> ComposeResult:
        yield Header()
        yield Footer()
