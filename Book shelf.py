import operator
from graphics import *
import time
#API to access library of congress and get each book size?   

class book:
    libr = []

    def __init__(self, name, length, height):
        self.name = name
        self.length = length
        self.height = height
        book.libr.append(self)
    def shelve(self,x,y,standTall=False):
        if standTall:
            self.rectangle = Rectangle(Point(x,y),Point(x+self.height,y+self.length))
            self.title = Text(self.rectangle.getCenter(), "\n".join(self.name))
        else:
            self.rectangle = Rectangle(Point(x,y),Point(x+self.length,y-self.height))
            self.title = Text(self.rectangle.getCenter(), self.name)  

def main():
#gather data
    shelfwidth = 94
    shelfheight = 60
    f = open("/home/beckwithdevin/books", "r")
    books = f.readlines()
    for i in books:
        newi = i.strip().split()
        i = book(newi[0],float(newi[1]),float(newi[2]))
#organize books by length
    sortlength = sorted(book.libr, key = lambda book: book.length)
    lengthionary = {}
    for i in sortlength:
        if i.length not in lengthionary:
            lengthionary[i.length] = list()
        lengthionary[i.length].extend([i.height])
    keyLength = sorted(lengthionary, reverse = True)
#organize books by height
    sortheight = sorted(book.libr, key = lambda book: book.height)
    heightionary = {}
    for i in sortheight:
        if i.height not in heightionary:
            heightionary[i.height] = list()
        heightionary[i.height].extend([i.length])
    keyHeight = sorted(heightionary, reverse = True)

#build gi
    win = GraphWin("bookshelf", 500,500)
    win.setCoords(0,0,shelfwidth,shelfheight)
    tally = shelfheight-keyLength[0]
    verticalSpace = shelfheight-keyLength[0]
    tallx = 0
    flatx = 0

#stack/draw books goal is to minimize floor length
    unplacedBooks = sorted(book.libr, key = lambda book: book.length)
    placedBooks = []
    while unplacedBooks:
        tallEdge = unplacedBooks[0].length + flatx
        for j in range(len(lengthionary[unplacedBooks[0].length])):
            i = unplacedBooks[0]
            i.shelve(flatx,verticalSpace)
            i.rectangle.draw(win)
            i.title.draw(win)
            unplacedBooks.remove(i)
            placedBooks.append(i)
            verticalSpace -= i.height
        availSpace = tallEdge-tallx
        if unplacedBooks == []:
            break
        while availSpace >= min(i.height for i in unplacedBooks):
            for i in reversed(unplacedBooks): 
                if i.height <= availSpace:
                    i.shelve(tallx,tally,standTall=True)
                    i.rectangle.draw(win)
                    i.title.draw(win)
                    unplacedBooks.remove(i)
                    placedBooks.append(i)
                    tallx += i.height
                    availSpace -= i.height
            if unplacedBooks == []:
                break
        tallx = tallEdge
        tally = verticalSpace
        if verticalSpace < keyHeight[-1]:
            flatx += tallEdge
            for i in placedBooks:
                i.rectangle.move(0,-verticalSpace)
                i.title.move(0,-verticalSpace)
            verticalSpace = shelfheight - max(i.length for i in unplacedBooks)
            tally = shelfheight - max(i.length for i in unplacedBooks)
            placedBooks = []
    for i in placedBooks:
        i.rectangle.move(0,-verticalSpace)
        i.title.move(0,-verticalSpace)
        placedBooks = []            
    win.getMouse()
    f.close()    
main()