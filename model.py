from flask import Flask,request,render_template, session
import mysql.connector

mydb = mysql.connector.connect(
    port = 8889,
    host="localhost",
    user="root",
    password="root",
    database="pigeon-gate",
)

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
            "idUser": pigeon[7]
        }    
        pigeons.append(pigeon)
    return pigeons

def getUserbyPseudo(pseudo):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM User WHERE pseudo = %s", (pseudo,))
    return mycursor.fetchall()

def addPigeon(prenomPigeon, color, rateWalk, rateVibe, rateOriginality, place, urlPhoto, idUser):
    mycursor = mydb.cursor()
    mycursor.execute("INSERT INTO Pigeon (prenomPigeon, color, rateWalk, rateVibe, rateOriginality, place, urlPhoto, idUser) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)", (prenomPigeon, color, rateWalk, rateVibe, rateOriginality, place, urlPhoto, idUser))
    mydb.commit()

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