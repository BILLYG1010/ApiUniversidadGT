from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from config import confgig
from datetime import datetime

app = Flask(__name__)
conexion = MySQL(app)

@app.route("/registration", methods = ['POST'])
def register_users():
     cursor = conexion.connection.cursor()
     carnet =  request.json['carnet']
     created_at = datetime.now()

     if len(carnet) > 6:
        return jsonify({'Message': "El carnet no puede tener mas de 6 caracteres"})
    

     sql = """INSERT INTO contestant (carnet,name, last_name, adress, gender,
        phone_number, birth, student_career, registration_date,declamation_date,
        genre_poetry) 
        VALUES ('{0}', '{1}', '{2}', '{3}', '{4}','{5}','{6}', '{7}', '{8}', '{9}','{10}')""".format(
            carnet, request.json['name'], request.json['last_name'],
            request.json['adress'], request.json['gender'], request.json['phone_number'], 
            request.json['birth'], request.json['student_career'], created_at, 
            request.json['declamation_date'], request.json['genre_poetry'])
     
     cursor.execute(sql)
     conexion.connection.commit()

     return jsonify({'Message': "User Registered Successfully"})

@app.route("/contestant")
def list_contestant():

    cursor = conexion.connection.cursor()

    sql =  """SELECT student_career, birth as age, g.Type_genre ,declamation_date
     FROM contestant, genre g WHERE contestant.genre_poetry = g.id;"""
    
    cursor.execute(sql)
    data = cursor.fetchall()
    contestants = []

    for fila in data:
        contestant = {'student_career':fila[0], 'age':fila[1], 'Type_genre':fila[2],
         'declamation_date':fila[3]}
        contestants.append(contestant)


    return jsonify({'contestant:':contestants, 'message': "List contestants"})
        
def page_not_found(error):
    return "<h1> The page you're trying to search for doesn't exist...<h1>" ,404

if __name__ == '__main__':
    app.config.from_object(confgig['development'])
    app.register_error_handler(404,page_not_found)
    app.run()
