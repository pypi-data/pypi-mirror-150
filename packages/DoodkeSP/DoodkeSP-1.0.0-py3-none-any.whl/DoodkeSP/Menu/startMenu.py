from turtle import *
#from printTextMenu import *
from firebase import firebase


auth = firebase.FirebaseAuthentication('vs5o1lxVx5KvCdNc2BX0qpZfuJq4Ulnz3Q0Zs45f', 'schooldavid69420@gmail.com', extra={'id': 123})
firebase = firebase.FirebaseApplication('https://schoolproject-amen-default-rtdb.firebaseio.com', authentication=auth)


Menu = Screen()
Menu.screensize(500,500)

color = firebase.get('/Settings/backRoundColor', '')

Menu.bgcolor(f"{color}")

from printTextMenu import *

pensize(9)

def printMenu():

    up()
    goto(-50, 100)
    down()

    goto(100, 100)
    goto(100, 50)
    goto(-50, 50)
    goto(-50, 100)

    up()
    goto(-50, 0)
    down()

    goto(100, 0)
    goto(100, -50)
    goto(-50, -50)
    goto(-50, 0)

printMenu()



#pensize(9)
#
#up()
#goto(-245, 0)
#down()
#goto(238, 0)
#
#def checkPos(x, y):
#    print(f"X: {x}, Y: {y}")
#
#
#onscreenclick(checkPos)

mainloop()


