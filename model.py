from flask import Flask,request,render_template, session
from flask_bcrypt import Bcrypt
from dotenv import load_dotenv
import mysql.connector
import os

load_dotenv()
db_port = os.getenv('DB_PORT')
db_host = os.getenv('DB_HOST')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')
db_name = os.getenv('DB_NAME')


mydb = mysql.connector.connect(
    port = db_port,
    host=db_host,
    user=db_user,
    password=db_password,
    database=db_name
)

## User

def getUserbyPseudo(pseudo):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM User WHERE pseudo = %s", (pseudo,))
    userData = mycursor.fetchall()
    if not userData:
        return None
    user = {
        "idUser": userData[0][0],
        "pseudo": userData[0][1],
        "bio": userData[0][3],
        "typeProfilePicture": userData[0][4],
        "sommePigeons": sumAllPigeonsByUser(userData[0][0])
    }
    return user

def getUserbyId(idUser):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM User WHERE idUser = %s", (idUser,))
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
    mycursor.execute("SELECT * FROM User WHERE pseudo = %s", (pseudo,))
    user = mycursor.fetchone()
    if user == None:
        return False
    hashed_password = user[2]
    if Bcrypt().check_password_hash(hashed_password, password):
        return True
    return False

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

def changeProfilePicture(idUser, newTypeProfilePicture):
    mycursor = mydb.cursor()
    mycursor.execute("UPDATE User SET typeProfilePicture = %s WHERE idUser = %s", (newTypeProfilePicture, idUser))
    mydb.commit()

def changePseudo(idUser, newPseudo):
    mycursor = mydb.cursor()
    mycursor.execute("UPDATE User SET pseudo = %s WHERE idUser = %s", (newPseudo, idUser))
    mydb.commit()

def sumUsers():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT COUNT(*) FROM User")
    sumUsers = mycursor.fetchone()
    return sumUsers[0]


## Pigeon

def sumAllPigeonsByUser(idUser):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT COUNT(*) FROM Pigeon WHERE idUser = %s", (idUser,))
    sumPigeons = mycursor.fetchone()
    if not sumPigeons:
        return 0
    return sumPigeons[0]

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
            "nbLike": pigeon[8],
            "idUser": pigeon[9],
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

def getCardPigeonsById(idPigeon):
    mycursor = mydb.cursor()
    query = "SELECT * FROM Pigeon WHERE idPigeon = %s";
    mycursor.execute(query, (idPigeon,))
    cardPigeons = mycursor.fetchone()
    pigeon = {
        "idPigeon": cardPigeons[0],
        "prenomPigeon": cardPigeons[1],
        "color": cardPigeons[2],
        "rateWalk": cardPigeons[3],
        "rateVibe": cardPigeons[4],
        "rateOriginality": cardPigeons[5],
        "place": cardPigeons[6],
        "urlPhoto": cardPigeons[7],
        "nbLike": cardPigeons[8],
        "idUser": cardPigeons[9],
    }
    return pigeon

def addRatePigeon(idPigeon, rateWalk, rateVibe, rateOriginality):
    mycursor = mydb.cursor()
    pigeon = getCardPigeonsById(idPigeon)
    rateWalk = (pigeon['rateWalk'] + rateWalk) / 2
    rateVibe = (pigeon['rateVibe'] + rateVibe) / 2
    rateOriginality = (pigeon['rateOriginality'] + rateOriginality) / 2
    mycursor.execute("UPDATE Pigeon SET rateWalk = %s, rateVibe = %s, rateOriginality = %s WHERE idPigeon = %s", (rateWalk, rateVibe, rateOriginality, idPigeon))
    mydb.commit()

def getTrendingPigeons():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM Pigeon ORDER BY nbLike DESC LIMIT 4")
    trendingPigeons = mycursor.fetchall()
    return dataToPigeon(trendingPigeons)


def getWorstPigeon():
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM Pigeon ORDER BY nbLike ASC LIMIT 1")
    result = mycursor.fetchone()
    if result:
        return {
            "idPigeon": result[0],
            "prenomPigeon": result[1],
            "color": result[2],
            "rateWalk": result[3],
            "rateVibe": result[4],
            "rateOriginality": result[5],
            "place": result[6],
            "urlPhoto": result[7],
            "nbLike": result[8],
            "idUser": result[9],
        }
    else:
        return None


# Comment

def dataToComment(datas, pseudoUser):
    comments = []
    for comment in datas:
        comment = {
            "idComment": comment[0],
            "textCom": comment[1],
            "nbLike": comment[2],
            "idUser": comment[3],
            "idPigeon": comment[4],
            "pseudoUser": pseudoUser,
        }
        comments.append(comment)
    return comments

def getCommentsByIdPigeon(idPigeon, idUser):
    mycursor = mydb.cursor()
    query = "SELECT * FROM commentaire WHERE idPigeon = %s";
    mycursor.execute(query, (idPigeon,))
    comments = mycursor.fetchall()
    user = getUserbyId(idUser)
    return dataToComment(comments, user['pseudo'])

def addComment(textCom, idUser, idPigeon):
    mycursor = mydb.cursor()
    mycursor.execute("INSERT INTO commentaire (textCom, nbLike, idUser, idPigeon) VALUES (%s, %s, %s, %s)", (textCom, 0, idUser, idPigeon))
    mydb.commit()

def getFourRandomPigeons(currentIdPigeon):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT * FROM Pigeon WHERE idPigeon != %s ORDER BY RAND() LIMIT 4", (currentIdPigeon,))
    fourRandomPigeons = mycursor.fetchall()
    return dataToPigeon(fourRandomPigeons)


# Category

def getIDCategoryByName(category):
    mycursor = mydb.cursor()
    mycursor.execute("SELECT idCat FROM Categorie WHERE nom = %s", (category,))
    result = mycursor.fetchone()
    if result:
        return result[0]
    return None


def getAllCategories():
    categoriesList = []
    mycursor = mydb.cursor()
    mycursor.execute("SELECT nom FROM Categorie")
    categories = mycursor.fetchall()
    
    for category in categories:
        category_dict = {
            "nom": category[0],
            "idCat": getIDCategoryByName(category[0])
        }
        categoriesList.append(category_dict)
    return categoriesList


def getPigeonsByCategory(idcategory):
    mycursor = mydb.cursor()
    query = "SELECT * FROM Pigeon INNER JOIN Categorise ON Categorise.idPigeon = Pigeon.idPigeon INNER JOIN Categorie ON Categorie.idCat = Categorise.idCat WHERE Categorie.idCat = %s"
    mycursor.execute(query, (idcategory,))
    pigeons = mycursor.fetchall()
    return dataToPigeon(pigeons)

def addCategoryToPigeonById(idPigeon, idCat):
    mycursor = mydb.cursor()
    mycursor.execute("INSERT INTO Categorise (idPigeon, idCat) VALUES (%s, %s)", (idPigeon, idCat))
    mydb.commit()

def addCategoryByCheckbox(namePigeon, tabCategories):
    idPigeon = getPigeonByName(namePigeon)
    for category in tabCategories:
        addCategoryToPigeonById(idPigeon, category)

def getPigeonByName(namePigeon):
    mycursor = mydb.cursor()
    query = "SELECT * FROM Pigeon WHERE prenomPigeon = %s"
    mycursor.execute(query, (namePigeon,))
    pigeon = mycursor.fetchone()
    if pigeon:
        return pigeon[0]
    return None