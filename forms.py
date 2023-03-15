from flask_wtf import FlaskForm
from wtforms import 




@app.route('/edit_bill/<int:id>', methods=['GET', 'POST'])
def edit_bill(id):
    bill = Bill.get_by_id(id)
    if not bill:
        return "Bill not found"
    if request.method == 'POST':
        # Handle form submission
        bill.name = request.form['name']
        bill.amount = float(request.form['amount'])
        bill.date = datetime.datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        bill.paid_by = request.form['paid_by']
        bill.save()
        return redirect('/')
    else:
        # Render the form
        users = User.get_all()
        return render_template('edit_bill.html', bill=bill, users=users)

@app.route('/new_bill', methods=['GET', 'POST'])
def new_bill():
    if request.method == 'POST':
        # Handle form submission
        name = request.form['name']
        amount = float(request.form['amount'])
        date = datetime.datetime.strptime(request.form['date'], '%Y-%m-%d').date()
        paid_by = request.form['paid_by']
        bill = Bill(name, amount, date, paid_by)
        bill.save()
        return redirect('/')
    else:
        # Render the form
        users = User.get_all()
        return render_template('new_bill.html', users=users)

The error message indicates that the requested URL is not found. You need to define routes in your Flask application to handle the URLs /edit_bill and /new_bill. Here's an example of how you can define these routes:

less


Note that these routes assume that you have templates named edit_bill.html and new_bill.html in your templates directory. You should also make sure that you have imported the required classes and modules, such as Bill, User, datetime, and mongo.



@app.route("/bills/new", methods=["GET", "POST"])
def new_bill():
    if request.method == "POST":
        amount = request.form["amount"]
        split_type = request.form["split_type"]
        split_value = request.form["split_value"]
        user_id = request.form["user_id"]
        group_id = request.form["group_id"]
        bill = Bill(amount, split_type, split_value, user_id, group_id)
        bill.save()
        return redirect("/bills")
    else:
        users = mongo.db.users.find()
        groups = mongo.db.groups.find()
        return render_template("new_bill.html", users=users, groups=groups)

@app.route("/summary")
def summary():
    
    user_id = get_current_user_id()
    
    # get all bills that user is involved in
    bills = Bill.get_by_id(user_id)
    
    # calculate total amount owed by user to each person
    balances = {}
    simplified ={}
    for bill in bills:
        if bill.user_id == user_id:
            # user paid the bill
            for share in bill.shares:
                if share.user_id != user_id:
                    if share.user_id in balances:
                        balances[share.user_id] += share.amount
                    else:
                        balances[share.user_id] = share.amount
        else:
            # user owes a portion of the bill
            if bill.user_id in balances:
                balances[bill.user_id] -= bill.get_user_share_amount(user_id)
            else:
                balances[bill.user_id] = -bill.get_user_share_amount(user_id)

    return render_template("summary.html", balances=balances, simplified=simplified)



from flask import Flask, render_template

app = Flask(__name__)

@app.route('/debts')
def debts():
    debts = {"User A": "$50", "User B": "$75", "User C": "$25"}
    return render_template('debts.html', debts=debts)

@app.route('/reset-balance', methods=['POST'])
def reset_balance():
    # Code to reset the balance
    return "Balance has been reset."

if __name__ == '__main__':
    app.run(debug=True)



from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)

