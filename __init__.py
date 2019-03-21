from flask import Flask, render_template
from random import randint,choice
from math import floor
import threading
import time

referenceGrid = []
openFeilds = []
flagedFeilds = []
knowledgeBaseList = {}
updatedGrid = []

'''app = Flask(__name__)

@app.route("/")
@app.route("/home")
def home():
    return render_template('index.html')

@app.route("/test")
def test():grid[row - 1][col - 1].weight += 1
    return ("Success")

if __name__ == '__main__':
    app.run(debug=True) '''


#every element of the grid template:
class gridElement:
    def __init__(self):
        self.location = ()
        self.bomb = False
        self.weight = 0
        self.flag = False
        self.open = False

#just a setup of the grid and bombs:
def mine(dim) :
    grid = makeGrid(dim)
    gridWithBombs = setBombs(grid,dim)

    global referenceGrid
    referenceGrid = setWeights(gridWithBombs,dim)

    for i in range(dim):
        list = []
        for j in range(dim):
            list.append(referenceGrid[i][j].weight)
        print(list)

    mazeSolver(dim)


def mazeSolver(dim):

    global updatedGrid
    updatedGrid = makeGrid(dim)
    global openFeilds
    point = randomStart(dim)
    print("First move "+ str(point))
    while (len(openFeilds) < (dim*dim)):

        row = point[0]
        col = point[1]

        if(referenceGrid[row][col].bomb == False):
            if(referenceGrid[row][col].weight == 0):
                updatedGrid[row][col].open = True
                openFeilds.append((row,col))
                neighbour = neighbours(point,dim)

                for temp in neighbour:
                    openFeilds.append(temp)

                for temp in neighbour:
                    if (referenceGrid[temp[0]][temp[1]].weight == 0):
                        tempNeighbour = neighbours(temp,dim)
                        for tempTemp in tempNeighbour:
                            neighbour.append(tempTemp)
                            openFeilds.append(tempTemp)
                #print(openFeilds)

            else:
                updatedGrid[row][col].open = True
                openFeilds.append((row,col))
        else:
            print("Dead")
            return

        #printing updated maze
        for x in openFeilds:
            updatedGrid[x[0]][x[1]].weight = referenceGrid[x[0]][x[1]].weight
            updatedGrid[x[0]][x[1]].open = True

        #printing the maze
        printGrid(updatedGrid,dim)

        threading.Thread(target=mazeSolver(dim))
        threading.Thread(target=knowledgeBase(dim))

        point = knowledgeBase(dim)

        print("printing updated maze:")

        printGrid(updatedGrid,dim)

        if not point:
            print("Printing updated grid")
            for i in range(dim):
                for j in range(dim):
                    if (i,j) not in openFeilds:
                        openFeilds.append((i,j))
                        updatedGrid[i][j].open = True
            printGrid(updatedGrid,dim)
            print("you won!")
            return
        print("Next movie to: " + str(point))

    print(openFeilds)
    for i in range(dim):
        for j in range(dim):
            if (i, j) not in openFeilds:
                openFeilds.append((i, j))
                updatedGrid[i][j].open=True
    printGrid(updatedGrid, dim)
    print("you won!")



