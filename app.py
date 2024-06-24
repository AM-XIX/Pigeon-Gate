from flask import Flask,request,render_template, jsonify,abort
import random
import mysql.connector

app = Flask(__name__)

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="rootroot",
    database="pigeon-gate"
)

mycursor = mydb.cursor()

jeux=[]
typesJeu = ["Plateforme", "RPG", "FPS", "Aventure", "Stratégie"]

@app.route("/", methods=['GET', 'POST'])
def welcome():
    mycursor.execute("SELECT * FROM users")
    users = mycursor.fetchall()
    print(users)


@app.route("/saisie-jeu", methods=['GET', 'POST'])
def saisieJeu():
    if request.method == 'POST':
        nom = request.form['nom']
        typejeu = request.form['types']
        prix = request.form['prix']
        description = request.form['description']
        jeux.append({'nom':nom, 'typeJeu':typejeu, 'prix':prix, 'description':description})
    return render_template("saisieJeu.html", typesJeu=typesJeu);

@app.route("/delete/<id>", methods=['GET'])
def delete(id):
    jeux.remove(jeux[int(id)])
    return render_template("welcome.html", jeux=jeux, message="Un jeu a été supprimé");

@app.route("/infos/<id>", methods=['GET', 'POST'])
def infos(id):
    return render_template("infos.html", jeu=jeux[int(id)]);

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)