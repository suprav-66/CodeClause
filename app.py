from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
import secrets
import string
from models import db, User, URL

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///url_shortener.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'your_secret_key'

db.init_app(app)

# Create all tables within the context of the application
with app.app_context():
    db.create_all()
    print("Database tables created successfully.")

# Function to generate a short URL
def generate_short_url():
    characters = string.ascii_letters + string.digits
    short_url = ''.join(secrets.choice(characters) for i in range(6))
    return short_url

# Routes
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        try:
            new_user = User(username=username, password=password)
            db.session.add(new_user)
            db.session.commit()
            return redirect(url_for('login'))
        except IntegrityError:
            db.session.rollback()
            return 'Username already exists!'
    
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Replace with your actual authentication logic
        user = User.query.filter_by(username=username, password=password).first()

        if user:
            session['user_id'] = user.id
            return redirect(url_for('dashboard'))
        else:
            return 'Invalid username or password!'
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('index'))

@app.route('/dashboard')
def dashboard():
    if 'user_id' not in session:
        return redirect(url_for('login'))

    user_id = session['user_id']
    user = User.query.get(user_id)
    urls = URL.query.filter_by(user_id=user_id).all()

    return render_template('dashboard.html', user=user, urls=urls)

@app.route('/shorten_url', methods=['POST'])
def shorten_url():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('login'))

    original_url = request.form['url']

    # Generate a short URL
    short_url = generate_short_url()

    # Save to the database
    new_url = URL(original_url=original_url, short_url=short_url, user_id=user_id)
    db.session.add(new_url)
    db.session.commit()

    # Optionally return JSON response (adjust as needed)
    return jsonify({'message': 'URL shortened successfully', 'short_url': short_url})

@app.route('/<short_url>')
def redirect_to_url(short_url):
    url = URL.query.filter_by(short_url=short_url).first_or_404()
    url.click_count += 1
    db.session.commit()
    return redirect(url.original_url)

@app.route('/analytics/<short_url>')
def get_analytics(short_url):
    url = URL.query.filter_by(short_url=short_url).first_or_404()
    return render_template('analytics.html', url=url)

if __name__ == '__main__':
    app.run(debug=True)