def knowledgeBase(dim):

    global knowledgeBaseList
    global flagCount
    global flagedFeilds

    #initializing the knowledge base
    if not knowledgeBaseList:
        for i in range(dim):
            for j in range(dim):
                knowledgeBaseList.__setitem__((i,j),0)


    for tempo in flagedFeilds:
        i=tempo[0]
        j=tempo[1]
        openFeilds.remove((i, j))
        updatedGrid[i][j].flag = False
        updatedGrid[i][j].bomb = False
        updatedGrid[i][j].open = False
    flagedFeilds.clear()

    for x in openFeilds:
        if(updatedGrid[x[0]][x[1]].weight != 0):
            neighbour = notOpenNeighbours(x, dim)
            if not(not neighbour):
                probOfNeighbours = (updatedGrid[x[0]][x[1]].weight / len(neighbour))
                #print("1  " + str(probOfNeighbours))
                for temp in neighbour:
                    initialProb = knowledgeBaseList.get((temp[0],temp[1]))
                    #print("initial prob"+str(initialProb))
                    tempProb = initialProb + probOfNeighbours
                    #print("temp prob" + str(tempProb))
                    knowledgeBaseList.__setitem__((temp[0],temp[1]),tempProb)

        else:
            neighbour = notOpenNeighbours(x,dim)
            for temp in neighbour:
                if temp not in openFeilds:
                    print("Opening all fields around "+str(x))
                    openFeilds.append(temp)

                    printGrid(updatedGrid,dim)


    flagCount = floor((dim*dim)/15
                      )

    while True:
        tempList=0.00
        temp = ()
        for i in range(dim):
            for j in range(dim):
                if((knowledgeBaseList.get((i,j))*10.00) >= tempList and (i,j) not in flagedFeilds and validityCheck(updatedGrid,(i,j),dim)):
                    print(knowledgeBaseList.get((i,j))*10.00)
                    temp = (i,j)
                    tempList = (knowledgeBaseList.get((i,j))*10.00)
        if not(not temp):
            flagedFeilds.append((temp[0],temp[1]))
            openFeilds.append((temp[0],temp[1]))
            updatedGrid[temp[0]][temp[1]].open = True
            updatedGrid[temp[0]][temp[1]].flag = True
            updatedGrid[temp[0]][temp[1]].bomb = True
            print("printing after flaging:"+str(temp))
            printGrid(updatedGrid,dim)
        flagCount-=1
        if flagCount<=0:
            break


    count = len(knowledgeBaseList)
    fPoint = ()
    temp = 5000

    for tempPoint in setup_cells(dim):

        val = knowledgeBaseList.get(tempPoint)
        if (tempPoint not in openFeilds and tempPoint not in flagedFeilds and temp>val):
            temp = val
            fPoint = tempPoint

    time.sleep(.5)
    return fPoint


def setup_cells(dim):

    #noting all the unvisited cells
    unvisited = []
    for row in range(dim):
        for col in range(dim):
            unvisited.append((row, col))

    return unvisited

def validityCheck(updatedGrid,point,dim):
    #checks for one
    neighbour = neighbouringPoints(updatedGrid,point,dim)
    tempFlagedFields = []
    if (point[0]-1,point[1]) in neighbour and (point[0]-1,point[1]) in flagedFeilds:
        if(point[0]-1>=0 and point[1]-1>=0 and updatedGrid[point[0]-1][point[1]-1].weight>1):
            return True
        elif(point[1]+1<=dim-1 and point[0]-1>=0 and updatedGrid[point[0]-1][point[1]+1].weight>1):
            return True
        else:
            return False
    if (point[0]+1,point[1]) in neighbour and (point[0]+1,point[1]) in flagedFeilds:
        if(point[1]-1>=0 and updatedGrid[point[0]+1][point[1]-1].weight>1):
            return True
        elif(point[1]+1<=dim-1 and updatedGrid[point[0]+1][point[1]+1].weight>1):
            return True
        else:
            return False
    if (point[0],point[1]+1) in neighbour and (point[0],point[1]+1) in flagedFeilds:
        if(point[0]-1>=0 and point[1]+1<dim-1 and updatedGrid[point[0]-1][point[1]+1].weight>1):
            return True
        elif(point[0]+1<=dim-1 and point[1]+1<=dim-1 and updatedGrid[point[0]+1][point[1]+1].weight>1):
            return True
        else:
            return False
    if (point[0],point[1]-1) in neighbour and (point[0],point[1]-1) in flagedFeilds:
        if(point[0]-1>=0 and point[1]-1>=0 and updatedGrid[point[0]-1][point[1]-1].weight>1):
            return True
        elif(point[0]+1<=dim-1 and point[1]-1>=0 and updatedGrid[point[0]+1][point[1]-1].weight>1):
            return True
        else:
            return False
    if (point[0]-1,point[1]-1) in neighbour and (point[0]-1,point[1]-1) in flagedFeilds:
        if(point[0]-1>=0 and updatedGrid[point[0]-1][point[1]].weight>1):
            return True
        elif(updatedGrid[point[0]][point[1]-1].weight>1 and point[1]-1>=0):
            return True
        else:
            return False
    if (point[0]+1,point[1]+1) in neighbour and (point[0]+1,point[1]+1) in flagedFeilds:
        if(point[0]+1<=dim-1 and updatedGrid[point[0]+1][point[1]].weight>1):
            return True
        elif(point[1]+1<=dim-1 and updatedGrid[point[0]][point[1]+1].weight>1):
            return True
        else:
            return False
    if (point[0]-1,point[1]+1) in neighbour and (point[0]-1,point[1]+1) in flagedFeilds:
        if(point[0]-1>=0 and updatedGrid[point[0]-1][point[1]].weight>1):
            return True
        elif(point[1]+1<=dim-1 and updatedGrid[point[0]][point[1]+1].weight>1):
            return True
        else:
            return False
    if (point[0]+1,point[1]-1) in neighbour and (point[0]+1,point[1]-1) in flagedFeilds:
        if(point[0]+1<=dim-1 and updatedGrid[point[0]+1][point[1]].weight>1):
            return True
        elif(point[1]-1>=0 and updatedGrid[point[0]][point[1]-1].weight>1):
            return True
        else:
            return False

    return True


