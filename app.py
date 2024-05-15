from flask import Flask, render_template, request, redirect, url_for
import pymysql
from pymysql.cursors import DictCursor

app = Flask(__name__)

# Database connection details
host_name = "localhost"
port = 3307
user_name = "root"
password = "maria"
database = "db1"

def get_db_connection():
    return pymysql.connect(
        host=host_name,
        port=port,
        user=user_name,
        password=password,
        database=database,
        cursorclass=DictCursor
    )

@app.route('/')
def index():
    con = get_db_connection()
    try:
        with con.cursor() as cursor:
            query = "SELECT * FROM mahasiswa"
            cursor.execute(query)
            results = cursor.fetchall()
            return render_template('index.html', results=results)
    finally:
        con.close()

@app.route('/insert', methods=['GET', 'POST'])
def insert():
    if request.method == 'POST':
        nim = request.form['nim']
        nama = request.form['nama']
        con = get_db_connection()
        try:
            with con.cursor() as cursor:
                query = "INSERT INTO mahasiswa (nim, nama) VALUES (%s, %s)"
                cursor.execute(query, (nim, nama))
                con.commit()
            return redirect(url_for('index'))
        finally:
            con.close()
    return render_template('insert.html')

@app.route('/update', methods=['GET', 'POST'])
def update():
    id = request.args.get('id')
    con = get_db_connection()
    try:
        if request.method == 'POST':
            nim = request.form['nim']
            nama = request.form['nama']
            with con.cursor() as cursor:
                query = "UPDATE mahasiswa SET nim=%s, nama=%s WHERE id=%s"
                cursor.execute(query, (nim, nama, id))
                con.commit()
            return redirect(url_for('index'))
        else:
            with con.cursor() as cursor:
                query = "SELECT * FROM mahasiswa WHERE id=%s"
                cursor.execute(query, (id,))
                result = cursor.fetchone()
            return render_template('update.html', result=result)
    finally:
        con.close()

@app.route('/delete')
def delete():
    id = request.args.get('id')
    con = get_db_connection()
    try:
        with con.cursor() as cursor:
            query = "DELETE FROM mahasiswa WHERE id=%s"
            cursor.execute(query, (id,))
            con.commit()
        return redirect(url_for('index'))
    finally:
        con.close()

if __name__ == '__main__':
    app.run(debug=True)
