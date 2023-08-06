from pytermgui import terminal
from rich.syntax import Syntax

syntax = Syntax(
    """\
from pytermgui import terminal, tim

with terminal.record() as recording:
    tim.print("[72 italic]Everything[/italic] will now be recorded!")
    tim.print(locals())
""",
    "python",
)

with terminal.record() as recording:
    terminal.print(syntax)

recording.save_svg("syntax")
