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



