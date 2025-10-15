#import level size and origloc
#Level Data
mapSize=(30,30)
origLoc=(0,0)
currentLoc=origLoc

def userInput(maxRange,prevLoc):
    command=tuple(input("What will you do? ").upper())
    possibleInputs={"W":(0,-1),"A":(-1,0),"S":(0,1),"D":(1,0),"!":"!"}
    if all(x in possibleInputs for x in set(command)):
        output=[]
        for action in command:
            if action=="!":
                output.append("!") 
                return output
            x,y=prevLoc
            i,j=possibleInputs[action]
            if 0<=x+i<=maxRange[0] and 0<=y+j<=maxRange[1]:
                prevLoc=(x+i,y+j)
                output.append(prevLoc)
        return output
    else:
        return "Invalid input. Try again."

while True:
    inp=userInput(mapSize,currentLoc)
    if "!" in inp:
        print(inp[:-1])
        currentloc = origLoc
        print("Level has been reset.")
    elif inp=="Invalid input. Try again.":
        print("Invalid input. Try again.")
    elif inp==[]:
        print([currentLoc,])
    else:
        print(inp)
        currentloc=inp[-1]

