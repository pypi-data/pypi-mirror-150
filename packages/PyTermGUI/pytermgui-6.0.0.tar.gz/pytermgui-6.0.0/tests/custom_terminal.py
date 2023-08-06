import pytermgui as ptg


class CustomTerminal(ptg.Terminal):
    def print(*args, **kwargs):
        super().print("\x1b[31m", *args, **kwargs)


ptg.set_global_terminal(CustomTerminal())

ptg.tim.print("hello")
