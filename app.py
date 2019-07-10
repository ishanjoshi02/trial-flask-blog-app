from flask import Flask, render_template, redirect
from flask import request

from flask_login import LoginManager, login_required, login_user, logout_user, current_user

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
    user_id = current_user.user_id
    blogs = session.query(BlogModel).filter(BlogModel.author==user_id)
    for blog in blogs:
        print(blog)
    return render_template("index.html",name=current_user.name, blogs=blogs)


@login_manager.user_loader
def load_user(user_id):
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
    blog_id = request.args['id']
    blog = session.query(BlogModel).get(blog_id)
    author = session.query(UserModel).get(blog.author)
    return render_template("blog.html", name=blog.title, content=blog.content, author=author.name)

@app.route("/newBlog", methods=["GET", "POST"])
@login_required
def newBlog():
    print("hello")
    if request.form:
        form = request.form
        print(form)
        title = form['title']
        content = form['content']
        blog = BlogModel(title=title, content=content,author=current_user.user_id)
        session.add(blog)
        session.commit()
        return redirect('/blog?id={}'.format(blog.blog_id))
    else:
        return render_template("post_blog.html")