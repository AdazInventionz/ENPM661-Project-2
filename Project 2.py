#!/usr/bin/env python
# coding: utf-8

# In[3]:


#Imported libraries
import numpy as np
import cv2 as cv
import time
import heapq as hq


#Prompts the user to enter start and end nodes/coordinates
def getEndpoints():
    
    j = -1
    
    while (j < 0):
        
        xstart = ""
        ystart = ""
        xend = ""
        yend = ""
        
        while validEntry(xstart, 599) == False:

            xstart = input('Enter the x value for the starting coordinate: ')

        while validEntry(ystart, 249) == False:

            ystart = input('Enter the y value for the starting coordinate: ')

        while validEntry(xend, 599) == False:

            xend = input('Enter the x value for the ending coordinate: ')

        while validEntry(yend, 249) == False:

            yend = input('Enter the y value for the ending coordinate: ')
            
        if (canvas[249 - int(ystart), int(xstart), 2] != 255) and (canvas[249 - int(yend), int(xend), 2] != 255) and (canvas[249 - int(ystart), int(xstart), 2] != 177) and (canvas[249 - int(yend), int(xend), 2] != 177):
            break
    
    xstart = int(xstart)
    ystart = int(ystart)
    xend = int(xend)
    yend = int(yend)
    
    ystart = 249 - ystart
    yend = 249 - yend
    
    return xstart, ystart, xend, yend

#Determines if a user-entered cordinate is a valid number and within range of the arena
def validEntry(val, max):
    
    if val.isdigit() == False:
        return False
    
    if int(val) < 0:
        return False
    
    if int(val) > max:
        return False
    
    return True

#Sets up arena, including unexplored nodes and obstacles (and their borders)
def setup():

    global canvas
    
    #Colors
    white = (255, 255, 255)
    gray = (177, 177, 177)

    #Polygon (pts)
    hexagonBorder = np.array([[300, 45], [370, 86], [370, 164], [300, 205], [230, 164], [230, 86]], np.int32)
    hexagonBorder = hexagonBorder.reshape((-1, 1, 2))
    
    hexagon = np.array([[300, 50], [365, 88], [365, 162], [300, 200], [235, 162], [235, 88]], np.int32)
    hexagon = hexagon.reshape((-1, 1, 2))
    
    triangleBorder = np.array([[455, 5], [455, 245], [515, 125]], np.int32)
    triangleBorder = triangleBorder.reshape((-1, 1, 2))
    
    triangle = np.array([[460, 25], [460, 225], [510, 125]], np.int32)
    triangle = triangle.reshape((-1, 1, 2))

    #Obstacles (shapes)
    cv.rectangle(canvas, (95, 0), (155, 105), gray, -1)
    cv.rectangle(canvas, (95, 145), (155, 250), gray, -1)
    cv.rectangle(canvas, (100, 0), (150, 100), white, -1)
    cv.rectangle(canvas, (100, 150), (150, 250), white, -1)

    cv.fillPoly(canvas, [hexagonBorder], gray)
    cv.fillPoly(canvas, [hexagon], white)
    
    cv.fillPoly(canvas, [triangleBorder], gray)
    cv.fillPoly(canvas, [triangle], white)

#Backtracks to determin optimal solution
def backtrack():
    
    global start
    global end
    
    p = len(closedNodes) - 1
    b = closedNodes[(end[0], end[1])]
    
    while b != (-1, -1):
        
        solution.insert(0, [b[0], b[1]])
        b = closedNodes[(b[0], b[1])]

#Checks to see if a node exists in the closed dictionary
def checkClosed(n):
    
    global closedNodes
    
    if (n[3][0], n[3][1]) in closedNodes:
        return True
    
    return False

#Checks to see if a node exists in the open list
def checkOpen(n):
    
    global openNodes
        
    for i in range(0, len(openNodes)):
        
        if n[3] == openNodes[i][3]:
            return i
        
    return None
    
#Checks to see if a node is an obstacle (or its border)
def checkObstacle(n):
    
    if canvas[n[3][1], n[3][0], 2] == 255:
        return True
    
    if canvas[n[3][1], n[3][0], 2] == 177:
        return True
        
    return False






def moveUp(n):
    
    global openNodes
    global ni
    
    ni += 1
    
    new = [n[0] + 1, ni, [n[3][0], n[3][1]], [n[3][0], n[3][1] - 1]]
    
    if (new[3][1] >= 0):
        
        if (checkObstacle(new) == False) and (checkClosed(new) == False):
        
            ex = checkOpen(new)
            
            if (ex == None):
                
                hq.heappush(openNodes, new)
                
            elif (new[0] < openNodes[ex][0]):
                
                openNodes.pop(ex)
                hq.heappush(openNodes, new)

def moveDown(n):
    
    global openNodes
    global ni
    
    ni += 1
    
    new = [n[0] + 1, ni, [n[3][0], n[3][1]], [n[3][0], n[3][1] + 1]]
    
    if (new[3][1] < 250):
        
        if (checkObstacle(new) == False) and (checkClosed(new) == False):
        
            ex = checkOpen(new)
            
            if (ex == None):
                
                hq.heappush(openNodes, new)
                
            elif (new[0] < openNodes[ex][0]):
                
                openNodes.pop(ex)
                hq.heappush(openNodes, new)

