from random import choice as rc
from models import db, Hero, Power, HeroPower

def clear_db():
    """Clear the database of all data."""
    print("Clearing db...")
    HeroPower.query.delete()  
    Power.query.delete()       
    Hero.query.delete()        
    db.session.commit()
    print("Database cleared!")

def seed_powers():
    """Seed the database with powers."""
    print("Seeding powers...")
    powers = [
        Power(name="Super Strength", description="Gives the wielder super-human strength."),
        Power(name="Flight", description="Gives the wielder the ability to fly through the skies at supersonic speed."),
        Power(name="Super Human Senses", description="Allows the wielder to use her senses at a super-human level."),
        Power(name="Elasticity", description="Can stretch the human body to extreme lengths."),
    ]
    db.session.add_all(powers)
    db.session.commit()
    print("Powers seeded!")

def seed_heroes():
    """Seed the database with heroes."""
    print("Seeding heroes...")
    heroes = [
        Hero(name="Kamala Khan", super_name="Ms. Marvel"),
        Hero(name="Doreen Green", super_name="Squirrel Girl"),
        Hero(name="Gwen Stacy", super_name="Spider-Gwen"),
        Hero(name="Janet Van Dyne", super_name="The Wasp"),
        Hero(name="Wanda Maximoff", super_name="Scarlet Witch"),
        Hero(name="Carol Danvers", super_name="Captain Marvel"),
        Hero(name="Jean Grey", super_name="Dark Phoenix"),
        Hero(name="Ororo Munroe", super_name="Storm"),
        Hero(name="Kitty Pryde", super_name="Shadowcat"),
        Hero(name="Elektra Natchios", super_name="Elektra"),
    ]
    db.session.add_all(heroes)
    db.session.commit()
    print("Heroes seeded!")

def add_powers_to_heroes(heroes, powers):
    """Randomly assign powers to heroes."""
    print("Adding powers to heroes...")
    strengths = ["Strong", "Weak", "Average"]
    hero_powers = []
    for hero in heroes:
        power = rc(powers)  
        hero_power = HeroPower(hero=hero, power=power, strength=rc(strengths))
        hero_powers.append(hero_power)
    db.session.add_all(hero_powers)
    db.session.commit()
    print("Powers added to heroes!")

def run_seeding():
    """Run the seeding process within the app context."""
    with app.app_context():
        clear_db()
        seed_powers()
        seed_heroes()
        heroes = Hero.query.all()  
        powers = Power.query.all()  
        add_powers_to_heroes(heroes, powers)
        print("Done seeding!")

if __name__ == '__main__':
    from app import app  
    with app.app_context():
        run_seeding()
