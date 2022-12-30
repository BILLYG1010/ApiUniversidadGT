from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from config import confgig
from datetime import datetime, timedelta
import calendar 

app = Flask(__name__)
conexion = MySQL(app)

@app.route("/registration", methods = ['POST'])
def register_contestants():

     cursor = conexion.connection.cursor()
     carnet =  request.json['carnet']
     created_at = datetime.now()
     genre_poetry = request.json['genre_poetry']
    
     def carnet_has_0(cadena):
        for char in cadena:
            if char == "0":
                return True
        return False
     
     def carnet_finish(cadena):
        if cadena[5] == "1":
           return True
        elif cadena[5] == "3":
            return True
        elif cadena[5] == "9":
            return True
        else:
            return False         

     def generator_date_declamation(number):
        if number == "1" and genre_poetry == 3:
            now = datetime.now()
            new_date = now + timedelta(days = 5)

            if new_date.weekday() == 5:
                date_finaly = new_date + timedelta(days=2)
                return date_finaly
            elif new_date.weekday() == 6:
                date_finaly = new_date + timedelta(days=1)
                return date_finaly

        elif number == "3" and genre_poetry == 2:
            mes = datetime.now().month
            anio = datetime.now().year
            ultimo_day = calendar.monthrange(anio, mes)
            string_date = "{0}/{1}/{2}".format(anio,mes,ultimo_day[1])
            new_date =datetime.strptime(string_date,"%Y/%m/%d")

            if new_date.weekday() == 5:
                date_finaly = new_date + timedelta(days=2)
                return date_finaly
            elif new_date.weekday() == 6:
                date_finaly = new_date + timedelta(days=1)
                return date_finaly
        else:
            now = datetime.now()
            while now.weekday() != 4 :
                now = now + timedelta(days=1)
                if now.weekday()== 4:
                    return now 
        return new_date

     if len(carnet) == 6:
        if carnet[0] == "A" and carnet[2] == "5" and carnet_has_0(carnet) == False and carnet_finish(carnet) == True:

            sql = """INSERT INTO contestant (carnet,name, last_name, adress, gender,
            phone_number, birth, student_career, registration_date,declamation_date,
            genre_poetry) 
            VALUES ('{0}', '{1}', '{2}', '{3}', '{4}','{5}','{6}', '{7}', '{8}', '{9}','{10}')""".format(
                carnet, request.json['name'], request.json['last_name'],
                request.json['adress'], request.json['gender'], request.json['phone_number'], 
                request.json['birth'], request.json['student_career'], created_at, generator_date_declamation(carnet[5]),
                request.json['genre_poetry'])
        
            cursor.execute(sql)
            conexion.connection.commit()

            return jsonify({'Message': "contestant Registered Successfully"})
     
     else:
        return  jsonify({'Message': "El carnet debe tener 6 caracteres,"})

     return jsonify({'Message': "El carnet debe comenzar con 'A', el tercer caracter debe ser 5, el ultimo 1, 3 o 9 y no debe tener '0',"})
       
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
