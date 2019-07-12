from flask import Flask, render_template, redirect, make_response, flash
from flask import request

from werkzeug.security import generate_password_hash, check_password_hash
from flask_wtf.csrf import CSRFProtect

from flask_login import LoginManager, login_required, login_user, logout_user, current_user

from flask_restful import Resource, Api

import json
import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models.user import UserModel
from models.blog import BlogModel

from forms import RegisterForm, LoginForm, BlogForm

from instance.config import db_connection_url

# database_uri = "mysql://root:toor2019@flaskdemoinstance.c0x127jnab22.ap-south-1.rds.amazonaws.com:3306/sys"
database_uri = db_connection_url
engine = create_engine(database_uri)

Session = sessionmaker()
Session.configure(bind=engine)
session = Session()

login_manager = LoginManager()

csrf = CSRFProtect()

app = Flask(__name__)
api = Api(app)
app.config.from_object('config')
app.config.from_pyfile('instance/config.py')


login_manager.init_app(app)
login_manager.login_view = '/login'


@app.route("/")
@login_required
def index():
    user_id = current_user.id
    blogs = session.query(BlogModel).filter(
        BlogModel.author == current_user.id).filter(BlogModel.deleted_on == None)
    return render_template("index.html", name=current_user.name, blogs=blogs)


@login_manager.user_loader
def load_user(user_id):
    if user_id:
        return session.query(UserModel).get(user_id)
    else:
        return None


@app.route("/login", methods=["GET", "POST"])
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
                flash("")
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
            flash("")
            return redirect("/")
        else:
            form.errors['password_dont_match'] = ["Passwords don't match"]
        return render_template("register.html", form=form)

    elif request.form:
        print(form.errors)

    return render_template("register.html", form=form)


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


def output_html(html, code=200):
    headers = {'Content-Type': 'text/html'}
    return make_response(html, code, headers)


# /blog/new
# /blog/id/edit

@app.route('/blog/<int:id>/edit', methods=["POST", "GET"])
@login_required
def editBlog(id):
    blog_id = id
    org_blog = session.query(BlogModel).get(blog_id)
    form = BlogForm()
    if form.validate_on_submit():
        name = form['title'].data
        content = form['content'].data
        if org_blog.author != current_user.id:
            return "Permission Denied"
        session.query(BlogModel).filter(BlogModel.id == blog_id).update({
            "name": name,
            "content": content,
            "edited_on": datetime.datetime.now()
        })

        session.commit()
        flash("Blog edited successfully")
        return redirect("/blog/%d" % id)
    else:
        blog = session.query(BlogModel).get(blog_id)
        if blog.author == current_user.id:
            form.title.data = blog.name
            form.content.data = blog.content
            return render_template('edit_blog.html', title=blog.name, content=blog.content, blog_id=blog_id, form=form)
        else:
            return "Sign in with correct user"


@app.route('/blog/new', methods=["GET", "POST"])
@login_required
def newBlog():
    form = BlogForm()
    if form.validate_on_submit():
        print(form)
        title = form['title'].data
        content = form['content'].data
        blog = BlogModel(name=title, content=content,
                         author=current_user.id, created_on=datetime.datetime.now())
        session.add(blog)
        session.commit()
        return redirect('/blog/{}'.format(blog.id))
    else:
        return render_template("post_blog.html", form=form)


@app.route("/dashboard")
def dashboard():
    return render_template(
        'dashboard.html'
    )


class BlogList(Resource):

    def get(self, start, end):
        ret_val = []
        blogs = session.query(BlogModel).filter(
            BlogModel.deleted_on == None).all()
        print(len(blogs))
        if len(blogs) < end:
            end = len(blogs)
        for i in range(start, end, 1):
            print(i)
            blog = blogs[i]
            temp = blog.getDict()
            temp['author'] = session.query(
                UserModel).get(temp['author']).name
            ret_val.append(temp)

        return ret_val


@app.route("/user/<int:id>")
def viewUser(id):
    user_id = id
    try:
        user = session.query(UserModel).get(user_id)
        name = user.name
        username = user.username
        blogs = session.query(BlogModel).filter(
            BlogModel.author == user_id).filter(BlogModel.deleted_on == None)
        if blogs.count() == 0:
            blogs = False
        return render_template("view_user.html", name=name, username=username, blogs=blogs)
    except AttributeError:
        return "User doesn't exist"


class Blog(Resource):

    def get(self, id):
        blog_id = id
        try:
            blog = session.query(BlogModel).get(id)
            author = session.query(UserModel).get(blog.author)
            if blog.deleted_on:
                return output_html(render_template("blog_deleted.html"))
            editable = False
            try:
                editable = (blog.author == current_user.id)
            except AttributeError:
                pass
            return output_html(render_template("blog.html", name=blog.name, content=blog.content, author=author.name, editable=editable, blog_id=blog_id, edited=False, author_id=author.id), 200)
        except AttributeError:
            return output_html(render_template('blog_404.html'), 404)

    def delete(self, id):
        print(id)
        blog_id = id
        blog = session.query(BlogModel).get(id)
        if blog.author == current_user.id:
            session.query(BlogModel).filter(
                BlogModel.id == blog_id).update({
                    "deleted_on": datetime.datetime.now()
                })
            session.commit()
            flash("Blog deleted successfully!")
            return True
        return "Permission Denied"


api.add_resource(BlogList, '/blog/<int:start>/<int:end>')
api.add_resource(Blog, '/blog/<int:id>')

if __name__ == '__main__':
    app.run()
