from turtle import *


def checkPos(x,y):
    #print(f"X: {x}; Y: {y}")

    if x>=100 and x<150 and y<0 and y>-50:
        print(1)
    elif x>=100 and x<150 and y<-50 and y>-100:
        print(2)
    
    
    else:
        print('Error')




#checkPos2()

onscreenclick(checkPos)


