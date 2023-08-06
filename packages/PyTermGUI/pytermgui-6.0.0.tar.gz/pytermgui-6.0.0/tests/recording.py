from random import randint
from argparse import Namespace
from pytermgui import terminal, DensePixelMatrix

with terminal.record() as recording:
    from pytermgui import pretty, tim

    pretty.print(locals())

    width, height = 30, 30
    matrix = DensePixelMatrix(width, height)

    for y in range(matrix.rows):
        for x in range(matrix.columns):
            matrix[y, x] = str(randint(17, 232))
    matrix.build()

    for line in matrix.get_lines():
        terminal.print(line)

    tim.print("[141 @61]Hello[inverse]There")

recording.save_svg("recording", title="DensePixelMatrix stress test")
