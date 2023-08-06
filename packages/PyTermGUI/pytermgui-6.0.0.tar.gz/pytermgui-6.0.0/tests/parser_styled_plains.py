from pytermgui import tim, pretty

text = tim.parse("[141 bold]Hello [italic dim]There [yellow /bold /italic /fg]!")
for styled in tim.get_styled_plains(text):
    print(styled + "\x1b[0m")