def neighbouringPoints(updatedGrid,point,dim):

    listOfNeighbours = []

    row = point[0]
    col = point[1]

    #north
    if (row - 1 >= 0 and ((row - 1, col)) not in listOfNeighbours):
        listOfNeighbours.append((row - 1, col))
    # checking for the south neighbour
    if (row + 1 <= (dim - 1) and ((row + 1, col)) not in listOfNeighbours):
        listOfNeighbours.append((row + 1, col))
    # checking for the east neighbour
    if (col + 1 <= (dim - 1) and ((row, col + 1)) not in listOfNeighbours):
        listOfNeighbours.append((row, col + 1))
    # checking for the west neighbour
    if (col - 1 >= 0 and ((row, col - 1)) not in listOfNeighbours):
        listOfNeighbours.append((row, col - 1))
    # checking for the south east
    if (col + 1 <= (dim - 1) and row + 1 <= (dim - 1)
        and ((row + 1, col + 1)) not in listOfNeighbours):
        listOfNeighbours.append((row + 1, col + 1))
    # checking for the south west
    if (col - 1 >= 0 and row + 1 <= (dim - 1) and
            ((row + 1, col - 1)) not in listOfNeighbours):
        listOfNeighbours.append((row + 1, col - 1))
    # checking for the north east
    if (col + 1 <= (dim - 1) and row - 1 >= 0 and
            ((row - 1, col + 1)) not in listOfNeighbours):
        listOfNeighbours.append((row - 1, col + 1))
    # checking for the north west
    if (col - 1 >= 0 and row - 1 >= 0 and
            ((row - 1, col - 1)) not in listOfNeighbours):
        listOfNeighbours.append((row - 1, col - 1))

    return listOfNeighbours



def printGrid(grid,dim):

    for i in range(dim):
        list = []
        for j in range(dim):
            if ( grid[i][j].open == True and  grid[i][j].flag == False):
                list.append(grid[i][j].weight)
            elif (grid[i][j].flag == True):
                list.append("F")
            else:
                list.append("x")
        print(list)

