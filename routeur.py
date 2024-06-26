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
        pigeons = model.getAllPigeons()
        return render_template("welcome.html", pigeons=pigeons);

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
            session['idUser'] = model.getUserbyPseudo(pseudo);
            model.newUser(pseudo, password, typeProfilePicture)
            pigeons = model.getAllPigeons()
            return render_template("welcome.html", pigeons=pigeons, pseudo=pseudo);
    else:
        return render_template("register.html");

@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST' and 'pseudo' not in session:
        pseudo = request.form['pseudo']
        password = request.form['password']
        if model.checkLogin(pseudo, password):
            session['idUser'] = model.getUserbyPseudo(pseudo)['idUser']
            session['pseudo'] = pseudo
            pigeons = model.getAllPigeons()
            return render_template("welcome.html", pigeons=pigeons, pseudo=pseudo);
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
        model.addPigeon(request.form['prenom'], request.form['couleur'], request.form['noteWalk'], request.form['notevibe'], request.form['noteoriginalite'], request.form['place'], request.form['urlPhoto'], session['pseudo'])
        pigeons = model.getAllPigeons()
        return render_template("welcome.html", pigeons=pigeons);
    else:
        return render_template("new_pigeon.html");

@app.route("/logout", methods=['POST', 'GET'])
def logout():
    session.clear()
    pigeons = model.getAllPigeons()
    return render_template("welcome.html", pigeons=pigeons);

@app.route("/profil", methods=['POST', 'GET'])
def profil():
    if 'pseudo' not in session:
        return render_template("login.html") 
    user = model.getUserbyPseudo(session['pseudo'])
    page = request.args.get('page', default=0, type=int)
    lastPigeons = model.getLastPigeonsByUser(user['idUser'], page)
    return render_template("profile.html", user=user, lastPigeons=lastPigeons, page=page)

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
    if 'pseudo' not in session:
        return render_template("login.html")
    if request.method == 'POST' and 'pseudo' in session:
        newBio = request.form['bio']
        model.changeBio(session['idUser'], newBio)
        user = model.getUserbyPseudo(session['pseudo'])
        return render_template("profile.html", user=user, lastPigeons=model.getLastPigeonsByUser(user['idUser'], 0), page=0)
    else:
        return render_template("profileEdit.html", user=model.getUserbyPseudo(session['pseudo']))


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)