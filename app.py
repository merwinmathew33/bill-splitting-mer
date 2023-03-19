from flask import Flask, render_template, url_for, redirect, request, session, flash
from flask_pymongo import PyMongo
from bson.objectid import ObjectId
import bcrypt
from collections import defaultdict

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
            return None  
    

class Bill:
    def __init__(self, amount, split_type, split_value, user_name, group_name):
        self.amount = amount
        self.split_type = split_type
        self.split_value = split_value
        self.user_name = user_name
        self.group_name = group_name
        
        # retrieve user and group objects based on names
        user = mongo.db.users.find_one({'username': user_name})
        if user:
            self.user_id = user['_id']
        else:
            self.user_id = None
        group = mongo.db.groups.find_one({'name': group_name})
        if group:
            self.group_id = group['_id']
        else:
            self.group_id = None
        
        

    def save(self):
        
            bill = {
                'amount': self.amount,
                'split_type': self.split_type,
                'split_value': self.split_value,
                'user_id': self.user_id,
                'group_id': self.group_id,
                
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

    @staticmethod
    def update(id, amount, split_type, split_value, user_name,group_name):
        mongo.db.bills.update_one({'_id': ObjectId(id)}, {"$set": {'amount': amount, 'split_type': split_type, 'split_value': split_value,'user_name':user_name,'group_name':group_name}})
    
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
    @staticmethod
    def update(id,name,users):
        mongo.db.groups.update_one({'_id': ObjectId(id)}, {"$set": {'name': name, 'users': users}})
 
    @staticmethod
    def delete(id):
        mongo.db.groups.delete_one({'_id': ObjectId(id)})



     

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
    
    return redirect(url_for("login"))


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
            flash("enter any one field(user name or group name)")
            return render_template("add_bill.html")
        if user or group:
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
        amount = request.form.get("amount")
        split_type = request.form.get("split_type")
        split_value = request.form.get("split_value")
        user_name = request.form.get("user_name")
        group_name = request.form.get("group_name")
        
        Bill.update(id, amount, split_type, split_value, user_name,group_name)
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

@app.route("/group/add", methods=["GET", "POST"])
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
        Group.update(id, name, users)
        return redirect("/groups")
    else:
        group = Group.get_by_id(id)
        users = mongo.db.users.find()
        return render_template("edit_group.html", group=group, users=users)


@app.route("/group/delete/<id>",methods=["POST"])
def delete_group(id):    
    Group.delete(id)
    return redirect("/groups")





@app.route("/summary")
def summary():
    if 'username' in session:
        user_id = mongo.db.users.find_one({'username': session['username']})['_id']
        bills = mongo.db.bills.find({'user_id': user_id})
        debts = defaultdict(float)
        am = []
        for bill in bills:
            if bill['split_type'] == 'percentage':
                    if user_id != str(user_id):
                        amount = (int(bill['amount']) * int(bill['split_value'])) / 100
                        debts[user_id] += amount
                        am.append({"Name": bill['user_name'], "Money": amount})
            else:
                
                    if user_id != str(user_id):
                        amount = bill['split_value']
                        debts[user_id] += amount
                        am.append({"Name": bill['user_name'], "Money": amount})
        return render_template("summary.html", am=am, debts=debts)
    else:
        flash("You need to be logged in to view this page", "danger")
        return redirect(url_for("login"))

@app.route("/gsummary", methods=["GET", "POST"])
def gsummary():
    if 'username' in session:
        user_id = mongo.db.users.find_one({'username': session['username']})['_id']
        bill_id = request.args.get('bill_id')
        bills = Bill.get_all()
        debts = {}
        am = {}
        peers = []
        for bill in bills:
            user = mongo.db.bills.find_one({'group_name': {'$ne': None}})
            if user:
                bills.user_id = user['_id']
            else:
                bills.user_id = None
            if bill['user_id']!= None:
                pipeline = [{"$match": {"_id": bill_id}},
                {"$lookup": {
                            "from": "groups",
                            "localField": "group_id",
                            "foreignField": "_id",
                            "as": "group"
                             }},
                {"$unwind": "$group"},
                {"$project": {
                    "_id": 0,
                    "user_ids": "$group.members.user_id"
                }}
                            ]

                result = mongo.db.bills.aggregate(pipeline)
                buser_ids = []
                for r in result:
                    user_ids += r['user_ids']    
                for bid in buser_ids:
                    if bid== user_id:
                        if bill['split_type'] == 'percentage':
                            for user in bid:
                                if user != user_id:
                                    amount = (int(bill['amount']) * int(bill['split_value'])) / 100
                                    if user in debts:
                                        debts[user] += amount
                                    else:
                                        debts[user] = amount
                                    am.update({"Name":bill['user_name'], "Money":amount})
                        else:
                            for user in bid:
                                if user != str(user_id):
                                    amount = bill['split_value']
                                    if user in debts:
                                        debts[user] += amount
                                    else:
                                        debts[user] = amount
                                    am.update({"Name":bill['user_name'], "Money":amount})
                    else:
                        if bill['split_type'] == 'percentage':
                            amount = (int(bill['amount']) * int(bill['split_value'])) / 100
                            if bill['user_id'] in debts:
                                debts[bill['user_id']] += amount
                            else:
                                debts[(bill['user_id'])] = amount
                            am.update({"Name":bill['user_name'], "Money":amount})                          
                    
                              

            


@app.route("/simplified_bills", methods=["GET", "POST"])
def simplified_bills():       
    for bill in bills:
        if bill['user_id'] == str(user_id):
            for user in bill['split_value']:
                if user != str(user_id) and user not in peers:
                    peers.append(user)
        elif str(user_id) in bill['split_value']:
            if str(bill['user_id']) != str(user_id) and str(bill['user_id']) not in peers:
                peers.append(str(bill['user_id']))
        
    for peer in peers:
        if peer in debts and debts[peer] > 0 and str(peer) != str(user_id):
            for peer2 in peers:
                if peer != peer2 and peer2 in debts and debts[peer2] < 0 and debts[peer] != 0:
                    if abs(debts[peer2]) > debts[peer]:
                        debts[peer2] += debts[peer]
                        print(f"You owe {peer2} ₹{abs(debts[peer])}")
                        debts[peer] = 0
                    else:
                        debts[peer] += debts[peer2]
                        print(f"You owe {peer2} ₹{abs(debts[peer2])}")
                        debts[peer2] = 0

    return render_template("settle_bills.html", debts=debts)
    








