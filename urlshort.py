#Shortens URLs into URLs to about 6 characters long

import sqlite3, random, string

def urlcreate():
    #This is the list of numbers and letters that can be chosen from to create a URL
    letters = string.ascii_letters + "0123456789"
    return ''.join(random.choice(letters) for i in range(6))

#Checks if the link won't fit in the database
def checklength(link):
    if len(link) > 255:
        return True
    return False

#Finds the link associated with an ID
def checkid(id):
    db = sqlite3.connect("urls.db")
    cur = db.cursor()
    idlist = cur.execute(f"select * from urls where id like '{id}'").fetchall()
    #Goes row by row through what the query returns
    for row in idlist:
        if id in row:
            #Returns the corresponding URL
            return row[1]
    return False

#The same as ID check but it looks to see if the link supplied has already been shortened, and then returns that ID if the link is found
def checklink(link):
    db = sqlite3.connect("urls.db")
    cur = db.cursor()
    linklist = cur.execute(f"select * from urls where url like '{link}'").fetchall()
    for row in linklist:
        if link in row:
            return row[0]
    return False

#Checks to see if there are illegal characters in the custom link (alphanumeric characters only)
def checkcustom(link):
    for ch in str(link):
        if ch not in (string.ascii_letters + "0123456789"):
            return False

#Creates the database with the URL table
def createdb():
    db = sqlite3.connect("urls.db")
    cur = db.cursor()
    cur.execute("create table if not exists urls (id varchar(255), url varchar(255))")

#Main function that shortens URLs
def shorten(sl):
    #Runs the checks for if the link is too long and if the link was already made
    if checklength(sl):
        return "long"
    cl = checklink(sl)
    if cl != False:
        return cl

    #connects to database and sets cursor
    db = sqlite3.connect("urls.db")
    cur = db.cursor()

    #This creates the new shortened URL
    shortened = urlcreate()

    #If the generated ID is in the database already, keep generating new IDs until it's an ID that doesn't exist
    if checkid(shortened) != False:
        while shortened in cur.execute(f"select * from urls where id like '{shortened}'").fetchall():
            shortened = urlcreate()

    #Insert the ID and the original link into the URLs table
    cur.execute(f"insert into urls (id, url) values('{shortened}', '{sl}')")
    db.commit()
    return shortened

#This is for creating custom links
def customlink(cid, sl):
    if checkcustom(cid) == False:
        return "illegal"
    if checklength(cid):
        return "long"
    if checkid(cid) != False:
        return "taken"
    
    db = sqlite3.connect("urls.db")
    cur = db.cursor()

    cur.execute(f"insert into urls (id, url) values('{cid}', '{sl}')")
    db.commit()

    return cid
    