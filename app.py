from flask import Flask, render_template, url_for, redirect, request, session
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import bcrypt

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/myDatabase"
app.secret_key = "mysecretkey"
mongo = PyMongo(app)

# Define models for the database collections
class User:
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
            return None


class Bill:
    def __init__(self, amount, split_type, split_value, user_id, group_id):
        self.amount = amount
        self.split_type = split_type
        self.split_value = split_value
        self.user_id = user_id
        self.group_id = group_id

    def save(self):
        bill = {
            'amount': self.amount,
            'split_type': self.split_type,
            'split_value': self.split_value,
            'user_id': self.user_id,
            'group_id': self.group_id
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

    def delete(self):
        mongo.db.bills.delete_one({'_id': ObjectId(self.id)})

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
    session.pop('username', None)
    return redirect("/login")

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
@app.route("/add_group", methods=["GET", "POST"])
def add_group():
    if request.method == "POST":
        name = request.form["name"]
        users = request.form.getlist("users")
        group = Group(name, users)
        group.save()
        return redirect("/")
    else:
        users = User.get_all()
        return render_template("add_group.html", users=users)

@app.route("/groups")
def groups():
    groups = Group.get_all()
    return render_template("groups.html", groups=groups)

@app.route("/groups/<id>")
def group_detail(id):
    group = Group.get_by_id(id)
    if group:
        return render_template("group_detail.html", group=group)
    else:
        return "Group not found"

@app.route("/bills")
def bills():
    bills = Bill.get_all()
    return render_template("bills.html", bills=bills)

@app.route("/new_bill", methods=["GET", "POST"])
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

@app.route("/bills/<id>/edit", methods=["GET", "POST"])
def edit_bill(id):
    bill = Bill.get_by_id(id)
    if request.method == "POST":
        amount = request.form["amount"]
        split_type = request.form["split_type"]
        split_value = request.form["split_value"]
        bill.amount = amount
        bill.split_type = split_type
        bill.split_value = split_value
        bill.update()
        return redirect("/bills")
    else:
        users = mongo.db.users.find()
        groups = mongo.db.groups.find()
        return render_template("edit_bill.html", bill=bill, users=users, groups=groups)

@app.route("/bills/<id>/delete", methods=["POST"])
def delete_bill(id):
    bill = Bill.get_by_id(id)
    bill.delete()
    return redirect("/bills")






