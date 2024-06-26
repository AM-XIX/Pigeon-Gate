from flask import Flask,request,render_template, session, jsonify, redirect, url_for
from flask_bcrypt import Bcrypt
import model

app = Flask(__name__)
bcrypt = Bcrypt(app)

app.config.from_object('config.Config')


@app.route("/", methods=['GET', 'POST'])
def welcome():
    if model.mydb.is_connected():
        session.clear()
        pigeonsBdd = model.getTrendingPigeons()
        return render_template("welcome.html", pigeons=pigeonsBdd);

@app.route("/accueil", methods=['GET', 'POST'])
def accueil():
    if model.mydb.is_connected():
        pigeonsBdd = model.getTrendingPigeons()
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
            model.newUser(pseudo, password, typeProfilePicture)
            pigeonsBdd = model.getAllPigeons()
            session['idUser'] = model.getUserbyPseudo(pseudo)['idUser']
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
        elif model.getUserbyPseudo(pseudo)==None:
            messageErrorLogin = "Pseudo ou mot de passe incorrect"
            return render_template("login.html", messageErrorLogin=messageErrorLogin);
        elif session['pseudo'] != None:
            messageErrorLogin = "Vous êtes déjà connecté"
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

@app.route("/profil", methods=['GET'])
def profil():
    otherProfilePicture = ['profile1', 'profile2', 'profile3', 'profile4']
    if 'pseudo' not in session:
        return render_template("login.html")
    user = model.getUserbyPseudo(session['pseudo'])
    otherProfilePicture.remove(user['typeProfilePicture'])
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
    
@app.route("/edit-profile", methods=['POST', 'GET'])
def editProfile():
    if 'pseudo' not in session:
        return render_template("login.html")
    otherProfilePicture = ['profile1', 'profile2', 'profile3', 'profile4']
    user = model.getUserbyPseudo(session['pseudo'])
    currentProfilePicture = user['typeProfilePicture']
    if request.method == 'POST':
        if 'typeProfilePicture' in request.form:
            newPP = request.form['typeProfilePicture']
            model.changeProfilePicture(session['idUser'], newPP)
            currentProfilePicture = newPP
        if 'bio' in request.form or 'pseudo' in request.form:
            newBio = request.form['bio']
            model.changeBio(session['idUser'], newBio)
            newPseudo = request.form['pseudo']
            if newPseudo != session['pseudo'] and model.getUserbyPseudo(newPseudo)==None:
                model.changePseudo(session['idUser'], newPseudo)
                session['pseudo'] = newPseudo
            else:
                return render_template("profileEdit.html", user=user, otherProfilePicture=otherProfilePicture)
        user = model.getUserbyPseudo(session['pseudo'])
        lastPigeons = model.getLastPigeonsByUser(user['idUser'], 0)
        page = request.args.get('page', default=0, type=int)
        return render_template("profile.html", user=user, lastPigeons=lastPigeons, page=page, otherProfilePicture=[pic for pic in otherProfilePicture if pic != currentProfilePicture])
    otherProfilePicture = [pic for pic in otherProfilePicture if pic != currentProfilePicture]
    return render_template("profileEdit.html", user=user, otherProfilePicture=otherProfilePicture)


@app.route("/galery", methods=['GET'])
def galery():
    if 'pseudo' not in session:
        pseudo = None
    else:
        pseudo = session['pseudo']
    pigeons = model.getAllPigeons()
    return render_template("galery.html", pigeons=pigeons, pseudo=pseudo);

@app.route("/about", methods=['GET'])
def about():
    pigeonBdd = model.getCardPigeonsById()
    return render_template("cardPigeon.html", pigeon=pigeonBdd);

@app.route("/pigeon/<idPigeon>", methods=['GET'])
def cardPigeon(idPigeon):
    pigeon = model.getCardPigeonsById(idPigeon)
    user = model.getUserbyId(pigeon['idUser'])
    comments = model.getCommentsByIdPigeon(idPigeon, user['idUser'])
    randomPigeons = model.getFourRandomPigeons(idPigeon)
    if 'idUser' not in session:
        userConnected = None
        return render_template("cardPigeon.html", pigeon=pigeon, user=user, comments=comments, randomPigeons=randomPigeons, userConnected=userConnected);
    userConnected = model.getUserbyId(session['idUser'])
    return render_template("cardPigeon.html", pigeon=pigeon, user=user, userConnected=userConnected, comments=comments, randomPigeons=randomPigeons);

@app.route("/pigeon/<int:idPigeon>/comment", methods=['POST'])
def addComment(idPigeon):
    if 'idUser' not in session:
        return redirect(url_for('login'))
    textCom = request.form.get('comment')
    idUser = session['idUser']
    model.addComment(textCom, idUser, idPigeon)
    showCommentForm = request.args.get('showCommentForm', 'False') == 'True'
    randomPigeons = model.getFourRandomPigeons(idPigeon)
    return render_template("cardPigeon.html", pigeon=model.getCardPigeonsById(idPigeon), user=model.getUserbyId(idUser), comments=model.getCommentsByIdPigeon(idPigeon, idUser), randomPigeons=randomPigeons, showCommentForm=showCommentForm)

@app.route("/pigeon/<int:idPigeon>/rate", methods=['POST'])
def addRate(idPigeon):
    if 'idUser' not in session:
        return redirect(url_for('login'))
    idUser = session['idUser']
    noteWalk = int(request.form['notewalk'])
    noteVibe = int(request.form['notevibe'])
    noteOriginalite = int(request.form['noteoriginalite'])
    model.addRatePigeon(idPigeon, noteWalk, noteVibe, noteOriginalite)
    randomPigeons = model.getFourRandomPigeons(idPigeon)
    return render_template("cardPigeon.html", pigeon=model.getCardPigeonsById(idPigeon), user=model.getUserbyId(idUser), comments=model.getCommentsByIdPigeon(idPigeon, idUser), randomPigeons=randomPigeons)

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)