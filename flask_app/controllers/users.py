from crypt import methods
from flask import render_template, request, redirect, session, flash
from flask_app import app
from flask_app.models.user import User
from flask_app.models.product import Product
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return redirect('/form')


@app.route('/register/user', methods=["POST"])
def register_user():
    if not User.validate_user(request.form):
        return redirect('/')
    data ={
        "first_name": request.form['first_name'],
        "last_name": request.form['last_name'],
        "email": request.form['email'],
        "password": bcrypt.generate_password_hash(request.form['password'])
    }
    id = User.save(data)
    session['user_id'] = id
    return redirect('/form')

@app.route('/form')
def form():
    return render_template("form.html")


@app.route('/login', methods=["POST"])
def login():
    user = User.get_email(request.form)
    if not user:
        flash("Invalid Email","login")
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash("Invalid Password","login")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/dashboard')

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect('/logout')
    data ={
        'id': session['user_id']
    }
    return render_template("dashboard.html", user=User.get_by_id(data))


@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')


@app.route('/add/<int:product_id>')
def add_product(product_id):
        if 'user_id' in session:
            Product.add_product(product_id)
        return redirect('/')

@app.route('/cart/<int:id>')
def checkout():
    return render_template("checkout.html")
