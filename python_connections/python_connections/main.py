import pymysql
from werkzeug.security import generate_password_hash

from app import app
from db import mysql
from flask import jsonify
from flask import flash, request


# READ the data
@app.route('/users/')
def users():
    try:
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT user_id id, user_name name, user_email email, user_password pwd FROM user")
        #user_name name aliasing
        rows = cursor.fetchall()
        resp = jsonify(rows)
        resp.status_code = 200
        return resp
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

@app.route('/user/<int:id>/')
def user(id):
    try:
        msg = {
            'status': 404,
            'message': 'User not Found: ' + request.url,
        }
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT user_id id, user_name name, user_email email FROM user WHERE user_id = %s", id)
        rows = cursor.fetchall()
        resp = jsonify(rows)
        print(resp)
        resp.status_code = 200
        if resp:
            resp.id = id
            return resp
        else:
            return msg

    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()



# ADDING THE DATA
@app.route('/add', methods=['POST'])
def add_user():
    global cursor, conn
    try:
        _json = request.json
        _name = _json['name']
        _email = _json['email']
        _password = _json['pwd']
        # validate the received values
        if _name and _email and _password and request.method == 'POST':
            # do not save password as a plain text
            _hashed_password = generate_password_hash(_password)
            # save edits
            sql = "INSERT INTO user(user_name, user_email, user_password) VALUES(%s, %s, %s)"
            #username name->aliasing
            data = (_name, _email, _hashed_password,)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify('User added successfully!')
            resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

#delete the data
@app.route('/user/<int:id>/')
def user(id):
    try:
        msg = {
            'status': 404,
            'message': 'User not Found: ' + request.url,
        }
        conn = mysql.connect()
        cursor = conn.cursor(pymysql.cursors.DictCursor)
        cursor.execute("SELECT user_id id, user_name name, user_email email FROM user WHERE user_id = %s", id)
        rows = cursor.fetchall()
        resp = jsonify(rows)
        print(resp)
        resp.status_code = 200
        if resp:
            resp.id = id
            return resp
        else:
            return msg

    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()

        #upate

@app.route('/update_user', methods=['PUT'])
def update_user():
    global cursor, conn
    try:
        _json = request.json
        _name = _json['name']
        _email = _json['email']
        _password = _json['pwd']
        # validate the received values
        if _name and _email and _password and request.method == 'PUT':
            # do not save password as a plain text
            _hashed_password = generate_password_hash(_password)
            # save edits
            sql = "UPDATE user SET user_name=%s, user_email=%s, user_password=%s WHERE user_id=%s"
            #username name->aliasing
            data = ( id , _name, _email, _hashed_password,)
            conn = mysql.connect()
            cursor = conn.cursor()
            cursor.execute(sql, data)
            conn.commit()
            resp = jsonify('User added successfully!')
            resp.status_code = 200
            return resp
        else:
            return not_found()
    except Exception as e:
        print(e)
    finally:
        cursor.close()
        conn.close()
        


@app.errorhandler(404)
def not_found(error=None):
    message = {
        'status': 404,
        'message': 'Not Found: ' + request.url,
    }
    resp = jsonify(message)
    resp.status_code = 404

    return resp


if __name__ == "__main__":
    app.run(debug=True)