def moveLeft(n):
    
    global openNodes
    global ni
    
    ni += 1
    
    new = [n[0] + 1, ni, [n[3][0], n[3][1]], [n[3][0] - 1, n[3][1]]]
    
    if (new[3][0] >= 0):
        
        if (checkObstacle(new) == False) and (checkClosed(new) == False):
        
            ex = checkOpen(new)
            
            if (ex == None):
                
                hq.heappush(openNodes, new)
                
            elif (new[0] < openNodes[ex][0]):
                
                openNodes.pop(ex)
                hq.heappush(openNodes, new) 

def moveRight(n):
    
    global openNodes
    global ni
    
    ni += 1
    
    new = [n[0] + 1, ni, [n[3][0], n[3][1]], [n[3][0] + 1, n[3][1]]]
    
    if (new[3][0] < 600):
        
        if (checkObstacle(new) == False) and (checkClosed(new) == False):
        
            ex = checkOpen(new)
            
            if (ex == None):
                
                hq.heappush(openNodes, new)
                
            elif (new[0] < openNodes[ex][0]):
                
                openNodes.pop(ex)
                hq.heappush(openNodes, new)
                
def moveUpLeft(n):
    
    global openNodes
    global ni
    
    ni += 1
    
    new = [n[0] + 1.4, ni, [n[3][0], n[3][1]], [n[3][0] - 1, n[3][1] - 1]]
    
    if (new[3][1] >= 0) and (new[3][0] >= 0):
        
        if (checkObstacle(new) == False) and (checkClosed(new) == False):
        
            ex = checkOpen(new)
            
            if (ex == None):
                
                hq.heappush(openNodes, new)
                
            elif (new[0] < openNodes[ex][0]):
                
                openNodes.pop(ex)
                hq.heappush(openNodes, new)

def moveUpRight(n):
    
    global openNodes
    global ni
    
    ni += 1
    
    new = [n[0] + 1.4, ni, [n[3][0], n[3][1]], [n[3][0] + 1, n[3][1] - 1]]
    
    if (new[3][1] >= 0) and (new[3][0] < 600):
        
        if (checkObstacle(new) == False) and (checkClosed(new) == False):
        
            ex = checkOpen(new)
            
            if (ex == None):
                
                hq.heappush(openNodes, new)
                
            elif (new[0] < openNodes[ex][0]):
                
                openNodes.pop(ex)
                hq.heappush(openNodes, new)

def moveDownLeft(n):
    
    global openNodes
    global ni
    
    ni += 1
    
    new = [n[0] + 1.4, ni, [n[3][0], n[3][1]], [n[3][0] - 1, n[3][1] + 1]]
    
    if (new[3][1] < 250) and (new[3][0] >= 0):
        
        if (checkObstacle(new) == False) and (checkClosed(new) == False):
        
            ex = checkOpen(new)
            
            if (ex == None):
                
                hq.heappush(openNodes, new)
                
            elif (new[0] < openNodes[ex][0]):
                
                openNodes.pop(ex)
                hq.heappush(openNodes, new) 

def moveDownRight(n):
    
    global openNodes
    global ni
    
    ni += 1
    
    new = [n[0] + 1.4, ni, [n[3][0], n[3][1]], [n[3][0] + 1, n[3][1] + 1]]
    
    if (new[3][1] < 250) and (new[3][0] < 600):
        
        if (checkObstacle(new) == False) and (checkClosed(new) == False):
        
            ex = checkOpen(new)
            
            if (ex == None):
                
                hq.heappush(openNodes, new)
                
            elif (new[0] < openNodes[ex][0]):
                
                openNodes.pop(ex)
                hq.heappush(openNodes, new)
    
    
#------------ Main Code ------------

#New image (canvas)
canvas = np.zeros((250, 600, 3), dtype = "uint8")

#Setup black canvas with white obstacles containing gray boundaries
setup()



#Start & end nodes
start = [-1, -1]
end = [-1, -1]

start[0], start[1], end[0], end[1] = getEndpoints()



#Global variables
openNodes = []
hq.heapify(openNodes)
closedNodes = {}
solution = []
ni = 0
l = 0

current = [0, 0, [-1, -1], [start[0], start[1]]]
closedNodes[(current[3][0], current[3][1])] = (current[2][0], current[2][1])

#Explore nodes
while (current[3] != end):
    
    l += 1
    
    moveUp(current)
    moveDown(current)
    moveLeft(current)
    moveRight(current)
    moveUpLeft(current)
    moveUpRight(current)
    moveDownLeft(current)
    moveDownRight(current)
    
    current = hq.heappop(openNodes)
    closedNodes[(current[3][0], current[3][1])] = (current[2][0], current[2][1])

#Plot start/end nodes
print("Found Solution!")
canvas[start[1], start[0]] = (3, 240, 252)
canvas[end[1], end[0]] = (0, 240, 10)
cv.imshow("Canvas", canvas)
cv.waitKey(3000)
    
#Plot explored nodes 
for i in closedNodes:
    
    x = i[0]
    y = i[1]
    
    if canvas[y, x, 2] != 252 and canvas[y, x, 2] != 10:
    
        canvas[y, x] = (0, 0, 200)
        cv.imshow("Canvas", canvas)
        cv.waitKey(1)
    
#Backtrack, finding optimal solution
backtrack()

#Plot optimal solution
for i in solution:
    
    x = i[0]
    y = i[1]
    
    if canvas[y, x, 2] != 252 and canvas[y, x, 2] != 10:
    
        canvas[y, x] = (255, 2, 2)
        cv.imshow("Canvas", canvas)
        cv.waitKey(1)

print("DONE!")
    
cv.waitKey()
cv.destroyAllWindows()


# In[ ]:





# In[ ]:





# In[ ]:




