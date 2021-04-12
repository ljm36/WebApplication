from typing import List, Dict
import simplejson as json
from flask import Flask, request, Response, redirect
from flask import render_template
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

app = Flask(__name__)
mysql = MySQL(cursorclass=DictCursor)

app.config['MYSQL_DATABASE_HOST'] = 'db'
app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'root'
app.config['MYSQL_DATABASE_PORT'] = 3306
app.config['MYSQL_DATABASE_DB'] = 'snakeData'
mysql.init_app(app)


@app.route('/', methods=['GET'])
def index():
    user = {'username': 'snake Project'}
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM snake_count_100')
    result = cursor.fetchall()
    return render_template('index.html', title='Home', user=user, snakes=result)


@app.route('/view/<int:snake_id>', methods=['GET'])
def record_view(snake_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM snake_count_100 WHERE id=%s', snake_id)
    result = cursor.fetchall()
    return render_template('view.html', title='View Form', snake=result[0])


@app.route('/edit/<int:snake_id>', methods=['GET'])
def form_edit_get(snake_id):
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM snake_count_100 WHERE id=%s', snake_id)
    result = cursor.fetchall()
    return render_template('edit.html', title='Edit Form', city=result[0])


@app.route('/edit/<int:snake_id>', methods=['POST'])
def form_update_post(snake_id):
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('Game_Number'), request.form.get('Game_Length'), snake_id)
    sql_update_query = """UPDATE snake_count_100 t SET t.Game_Number = %s, t.Game_Length = %s WHERE t.id = %s """
    cursor.execute(sql_update_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)

@app.route('/snakes/new', methods=['GET'])
def form_insert_get():
    return render_template('new.html', title='New Game Form')


@app.route('/snakes/new', methods=['POST'])
def form_insert_post():
    cursor = mysql.get_db().cursor()
    inputData = (request.form.get('Game_Number'), request.form.get('Game_Length'))
    sql_insert_query = """INSERT INTO snake_count_100 (Game_Number,Game_Length) VALUES (%s, %s) """
    cursor.execute(sql_insert_query, inputData)
    mysql.get_db().commit()
    return redirect("/", code=302)

@app.route('/delete/<int:snake_id>', methods=['POST'])
def form_delete_post(snake_id):
    cursor = mysql.get_db().cursor()
    sql_delete_query = """DELETE FROM snake_count_100 WHERE id = %s """
    cursor.execute(sql_delete_query, snake_id)
    mysql.get_db().commit()
    return redirect("/", code=302)


@app.route('/api/v1/snakes', methods=['GET'])
def api_browse() -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM snake_count_100')
    result = cursor.fetchall()
    json_result = json.dumps(result)
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/snakes/<int:snake_id>', methods=['GET'])
def api_retrieve(snake_id) -> str:
    cursor = mysql.get_db().cursor()
    cursor.execute('SELECT * FROM snake_count_100 WHERE id=%s', snake_id)
    result = cursor.fetchall()
    json_result = json.dumps(result)
    resp = Response(json_result, status=200, mimetype='application/json')
    return resp


@app.route('/api/v1/snakes/', methods=['POST'])
def api_add() -> str:
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/v1/snakes/<int:snake_id>', methods=['PUT'])
def api_edit(snake_id) -> str:
    resp = Response(status=201, mimetype='application/json')
    return resp


@app.route('/api/snakes/<int:snake_id>', methods=['DELETE'])
def api_delete(snake_id) -> str:
    resp = Response(status=210, mimetype='application/json')
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)