class Split(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    split_with = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    amount = db.Column(db.Float, nullable=False)

def calculate_owed_amount(user_id):
    users = User.query.all()
    split_list = Split.query.filter_by(user_id=user_id).all()
    owed_amount = {}
    for user in users:
        owed_amount[user.id] = 0
    for split in split_list:
        owed_amount[split.split_with] += split.amount
        owed_amount[user_id] -= split.amount
    return owed_amount

def simplify_debt(owed_amount):
    simplified_debt = {}
    for user_id in owed_amount.keys():
        simplified_debt[user_id] = 0
    for user_id in owed_amount.keys():
        for other_id in owed_amount.keys():
            if user_id != other_id and owed_amount[user_id] > 0 and owed_amount[other_id] < 0:
                if abs(owed_amount[other_id]) > owed_amount[user_id]:
                    simplified_debt[other_id] += owed_amount[user_id]
                    owed_amount[other_id] += owed_amount[user_id]
                    owed_amount[user_id] = 0
                else:
                    simplified_debt[other_id] += abs(owed_amount[other_id])
                    owed_amount[user_id] += owed_amount[other_id]
                    owed_amount[other_id] = 0
    return simplified_debt

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summary')
def summary():
    user_id = request.args.get('user_id')
    owed_amount = calculate_owed_amount(user_id)
    return render_template('summary.html', user_id=user_id, owed_amount=owed_amount)

@app.route('/simplified-debt')
def simplified_debt():
    user_id = request.args.get('user_id')
    owed_amount = calculate_owed_amount(user_id)
    simplified_debt = simplify_debt(owed_amount)
    return render_template('simplified-debt.html', user_id=user_id, simplified_debt=simplified_debt)

if __name__ == '__main__':
    app.run(debug=True)


<!DOCTYPE html>
<html>
<head>
    <title>Bill Splitting App</title>
</head>
<body>
    {% if username %}
        <h1>Welcome, {{ username }}!</h1>
        <a href="/logout"><button>Logout</button></a><br>
        <a href="/add_group"><button>Add group</button></a><br>
        <a href="/bills"><button>Bills</button></a>
    {% else %}
        <h1>Please login to continue</h1>
        <form method="post" action="/login">
            <label for="username">Username:</label>
            <input type="text" name="username"><br>
            <label for="password">Password:</label>
            <input type="password" name="password"><br>
            <input type="submit" value="Login">
        </form>
    {% endif %}
</body>
</html>

    
@app.route('/summary')
def summary():
    username = ""
    if 'username' in session:
        if session.get('username'):
            user = User.get_by_username(session['username'])
            if user:
                owed_amount = user.calculate_owed_amount()
                return render_template('summary.html', user=user, owed_amount=owed_amount)
            else:
                return redirect("/login")
        else:
            return redirect("/login")
@app.route('/summary')
def summary():
    user_id = session.get('user_id')
    if user_id:
        user = User.query.get(user_id)
        owed_amount = calculate_owed_amount(user_id)
        return render_template('summary.html', user=user, owed_amount=owed_amount)
    else:
        # handle case where user is not logged in
        return redirect(url_for('login'))

@app.route('/summary')
def summary():
    if 'username' in session:

        username = request.args.get('username')
        user = User.get_by_username(username)
        owed_amount = user.calculate_owed_amount()
        return render_template('summary.html', user=user, owed_amount=owed_amount)



@staticmethod
    def get_all():
        bills = []
        for bill in mongo.db.bills.find():
            user = mongo.db.users.find_one({'_id': bill['user_id']},{'user_name': 1})
            group = mongo.db.groups.find_one({'_id': bill['group_id']},{'group_name': 1})
            if user and group:
                bill['user_name'] = user.get('user_name')
                bill['group_name'] = group.get('group_name')
                bills.append(bill)
        return bills


@app.route("/bill/add", methods=["GET", "POST"])
def add_bill():
    if request.method == "POST":
        amount = request.form["amount"]
        split_type = request.form["split_type"]
        split_value = request.form["split_value"]
        user_name = request.form["user_name"]
        group_name = request.form["group_name"]
        
        # retrieve user and group objects based on names
        user = mongo.db.users.find_one({'username': user_name})
        group = mongo.db.groups.find_one({'name': group_name})
        
        # create Bill object using user and group IDs
        if user and group:
            bill = Bill(amount, split_type, split_value, user['_id'], group['_id'])
            bill.save()
            return redirect("/bills")
        else:
            flash("User or group not found.")
            return render_template("add_bill.html")
    else:
        return render_template("add_bill.html")

# set user_id and group_id attributes based on IDs retrieved from the database
        if user and group:
            self.user_id = user['_id']
            self.group_id = group['_id']
        else:
            self.user_id = None
            self.group_id = None