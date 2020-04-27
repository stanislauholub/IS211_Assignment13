#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from flask import Flask, render_template, request, redirect, url_for
import sqlite3
app = Flask(__name__)


# PART I - DATABASE SETUP AND INITIALIZATION

conn = sqlite3.connect('hw13.db')

cur = conn.cursor()
cur.execute('CREATE TABLE IF NOT EXISTS student(std_id INTEGER PRIMARY KEY AUTOINCREMENT, first_name TEXT, last_name TEXT)')
cur.execute('CREATE TABLE IF NOT EXISTS result(res_id INTEGER, std_id INTEGER, quiz_id INTEGER, marks INTEGER, PRIMARY KEY(res_id), FOREIGN KEY(quiz_id) REFERENCES quiz(quiz_id), FOREIGN KEY(std_id) REFERENCES student(std_id))')
cur.execute('CREATE TABLE IF NOT EXISTS quiz(quiz_id INTEGER PRIMARY KEY AUTOINCREMENT, subject TEXT, number_of_questions TEXT, Date TEXT)')
conn.close()

print('Data inserted successfully...')

global mylist, task, email, periority, list1


# PART II - TEACHER LOGIN

@app.route('/', methods = ['POST', 'GET'])
def index():
    return render_template('teacherlogin.html')
    return redirect('/login')

@app.route('/login', methods = ['POST', 'GET'])
def login():
    value = ""
    if request.method == 'POST':
        name = request.form['name']
        password = request.form['password']
        if name == 'admin' and password == 'password':
            return redirect('/dashboard')
        else:
            value = 'Invalid username or Password'
            return render_template('teacherlogin.html', value = value)


# PART III - DASHBOARD: VIEW STUDENTS AND QUIZZES IN THE CLASS

@app.route('/dashboard', methods = ['POST', 'GET'])
def dashboard():
    conn = sqlite3.connect('hw13.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM student')
    data = cur.fetchall()
    cur.execute('SELECT * FROM quiz')
    data2 = cur.fetchall()
    print('data: ', data)
    print('Data2: ', data2)
    if request.method == 'POST':
        return render_template('addStudent.html')
    return render_template('dashboard.html', data = data, data2 = data2)


# PART IV - ADD STUDENTS TO THE CLASS

@app.route('/student/add', methods = ['POST', 'GET'])
def addStudent():
    fName = ""
    lName = ""
    dt = ()
    if request.method == 'POST':
        fName = request.form['firstName']
        lName = request.form['lastName']
        if fName != "" and lName != "":
            query = '''INSERT INTO student (first_name,last_name) VALUES (?, ?);'''
            dt = (fName, lName)
            conn = sqlite3.connect('hw13.db')
            cur = conn.cursor()
            cur.execute(query, dt)
            conn.commit()
            print('Data inserted successfully...')
            return redirect('/dashboard')
        else:
            value = 'Data has not been added. Please fill up the form correctly...'
            return render_template('addStudent.html', value = value)
    return render_template('addStudent.html')


# PART V - ADD QUIZZES TO THE CLASS

@app.route('/quiz/add', methods = ['POST', 'GET'])
def addQuiz():
    print('"Add Quiz" has been called...')
    subject = ""
    noq = ""
    date = ""
    dt1 = ()
    if request.method == 'POST':
        print('Add Post Called')
        subject = request.form['subject']
        noq = request.form['noq']
        date = request.form['date']
        print('sub:', subject)
        print('noq: ',noq)
        print('Date: ',date)
        if subject != "" and noq != "" and date != "":
            print('"If" has beein called...')
            query = '''INSERT INTO quiz (subject, number_of_questions, Date) VALUES (?, ?, ?);'''
            dt1 = (subject, noq,date)
            conn = sqlite3.connect('hw13.db')
            cur = conn.cursor()
            cur.execute(query, dt1)
            conn.commit()
            print('Data inserted Successfully...')
            return redirect('/dashboard')
        else:
            value = 'Data has not been added. Please fill up the form correctly...'
            return render_template('addQuiz.html', value = value)
    return render_template('addQuiz.html')
    

# PART VI - VIEW QUIZ RESULTS

