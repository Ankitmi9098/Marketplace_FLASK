from re import S
import flask
from flask.helpers import flash
from market import app
from flask import render_template, redirect, url_for, flash, request
from market.models import Item, User
from market.forms import RegisterForm, LoginForm, PurchaseItemForm, SellItemForm
from market import db
from flask_login import login_user, logout_user, login_required, current_user


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/market', methods = ['GET', 'POST'])
@login_required
def market():
    purchase_form = PurchaseItemForm()
    selling_form = SellItemForm()
    if request.method == "POST":
        # Purchase Item Logic
        purchased_item = request.form.get('purchased_item')
        p_item_object = Item.query.filter_by(name= purchased_item).first()
        if p_item_object:
            if current_user.can_purchase(p_item_object):
                p_item_object.buy(current_user)
                flash(f'Congratulation! You have purchased {p_item_object.name} for {p_item_object.price}')
            else:
                flash(f"You don't have enough money in wallet",category="danger")
        
        # Sell Item Logic
        sold_item = request.form.get('sold_item')
        s_item_object = Item.query.filter_by(name=sold_item).first()
        if s_item_object:
            if current_user.can_sell(s_item_object):
                s_item_object.sell(current_user)
                flash(f'Congratulation! You have sold {s_item_object.name} for {s_item_object.price}', category='Success')
            else:
                flash(f'Something went wrong with selling {s_item_object.name}', category="danger")
        
        return redirect(url_for('market'))        
    if request.method == "GET":
        items = Item.query.filter_by(owner=None)  
        owned_items = Item.query.filter_by(owner=current_user.id)  
        return render_template('market.html', items=items, selling_form=selling_form, purchase_form=purchase_form, owned_items = owned_items)

@app.route('/register', methods = ['GET', 'POST'])
def register_page():
    form = RegisterForm() 
    if form.validate_on_submit():
        user_to_create = User(username = form.username.data,
                                email_address = form.email_address.data,
                                password = form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f'Account Created Successfully! You are now logged in as {user_to_create.username}', category='success')
        return redirect( url_for('market'))
    if form.errors!= {}:  #if there are not errors from validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating user: {err_msg}', category='danger')
    return render_template('register.html',form=form)

@app.route('/login', methods = ['GET','POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('market'))
        else:
            flash('Invalid Username and password. Please try again', category='danger')
    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash(f'You have been logged out', category='info')
    return redirect(url_for('home_page'))


# BASICS
# @app.route("/")
# def hello_world():
#     return "<h1>Hello, World!</h1>"   

# @app.route("/about")
# def about_page():
#     return "<h2>About Page</h2>"

# # Dynamic Rouiting

# @app.route("/about/<username>")
# def dynamic_about_page(username):
#     return f'<h1>This is the about page of {username}</h1>'