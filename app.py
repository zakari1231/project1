from flask import Flask, request, render_template, jsonify, Blueprint, flash, session, url_for, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, logout_user, current_user, login_user, login_required, mixins, login_manager, logout_user
from flask_login.mixins import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from forms import SignupForm, LoginForm, SearchForm

#from flask_marshmallow import Marshmallow


#db app..
app = Flask(__name__,template_folder='templates',static_url_path='')
app.config['SECRET_KEY'] = "44e04c1e98a03ede943c9f026fd612e59b50901a5c1b6acf1713edc9743361fd"
#TODO:INFO: you need a secret key(above). Without one FlaskForm will not work 
#   Your application will be vunerable to CSFT attack without one.
#   It is a secret key for a reason. For best practice,
#   you should NOT have it visible in plain sight like this when 
#   deploying your app in a "real-world" web application.

# For this application it should be fine, but we should be mindful and follow best practice.
"""
### TO GET A SECRET KEY ####
> run python from cmdline 

 import secrets
 secrets.token_hex(32)

# STORE YOUR RESULTS TO ENVIRONMENT VARIABLE IN CMDLINE.
 export FLASK_SECRET = " your secret key above (result on line no.18)

#THEN USE IT IN THIS FILE LIKE THIS:
import os
app.config['SECRET_KEY'] = os.environ['FLASK_SECRET']
"""

#NOTE: ADDED MORE CONFIGURATION TO HELP WHEN RELOAD APP
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["TEMPLATES_AUTO_RELOAD"] = True # reload WITHOUT restarting you application
login_manager = LoginManager(app)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@login_manager.unauthorized_handler
def unauthorized():
    flash('You must be logged in to view that page.')
    return redirect(url_for('login'))


'''
login = LoginManager(app)
login.login_view = 'auth.login'
'''
'''
@app.route('/', methods= ['GET'])
def get():
    return jsonify({ 'msg': 'hello world' })
'''
#database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgres://tpkqhqnetayrsu:23c139d1b303cb7ddf334cce450d0bef1e0a77aa5fbf00995569b0d9416f90fd@ec2-3-223-21-106.compute-1.amazonaws.com:5432/dk1prhbsjkpq9'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] =False
#INT DB 
db = SQLAlchemy(app)
login_manager = LoginManager()
#init march
#ma = Marshmallow(app)

# book and users and reviews class 

class User(UserMixin, db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key = True)
    full_name = db.Column(db.String, nullable=False)
    username = db.Column(db.String, unique=True, nullable=False)
    email = db.Column(db.String, nullable=False)
    password = db.Column(db.String, nullable=False)
    password_hash = db.Column(db.String(128))



    def set_password(self, password):
        """Create hashed password."""
        self.password = generate_password_hash(password, method='sha256')

    def check_password(self, password):
        """Check hashed password."""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)

    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True
    
    def is_anonymous(self):
        return False

'''     
    def get_id(self):
        User_id = User.id
        return str(self.User_id)
        
    def set_id(self, User_id):
        User_id = User.id
        self.User_id = User_id
'''

class Books(db.Model):
    __tablename__ = "books"
    id = db.Column(db.Integer, primary_key = True)
    isbn = db.Column(db.String, nullable=False)
    title = db.Column(db.String, nullable=False)
    author = db.Column(db.String, nullable=False)
    year = db.Column(db.String, nullable=False)

    def __init__(self, isbn, title, author, year):
        self.isbn = isbn
        self.title = title
        self.author = author
        self.year = year


class Reviews(db.Model):
    __tablename__ = "reviews"
    id = db.Column(db.Integer, primary_key = True)
    rating = db.Column(db.Integer, nullable=False)
    review = db.Column(db.Text(), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey("books.id"), nullable=False)
    users_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    def __init__(self, rating, review, book_id, users_id):
        self.rating = rating
        self.review = review
        self.book_id = book_id
        self.users_id = users_id


# register 

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    """
    Sign-up form to create new user accounts.

    GET: Serve sign-up page.
    POST: Validate form, create account, redirect user to dashboard.
    """
    form = SignupForm()
    if form.validate_on_submit():
        existing_user = User.query.filter_by(email=form.email.data).first()
        if existing_user is None:
            new_user = User(full_name=form.full_name.data, username=form.username.data, email=form.email.data, password=form.password.data)
            new_user.set_password(form.password.data)
            db.session.add(new_user)
            db.session.commit()  # Create new user
            login_user(new_user)  # Log in as newly created user
            return  render_template('login.html', form = form)      # redirect(url_for('main_bp.dashboard'))
        flash('A user already exists with that email address.')
    return render_template('signup.html', title='Create an Account.', template='signup-page', body="Sign up for a user account.", form = form)


@app.route("/logout")
@login_required
def logout():
    """User log-out logic."""
    logout_user()
    return redirect(url_for('login'))



@app.route('/login', methods=['GET', 'POST'])
def login():
    """
    Log-in page for registered users.

    GET: Serve Log-in page.
    POST: Validate form and redirect user to dashboard.
    """
    if current_user.is_authenticated:
        return render_template('books.html')    #redirect(url_for('dashboard'))   Bypass if user is logged in

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()  # Validate Login Attempt
        if user and user.check_password(password=form.password.data):
            login_user(user) #remeber=form.remmber.data 
            return render_template('search.html')    #redirect(next_page or url_for('main_bp.dashboard'))
        else:
            flash('Invalid username/password combination')
        return render_template('book.html')
    return render_template('login.html', form=form, title='Log in.', template='login-page', body="Log in with your User account.")


@app.route("/books", methods=['GET', 'POST'])
def books():
    list_of_book = Books.query.all()
    return render_template("books.html", list_of_book=list_of_book)

@app.route("/search", methods=['GET', 'POST'])
def search():
    form = SearchForm()
    search = form.search.data
    if request.method == 'POST':
        search = form.search.data
        #TODO:INFO:: Filter the results before calling Books.query
        # Filter it like this
        if not search: # check for None value
            return " ---ROUTE TO YOUR Error PAGE ---"
        
        #TODO:INFO: make sure to remove spaces form beginning and end
        # SQLAlchemy is really sensitive and particular when query for data   
        search = search.strip() 
        results = Books.query.filter(Books.title.ilike(f'%{search}%')).all()

        #NOTE:DELETE: Delete these lines below. . This is just a test to check if result is populating correctly.
        test = results[0] if results else {'title':'None'}
        return f"""<h1>title: {test.title} </h1>
                    <ul>
                        <li>ID:{test.id}</li>
                        <li>ISBN: {test.isbn}</li>
                        <li>Author: {test.author}</li>
                        <li>YEAR {test.year}</li>
                    </ul>
                """
        # STOP DELETING HERE

        #TODO:NEED:: return to another page to show results
        #      You are returning to the same route so the search form 
        #      will rendering again
        return render_template('search.html', results=results, form=form, search=search)
    return render_template('search.html', form=form, search=search)


'''
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            next = request.args.get('next')
            if next is None or not next.startswith('/'):
                next = url_for('main.index')
                return redirect(next)
                flash('Invalid username or password.')
    return render_template('login.html', form=form)
'''



'''
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == "POST":
        session.pop('users_id')
        username = request.form['username']
        password = request.form['password']
        chek_user = Users.query.filter_by(username=Users.username).first() 
        if chek_user and Users.password = password: 
           session['Users_id'] = Users.username
           return render_template ("index.html", message="you logged succfully!!...")
    
        return render_template ("login.html", message="incorrect username or/and password please try again")
         
       
    return render_template("login.html")
'''




#server 
if __name__ == "__main__":
    app.run(port=5001,debug=True)
