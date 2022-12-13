from crypt import methods
import email
from flask import Flask,render_template,redirect,url_for,session,flash
from requests import request
from sqlalchemy import true

from app import DB_HOST, DB_NAME, DB_PASS, DB_USER
app=Flask(__name__)
import psycopg2
import psycopg2.extras

app.secret_key="dadsaheb"
DB_HOST = "localhost"
DB_NAME = "test"
DB_USER ="postgres"
DB_PASS = "dada"

conn =psycopg2.connect(dbname=DB_HOST,host=DB_NAME,name=DB_USER,password=DB_PASS)

@app.route('/')
def index():
    if 'username' in session:
        cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        s=('select * from demo')
        cur.execute(s)
        list_users =cur.fetchall
        return render_template('index.html',list_users=list_users, username=session['username'])
    return redirect(url_for('login'))

@app.route('/login',methods=['POST','GET'])
def login():
    if request.method =='POST':
        username =request.form['username']
        password =request.form['password']
        cur =conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
        s=("selct * from demo where fname='"+username+"' and email = '"+password+"'")
        cur.execute(s)
        data =cur.fetchall
        for i in data:
            if username == i[2] and password==i[3]:
                session['username']=True
                session['username']=password
                return redirect(url_for('index'))
            else:
                flash("Username and Password is incorrect")
        return redirect(url_for('login'))
@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/add_student')
def add_student():
    if 'username' in session:
        if request.methods=='POST':
            fname =request.form['fname']
            lname =request.form['lname']
            email =request.form['email']
            cur=conn.cursor(cursor_factory=psycopg2.extras.DictCursor)
            cur.execute=("insert into data (fname,lname,email) VALUES=(%s,%s,%s)",(fname,lname,email))
            conn.commit()
            flash("student added suceessfully")
            return redirect(url_for('index'))
        return redirect(url_for('login'))
    return redirect(url_for('login'))

if __name__=="__main__":
    app.run()

