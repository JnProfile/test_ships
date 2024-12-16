import random
import os
import glob
import sys
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from models.tables import Base, Ship, Weapon, Hull, Engine


def remove_old_databases():
    for f in glob.glob("data/temp*", recursive=True):
        os.remove(f)


def create_and_fill_database(session):
    for i in range(1, 21):
        weapon = Weapon(
            weapon=f"Weapon-{i}",
            reload_speed=random.randint(1, 20),
            rotational_speed=random.randint(1, 20),
            diameter=random.randint(1, 20),
            power_volley=random.randint(1, 20),
            count=random.randint(1, 20),
        )
        session.add(weapon)

    for i in range(1, 6):
        hull = Hull(
            hull=f"Hull-{i}",
            armor=random.randint(1, 20),
            type=random.randint(1, 20),
            capacity=random.randint(1, 20),
        )
        session.add(hull)

    for i in range(1, 7):
        engine = Engine(
            engine=f"Engine-{i}",
            power=random.randint(1, 20),
            type=random.randint(1, 20),
        )
        session.add(engine)

    session.commit()

    for i in range(1, 201):
        ship = Ship(
            ship=f"Ship-{i}",
            weapon=f"Weapon-{random.randint(1, 20)}",
            hull=f"Hull-{random.randint(1, 5)}",
            engine=f"Engine-{random.randint(1, 6)}",
        )
        session.add(ship)

    session.commit()
    session.close()


if __name__ == "__main__":
    remove_old_databases()
    os.makedirs("data", exist_ok=True)
    engine = create_engine("sqlite:///data/database.db")
    Base.metadata.create_all(bind=engine)

    Session = sessionmaker(bind=engine)
    session = Session()

    create_and_fill_database(session)

    session.close()
