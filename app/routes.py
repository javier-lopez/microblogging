from flask import render_template, flash, redirect, url_for, request
from flask_login import login_required, current_user, login_user, logout_user

from app import app, bcrypt, login_manager
from app.models import User, Post
from app.forms  import LoginForm, RegisterForm, PostForm, EditForm, SearchForm
from app.mails  import email_follower_notification

from datetime import datetime

items_per_page = app.config['PAGINATION_SETTINGS']['items_per_page']

@app.route('/',      methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@app.route('/index/<int:page>', methods=['GET', 'POST'])
def index(page=1):
    if current_user.is_authenticated:
        user  = User.objects(email=current_user.email).first()
        posts = user.posts_from_following_users().paginate(page=page, per_page=items_per_page)
        # posts = user.posts_from_following_users()
    else:
        # app.logger.debug('index => user => None')
        user  = None
        posts = Post.objects.paginate(page=page, per_page=items_per_page)

    form = PostForm()
    if request.method == 'POST' and form.validate():
        user = User.objects(email=current_user.email).first()
        post = Post(author=user, body=form.post.data).save()
        #force the browser to issue another request after the form submission
        #avoid untended duplicated posts on refresh actions
        return redirect(url_for('index'))

    return render_template("index.html.j2", title='Inicio', user=user, posts=posts, form=form)

@login_manager.user_loader
def load_user(user_id):
    return User.objects(pk=user_id).first()

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.objects(email=form.email.data).first()
        if user is None:
            flash('El usuario con el correo "{}" no existe'.format(form.email.data))
            return render_template('login.html.j2', title='Iniciar sesión', form=form)
        else:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                user.last_seen = datetime.utcnow()
                return redirect(url_for('index'))
    return render_template('login.html.j2', title='Iniciar sesión', form=form)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if request.method == 'POST' and form.validate():
        user = User.objects(email=form.email.data).first()
        if user is None:
            password_hash =  bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            new_user = User(username=form.username.data,
                        first_name=form.first_name.data,
                        last_name=form.last_name.data,
                        email=form.email.data,
                        password=password_hash,
                        ).save()
            login_user(new_user)
            return redirect(url_for('index'))
        else:
            flash('El usuario con el correo {} ya existe'.format(form.email.data))
    return render_template('register.html.j2', title='Registrarse', form=form)

@app.route('/edit', methods=['GET', 'POST'])
@login_required
def edit():
    form = EditForm()
    if request.method == 'POST' and form.validate():
        user          = User.objects(id=current_user.id).first()
        form_username = User.objects(username=form.username.data).first()
        form_email    = User.objects(email=form.email.data).first()

        if form_username != None and user.id != form_username.id:
            flash('Ya existe un usuario con el mismo nombre, seleccione otro')
            return redirect(url_for('edit'))

        if form_email != None and user.id != form_email.id:
            flash('Ya existe un usuario con el mismo correo, seleccione otro')
            return redirect(url_for('edit'))

        user.username = form.username.data
        user.email    = form.email.data
        user.about_me = form.about_me.data
        user.save()
        flash('Los cambios han sido guardados.')
        return redirect(url_for('edit'))
    else:
        user               = User.objects(email=current_user.email).first()
        form.username.data = user.username
        form.email.data    = user.email
        form.about_me.data = user.about_me
    return render_template('edit.html.j2', form=form)

@app.route('/user/<username>')
@login_required
def user(username):
    user = User.objects(username=username).first()

    if user == None:
        flash('User %s not found.' % username)
        return redirect(url_for('index'))
    posts = Post.objects(author=user.id)
    return render_template('user.html.j2', user=user, posts=posts)

@app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.objects(id=current_user.id).first()
    interesting_user = User.objects(username=username).first()
    if interesting_user is None:
        flash('El usuario "%s" no existe' % username)
        return redirect(url_for('index'))
    if user.id == interesting_user.id:
        flash('No puedes seguirte a ti mismo, ¡sería extraño!')
        return redirect(url_for('user', username=username))

    user.follow(interesting_user).save()
    flash('Ahora sigues a "%s"' % username)
    email_follower_notification(user, interesting_user)
    return redirect(url_for('user', username=username))

@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.objects(id=current_user.id).first()
    annoying_user = User.objects(username=username).first()
    if annoying_user is None:
        flash('El usuario "%s" no existe' % username)
        return redirect(url_for('index'))
    if user.id == annoying_user.id:
        flash('No puedes seguirte a ti mismo, ¡sería extraño!')
        return redirect(url_for('user', username=username))

    user.unfollow(annoying_user).save()
    flash('Has dejado de seguir a "%s"' % username)
    return redirect(url_for('user', username=username))

@app.route('/search', methods=['GET', 'POST'])
@app.route('/search/<pattern>/<int:page>', methods=['GET', 'POST'])
@login_required
def search(pattern=None, page=1):
    form = SearchForm()
    if request.method == 'POST' and form.validate():
        pattern = form.search.data
        return redirect(url_for('search', pattern=pattern, page=page))

    if pattern is not None:
        results = Post.objects.search_text(pattern).paginate(page=page, per_page=items_per_page)
        if not results.items: #results.items is a []
            return render_template('search_not_found.html.j2', pattern=pattern)
        return render_template('search.html.j2', pattern=pattern, posts=results)

    return render_template('search.html.j2', posts=None, form=form)

@app.errorhandler(401)
def not_found_error(error):
    return render_template('401.html.j2'), 401

@app.errorhandler(404)
def not_found_error(error):
    return render_template('404.html.j2'), 404

@app.errorhandler(500)
def internal_error(error):
    db.session.rollback()
    return render_template('500.html.j2'), 500
