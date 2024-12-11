from flask import Flask,render_template,request
from datetime import datetime, timedelta
import time,random
app=Flask(__name__)

def generate_order_id():
    return str(random.randint(10000, 99999))

def currenttime():
    local_time = time.localtime()
    # Convert the time to a datetime object
    formatted_time = time.strftime("%Y-%m-%d %H:%M:%S", local_time)
    return formatted_time

def collectingtime():
    # Get the current time as a string
    current_time_str = currenttime()
    # Convert the string back to a datetime object
    current_time = datetime.strptime(current_time_str, "%Y-%m-%d %H:%M:%S")
    
    # Add 15 minutes to the current time
    time_to_add = timedelta(minutes=15)
    new_time = current_time + time_to_add
    
    # Return the result as a string, formatted properly
    return new_time.strftime("%H:%M:%S")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit-order',methods=["POST"])
def ordersubmit():
    CustName=request.form['name']
    Order=request.form['order']
    OrderQuantity=request.form['orderquantity']
    MobileNumber=request.form['mobilenumber']
    PaymentMethod=request.form['paymentmethod']
    OrderId=generate_order_id()
    OrderDetails={
        'CustomerName':CustName,
        'Order':Order,
        'OrderQuantity':OrderQuantity,
        'MobileNumber':MobileNumber,
        'PaymentMethod':PaymentMethod,
        'OrderId':OrderId,
        'OrderTime':currenttime(),
        'CollectingTime':collectingtime()
    }
    return render_template('ordersummary.html',OrderDetails=OrderDetails)

if __name__==('__main__'):
        app.run(debug=True)