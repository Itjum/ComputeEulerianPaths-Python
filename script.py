#!/usr/bin/python

from pratique.pratique import deneigeuse, drone
import sys

if (len(sys.argv) == 2):
    if (sys.argv[1] == "--deneigeuse"):
        print("Veuillez entrer le nombre de deneigeuse que vous souhaitez")
    elif (sys.argv[1] == "--drone"):
        drone('Montréal,Canada')
    else:
        print("Veuillez entrer des arguments valides")

elif (len(sys.argv) == 3):
    if (sys.argv[2] == "--deneigeuse" and sys.argv[1].isnumeric()):
        deneigeuse(int(sys.argv[1]))
    elif (sys.argv[1] == "--deneigeuse" and sys.argv[2].isnumeric()):
        deneigeuse(int(sys.argv[2]))

    elif (sys.argv[1] == "--drone"):
        drone(sys.argv[2])
    elif (sys.argv[2] == "--drone"):
        drone(sys.argv[1])
    else:
        print("Veuillez entrer des arguments valides")
else :
        print("Veuillez entrer un nombre d'argument valide")
