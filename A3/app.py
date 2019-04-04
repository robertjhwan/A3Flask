from flask import Flask, session, redirect, url_for, escape, request, render_template
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.sql import text

app=Flask(__name__)
app.secret_key='abbas'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///a3.db'
db = SQLAlchemy(app)

results = None

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
		password = request.form['utorid']
		sql1 = """
				INSERT INTO users
				VALUES ('{}', '{}', 'student')
				""".format(utorid, password)
		results = db.engine.execute(text(sql1))
		sql1 = """
				INSERT INTO users
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
					SELECT *
					FROM marks
					where utorid='{}'""".format(session['utorid'])
		results = db.engine.execute(text(sql1))
		return render_template('marks.html',results=results)
	else:
		return redirect(url_for('login'))

# "INERT INTO users VALUES ('{}', '{}', 'stu')".format(var1, var2)
# text(sql).autocommit = true

@app.route('/logout')
def logout():
	session.pop('utorid', None)
	return redirect(url_for('login'))

if __name__=="__main__":
	app.run(debug=True,host='0.0.0.0')

