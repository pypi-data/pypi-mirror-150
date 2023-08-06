import pytermgui as ptg

with ptg.WindowManager() as manager:
    for _ in range(100):
        manager.add(ptg.Window(ptg.ColorPicker()))
