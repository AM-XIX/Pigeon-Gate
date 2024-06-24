from flask import Flask,request,render_template, jsonify,abort
import random
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

@app.route("/", methods=['GET', 'POST'])
def welcome():
    if mydb.is_connected():
        mycursor.execute("SELECT * FROM Pigeon")
        testLogin = mycursor.fetchall()
    return render_template("welcome.html", pigeons=testLogin);

@app.route("/login")
def login():
    return render_template("login.html");

@app.route("/register")
def register():
    return render_template("register.html");

@app.route("/register_user", methods=['POST'])
def register_user():
    if request.method == 'POST':
        pseudo = request.form['pseudo']
        password = request.form['password']
        mycursor.execute("INSERT INTO User (pseudo, password) VALUES (%s, %s)", (pseudo, password))
        mydb.commit()
        return render_template("welcome.html");

@app.route("/login_user", methods=['POST'])
def login_user():
    if request.method == 'POST':
        pseudo = request.form['pseudo']
        password = request.form['password']
        mycursor.execute("SELECT * FROM User WHERE pseudo = %s AND password = %s", (pseudo, password))
        testLogin = mycursor.fetchall()
        mycursor.execute("SELECT * FROM Pigeon")
        resultPigeon = mycursor.fetchall()
        if testLogin:
            return render_template("welcome.html", pigeons=resultPigeon);
        else:
            return render_template("login.html");



if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)