from flask import Flask, render_template, url_for, redirect, request, session, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import bcrypt

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
app.secret_key = "mysecretkey"
mongo = PyMongo(app)

# Define models for the database collections
class User:
    query = mongo.db.users

    def __init__(self, username, password):
        self.username = username
        self.password = password

    def save(self):
        hashed_password = bcrypt.hashpw(self.password, bcrypt.gensalt())

        user = {
            'username': self.username,
            'password': hashed_password
        }
        mongo.db.users.insert_one(user)
 
    
 
    @staticmethod
    def get_all():
        users = []
        for user in mongo.db.users.find():
            users.append(User(user['username'], user['password']))
        return users

    @staticmethod
    def get_by_username(username):
        user = mongo.db.users.find_one({'username': username})
        if user:
            return User(user['username'], user['password'])
        else:
            return user_user  
    def calculate_owed_amount(self):
        split_list = mongo.db.split.find({'user_id': self.username})
        owed_amount = {}
        for split in split_list:
            owed_amount[split['split_with']] = owed_amount.get(split['split_with'], 0) + split['amount']
            owed_amount[self.username] = owed_amount.get(self.username, 0) - split['amount']
        return owed_amount

    def simplify_debt(self, owed_amount):
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


class Bill:
    def __init__(self, amount, split_type, split_value, user_name, group_name):
        self.amount = amount
        self.split_type = split_type
        self.split_value = split_value
        self.user_name = user_name
        self.group_name = group_name
        
        # retrieve user and group objects based on names
        user = mongo.db.users.find_one({'username': user_name})
        group = mongo.db.groups.find_one({'name': group_name})
        
        self.user_id = user['_id']
        self.group_id = group['_id']
        

    def save(self):
        
            bill = {
                'amount': self.amount,
                'split_type': self.split_type,
                'split_value': self.split_value,
                
                'user_name': self.user_name,
                'group_name': self.group_name
            }
            mongo.db.bills.insert_one(bill)

        

    @staticmethod
    def get_all():
        bills = mongo.db.bills.find()
        return bills

    @staticmethod
    def get_by_id(id):
        bill = mongo.db.bills.find_one({'_id': ObjectId(id)})

        return bill

    def update(self):
        mongo.db.bills.update_one({'_id': ObjectId(self.id)}, {"$set": {'amount': self.amount, 'split_type': self.split_type, 'split_value': self.split_value}})
    
    @staticmethod
    def delete(id):
        mongo.db.bills.delete_one({'_id': ObjectId(id)})


class Group:
    def __init__(self, name, users):
        self.name = name
        self.users = users

    def save(self):
        group = {
            'name': self.name,
            'users': self.users
        }
        mongo.db.groups.insert_one(group)

    @staticmethod
    def get_all():
        groups = mongo.db.groups.find()
        return groups

    @staticmethod
    def get_by_id(id):
        group = mongo.db.groups.find_one({'_id': ObjectId(id)})
        return group

    def update(self):
        mongo.db.groups.update_one({'_id': ObjectId(self.id)}, {"$set": {'name': self.name, 'users': self.users}})

    def delete(self):
        mongo.db.groups.delete_one({'_id': ObjectId(self.id)})


# Define routes and views
@app.route("/")
def home():
    if 'username' in session:
        return render_template("index.html", username=session['username'])
    else:
        return redirect("/login")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"].encode('utf-8')
        user = User.get_by_username(username)
        if user and bcrypt.checkpw(password, user.password):
            session['username'] = username
            return redirect("/")
        else:
            return  render_template("login.html", error="Invalid username or password")
    else:
        return render_template("login.html")

@app.route("/logout")
def logout():
    session.pop('username', user_id)
    return redirect("/luser")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"].encode('utf-8')
        confirm_password = request.form["confirm_password"].encode('utf-8')
        if password != confirm_password:
            return render_template("register.html", error="Passwords do not match")
        existing_user = User.get_by_username(username)
        if existing_user:
            return render_template("register.html", error="Username already taken")
        else:
            new_user = User(username, password)
            new_user.save()
            session['username'] = username
        return redirect("/")
    else:
        return render_template("register.html")
@app.route("/bills")
def bills():
    if 'username' in session:
        bills = Bill.get_all()
        return render_template("bills.html", bills=bills)
    else:
        return redirect("/login")

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
            bill = Bill(amount, split_type, split_value, user_name, group_name)
            bill.save()
            return redirect("/bills")
        else:
            flash("User or group not found.")
            return render_template("add_bill.html")
    else:
        return render_template("add_bill.html")




@app.route("/bill/edit/<id>", methods=["GET", "POST"])
def edit_bill(id):
    if request.method == "POST":
        amount = request.form["amount"]
        split_type = request.form["split_type"]
        split_value = request.form["split_value"]
        bill = Bill.get_by_id(id)
        bill.amount = amount
        bill.split_type = split_type
        bill.split_value = split_value
        bill.update()
        return redirect("/bills")
    else:
        bill = Bill.get_by_id(id)
        return render_template("edit_bill.html", bill=bill)

@app.route("/bill/delete/<id>", methods=["POST"])
def delete_bill(id):
    Bill.delete(id)
    return redirect("/bills")



@app.route("/groups")
def groups():
    if 'username' in session:
        groups = Group.get_all()
        return render_template("groups.html", groups=groups)
    else:
        return redirect("/login")

@app.route("/add_group", methods=["GET", "POST"])
def add_group():
    if request.method == "POST":
        name = request.form["name"]
        user_ids = request.form.getlist("users")
        user_objs = [mongo.db.users.find_one({'_id': ObjectId(user_id)}) for user_id in user_ids]
        group = Group(name, user_objs)
        group.save()
        return redirect("/groups")
    else:
        users = mongo.db.users.find()
        return render_template("add_group.html", users=users)



@app.route("/group/edit/<id>", methods=["GET", "POST"])
def edit_group(id):
    if request.method == "POST":
        name = request.form["name"]
        users = request.form.getlist("users")
        group = Group.get_by_id(id)
        group.name = name
        group.users = users
        group.update()
        return redirect("/groups")
    else:
        group = Group.get_by_id(id)
        return render_template("edit_group.html", group=group)

@app.route("/group/delete/<id>")
def delete_group(id):
    group = Group.get_by_id(id)
    group.delete()
    return redirect("/groups")



@app.route('/summary')
def summary():
    username = ""
   
    user = User.get_by_username(session['username'])
            
    owed_amount = user.calculate_owed_amount()
    return render_template('summary.html', user=user, owed_amount=owed_amount)
           

@app.route('/simplified-debt')
def simplified_debt():
    username = request.args.get('username')
    user = User.get_by_username(username)
    owed_amount = user.calculate_owed_amount()
    simplified_debt = user.simplify_debt(owed_amount)
    return render_template('simplified-debt.html', user=user, simplified_debt=simplified_debt)




