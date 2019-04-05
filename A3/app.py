from flask import Flask, session, redirect, url_for, escape, request, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

app=Flask(__name__)
app.secret_key='abbas'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///a3.db'
db = SQLAlchemy(app)

@app.route('/')
def index():
	if 'utorid' in session:
		sql1 = """
					SELECT *
					FROM marks
					where utorid='{}'""".format(session['utorid'])
		results = db.engine.execute(text(sql1))
		return render_template('index.html',results=results)
	else:
		return redirect(url_for('login'))

@app.route('/login',methods=['GET','POST'])
def login():
	if request.method=='POST':
		sql = """
			SELECT *
			FROM users
			"""
		results = db.engine.execute(text(sql))
		for result in results:
			if result['utorid']==request.form['utorid']:
				if result['password']==request.form['password']:
					session['utorid']=request.form['utorid']
					sql1 = """
						SELECT *
						FROM marks
						where utorid='{}'""".format(request.form['utorid'])
					results = db.engine.execute(text(sql1))
					return render_template('marks.html',results=results)
		return "Incorrect UserName/Password"
	elif 'utorid' in session:
			sql1 = """
					SELECT *
					FROM marks
					where utorid='{}'""".format(session['utorid'])
			results = db.engine.execute(text(sql1))
			return render_template('marks.html',results=results)
	elif request.method == 'GET':
		return render_template('login.html')
	else:
		return render_template('login.html')

@app.route('/signup',methods=['GET','POST'])
def sign_up():
	if request.method=='POST':
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
		sql1 = """
			SELECT type
			FROM users
			where utorid='{}'""".format(session['utorid'])
		results = db.engine.execute(text(sql1))
		
		if results == "s":
			sql1 = """
				SELECT *
				FROM marks
				where utorid='{}'""".format(session['utorid'])	
			results = db.engine.execute(text(sql1))
			return render_template('marksStudent.html',results=results)

		elif results == "i":
			sql1 = """
				SELECT *
				FROM marks""".format()	
			results = db.engine.execute(text(sql1))
			return render_template('marksInstructor.html',results=results)
	else:
		return redirect(url_for('login'))

@app.route('/changeMarks', methods=['GET', 'POST'])
def changeMarks():
	if 'utorid' in session:
		if request.method == 'POST':
			assign = request.form["assign"]
			mark = request.form["mark"]
			utorid = request.form["utorid"]

			sql1 = """
				UPDATE marks
				SET '{}' = '{}'
				where utorid='{}'""".format(assign, mark, utorid)
			results = db.engine.execute(text(sql1))

			return render_template('marksInstructor.html')
		elif request.method == 'GET':
			render_template('marksInstructor.html')
	else:
		return redirect(url_for('login'))


@app.route('/assignment')
def assignment():
	if 'utorid' in session:
		render_template('assignment.html')
	else:
		return redirect(url_for('login'))


@app.route('/logout')
def logout():
	session.pop('utorid', None)
	return redirect(url_for('login'))

if __name__=="__main__":
	app.run(debug=True,host='0.0.0.0')

