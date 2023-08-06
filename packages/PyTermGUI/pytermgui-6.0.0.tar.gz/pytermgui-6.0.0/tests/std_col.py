from pytermgui import tim, terminal

with terminal.record() as recording:
    for i in range(16):
        tim.print(f"[{i}]Fore[inverse]Back")

recording.save_html("std_col.html")
