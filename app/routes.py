from app import app, db
from flask import render_template, flash, redirect, url_for, request, Markup, jsonify
from app.forms import RegistrationForm, LoginForm, PostForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, Post
from werkzeug.urls import url_parse

@app.route('/')
def index():
    posts = Post.query.order_by(Post.upvotes.desc())
    return render_template('index.html', title='Home', posts=posts)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash('You are logged-in already')
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(Markup('Congratulations, you are now a registered user! Please <a href="/login" class="alert-link">login</a>'))
        # flash(Markup('Your post is now <a href="/" class="alert-link">live</a>!'))
        return redirect(url_for('index'))

    return render_template('register.html', title='Register', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You are logged-in already')
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')

        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        flash('Successfully logged-in!')
        return redirect(next_page)

    #  url is parsed with "url_parse" to determine is the netloc component is present
    # to avoid malitious hacker attacks

    return render_template('login.html', title='Login', form=form)

@app.route('/post', methods=['GET', 'POST'])
@login_required
def post():
    form=PostForm()
    if form.validate_on_submit():
        post = Post(body=form.post.data, author=current_user, upvotes=0)
        db.session.add(post)
        db.session.commit()
        flash(Markup('Your post is now <a href="/" class="alert-link">live</a>!'))
        # flash('Your post is now live!')
        return redirect(url_for('post'))
    return render_template('/post.html', title='Post', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/ulk')
def ulk():
    ppp = request.args.get('p', type=int)
    lpost = Post.query.filter_by(id=ppp).first()
    if lpost.upvotes is None:
        lpost.upvotes = 1
    else:
        lpost.upvotes += 1
    db.session.commit()
    return jsonify(result=ppp)

@app.route('/profile')
def profile():
    return "Profile page"