def neighbours(point,dim):

    listOfNeighbours = []

    row = point[0]
    col = point[1]
    if (row - 1 >= 0 and referenceGrid[row - 1][col].bomb == False and
            ((row - 1, col)) not in listOfNeighbours and ((row - 1, col)) not in openFeilds ):
        listOfNeighbours.append((row - 1, col))
    # checking for the south neighbour
    if (row + 1 <= (dim - 1) and referenceGrid[row + 1][
        col].bomb == False and ((row + 1, col)) not in listOfNeighbours and ((row + 1, col)) not in openFeilds ):
        listOfNeighbours.append((row + 1, col))
    # checking for the east neighbour
    if (col + 1 <= (dim - 1) and referenceGrid[row][
        col + 1].bomb == False and ((row, col + 1)) not in listOfNeighbours and ((row, col + 1)) not in openFeilds):
        listOfNeighbours.append((row, col + 1))
    # checking for the west neighbour
    if (col - 1 >= 0 and referenceGrid[row][col - 1].bomb == False and
            ((row, col - 1)) not in listOfNeighbours and
            ((row, col - 1)) not in openFeilds):
        listOfNeighbours.append((row, col - 1))
    # checking for the south east
    if (col + 1 <= (dim - 1) and row + 1 <= (dim - 1) and
            referenceGrid[row + 1][col + 1].bomb == False
            and ((row + 1, col + 1)) not in listOfNeighbours and ((row + 1, col + 1)) not in openFeilds):
        listOfNeighbours.append((row + 1, col + 1))
    # checking for the south west
    if (col - 1 >= 0 and row + 1 <= (dim - 1) and referenceGrid[row + 1][col - 1].bomb == False and
            ((row + 1, col-1)) not in listOfNeighbours and
            ((row + 1, col-1)) not in openFeilds):
        listOfNeighbours.append((row + 1, col - 1))
    # checking for the north east
    if (col + 1 <= (dim - 1) and row - 1 >= 0 and referenceGrid[row - 1][col + 1].bomb == False and
            ((row - 1, col+1)) not in listOfNeighbours and
            ((row - 1, col+1)) not in openFeilds):
        listOfNeighbours.append((row - 1, col + 1))
    # checking for the north west
    if (col - 1 >= 0 and row - 1 >= 0 and referenceGrid[row - 1][col - 1].bomb == False and
            ((row - 1, col-1)) not in listOfNeighbours and
            ((row - 1, col-1)) not in openFeilds):
        listOfNeighbours.append((row - 1, col - 1))

    return listOfNeighbours

def notOpenNeighbours(point,dim):

    listOfNonZeroNeighbours = []

    row = point[0]
    col = point[1]

    #north
    if ((row-1,col)) not in flagedFeilds:
        if ((row-1) >= 0 and ((row-1,col)) not in openFeilds and
                ((row-1,col)) not in listOfNonZeroNeighbours):

            listOfNonZeroNeighbours.append((row-1,col))

    else:
        listOfNonZeroNeighbours.append((row - 1, col))

    # checking for the south neighbour
    if ((row+1,col)) not in flagedFeilds:
        if ((row + 1) <= (dim - 1) and ((row+1,col)) not in openFeilds and
                ((row+1,col)) not in listOfNonZeroNeighbours):
            listOfNonZeroNeighbours.append((row+1,col))
    else:
        listOfNonZeroNeighbours.append((row+1, col))

    # checking for the east neighbour
    if ((row, col + 1)) not in flagedFeilds:
        if ((col+1) <= (dim - 1) and ((row, col + 1)) not in openFeilds and
                ((row,col+1)) not in listOfNonZeroNeighbours):
            listOfNonZeroNeighbours.append((row,col+1))

    else:
        listOfNonZeroNeighbours.append((row, col + 1))

    # checking for the west neighbour
    if ((row,col-1)) not in flagedFeilds:
        if ((col-1) >= 0 and ((row,col-1)) not in openFeilds and
                ((row,col-1)) not in listOfNonZeroNeighbours):
            listOfNonZeroNeighbours.append((row,col-1))
    else:
        listOfNonZeroNeighbours.append((row, col - 1))

    # checking for the south east
    if ((row+1,col+1 )) not in flagedFeilds:
        if ((col+1) <= (dim - 1) and row + 1 <= (dim - 1) and
                ((row+1,col+1 )) not in openFeilds and
                ((row+1,col+1 )) not in listOfNonZeroNeighbours):
            listOfNonZeroNeighbours.append((row+1,col+1))
    else:
        listOfNonZeroNeighbours.append((row + 1, col + 1))

    # checking for the south west
    if ((row + 1, col - 1)) not in flagedFeilds:
        if ((col-1) >= 0 and row + 1 <= (dim - 1) and
                ((row + 1, col - 1)) not in openFeilds and
                ((row+1,col-1)) not in listOfNonZeroNeighbours):
            listOfNonZeroNeighbours.append((row+1,col-1))
    else:
        listOfNonZeroNeighbours.append((row + 1, col - 1))

    # checking for the north east
    if ((row-1,col+1)) not in flagedFeilds:
        if ((col+1) <= (dim - 1) and row - 1 >= 0 and
                ((row-1,col+1)) not in openFeilds and
                ((row-1,col+1)) not in listOfNonZeroNeighbours):
            listOfNonZeroNeighbours.append((row-1,col+1))

    else:
        listOfNonZeroNeighbours.append((row - 1, col + 1))

    # checking for the north west
    if  ((row-1,col-1)) not in flagedFeilds:
        if ((col-1) >= 0 and row - 1 >= 0 and
                ((row-1,col-1)) not in openFeilds and
                ((row-1,col-1)) not in listOfNonZeroNeighbours):
            listOfNonZeroNeighbours.append((row-1,col-1))
    else:
        listOfNonZeroNeighbours.append((row - 1, col - 1))

    return listOfNonZeroNeighbours

