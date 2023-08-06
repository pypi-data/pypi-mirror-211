######## Textual imports ######
from textual.app import App

from .screens import Main


###### Main Class ########
class KULTIMATE(App):
    """The main app class"""

    TITLE = "KUltimate"
    SUB_TITLE = "Using Kanban with Markdown"
    SCREENS = {"main": Main}

    def on_mount(self) -> None:
        """Mount Main screen"""
        self.push_screen("main")


def main() -> None:
    KULTIMATE().run()
