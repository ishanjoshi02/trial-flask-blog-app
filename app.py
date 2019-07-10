from flask import Flask, render_template, redirect
from flask import request

from flask_login import LoginManager, login_required, login_user, logout_user

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


from models.user import UserModel
from models.blog import BlogModel

database_uri = "mysql://root:toor2019@localhost:3306/sys"
engine = create_engine(database_uri)

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

login_manager = LoginManager()

app = Flask(__name__)

app.config.from_object('config')
app.config.from_pyfile('instance/config.py')

login_manager.init_app(app)

@app.route("/")
@login_required
def hello():
    print(login_manager.user())
    return render_template("index.html",)


@login_manager.user_loader
def load_user(user_id):
    print(user_id)
    if user_id:
       return session.query(UserModel).get(user_id)
        
       
    else:
        return None
@app.route("/login", methods=["GET" ,"POST"])
def login():
        # Handle User input code (if request.form)
    if request.form:


        form = request.form
        username = form['username']
        password = form['password']

        query = session.query(UserModel).filter(UserModel.username==username)
        
        for row in query:
            
            if row.password == password:
                login_user(row)
                return redirect("/")

    return render_template("login.html")

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/login')

@app.route("/register", methods=["GET", "POST"])
def registerUser():

    if request.form:

        form = request.form
        
        firstname = form["firstname"]
        lastname = form["lastname"]
        username = form["username"]
        password = form["password"]
        confirm_password = form["confirm_password"]

        if password == confirm_password:
            # add user
            new_user = UserModel(name=firstname+" "+lastname, username=username, password=password)
            new_user.is_authenticated=True
            session.add(new_user)
            session.commit()
            print(new_user.user_id)
            login_user(new_user)
            return redirect("/")

    return render_template("register.html")


@app.route("/blog")
def getBlog():
    # TODO write code to fetch data from database
    id = request.args['id']
    print(id)
    return render_template("blog.html", name="Ishan's Blog", content="Lorem Ipsum", release_date="10th July 2019", author="Ishan Joshi")

@app.route("/newBlog", methods=["GET", "POST"])
@login_required
def newBlog(user_id):
    if request.form:

        blog = Blog()
    else:
        return render_template("post_blog.html")