def randomStart(dim):
    row = randint(0,dim-1)
    col = randint(0,dim-1)
    return (row,col)

#makes a initial template of the grid
def makeGrid(dim):
    grid = [[gridElement() for j in range(dim)] for i in range(dim)]
    for i in range (dim):
        for j in range (dim):
            grid[i][j].location = (i,j)
    return grid

#sets bombs inside the grid
def setBombs(grid,dim):

    count = floor((dim*dim)/15)

    while count > 0:
        i = randint(0,dim-1)
        j = randint(0,dim-1)

        if(grid[i][j].bomb == False):
            grid[i][j].bomb = True
            count-=1
    return grid

#gives the weights(adjecent number of fields with bombs)
def setWeights(grid,dim):

    for row in range(dim):
        for col in range(dim):
            if(grid[row][col].bomb == True):
                # checking for the north neighbour
                if (row - 1 >= 0 and grid[row-1][col].bomb==False):
                    grid[row-1][col].weight+=1
                # checking for the south neighbour
                if (row + 1 <= (dim-1) and grid[row+1][col].bomb==False):
                    grid[row+1][col].weight+=1
                # checking for the east neighbour
                if (col + 1 <= (dim-1) and grid[row][col+1].bomb==False):
                    grid[row][col+1].weight+=1
                # checking for the west neighbour
                if (col - 1 >= 0 and grid[row][col-1].bomb==False):
                    grid[row][col-1].weight+=1
                # checking for the south east
                if (col + 1 <= (dim-1) and row + 1 <= (dim-1) and grid[row+1][col+1].bomb==False):
                    grid[row+1][col+1].weight+=1
                #checking for the south west
                if (col -1 >= 0 and row + 1 <= (dim-1) and grid[row+1][col-1].bomb==False):
                    grid[row+1][col-1].weight+=1
                #checking for the north east
                if (col + 1 <= (dim-1) and row - 1 >= 0 and grid[row-1][col+1].bomb==False):
                    grid[row-1][col+1].weight+=1
                #checking for the north west
                if(col - 1 >= 0 and row - 1 >= 0 and grid[row-1][col-1].bomb==False):
                    grid[row-1][col-1].weight+=1

                #weight of the field with bomb
                grid[row][col].weight = 69
    return grid

if __name__ == "__main__":
    mine(7)