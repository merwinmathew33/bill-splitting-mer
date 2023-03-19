# Bill Splitting Application
This is a simple web application for splitting bills among a group of users. The application allows users to create groups, add other users to their groups, and create bills that can be split among group members.

## Features
* User registration and login
* Group creation and management
* Adding users to groups
* Bill creation and splitting among group members
* Summary of debts owed by and to each group member
## Technologies Used
* Python Flask web framework
* MongoDB database
* HTML, CSS, and JavaScript
* Bootstrap front-end framework
## Installation
1. Clone the repository to your local machine.
1. Install the required dependencies.
  ```
  > mkdir myproject
  > cd myproject
  > py -3 -m venv venv
  ```
  * Before you work on your project, activate the corresponding environment:
  ```
  > venv\Scripts\activate
  ```
  * Install the required packages such as Flask, Flask-PyMongo, and bcrypt.
  ```
  $ pip install Flask
  $ pip install Flask-PyMongo
  $ pip install bcrypt
  ```

3. Run the python app.py to start the Flask web server.
  ```
  flask run --debug
  ```
  Now our program run in debug mode \
4. Open your web browser and go to http://localhost:5000 to access the application.
## Usage
1. Register an account or login if you already have an account.
1. Create a group and add other users to the group.
1. Create a bill and specify the amount, split type, and split value.
1. Assign the bill to a group or an user and pay the bill.
1. View the summary page to see debts owed by and to each group member.
## Video Explanation
I have created a video explaining all essential features in this application. Click [here](https://drive.google.com/file/d/17NNVcN71e7NvEPnHmGFrhXM4e3m-nKZz/view?usp=sharing) to view it. \
If there is any issue in viewing that link, please check [here](https://youtu.be/jHaSEgAnun0)
## Code Expalnation
* **login**
This code displays a login form with input fields for the username and password. When the form is submitted, it sends a POST request to the /login route. If there is an error message, it is displayed above the form.
* **Register**
This code displays a registration form with input fields for the username and password, and a confirmation field for the password. When the form is submitted, it sends a POST request to the /register route. If there is an error message, it is displayed above the form.
* **Bill**
  @app.route("/bills") is a route that renders a template that displays all the bills in the system. If the user is not logged in, they are redirected to the login page.

  @app.route("/bill/add", methods=["GET", "POST"]) is a route that allows users to add a new bill. If the request method is POST, the form data is retrieved and a new    Bill object is created using the provided information. The Bill object is then saved to the database and the user is redirected to the bills page. If the user or group specified in the form is not found, an error message is displayed. If the user submits an empty form, they are redirected to the same page.

  @app.route("/bill/edit/<id>", methods=["GET", "POST"]) is a route that allows users to edit an existing bill. If the request method is POST, the form data is retrieved and the Bill object with the specified ID is updated with the new information. The user is then redirected to the bills page. If the user submits an empty form, they are redirected to the same page.

  @app.route("/bill/delete/<id>", methods=["POST"]) is a route that allows users to delete an existing bill. The Bill object with the specified ID is deleted from the database and the user is redirected to the bills page.
* **Group**
  @app.route("/groups"): This route renders the groups.html template, which shows a list of all groups in the application. It first checks if the user is logged in by checking if their username is in the session. If the user is not logged in, it redirects them to the login page.

  @app.route("/group/add", methods=["GET", "POST"]): This route is used to add a new group to the application. If the request method is POST, it retrieves the group name and the list of user IDs from the form data submitted by the user, looks up the corresponding user objects from the database, creates a new Group object with the provided information, and saves it to the database. Then it redirects to the groups route to display the updated list of groups. If the request method is GET, it renders the add_group.html template, which displays a form for creating a new group and a list of all users in the application.

  @app.route("/group/edit/<id>", methods=["GET", "POST"]): This route is used to edit an existing group. If the request method is POST, it retrieves the updated group name and list of user IDs from the form data submitted by the user, updates the corresponding Group object in the database with the new information, and redirects to the groups route to display the updated list of groups. If the request method is GET, it retrieves the group with the specified ID from the database and renders the edit_group.html template, which displays a form for editing the group information and a list of all users in the application.

  @app.route("/group/delete/<id>", methods=["POST"]): This route is used to delete an existing group. It retrieves the group with the specified ID from the database and deletes it, then redirects to the groups route to display the updated list of groups. Note that this route only accepts POST requests, so it can't be accessed directly from a web browser. Instead, it should be called from a form submission or an AJAX request.

* **Summary** 
  The first function, summary(), first checks if the user is logged in by verifying the presence of a 'username' key in the session object. If so, it retrieves the user's _id from the database and then finds all bills associated with that user. It then iterates over these bills, calculating the amount owed by or to the user for each bill and storing this information in a dictionary called debts. It also creates a list of dictionaries called am that contains information about the user's bills and the amounts owed. Finally, it renders an HTML template called 'summary.html', passing in the am and debts variables as arguments. If the user is not logged in, it displays a flash message and redirects them to the login page.

  The second function, gsummary(), follows a similar structure to summary(), but instead of retrieving bills associated with a single user, it retrieves bills associated with all users in a group that the logged-in user is a member of. It first retrieves the logged-in user's _id from the database and then finds all groups that include that user. It then iterates over these groups, retrieving all bills associated with each group and calculating the amount owed by or to each user in the group for each bill. It stores this information in a dictionary called debts, and returns a JSON object that contains the debts dictionary. If the user is not logged in, it displays a flash message and redirects them to the login page.
  

