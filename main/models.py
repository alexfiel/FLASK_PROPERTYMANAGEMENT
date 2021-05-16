from datetime import datetime
from sqlalchemy.orm import backref
#import flask_whooshalchemy as wa
from main import db, login_manager, app
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    password= db.Column(db.String(60), nullable=False)
    role=db.Column(db.String(50), nullable=False, default='User')
    is_admin = db.Column(db.Boolean, default=False)
    projects = db.relationship('Project', backref='author', lazy=True)

    def __repr__(self):
        return f"User('{self.username}','{self.email}','{self.image_file}')"

class Person(db.Model):
    __abstract__=True
    __tablename__='person'
    id = db.Column(db.Integer, primary_key=True, nullable = False)
    lastname = db.Column(db.String(50), nullable=False)
    firstname = db.Column(db.String(50), nullable=False)
    middlename = db.Column(db.String(50), nullable =True)
    dateofbirth = db.Column(db.DateTime, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    civilstatus = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    contact = db.Column(db.String(20), nullable = False)
    perm_address=db.Column(db.String(150), nullable = False)
    present_Address =db.Column(db.String(150), nullable=False)
    spouse_name = db.Column(db.String(100), nullable = False)
    education = db.Column(db.String(50), nullable = False)
    sourceofincome = db.Column(db.String(50), nullable=False)
    estimatedincome = db.Column(db.String(100), nullable=False)
    company_name = db.Column(db.String(150), nullable=False)
    company_address = db.Column(db.String(150), nullable=False)
    company_contact = db.Column(db.String(50), nullable=False)
    posted_by = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    date_posted= db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    

    def __repr__(self):
        return f"Person('{self.firstname}','{self.lastname}','{self.email}')"


class SalesPerson(db.Model):
    __tablename__='salesperson'
    id = db.Column(db.Integer, primary_key=True, nullable = False)
    lastname = db.Column(db.String(50), nullable=False)
    firstname = db.Column(db.String(50), nullable=False)
    middlename = db.Column(db.String(50), nullable =True)
    dateofbirth = db.Column(db.DateTime, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    civilstatus = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    contact = db.Column(db.String(20), nullable = False)
    perm_address=db.Column(db.String(150), nullable = False)
    present_Address =db.Column(db.String(150), nullable=False)
    designation = db.Column(db.String(30), nullable=False)
    realty_id=db.Column(db.Integer, db.ForeignKey('realty.id'),nullable=False)
    clients = db.relationship('Customer',backref='client', lazy='dynamic')

    def __repr__(self):
        return f"SalesPerson('{self.id}')"


class Customer(db.Model):
    __tablename__='customer'
    id = db.Column(db.Integer, primary_key=True, nullable = False)
    lastname = db.Column(db.String(50), nullable=False)
    firstname = db.Column(db.String(50), nullable=False)
    middlename = db.Column(db.String(50), nullable =True)
    dateofbirth = db.Column(db.DateTime, nullable=False)
    gender = db.Column(db.String(10), nullable=False)
    civilstatus = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    contact = db.Column(db.String(20), nullable = False)
    perm_address=db.Column(db.String(150), nullable = False)
    present_Address =db.Column(db.String(150), nullable=False)
    sp_id = db.Column(db.Integer, db.ForeignKey('salesperson.id'),nullable=False)
    owner = db.relationship('Product', backref='buyer', lazy="dynamic" )

    def __repr__(self):
        return f"Customer('{self.id}','{self.lastname}')"


class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(60), unique=True, nullable=False)
    description = db.Column(db.Text, nullable=False)
    price = db.Column(db.Float, nullable=False)
    project = db.Column(db.Integer, db.ForeignKey('project.id'), nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customer.id'), nullable=False)
    
    def __repr__(self):
        return f"Product('{self.name}','{self.description}')"


class Project(db.Model):
    __searchable__ = ['name', 'description','location', 'category']

    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name = db.Column(db.String(60), unique=True, nullable=False)
    category = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(60), nullable=False)
    description = db.Column(db.Text, nullable=False)
    owner = db.Column(db.String(60), nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.png')
    date_posted= db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False)
    products = db.relationship('Product', backref='product', lazy=True)

    def __repr__(self):
        return f"Project('{self.name}','{self.location}','{self.description}','{self.category}','{self.date_posted}')"



class Realty(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    name=db.Column(db.String(150), nullable=False)
    email=db.Column(db.String(60), nullable=False)
    contact=db.Column(db.String(15), nullable=False)
    logo_file = db.Column(db.String(20), nullable=False, default='default.png')
    brokername=db.Column(db.String(50), nullable=False)
    prcnumber=db.Column(db.String(50),nullable=False)
    sales_person = db.relationship('SalesPerson', backref='salesperson', lazy=True)

    def __repr__(self):
        return f"Realty('{self.name}','{self.brokername}')"


#wa.whoosh_index(app,Project)











    

