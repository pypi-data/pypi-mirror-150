from pytermgui import tim, to_html

with open("htmltest.html", "w") as html:
    print(tim.get_markup(tim.parse("[green]green")))
    html.write(to_html(tim.parse("[141 bold]Hello [italic green]There")))
