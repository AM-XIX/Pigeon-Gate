from flask import Flask,request,render_template, session
import model

app = Flask(__name__)

pigeons = model.getAllPigeons()

@app.route("/", methods=['GET', 'POST'])
def welcome():
    if model.mydb.is_connected():
        return render_template("welcome.html", pigeons=pigeons);

@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        pseudo = request.form['pseudo']
        password = request.form['password']
        typeProfilePicture = request.form['typeProfilePicture']
        model.newUser(pseudo, password, typeProfilePicture)
        return render_template("welcome.html", pigeons=pigeons, pseudo=pseudo);
    else:
        return render_template("register.html");

@app.route("/login", methods=['POST', 'GET'])
def login():
    if request.method == 'POST':
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


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)