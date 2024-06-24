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

mycursor = mydb.cursor()

@app.route("/", methods=['GET', 'POST'])
def welcome():
    if mydb.is_connected():
        mycursor.execute("SELECT * FROM Pigeon")
        myresult = mycursor.fetchall()
        print(myresult)
    return render_template("welcome.html", pigeons=myresult);


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)