@app.route('/student/<string:std_id>', methods=['POST', 'GET'])
def studentid(std_id):
    conn = sqlite3.connect('hw13.db')
    cur = conn.cursor()
    query ='''SELECT result.quiz_id, quiz.Date, quiz.subject, result.marks, result.res_id FROM result left join quiz on quiz.quiz_id=result.quiz_id WHERE result.std_id=?'''
    cur.execute(query, std_id)
    data = cur.fetchall()
    if len(data) > 0:
        return render_template('ViewQuizResult.html', data = data)
    else:
        return 'No Records Found...'


# PART VII - ADD A STUDENT’S QUIZ RESULT

@app.route('/results/add', methods = ['POST', 'GET'])
def AddResult():
    print('Add result...')
    conn = sqlite3.connect('hw13.db')
    cur = conn.cursor()
    cur.execute('SELECT * FROM student')
    data = cur.fetchall()
    cur.execute('SELECT * FROM quiz')
    data1 = cur.fetchall()
    cur.close()
    print('Data: ', type(data))
    print('Data1: ', type(data1))

    if request.method == 'POST':
        std_id = request.form['student']
        quiz_id = request.form['quiz']
        marks = request.form['marks']
        print('Student ID: ',std_id)
        print('Quiz ID: ', quiz_id)
        print('Marks', marks)
        markint = int(marks)
        if std_id != "" and quiz_id != "" and markint > 0 and markint <= 100:
            cur = conn.cursor()
            query = '''INSERT INTO result (std_id, quiz_id, marks) VALUES (?, ?, ?);'''
            dt1 = (std_id, quiz_id, marks)
            cur.execute(query,dt1)
            conn.commit()
            cur.close()
            return redirect('/dashboard')
        else:
            value = 'Data has not been submitted. Please enter marks between 0 - 100...'
            return render_template('AddResult.html', data = data, data1 = data1, value = value)
    else:
        return render_template('AddResult.html', data = data, data1 = data1)


# ADDITIONAL OPTIONS PART: DELETIONS 

# STUDENT DELETION

@app.route('/deleteStudent', methods=['GET', 'POST'])
def deleteStudent():
    id = ""
    if request.method == 'POST':
        id = request.form['std_id']
        sql = 'DELETE FROM student WHERE std_id=?'
        conn = sqlite3.connect('hw13.db')
        cur = conn.cursor()
        cur.execute(sql, id)
        conn.commit()
        cur.close()
        return redirect('/dashboard')
    

# QUIZ DELETION    

@app.route('/deleteQuiz', methods = ['GET', 'POST'])
def deleteQuiz():
    id = ""
    if request.method == 'POST':
        id=request.form['quiz_id']
        sql = 'DELETE FROM quiz WHERE quiz_id=?'
        conn = sqlite3.connect('hw13.db')
        cur = conn.cursor()
        cur.execute(sql, id)
        conn.commit()
        cur.close()
        return redirect('/dashboard')

    
# RESULT DELETION

@app.route('/deleteResult', methods = ['GET', 'POST'])
def deleteResult():
    id = ""
    if request.method == 'POST':
        id=request.form['res_id']
        if request.method == 'POST':
            id = request.form['res_id']
            sql = 'DELETE FROM result WHERE res_id=?'
            conn = sqlite3.connect('hw13.db')
            cur = conn.cursor()
            cur.execute(sql, id)
            conn.commit()
            cur.close()
            return render_template('ViewQuizResult.html')
    return render_template('ViewQuizResult.html')


# ANONYMOUS VIEW OF QUIZ RESULTS

@app.route('/anyquiz', methods = ['POST', 'GET'])
def anyquiz():
    print("Any Quiz")
    if request.method == 'POST':
        quiz_id = request.form['quizid']
        str1 = '/quiz/'+quiz_id+'/results'
        return redirect(str1)
    
    
# NON-LOGGED IN USER

@app.route('/quiz/<string:quiz_id>/results', methods = ['POST', 'GET'])
def noLoggedResult(quiz_id):
        query = '''Select result.std_id,result.marks from result where result.quiz_id=?'''
        conn = sqlite3.connect('hw13.db')
        cur = conn.cursor()
        cur.execute(query, quiz_id)
        data = cur.fetchall()
        if len(data) > 0:
            return render_template('nonLoggedResult.html', data = data)
        else:
            return 'No results found...'

if __name__ == '__main__':
    app.debug = True
    app.run()

