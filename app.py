from flask import Flask
from flask_migrate import Migrate
from models import db, Hero, Power  
from routes import bp  
import seeds  

app = Flask(__name__)


app.config.from_object('config.Config')


db.init_app(app)
migrate = Migrate(app, db)


app.register_blueprint(bp, url_prefix='/')  

@app.route('/')
def home():
    return "Welcome to the Superhero API!"

@app.cli.command('seed_db')
def seed_db():
    """Seed the database with initial data."""
    with app.app_context():
        seeds.clear_db()       
        seeds.seed_powers()    
        seeds.seed_heroes()     
        heroes = Hero.query.all()  
        powers = Power.query.all()  
        seeds.add_powers_to_heroes(heroes, powers)  
        print("Database seeded successfully!")

if __name__ == '__main__':
    with app.app_context():
        db.create_all()  
    app.run(debug=True)   
