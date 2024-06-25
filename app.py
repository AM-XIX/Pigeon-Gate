from flask import Flask,request,render_template, jsonify,abort
import random
import mysql.connector

app = Flask(__name__)

mydb = mysql.connector.connect(
    port = 3306,
    host="localhost",
    user="root",
    password="",
    database="pigeon-gate",
)

pigeons = [];
mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM Pigeon")
allPigeons = mycursor.fetchall()

@app.route("/", methods=['GET', 'POST'])
def welcome():
    if mydb.is_connected():
        dataToPigeon(allPigeons)
        return render_template("welcome.html", pigeons=pigeons);

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        pseudo = request.form['pseudo']
        password = request.form['password']
        typeProfilePicture = request.form['typeProfilePicture']
        mycursor.execute("SELECT * FROM User WHERE pseudo = %s", (pseudo,))
        messageError = "Ce pseudo est déjà utilisé"
        if mycursor.fetchall():
            print(typeProfilePicture)
            return render_template("register.html", messageError=messageError);
        if not pseudo or not password or not typeProfilePicture:
            message_error = "Tous les champs sont obligatoires."
            return render_template('register.html', messageError=message_error)
        mycursor.execute("INSERT INTO User (pseudo, password, typeProfilePicture) VALUES (%s, %s, %s)", (pseudo, password, typeProfilePicture))
        mydb.commit()
        return render_template("welcome.html", pigeons=pigeons, pseudo=pseudo);
    else:
        return render_template("register.html");

@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
        pseudo = request.form['pseudo']
        password = request.form['password']
        mycursor.execute("SELECT * FROM User WHERE pseudo = %s AND password = %s", (pseudo, password))
        testLogin = mycursor.fetchall()
        if testLogin:
            return render_template("welcome.html", pigeons=pigeons, pseudo=pseudo);
        else:
            messageErrorLogin = "Pseudo ou mot de passe incorrect"
            return render_template("login.html", messageErrorLogin=messageErrorLogin);
    else:
        return render_template("login.html");

def dataToPigeon(datas):
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


@app.route("/add_pigeon", methods=['POST'])
def add_pigeon():
    if request.method == 'POST':
        prenom_pigeon = request.form['prenom']
        color_pigeon = request.form['couleur']
        place_pigeon = request.form['place']
        originality = request.form['noteoriginalite']
        walk = request.form['notewalk']
        vibe = request.form['notevibe']
        mycursor.execute("INSERT INTO Pigeon (prenomPigeon, Color, Place, rateOriginality, rateWalk, rateVibe ) VALUES (%s, %s, %s, %d, %d, %d)", (prenom_pigeon, color_pigeon, place_pigeon, originality, walk, vibe))
        mydb.commit()
        return render_template("new_pigeon.html");
    else:
        return render_template("new_pigeon.html");



if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

