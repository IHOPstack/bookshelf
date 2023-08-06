from graphics import *
from collections import defaultdict

libr = [];

class book:
    def __init__(self, name, length, height):
        self.name = name
        self.length = length
        self.height = height
        libr.append(self)
    def shelve(self,x,y,standTall=False):
        if standTall:
            self.rectangle = Rectangle(Point(x,y),Point(x + self.height, y + self.length))
            self.title = Text(self.rectangle.getCenter(), "\n".join(self.name))
        else:
            self.rectangle = Rectangle(Point(x,y),Point(x+self.length,y-self.height))
            self.title = Text(self.rectangle.getCenter(), self.name)  

def makeDict(libr, height):
    sort = sorted(libr, key = lambda book: book.length if not height else book.height)
    dictionary = defaultdict(int)
    for i in sort:
        dictionary[i.length if not height else i.height] += 1
    keySize = sorted(dictionary, reverse = True)
    return (dictionary, keySize)

def main():
#gather data
    shelfwidth = 94
    shelfheight = 60
    f = open("books", "r")
    books = f.readlines()
    for thisBook in books:
        sanitBook = thisBook.strip().split()
        book(sanitBook[0], float(sanitBook[1]), float(sanitBook[2]))

#organize books by length and height
    (_, keyHeight) = makeDict(libr, True)
    (lengthionary, keyLength) = makeDict(libr, False)

#build gi
    win = GraphWin("bookshelf", 500,500)
    win.setCoords(0,0,shelfwidth,shelfheight)
    tally = shelfheight-keyLength[0]
    verticalSpace = shelfheight-keyLength[0]
    tallx = 0
    flatx = 0

#stack/draw books goal is to minimize floor length
    unplacedBooks = sorted(libr, key = lambda book: book.length)
    placedBooks = []
    while unplacedBooks:
        tallEdge = unplacedBooks[0].length + flatx
        shortestLenCount = lengthionary[unplacedBooks[0].length]
        for _ in range(shortestLenCount):
            firstBook = unplacedBooks[0]
            firstBook.shelve(flatx,verticalSpace)
            firstBook.rectangle.draw(win)
            firstBook.title.draw(win)
            lengthionary[firstBook.length] -= 1
            unplacedBooks.remove(firstBook)
            placedBooks.append(firstBook)
            verticalSpace -= firstBook.height
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
                    lengthionary[i.length] -= 1
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