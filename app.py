from flask import Flask,request,render_template, session
import mysql.connector

app = Flask(__name__)

mydb = mysql.connector.connect(
    port = 8889,
    host="localhost",
    user="root",
    password="root",
    database="pigeon-gate",
)

pigeons = [];
mycursor = mydb.cursor()
mycursor.execute("SELECT * FROM Pigeon")
allPigeons = mycursor.fetchall()


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

dataToPigeon(allPigeons)

@app.route("/", methods=['GET', 'POST'])
def welcome():
    if mydb.is_connected():
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
            return render_template("register.html", messageError=messageError);
        if not pseudo or not password or not typeProfilePicture:
            message_error = "Tous les champs sont obligatoires."
            return render_template('register.html', messageError=message_error)
        mycursor.execute("INSERT INTO User (pseudo, password, typeProfilePicture) VALUES (%s, %s, %s)", (pseudo, password, typeProfilePicture))
        mydb.commit()
        session['pseudo'] = pseudo
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
            session['pseudo'] = pseudo
            return render_template("welcome.html", pigeons=pigeons, pseudo=pseudo);
        else:
            messageErrorLogin = "Pseudo ou mot de passe incorrect"
            return render_template("login.html", messageErrorLogin=messageErrorLogin);
    else:
        return render_template("login.html");


@app.route("/add_pigeon", methods=['POST', 'GET'])
def add_pigeon():
    if 'pseudo' not in session:
        return render_template("login.html");
    if request.method == 'POST' and 'pseudo' in session:
        mycursor.execute("SELECT idUser FROM User WHERE pseudo = %s", session['pseudo'])
        idUser = mycursor.fetchall()[0][0]
        prenom_pigeon = request.form['prenom']
        color_pigeon = request.form['couleur']
        place_pigeon = request.form['place']
        originality = int(request.form['noteoriginalite'])
        walk = int(request.form['notewalk'])
        vibe = int(request.form['notevibe']) 
        url = request.form['urlPhoto']
        sql = "INSERT INTO Pigeon (prenomPigeon, color, rateWalk, rateOriginality, rateVibe, place, urlPhoto, idUser) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        val = (prenom_pigeon, color_pigeon, walk, originality, vibe, place_pigeon, url, idUser)
        mycursor.execute(sql, val)
        mydb.commit()
        return render_template("welcome.html", pigeons=pigeons);
    else:
        return render_template("new_pigeon.html");


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)

