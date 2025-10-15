#import level size and origloc
#Level Map Data
mapSize=(30,30)
origLoc=(0,0)
mushrooms=((3,3),(4,4))
trees=((2,2),(5,5))
water=((1,1),)
pavetile=((),)
rocks=((),)
itemsDict={(0,0):"Axe",(1,1):"Flamethrower"}
currentLoc=origLoc
currentItem="none"


def userInput(maxRange,prevLoc,item):
    command=tuple(input("What will you do? ").upper())
    possibleInputs={"W":(0,-1),"A":(-1,0),"S":(0,1),"D":(1,0),"!":"!", "P":""}
    if all(x in possibleInputs for x in set(command)):
        output=[]
        for action in command:
            if action=="!":
                output.append("!") 
                return (output,item)
            elif action=="P":
                if prevLoc not in itemsDict:
                    return "Invalid input. Try again."
                if item:
                    ...#drop current item
                item=itemsDict[prevLoc]
            else:
                x,y=prevLoc
                i,j=possibleInputs[action]
                if 0<=x+i<=maxRange[0] and 0<=y+j<=maxRange[1]:
                    prevLoc=(x+i,y+j)
                    output.append(prevLoc)
        return (output,item)
    else:
        return "Invalid input. Try again."

while True:
    inp=userInput(mapSize,currentLoc,currentItem)
    if "!" in inp[0]:
        print(inp[0][:-1])#pass to ui
        currentLoc = origLoc
        currentItem="none"
        print("Level has been reset.")
    elif inp=="Invalid input. Try again.":
        print("Invalid input. Try again.")
    elif inp[0]==[]:
        currentItem=inp[1]
        print(([currentLoc,],currentItem))#pass to ui
    else:
        print(inp)#pass to ui
        print("here")
        currentLoc=inp[0][-1]
        currentItem=inp[1]

#add mushroom states if all collected, done
#item interactions
#endgame