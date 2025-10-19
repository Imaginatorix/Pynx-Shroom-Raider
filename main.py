#import level size and origloc
#Level Map Data
mapSize=(30,30) #added
origLoc=(0,0) #added
mushrooms={(3,3),(4,4)} #added
collectedMush=set() #added
trees=((2,2),(5,5))
water=((1,1),)
pavetile=((),)
rocks=((),)
itemsDict={(0,0):"Axe",(1,1):"Flamethrower"} #added
currentLoc=origLoc
currentItem="none"


def userInput(maxRange,prevLoc,item,mush):
    command=tuple(ch for ch in tuple(input("What will you do? ").upper()) if ch !=" ")
    possibleInputs={"W":(0,-1),"A":(-1,0),"S":(0,1),"D":(1,0),"!":None, "P":None,"E":None}
    colMush=set()
    if not command:
        return
    if all(x in possibleInputs for x in set(command)):
        output=[]
        for action in command:
            if action=="E":
                output.append("End")
            elif action=="!":
                prevLoc=(0,0)
                output.append(prevLoc)
                item=""
            elif action=="P":
                if prevLoc not in itemsDict:
                    return 
                if item:
                    ...#drop current item
                item=itemsDict[prevLoc]
            else:
                x,y=prevLoc
                i,j=possibleInputs[action]
                if 0<=x+i<=maxRange[0] and 0<=y+j<=maxRange[1]:
                    prevLoc=(x+i,y+j)
                    output.append(prevLoc)
                    if prevLoc in mush:
                        mush.remove(prevLoc)
                        colMush.add(prevLoc)
        return [output,item,colMush]
    else:
        return 

while True:
    inp=userInput(mapSize,currentLoc,currentItem,mushrooms)
    if inp==None:
        print("Invalid input. Try again.")
    elif "End" in inp[0]:
        print("Test end")
        break
    else:
        if inp[0]==[]:
            inp[0]=[currentLoc,]
        print(inp)#pass to ui
        currentLoc=inp[0][-1]
        currentItem=inp[1]
        collectedMush|=inp[2]
        mushrooms-=inp[2]
        print(f"""
        location: {currentLoc}
        item: {currentItem}
        collected: {collectedMush}
        remaining: {mushrooms}""")
    if not mushrooms:
        print("Level done !")
        break

#to be added: item and environment interactions



#added better input logic and tested edge cases
#added temporary exit 
#added mushroom logic