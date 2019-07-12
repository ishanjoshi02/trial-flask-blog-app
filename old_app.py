from flask import Flask, render_template, redirect
from flask import request

from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf.csrf import CSRFProtect

from flask_login import LoginManager, login_required, login_user, logout_user, current_user

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.user import UserModel
from models.blog import BlogModel

from forms import RegisterForm, LoginForm

database_uri = "mysql://root:toor2019@localhost:3306/sys"
engine = create_engine(database_uri)

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

login_manager = LoginManager()

csrf = CSRFProtect()

app = Flask(__name__)

app.config.from_object('config')
app.config.from_pyfile('instance/config.py')

csrf.init_app(app)

login_manager.init_app(app)
login_manager.login_view = "/login"


@app.route("/")
@login_required
def hello():
    user_id = current_user.user_id
    blogs = session.query(BlogModel).filter(BlogModel.author == user_id)
    return render_template("index.html", name=current_user.name, blogs=blogs)

# def is_logged_in(a_func):

#     def internal_function():


#         a_func()
#     if current_user and current_user.is_authenticated:
#         return redirect('/')
#     return internal_function

@login_manager.user_loader
def load_user(user_id):
    if user_id:
        return session.query(UserModel).get(user_id)
    else:
        return None


@app.route("/login", methods=["GET", "POST"])
# @is_logged_in
def login():

    if current_user.is_authenticated:
        return redirect('/')
        # Handle User input code (if request.form)
    form = LoginForm()
    errors = {}
    if len(form.errors) != 0:
        errors.update(form.errors)

    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data
        query = session.query(UserModel).filter(UserModel.username == username)
        for row in query:
            if row.password == password or check_password_hash(row.password, password):
                login_user(row, remember=True)
                return redirect("/")
            else:
                form.errors['wrong_password'] = ["Wrong Password"]
    elif request.method == "POST":
        print(form.errors)

    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect('/login')


@app.route("/register", methods=["GET", "POST"])
# @is_logged_in
def registerUser():

    if current_user.is_authenticated:
        return redirect('/')

    form = RegisterForm()

    if form.validate_on_submit():
        firstname = form.firstname.data
        lastname = form.lastname.data
        username = form.username.data
        password = form.password.data
        confirm_password = form.confirm_password.data

        if session.query(UserModel).filter(UserModel.username == username).count() > 0:
            form.errors['username_exists'] = ["Username already exists"]
            return render_template("register.html", form=form)

        if password == confirm_password:
                # add user
            new_user = UserModel(
                name=firstname+" "+lastname, username=username, password=generate_password_hash(password))
            new_user.is_authenticated = True
            session.add(new_user)
            session.commit()
            login_user(new_user, remember=True)
            return redirect("/")
        else:
            form.errors['password_dont_match'] = ["Passwords don't match"]
        return render_template("register.html", form=form)

    elif request.form:
        print(form.errors)

    return render_template("register.html", form=form)


@app.route("/blog")
def getBlog():
    # TODO write code to fetch data from database
    blog_id = request.args['id']
    try:
        blog = session.query(BlogModel).get(blog_id)
        author = session.query(UserModel).get(blog.author)

        return render_template("blog.html", name=blog.title, content=blog.content, author=author.name, editable=(blog.author == current_user.user_id), blog_id=blog_id, edited=blog.edited, author_id=author.user_id)
    except AttributeError:
        last_blog_id = session.query(BlogModel).order_by(
            BlogModel.blog_id.desc()).first().blog_id
        if int(blog_id) < last_blog_id:
            return render_template("blog_deleted.html")
        else:
            return render_template("blog_404.html")


@app.route("/newBlog", methods=["GET", "POST"])
@login_required
def newBlog():
    if request.form:
        form = request.form
        print(form)
        title = form['title']
        content = form['content']
        blog = BlogModel(title=title, content=content,
                         author=current_user.user_id)
        session.add(blog)
        session.commit()
        return redirect('/blog?id={}'.format(blog.blog_id))
    else:
        return render_template("post_blog.html")


@app.route("/editBlog", methods=["GET", "POST"])
@login_required
def editBlog():
    blog_id = request.args['id']
    if request.form:
        form = request.form
        print(form)
        title = form['title']
        content = form['content']
        org_blog = session.query(BlogModel).get(blog_id)
        if org_blog.author != current_user.user_id:
            return "Permission Denied"
        session.query(BlogModel).filter(BlogModel.blog_id == blog_id).update({
            "title": title,
            "content": content,
            "edited": True
        })
        session.commit()
        return redirect('/blog?id={}'.format(blog_id))
    else:
        blog = session.query(BlogModel).get(blog_id)
        if blog.author == current_user.user_id:
            return render_template('edit_blog.html', title=blog.title, content=blog.content, blog_id=blog_id)
        else:
            return "Sign in with correct user"


# /blog/:id

@app.route("/deleteBlog", methods=["GET", "POST", "DELETE"])
@login_required
def delete_blog(blog_id):
    blog_id = request.args["id"]
    blog = session.query(BlogModel).get(blog_id)
    if blog.author == current_user.user_id:
        session.query(BlogModel).filter(BlogModel.blog_id == blog_id).delete()
        session.commit()
        return redirect("/")
    return "Permission Denied"


@app.route("/viewUser")
def viewUser():
    try:
        user_id = request.args["id"]
        user = session.query(UserModel).get(user_id)
        name = user.name
        username = user.username
        blogs = session.query(BlogModel).filter(BlogModel.author == user_id)
        if blogs.count() == 0:
            blogs = False
        return render_template("view_user.html", name=name, username=username, blogs=blogs)
    except AttributeError:
        return "User doesn't exist"


if __name__ == '__main__':
    app.run()
