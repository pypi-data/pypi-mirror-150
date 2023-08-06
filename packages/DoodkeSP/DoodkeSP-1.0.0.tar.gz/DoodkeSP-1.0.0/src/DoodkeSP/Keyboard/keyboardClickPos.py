from turtle import *


def checkPos(x,y):
    #print(f"X: {x}; Y: {y}")

    if x>=100 and x<150 and y<0 and y>-50:
        print(1)
    elif x>=100 and x<150 and y<-50 and y>-100:
        print(2)
    elif x>=100 and x<150 and y<-100 and y>-150:
        print(3)
    elif x>=150 and x<200 and y<0 and y>-50:
        print(4)
    elif x>=150 and x<200 and y<-50 and y>-100:
        print(5)
    elif x>=150 and x<200 and y<-100 and y>-150:
        print(6)
    elif x>=200 and x<250 and y<0 and y>-50:
        print(7)
    elif x>=200 and x<250 and y<-50 and y>-100:
        print(8)
    elif x>=200 and x<250 and y<-100 and y>-150:
        print(9)
    elif x>=250 and x<300 and y<0 and y>-50:
        print(10)
    elif x>=250 and x<300 and y<-50 and y>-100:
        print(11)
    elif x>=250 and x<300 and y<-100 and y>-150:
        print(12)
    elif x>=300 and x<350 and y<0 and y>-50:
        print(13)
    elif x>=300 and x<350 and y<-50 and y>-100:
        print(14)
    elif x>=300 and x<350 and y<-100 and y>-150:
        print(15)
    elif x>=350 and x<400 and y<0 and y>-50:
        print(16)
    elif x>=350 and x<400 and y<-50 and y>-100:
        print(17)
    elif x>=350 and x<400 and y<-100 and y>-150:
        print(18)
    elif x>=400 and x<450 and y<0 and y>-50:
        print(19)
    elif x>=400 and x<450 and y<-50 and y>-100:
        print(20)
    elif x>=400 and x<450 and y<-100 and y>-150:
        print(21)
    elif x>=450 and x<500 and y<0 and y>-50:
        print(22)
    elif x>=450 and x<500 and y<-50 and y>-100:
        print(23)
    elif x>=450 and x<500 and y<-100 and y>-150:
        print(24)
    elif x>=500 and x<550 and y<0 and y>-50:
        print(25)
    elif x>=500 and x<550 and y<-50 and y>-100:
        print(26)
    elif x>=500 and x<550 and y<-100 and y>-150:
        print(27)

    elif x>=600 and x<650 and y<-50 and y>-100:
        print(69)

    else:
        print('Error')




#checkPos2()

onscreenclick(checkPos)


