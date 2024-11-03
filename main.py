# my very own (microblog) v0.0
from pysondb import db
from flask import Flask, render_template, request, redirect
from markdown import markdown
from flask_simplelogin import SimpleLogin, is_logged_in
from datetime import datetime
from fileinput import filename

app = Flask(__name__)

# DO NOT DO THIS IN ANY CIRCUMSTANCES.
app.config['SECRET_KEY'] = 'put your own here'
app.config['SIMPLELOGIN_LOGIN_URL'] = '/login/'
app.config['SIMPLELOGIN_LOGOUT_URL'] = '/logout/'
app.config['SIMPLELOGIN_HOME_URL'] = '/main'

def supersecrethuh(user):
    if user.get('username') == 'admin' and user.get('password') == 'admin':
       return True
    return False

SimpleLogin(app, login_checker=supersecrethuh)
# ----------------------------------- #

database = db.getDb("./db.json")

@app.route('/')
def home():
    # i hate you pysondb
    return render_template('index.html', data=database.getAll()[:5][::-1], number=1)

@app.route('/page/<int:pagenumber>')
def page(pagenumber):
    if pagenumber <= 1:
        return redirect("/")
    # pysondb is my enem-b
    return render_template('index.html', data=database.getAll()[5*pagenumber:][:5][::-1], number=pagenumber)

@app.route('/post/<int:id>')
def post(id):
    if not id:
        return redirect("/")
    return render_template('post.html', data=database.getById(id))

@app.route('/main', methods=['GET', 'POST'])
def add():
    if is_logged_in():
        if request.method == 'POST':
            database.add({
                "title":request.form['title'],
                "date": datetime.today().strftime('%Y-%m-%d'),
                "description": request.form['description'],
                "content": markdown(request.form['content']),
                "original-content": request.form['content']
            })
            return redirect('/main')
        return render_template('main.html')
    return redirect('/login')

@app.route('/manage', methods=['GET', 'POST'])
def manage():
    if is_logged_in():
        if request.method == 'POST':
            if request.form['delete']:
                database.deleteById(request.form['delete'])
                return redirect('/manage')
        return render_template('manage.html', data=database.getAll()[::-1])
    return redirect('/login')

@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    if is_logged_in():
        if request.method == 'POST':
            database.updateById(id, {
                "title": request.form['title'],
                "description": request.form['description'],
                "content": markdown(request.form['content']),
                "original-content": request.form['content']
            })
            return redirect('/manage')
        return render_template('edit.html', data=database.getById(id))
    return redirect('/login')

if __name__ == '__main__':
    app.run(port=3000, debug=True)