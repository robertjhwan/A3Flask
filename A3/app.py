from flask import Flask, session, redirect, url_for, escape, request, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

app=Flask(__name__)
app.secret_key='abbas'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///a3.db'
db = SQLAlchemy(app)

@app.route('/')
def index():
	# if the user is already logged in, just take them directly to home page. If not, redirect them to the login page.
	if 'utorid' in session:
		return render_template('index.html')
	else:
		return redirect(url_for('login'))

@app.route('/login',methods=['GET','POST'])
def login():
	# first check if the user is in session. If they are, they will be automatically redirected instead of having to log in twice.
	if 'utorid' in session:
			return render_template('index.html')
	# first retrieve the data that includes all users and their passwords.
	elif request.method=='POST':
		sql = """
			SELECT *
			FROM users
			"""
		results = db.engine.execute(text(sql))
		for result in results:
			# make sure that the username and password actually matches up. If it does, redirect them to the home page
			if result['utorid']==request.form['utorid']:
				if result['password']==request.form['password']:
					session['utorid']=request.form['utorid']
					return render_template('index.html')
				else:
					# wrong username or password
					return render_template('login.html', wrong = "You have entered the wrong username or password")
			# wrong username or password
			else:
				return render_template('login.html', wrong = "You have entered the wrong username or password")
	# if the user clicked submit without actually entering anything at all
	elif request.method == 'GET':
		return render_template('login.html', wrong = "")
	# for any other cases we haven't checked, it will just reload an empty login page
	else:
		return render_template('login.html', wrong = "")

@app.route('/signup',methods=['GET','POST'])
def sign_up():
	if request.method=='POST':
		# a very simple query to add values into the database. After it is done, it will redirect to the login page,
		# like how all the other webpage does it.
		utorid = request.form['utorid']
		password = request.form['password']
		sql1 = """
				INSERT INTO users
				VALUES ('{}', '{}', 's')
				""".format(utorid, password)
		results = db.engine.execute(text(sql1))
		sql1 = """
				INSERT INTO marks
				VALUES ('{}', 0,0,0,0,0)
				""".format(utorid)
		results = db.engine.execute(text(sql1))

		return redirect(url_for('login'))
	elif request.method=='GET':
		return render_template('signup.html')

@app.route('/marks', methods=['GET', 'POST'])
def marks():
	if 'utorid' in session:
		# select the type of user in order for us to know what to query for the user
		sql1 = """
			SELECT type
			FROM users
			where utorid='{}'""".format(session['utorid'])
		results = db.engine.execute(text(sql1))
		# if student, retrieve all the data for that user alone
		if results == "s":
			sql1 = """
				SELECT *
				FROM marks
				where utorid='{}'""".format(session['utorid'])	
			results = db.engine.execute(text(sql1))
			
			return render_template('marksStudent.html',results=results)
		# if instructor, retrieve all the data for all users
		elif results == "i":
			sql1 = """
				SELECT *
				FROM marks""".format()
			results = db.engine.execute(text(sql1))
			# it should also display the database for all the remark requests that are available
			sql1 = """
			SELECT *
			FROM remarks
			"""
			results2 = db.engine.execute(text(sql1))

			return render_template('marksInstructor.html',results=results, results2=results2)
	else:
		return redirect(url_for('login'))

@app.route('/changeMarks', methods=['GET', 'POST'])
def changeMarks():
	if 'utorid' in session:
		if request.method == 'POST':
			# a query to update the mark of a particular student
			assign = request.form["assign"]
			mark = request.form["mark"]
			utorid = request.form["utorid"]

			sql1 = """
				UPDATE marks
				SET '{}' = '{}'
				where utorid='{}'""".format(assign, mark, utorid)
			results = db.engine.execute(text(sql1))
			return redirect(url_for('marks'))
		elif request.method == 'GET':
			return redirect(url_for('changeMarks'))
	else:
		return redirect(url_for('login'))


@app.route('/remark',methods=['GET','POST'])
def remark():
    if 'utorid' in session:
        if request.method == 'POST':
            utorid = request.form['utorid']
            evaluation = request.form['evaluation']
            explanation = request.form['explanation']
            sql1 = """
                    INSERT INTO remarks
                    VALUES ('{}', '{}', '{}')
                    """.format(utorid, evaluation, explanation)
            results = db.engine.execute(text(sql1))
            return redirect(url_for('marks'))
        elif request.method=='GET':
            return redirect(url_for('marks'))
    else:
        return redirect (url_for ('login'))

@app.route('/feedback')
def feedback():
	if 'utorid' in session:
		# select the type of user in order for us to know what to query for the user
		sql1 = """
			SELECT type
			FROM users
			where utorid='{}'""".format(session['utorid'])
		results = db.engine.execute(text(sql1))
		# if the user is a student, they can submit a anon feedback form
		if results == "s":
			if request.method == 'POST':
				utorid = request.form['utorid']
				q1 = request.form['q1']
				q2 = request.form['q2']
				sql1 = """
						INSERT INTO feedback
						VALUES ('{}', '{}', '{}')
						""".format(utorid, q1, q2)
				results = db.engine.execute(text(sql1))
				return redirect(url_for('index'))
			# if nothing on the form is entered (yet), it will load the form again
			else:
				return render_template('feedbackStudent.html')
		# if it is an instructor, then the database just need to be shown accordingly
		elif results == "i":
			sql1 = """
					SELECT *
					FROM feedback
					where utorid='{}'""".format(session['utorid'])
			results = db.engine.execute(text(sql1))
			return render_template('feedbackInstructor.html', results = results)
	else:
		return redirect(url_for('login'))

@app.route('/assignment')
def assignment():
	if 'utorid' in session:
		render_template('assignment.html')
	else:
		return redirect(url_for('login'))

@app.route('/announcements')
def annoucements():
	if 'utorid' in session:
		render_template('annoucements.html')
	else:
		return redirect(url_for('login'))

@app.route('/calender')
def calender():
	if 'utorid' in session:
		render_template('calender.html')
	else:
		return redirect(url_for('login'))

@app.route('/slides')
def slides():
	if 'utorid' in session:
		render_template('slides.html')
	else:
		return redirect(url_for('login'))

@app.route('/tests')
def tests():
	if 'utorid' in session:
		render_template('tests.html')
	else:
		return redirect(url_for('login'))

@app.route('/resources')
def resources():
	if 'utorid' in session:
		render_template('resources.html')
	else:
		return redirect(url_for('login'))

@app.route('/courseteam')
def courseteam():
	if 'utorid' in session:
		render_template('courseteam.html')
	else:
		return redirect(url_for('login'))

@app.route('/logout')
def logout():
	session.pop('utorid', None)
	return redirect(url_for('login'))

if __name__=="__main__":
	app.run(debug = True,host='0.0.0.0')
