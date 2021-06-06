from datetime import timedelta
import os
import secrets
from PIL import Image
from flask import Flask, render_template,url_for, flash, redirect, request, abort
from wtforms.validators import URL
from main import app, db, bcrypt
from main import form
from main.form import RealtyForm, RegistrationForm, LoginForm, UpdateAccountForm, ProjectForm
from main.models import User, Project, Realty
from flask_login import login_user, current_user, logout_user, login_required

@app.route('/',methods=['GET','POST'])
@app.route('/home',methods=['GET','POST'])
def home():
    projects = Project.query.all()
   # project_image=url_for('static', filename='profilepics/' + projects.image_file)
    return render_template('home.html',projects=projects)


@app.route('/realty',methods=['GET','POST'])
def realty():
    realties = Realty.query.all()
    return render_template('realty_list.html',realties=realties)
    

@app.route('/about')
def about():
    return render_template('about.html', title='About')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash('Your account has been ceated! You are now able to log in','success' )
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember= form.remember.data)
            next_page=request.args.get('next')
            return redirect(next_page)if next_page else redirect(url_for('home'))
        else:
            flash('Login failure, Please check username and password', 'danager')
    return render_template('login.html', title='Login', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext 
    picture_path = os.path.join(app.root_path, 'static/profilepics', picture_fn)
    
    output_size = (125, 125)
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

def save_picture_project(form_picture_project):
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture_project.filename)
    picture_fn = random_hex + f_ext 
    picture_path = os.path.join(app.root_path, 'static/profilepics', picture_fn)
    
    output_size = (125, 125)
    i = Image.open(form_picture_project)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn

@app.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form=UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Account has been updated!','success')
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file=url_for('static', filename='profilepics/' + current_user.image_file)
    return render_template('account.html', title='Account', 
                            image_file=image_file, form=form)


@app.route('/project/new', methods=['GET', 'POST'])
@login_required
def new_project():
    form = ProjectForm()
    if form.validate_on_submit():                      
        project = Project(name=form.name.data, location=form.location.data, 
                            owner=form.owner.data,category=form.category.data,
                            description=form.description.data,author=current_user)
        
        db.session.add(project)
        db.session.commit()
        flash('New Project has been saved', 'success')
        return redirect(url_for('home'))
    return render_template('create_project.html', title='New Project', 
                            form=form, legend='New Project')


@app.route('/realty/new', methods=['GET', 'POST'])
@login_required
def new_realty():
    form = RealtyForm()
    if form.validate_on_submit():
        realty=Realty(name=form.name.data,email=form.email.data,
                        address=form.address.data,contact=form.contact.data,
                        brokername=form.brokername.data,prcnumber=form.prcnumber.data)
        db.session.add(realty)
        db.session.commit()
        flash('New Realty has been registered', 'success')
        return redirect(url_for('realty'))
    return render_template('create_realty.html', title='Register New Realty', 
                            form=form, legend='New Realty')


@app.route('/project/<int:proj_id>')
def project(proj_id):
    project = Project.query.get_or_404(proj_id)
    return render_template('project.html',title=project.name, project=project)


@app.route('/search', methods=['GET', 'POST'])
def search_project():
    if request.method =='POST' and 'tag' in request.form:
        tag = request.form["tag"]
        search = "%{}%".format(tag)
        project = Project.query.filter(Project.name.like(search))
        return render_template('search_project.html', projects=project, tag=tag)
    return render_template('search_project.html',title='Search')


@app.route('/project/<int:proj_id>/delete', methods=['POST'])
@login_required
def delete_project(proj_id):
    project = Project.query.get_or_404(proj_id)
    if current_user.is_admin != True:
        abort(403)
    db.session.delete(project)
    db.session.commit()
    flash('Project has been deleted!','success')
    return redirect(url_for('home')) 


@app.route('/project/<int:proj_id>/update', methods=['GET', 'POST'])
@login_required
def update_project(proj_id):
    project = Project.query.get_or_404(proj_id)
    if current_user.is_admin != True:
        abort(403)
    form = ProjectForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            project.image_file = picture_file
        project.name=form.name.data
        project.location =form.location.data
        project.category = form.category.data
        project.owner=form.owner.data
        project.description = form.description.data
        db.session.commit()
        flash('Project has been updated!','success')
        return redirect(url_for('project', proj_id=project.id)) 
    elif request.method == 'GET':
        form.name.data = project.name
        form.location.data = project.location
        form.category.data = project.category
        form.owner.data = project.owner
        form.description.data = project.description
    return render_template('create_project.html', title='Update Project', 
                            form=form, legend='Update Project')

