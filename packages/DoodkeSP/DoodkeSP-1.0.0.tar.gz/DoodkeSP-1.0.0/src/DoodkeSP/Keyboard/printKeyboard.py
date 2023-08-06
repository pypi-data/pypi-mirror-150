from turtle import *

Keyboard = Screen()
Keyboard.setup(1600,500)

pensize(9)

speed(0)

up()
goto(100, 0)
down()

goto(550, 0)
goto(550, -150)
goto(100, -150)
goto(100, 0)
goto(100,-50)
goto(550, -50)
goto(550, -100)
goto(100, -100)
goto(100, -150)

for nice in range(150, 550, 50):

    goto(nice, -150)
    goto(nice, 0)
    goto(nice, -150)

up()
goto(650,-50)
down()
goto(600,-50)
goto(600,-100)
goto(650, -100)
goto(650,-50)

#mainloop()