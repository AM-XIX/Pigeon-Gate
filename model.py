from flask import Flask,request,render_template, session
import mysql.connector

mydb = mysql.connector.connect(
    port = 8889,
    host="localhost",
    user="root",
    password="root",
    database="pigeon-gate",
)

## User

def getUserbyPseudo(pseudo):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM User WHERE pseudo = %s", (pseudo,))
    userData = mycursor.fetchall()
    user = {
        "idUser": userData[0][0],
        "pseudo": userData[0][1],
        "bio": userData[0][3],
        "typeProfilePicture": userData[0][4],
        "sommePigeons": sumAllPigeonsByUser(userData[0][0])
    }
    return user

def checkLogin(pseudo, password):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM User WHERE pseudo = %s AND password = %s", (pseudo, password))
    testLogin = mycursor.fetchall()
    return testLogin

def newUser(pseudo, password, typeProfilePicture):
    if not pseudo or not password or not typeProfilePicture:
        return False
    if getUserbyPseudo(pseudo):
        return False
    mycursor = mydb.cursor()
    mycursor.execute("INSERT INTO User (pseudo, password, typeProfilePicture) VALUES (%s, %s, %s)", (pseudo, password, typeProfilePicture))
    mydb.commit()
    return True

def changeBio(idUser, newBio):
    mycursor = mydb.cursor()
    mycursor.execute("UPDATE User SET bio = %s WHERE idUser = %s", (newBio, idUser))
    mydb.commit()

def sumAllPigeonsByUser(idUser):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT COUNT(*) FROM Pigeon WHERE idUser = %s", (idUser,))
    sumPigeons = mycursor.fetchone()
    if not sumPigeons:
        return 0
    return sumPigeons[0]


## Pigeon

def getAllPigeons():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM Pigeon")
    allPigeons = mycursor.fetchall()
    return dataToPigeon(allPigeons)

def dataToPigeon(datas):
    pigeons = []
    for pigeon in datas:
        pigeon = {
            "idPigeon": pigeon[0],
            "prenomPigeon": pigeon[1],
            "color": pigeon[2],
            "rateWalk": pigeon[3],
            "rateVibe": pigeon[4],
            "rateOriginality": pigeon[5],
            "place": pigeon[6],
            "urlPhoto": pigeon[7],
            "idUser": pigeon[8]
        }    
        pigeons.append(pigeon)
    return pigeons


def addPigeon(prenomPigeon, color, rateWalk, rateVibe, rateOriginality, place, urlPhoto, idUser):
    mycursor = mydb.cursor()
    mycursor.execute("INSERT INTO Pigeon (prenomPigeon, color, rateWalk, rateVibe, rateOriginality, place, urlPhoto, idUser) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (prenomPigeon, color, rateWalk, rateVibe, rateOriginality, place, urlPhoto, idUser))
    mydb.commit()

def getLastPigeonsByUser(idUser, page):
    limit = 4
    offset = page * limit
    mycursor = mydb.cursor()
    query = "SELECT * FROM Pigeon INNER JOIN User ON Pigeon.idUser = User.idUser WHERE Pigeon.idUser = %s ORDER BY Pigeon.idPigeon DESC LIMIT %s OFFSET %s"
    mycursor.execute(query, (idUser, limit, offset))
    lastPigeons = mycursor.fetchall()
    return dataToPigeon(lastPigeons)