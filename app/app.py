
import re  
import os
from flask import Flask, render_template, request, redirect, url_for, session
from flask_mysqldb import MySQL
from datetime import datetime
import MySQLdb.cursors

app = Flask(__name__) 

app.secret_key = 'abcdefgh'
  
app.config['MYSQL_HOST'] = 'db'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'password'
app.config['MYSQL_DB'] = 'cs353hw4db'
  
mysql = MySQL(app)  

@app.route('/')

@app.route('/login', methods =['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM User WHERE username = % s AND password = % s', (username, password, ))
        user = cursor.fetchone()
        if user:              
            session['loggedin'] = True
            session['userid'] = user['id']
            session['username'] = user['username']
            session['email'] = user['email']
            message = 'Logged in successfully!'
            return redirect(url_for('tasks'))
        else:
            message = 'Please enter correct email / password !'
    return render_template('login.html', message = message)


@app.route('/register', methods =['GET', 'POST'])
def register():
    message = ''
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form :
        username = request.form['username']
        password = request.form['password']
        email = request.form['email']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM User WHERE username = % s', (username, ))
        account = cursor.fetchone()
        if account:
            message = 'Choose a different username!'
  
        elif not username or not password or not email:
            message = 'Please fill out the form!'

        else:
            cursor.execute('INSERT INTO User (id, username, email, password) VALUES (NULL, % s, % s, % s)', (username, email, password,))
            mysql.connection.commit()
            message = 'User successfully created!'

    elif request.method == 'POST':

        message = 'Please fill all the fields!'
    return render_template('register.html', message = message)

@app.route('/tasks', methods =['GET', 'POST'])
def tasks():
    message = ''
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * FROM Task WHERE user_id = %s ORDER BY deadline;', (session['userid'],))
    tasks = cursor.fetchall()

    cursor.execute('SELECT * FROM Task WHERE user_id = %s AND status = \'Done\' ORDER BY done_time;', (session['userid'],))
    completed = cursor.fetchall()
    cursor.execute('SELECT * FROM TaskType;')
    types = cursor.fetchall()
    return render_template('tasks.html', tasks=tasks, completed=completed, message=message, session=session, types = types)

@app.route('/add_task', methods =['POST'])
def add_task():
    message = ''
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if not session['loggedin']:
        message = 'Please log in first'
    else:
        if request.method == 'POST' and 'task_type' in request.form:
            cursor.execute('SELECT * FROM TaskType WHERE type = % s', (request.form['task_type'], ))
            type = cursor.fetchone()
            if not type:
                message = 'Invalid task type'
        if request.method == 'POST' and 'title' in request.form and 'description' in request.form and 'deadline_time' in request.form and 'deadline_date' in request.form and 'task_type' in request.form:
            now = datetime.now()
            current_time = now.strftime("%Y-%m-%d %H:%M:%S")
            deadline = request.form['deadline_date'] + ' ' + request.form['deadline_time']
            cursor.execute('''
            INSERT INTO Task(
                title,
                description,
                status,
                deadline,
                creation_time,
                done_time,
                user_id,  
                task_type
            ) VALUES(
                %s,
                %s,
                'Todo',
                %s,
                %s,
                NULL,
                %s,
                %s
            );
            ''', (request.form['title'],request.form['description'],deadline,current_time,session['userid'],request.form['task_type'],))

            mysql.connection.commit()
            message = 'success'
    return redirect(url_for('tasks'))


@app.route('/delete/<int:id>', methods =['GET'])
def delete(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if session['loggedin']:
        cursor.execute('DELETE FROM Task WHERE id = %s;', (id,))
        mysql.connection.commit()
    return redirect(url_for('tasks'))

@app.route('/complete/<int:id>', methods =['GET'])
def complete(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")
    if session['loggedin']:
        cursor.execute('UPDATE Task SET status=\'Done\', done_time=%s WHERE id = %s;', (current_time, id,))
        mysql.connection.commit()
    return redirect(url_for('tasks'))

@app.route('/uncomplete/<int:id>', methods =['GET'])
def uncomplete(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if session['loggedin']:
        cursor.execute('UPDATE Task SET status=\'Todo\', done_time=NULL WHERE id = %s;', (id,))
        mysql.connection.commit()
    return redirect(url_for('tasks'))

@app.route('/update', methods =['POST'])
def update():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    if session['loggedin'] and 'title' in request.form and 'description' in request.form and 'task_type' in request.form and 'deadline_time' in request.form and 'deadline_date' in request.form:
        cursor.execute('UPDATE Task SET title=%s WHERE id=%s;', (request.form['title'], session['selected']['id'],))
        cursor.execute('UPDATE Task SET description = %s WHERE id = %s;', (request.form['description'],session['selected']['id'],))
        cursor.execute('UPDATE Task SET task_type = %s WHERE id = %s;', (request.form['task_type'],session['selected']['id'],))
        deadline = request.form['deadline_date'] + ' ' + request.form['deadline_time']
        cursor.execute('UPDATE Task SET deadline = %s WHERE id = %s;', (deadline,session['selected']['id'],))
        mysql.connection.commit()
        session['selected'] = None

    
    return redirect(url_for('tasks'))

@app.route('/select/<int:id>', methods =['GET'])
def select(id):
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    
    cursor.execute('SELECT * FROM Task WHERE id = %s;', (id,))
    task = cursor.fetchone()
    
    session['selected'] = task
    
    return redirect(url_for('tasks'))

@app.route('/cancel', methods =['GET'])
def cancel():
    session['selected'] = None
    
    return redirect(url_for('tasks'))

@app.route('/logout', methods =['GET'])
def logout():
    session['loggedin'] = False
    session['userid'] = ""
    session['username'] = ""
    session['email'] = ""
    session['selected']= None
    
    return redirect(url_for('login'))


@app.route('/analysis', methods =['GET', 'POST'])
def analysis():
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    # List the title and latency of the tasks that were completed after their deadlines (for the user).
    cursor.execute('''SELECT title, done_time - deadline AS latency 
                        FROM Task 
                        WHERE user_id = %s 
                        AND status = 'Done' 
                        AND done_time > deadline;''', (session['userid'],))
    latencies = cursor.fetchall()
    # Give the average task completion time of the user.
    cursor.execute('''SELECT AVG(TIMESTAMPDIFF(SECOND, creation_time, done_time)) AS average
                        FROM Task
                        WHERE user_id = %s AND status=\'Done\';''', (session['userid'],))
    average_completion = cursor.fetchone()
    # List the number of the completed tasks per task type, in descending order (for the user).
    cursor.execute('SELECT task_type, COUNT(id) AS count FROM Task WHERE user_id = %s AND status=\'Done\' GROUP BY task_type;', (session['userid'],))
    task_counts = cursor.fetchall()
    # List the title and deadline of uncompleted tasks in increasing order of deadlines (for the user).
    cursor.execute('SELECT title, deadline FROM Task WHERE user_id = %s AND status = \'Todo\' ORDER BY deadline;', (session['userid'],))
    uncompleted = cursor.fetchall()
    # List the title and task completion time of the top 2 completed tasks that took the most time, in descending order (for the user). (You can use the LIMIT clause).
    cursor.execute('''SELECT title, done_time - creation_time AS completion_time 
                            FROM Task 
                            WHERE user_id = %s AND status = 'Done' 
                        ORDER BY done_time - creation_time DESC
                        LIMIT 2;''', (session['userid'],))
    top_completions = cursor.fetchall()

    return render_template('analysis.html', session=session, latencies=latencies, average_completion=average_completion,task_counts=task_counts,uncompleted=uncompleted, top_completions=top_completions)

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
