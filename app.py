from flask import Flask
from flask_migrate import Migrate
from models import db, Hero, Power  # Import Hero and Power models
from routes import bp  # Import your routes blueprint
import seeds  # Import seeds module

app = Flask(__name__)

# Load configuration from config.py
app.config.from_object('config.Config')

# Initialize the database
db.init_app(app)
migrate = Migrate(app, db)

# Register the routes blueprint
app.register_blueprint(bp, url_prefix='/')  

@app.route('/')
def home():
    return "Welcome to the Superhero API!"

@app.cli.command('seed_db')
def seed_db():
    """Seed the database with initial data."""
    with app.app_context():
        seeds.clear_db()       # Clear existing data
        seeds.seed_powers()    # Seed powers
        seeds.seed_heroes()     # Seed heroes
        heroes = Hero.query.all()  # Get all seeded heroes
        powers = Power.query.all()  # Get all seeded powers
        seeds.add_powers_to_heroes(heroes, powers)  # Assign powers to heroes
        print("Database seeded successfully!")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  # Create database tables if they don't exist
    app.run(debug=True)   # Start the application in debug mode
