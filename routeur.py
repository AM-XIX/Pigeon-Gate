from flask import Flask,request,render_template, session
import model

app = Flask(__name__)

app.config.from_object('config.Config')
pigeons = model.getAllPigeons()


@app.route("/", methods=['GET', 'POST'])
def welcome():
    if model.mydb.is_connected():
        session.clear()
        return render_template("welcome.html", pigeons=pigeons);

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST' and 'pseudo' not in session:
        pseudo = request.form['pseudo']
        password = request.form['password']
        typeProfilePicture = request.form['typeProfilePicture']
        model.getUserbyPseudo(pseudo)
        if model.getUserbyPseudo(pseudo):
            messageErrorRegister = "Pseudo déjà utilisé"
            return render_template("register.html", messageErrorRegister=messageErrorRegister);
        else:
            session['pseudo'] = pseudo
            model.newUser(pseudo, password, typeProfilePicture)
            return render_template("welcome.html", pigeons=pigeons, pseudo=pseudo);
    else:
        return render_template("register.html");

@app.route("/login", methods=['POST', 'GET'])
def login():
    print(session)
    if request.method == 'POST' and 'pseudo' not in session:
        pseudo = request.form['pseudo']
        password = request.form['password']
        if model.checkLogin(pseudo, password):
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
        model.addPigeon(request.form['prenom'], request.form['couleur'], request.form['noteWalk'], request.form['notevibe'], request.form['noteoriginalite'], request.form['place'], request.form['urlPhoto'], session['pseudo'])
        return render_template("welcome.html", pigeons=pigeons);
    else:
        return render_template("new_pigeon.html");

@app.route("/logout", methods=['POST', 'GET'])
def logout():
    session.clear()
    return render_template("welcome.html", pigeons=pigeons);

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)