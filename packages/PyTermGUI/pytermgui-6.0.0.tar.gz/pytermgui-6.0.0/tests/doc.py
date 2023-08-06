from pytermgui import terminal, inspect, pretty

with terminal.record() as recording:
    pretty.print(inspect(recording.save_svg))

recording.save_svg("inspect", title="Documentation example")
