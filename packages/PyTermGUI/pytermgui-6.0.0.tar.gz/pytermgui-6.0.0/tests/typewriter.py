from pytermgui import terminal, getch, keys, tim

tim.print("[green bold]Start typing...")
tim.print("[dim]> Press CTRL_D to exit.")
tim.print()
with terminal.record() as recording:
    key = None

    while True:
        key = getch(interrupts=False)
        if key in [keys.CTRL_D, keys.CTRL_C]:
            break

        terminal.write(key)
        terminal.flush()

tim.print("[yellow bold]Your recording:")
terminal.replay(recording)
