from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from __init__ import app, db, login_manager
from models import User, FoodDonation, FoodRequest

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        user_type = request.form.get('user_type')

        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists')
            return redirect(url_for('register'))

        hashed_password = generate_password_hash(password)
        new_user = User(username=username, email=email, password=hashed_password, user_type=user_type)
        db.session.add(new_user)
        db.session.commit()

        flash('Registration successful')
        return redirect(url_for('login'))

    return render_template('register.html')


@app.route('/dashboard')
@login_required
def dashboard():
    if current_user.user_type == 'donor':
        donations = FoodDonation.query.filter_by(donor_id=current_user.id).all()
        return render_template('donor_dashboard.html', donations=donations)
    elif current_user.user_type == 'foodbank':
        available_donations = FoodDonation.query.filter_by(status='available').all()
        my_requests = FoodRequest.query.filter_by(foodbank_id=current_user.id).all()
        return render_template('foodbank_dashboard.html', donations=available_donations, requests=my_requests)
    else:  # volunteer
        pending_requests = FoodRequest.query.filter_by(status='accepted', volunteer_id=None).all()
        my_deliveries = FoodRequest.query.filter_by(volunteer_id=current_user.id).all()
        return render_template('volunteer_dashboard.html', requests=pending_requests, deliveries=my_deliveries)

@app.route('/foodbank_signup', methods=['GET', 'POST'])
def foodbank_signup():
    if request.method == 'POST':
        food_bank_name = request.form.get('food_bank_name')
        email = request.form.get('email')
        phone = request.form.get('phone')
        address = request.form.get('address')
        # Process the registration...
        return redirect(url_for('food_listing'))
    return render_template('foodbank_signup.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route('/submit-request')
@login_required
def submit_request():
    # This will be implemented when you show the next page design
    return "Submit Request Page Coming Soon"


@app.route('/food_listing')
@login_required
def food_listing():
    # Sample data - in a real app, this would come from your database
    available_food = [
        {"name": "Baby Potatoes", "quantity": "1 bag", "image": "potatoes.jpg"},
        {"name": "Lasagna", "quantity": "5 servings", "image": "lasagna.jpg"},
        {"name": "Rasberry", "quantity": "7 cartons", "image": "rasberry.jpg"},
        {"name": "Low-fat Milk", "quantity": "2 gallons", "image": "milk.jpg"},
        {"name": "buldalk ramen", "quantity": "5 servings", "image": "ramen.jpg"}
    ]
    
    lacking_items = ["Milk", "Whole-Wheat Bread", "Carrots", "Canned Corn"]
    
    inventory = [
        {"name": "Steak", "quantity": "15 lbs", "image": "steak.jpg"},
        {"name": "Eggs", "quantity": "25 cartons", "image": "eggs.jpg"},
        {"name": "Tomatoes", "quantity": "17 bags", "image": "tomatoes.jpg"},
        {"name": "Canned Corn", "quantity": "7 cans", "image": "corn.jpg"},
        {"name": "Sugar", "quantity": "12 bags", "image": "sugar.jpg"}
    ]
    
    return render_template('food_listing.html', 
                         available_food=available_food,
                         lacking_items=lacking_items,
                         inventory=inventory)



@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')
        
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password, password):
            login_user(user)
            return redirect(url_for('food_listing'))  # Changed from dashboard to food_listing

        flash('Invalid email or password')
    return render_template('login.html')

@app.route('/food-request-form', methods=['GET', 'POST'])
@login_required
def food_request_form():
    if request.method == 'POST':
        # Collect form data
        food = request.form.get('food')
        quantity = request.form.get('food_quantity')
        by = request.form.get('by')
        food_bank = request.form.get('food_bank')
        
        # You might want to save this information to the database later
        # For now, we'll just flash a message and redirect
        flash('Your food request has been submitted successfully!')
        return redirect(url_for('food_listing'))
    
    return render_template('food_request_form.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        app.run(debug=True)