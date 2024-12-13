from flask import Flask, render_template, request, redirect, url_for, flash, session
from datetime import datetime, timedelta
import hashlib
import time
import random
import mysql.connector

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # For session management

# Home route
@app.route('/')
def home():
    return redirect(url_for('login'))

# Sign-Up Route
@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']

        # Check if the username already exists
        cursor.execute("SELECT username FROM users WHERE username = %s", (username,))
        if cursor.fetchone():  # If username already exists
            flash("Username already exists! Please choose a different one.", "error")
            return render_template('sign_up.html')
        
        query = "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)"
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        values = (username, hashed_password, email)
        cursor.execute(query, values)
        connection.commit()

        flash("Sign up successful! Please log in.", "success")
        return redirect(url_for('login'))
    
    return render_template('sign_up.html')

@app.route('/logout')
def logout():
    session.pop('username', None)  # Remove 'username' from session
    flash("You have been logged out.", "success")  # Optional: show a logout message
    return redirect(url_for('login'))  # Redirect to login page

# Login Route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if user exists and the password is correct
        cursor.execute("SELECT username, password FROM users WHERE username = %s", (username,))
        user = cursor.fetchone()
        
        if user:
            stored_password = user[1]
            hashed_password = hashlib.sha256(password.encode()).hexdigest()
            if stored_password == hashed_password:
                session['username'] = username  # Store username in session
                flash("Login successful!", "success")
                return redirect(url_for('dashboard'))
            else:
                flash("Incorrect password. Please try again.", "error")
        else:
            flash("No user found with that username.", "error")
    
    return render_template('login.html')

def getusername():
    username=request.form['username']
    return username

# Dashboard Route (for logged-in users)
@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('index.html')

connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="SAM124@sanyam",
    database="canteen_management",
    auth_plugin="mysql_native_password"
)

cursor = connection.cursor()

def mysqlconnectionprintall():
    username = session['username']
    cursor.execute("SELECT * FROM orders inner join users on orders.username=users.username WHERE users.username = %s", (username,))
    rows = cursor.fetchall()
    return rows

@app.route('/all_orders')
def all_orders():
    orders = mysqlconnectionprintall()
    return render_template('orders.html', orders=orders)

def generate_order_id():
    return str(random.randint(10000, 99999))

def currenttime():
    local_time = time.localtime()
    formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
    return formatted_time

def collectingtime():
    current_time_string = currenttime()
    current_time = datetime.strptime(current_time_string, "%Y-%m-%d %H:%M:%S")
    time_to_add = timedelta(minutes=15)
    new_time = current_time + time_to_add
    return new_time.strftime("%Y-%m-%d %H:%M:%S")

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/submit-order', methods=["POST"])
def ordersubmit():
    UserName=session['username']
    CustomerName = request.form['customername']
    OrderItem = request.form['orderitem']
    OrderQuantity = request.form['orderquantity']
    MobileNumber = request.form['mobilenumber']
    PaymentMethod = request.form['paymentmethod']
    OrderId = generate_order_id()
    OrderTime = currenttime()
    CollectingTime = collectingtime()
    
    query = "INSERT INTO orders (username, Name, OrderItem, OrderQuantity, MobileNumber, PaymentMethod, OrderId, OrderTime, CollectingTime) VALUES (%s, %s, %s ,%s ,%s, %s, %s, %s ,%s)"
    values = (UserName, CustomerName, OrderItem, OrderQuantity, MobileNumber, PaymentMethod, OrderId, OrderTime, CollectingTime)
    cursor.execute(query, values)
    connection.commit()
    
    OrderDetails = {
        'CustomerName': CustomerName,
        'Order': OrderItem,
        'OrderQuantity': OrderQuantity,
        'MobileNumber': MobileNumber,
        'PaymentMethod': PaymentMethod,
        'OrderId': OrderId,
        'OrderTime': currenttime(),
        'CollectingTime': collectingtime()
    }
    return render_template('ordersummary.html', OrderDetails=OrderDetails)

# User Profile Route
@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'username' not in session:
        return redirect(url_for('login'))
    username = session['username']
    
    # Fetch user details from the database
    cursor.execute("SELECT username, email, created_at FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()  # This fetches a single row (as a tuple or dictionary)
    if user:
        user = {
            'username': user[0],
            'email': user[1],
            'created_at': user[2].strftime('%Y-%m-%d %H:%M:%S') if user[2] else None
        }

    return render_template('profile.html', user=user)

if __name__ == '__main__':
    app.run(debug=True)
