from flask import Flask,request,render_template, session, jsonify
from flask_bcrypt import Bcrypt
import model

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config.from_object('config.Config')


@app.route("/", methods=['GET', 'POST'])
def welcome():
    if model.mydb.is_connected():
        session.clear()
        pigeonsBdd = model.getAllPigeons()
        return render_template("welcome.html", pigeons=pigeonsBdd);

@app.route("/accueil", methods=['GET', 'POST'])
def accueil():
    if model.mydb.is_connected():
        pigeonsBdd = model.getAllPigeons()
        return render_template("welcome.html", pigeons=pigeonsBdd);

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST' and 'pseudo' not in session:
        pseudo = request.form['pseudo']
        password = bcrypt.generate_password_hash(request.form['password']).decode('utf-8')
        typeProfilePicture = request.form['typeProfilePicture']
        if model.getUserbyPseudo(pseudo)!=None:
            messageErrorRegister = "Pseudo déjà utilisé"
            return render_template("register.html", messageErrorRegister=messageErrorRegister);
        else:
            session['pseudo'] = pseudo
            session['idUser'] = int(model.getUserbyPseudo(pseudo)['idUser'])
            model.newUser(pseudo, password, typeProfilePicture)
            pigeonsBdd = model.getAllPigeons()
            return render_template("welcome.html", pigeons=pigeonsBdd, pseudo=pseudo);
    else:
        return render_template("register.html");

@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST' and 'pseudo' not in session:
        pseudo = request.form['pseudo']
        password = request.form['password']
        if model.checkLogin(pseudo, password):
            session['idUser'] = int(model.getUserbyPseudo(pseudo)['idUser'])
            session['pseudo'] = pseudo
            pigeonsBdd = model.getAllPigeons()
            return render_template("welcome.html", pigeons=pigeonsBdd, pseudo=pseudo);
        else:
            messageErrorLogin = "Pseudo ou mot de passe incorrect"
            return render_template("login.html", messageErrorLogin=messageErrorLogin);
    else:
        return render_template("login.html");


@app.route("/add-pigeon", methods=['POST', 'GET'])
def addPigeon():
    if 'pseudo' not in session:
        return render_template("login.html");
    if request.method == 'POST' and 'pseudo' in session:
        idUser = session['idUser']
        noteWalk = int(request.form['notewalk'])
        noteVibe = int(request.form['notevibe'])
        noteOriginalite = int(request.form['noteoriginalite'])
        model.addPigeon(request.form['prenom'], request.form['couleur'], noteWalk, noteVibe, noteOriginalite, request.form['place'], request.form['urlPhoto'], idUser)
        pigeonBdd = model.getAllPigeons()
        return render_template("welcome.html", pigeons=pigeonBdd)
    else:
        return render_template("newPigeon.html");

@app.route("/logout", methods=['POST', 'GET'])
def logout():
    session.clear()
    pigeonsBdd = model.getAllPigeons()
    return render_template("welcome.html", pigeons=pigeonsBdd);

@app.route("/profil", methods=['POST', 'GET'])
def profil():
    otherProfilePicture = ['profile1', 'profile2', 'profile3', 'profile4']
    if 'pseudo' not in session:
        return render_template("login.html") 
    user = model.getUserbyPseudo(session['pseudo'])
    otherProfilePicture.remove(user['typeProfilePicture'])
    page = request.args.get('page', default=0, type=int)
    lastPigeons = model.getLastPigeonsByUser(user['idUser'], page)
    return render_template("profile.html", user=user, lastPigeons=lastPigeons, page=page, otherProfilePicture=otherProfilePicture)

@app.route("/loadMorePigeons", methods=['GET'])
def loadMorePigeons():
    if 'pseudo' not in session:
        return render_template("login.html")
    idUser = session['idUser']
    page = request.args.get('page', default=0, type=int)
    try:
        morePigeons = model.getLastPigeonsByUser(idUser, page)
        morePigeonsJson = [{"id": p['idPigeon'], "prenomPigeon": p['prenomPigeon'], "color": p['color'], "place": p['place'], "urlPhoto": p['urlPhoto']} for p in morePigeons]
        return jsonify(morePigeonsJson)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/change-bio", methods=['POST', 'GET'])
def changeBio():
    otherProfilePicture = ['profile1', 'profile2', 'profile3', 'profile4']
    if 'pseudo' not in session:
        return render_template("login.html")
    if request.method == 'POST' and 'pseudo' in session:
        newBio = request.form['bio']
        model.changeBio(session['idUser'], newBio)
        user = model.getUserbyPseudo(session['pseudo'])
        otherProfilePicture.remove(user['typeProfilePicture'])
        return render_template("profile.html", user=user, lastPigeons=model.getLastPigeonsByUser(user['idUser'], 0), page=0, otherProfilePicture=otherProfilePicture)
    else:
        return render_template("profileEdit.html", user=model.getUserbyPseudo(session['pseudo']))

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)