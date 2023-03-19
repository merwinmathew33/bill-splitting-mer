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
