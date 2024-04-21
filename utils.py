from flask import Flask, render_template, request, redirect, url_for, session
import bcrypt
from db_util import *


def hash_password(password):
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password.decode('utf-8')


def check_password(hashed_password, password):
    password1 = password.encode('utf-8')
    return bcrypt.checkpw(password1, hashed_password.encode('utf-8'))


def check_role(user_id):
    try:
        connection = connect_to_db()
        cursor = connection.cursor()
        cursor.execute("""SELECT * FROM instadmin WHERE user_id = %s""", (user_id,))
        response = cursor.fetchone()
        close_connection(connection)
        print("admin ", response)
        if response:
            return "admin"
        else:
            connection = connect_to_db()
            cursor = connection.cursor()
            cursor.execute("""SELECT * FROM teacher WHERE user_id = %s""", (user_id,))
            response = cursor.fetchone()
            close_connection(connection)
            print("teacher ", response)
            if response:
                return "teacher"
            else:
                connection = connect_to_db()
                cursor = connection.cursor()
                cursor.execute("""SELECT * FROM student WHERE user_id = %s""", (user_id,))
                response = cursor.fetchone()
                close_connection(connection)
                print("student ", response)
                if response:

                    return "student"
    except (Exception, psycopg2.Error) as error:
        print("Error : ", error)

def role(role_argument):
    if role_argument == 'admin':
        return redirect(url_for('admin'))
    elif role_argument == 'teacher':
        return redirect(url_for('teacher'))
    else:
        return redirect(url_for('home'))