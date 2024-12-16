import pytest
import random
import os
import glob
from warnings import warn
from time import sleep
from tables import Ship, Weapon, Hull, Engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine


@pytest.fixture(scope="session")
def cleanup_temp_database():
    for f in glob.glob("data/temp*", recursive=True):
        os.remove(f)


@pytest.fixture(scope="session")
def original_db_session():
    engine = create_engine("sqlite:///data/database.db")
    Session = sessionmaker(bind=engine)
    session = Session()

    yield session

    session.close()


@pytest.fixture(scope="session")
def temp_db_session(cleanup_temp_database):
    if not os.path.exists("data/database.db"):
        raise FileNotFoundError("Original database file not found")

    original_engine = create_engine("sqlite:///data/database.db")
    temp_engine = create_engine("sqlite:///data/temporary_database.db")

    original_connection = original_engine.raw_connection().driver_connection
    temp_connection = temp_engine.raw_connection().driver_connection

    try:
        original_connection.backup(temp_connection)
    finally:
        original_connection.close()
        original_engine.dispose()

    TempSession = sessionmaker(bind=temp_engine)
    temp_session = TempSession()

    weapons = temp_session.query(Weapon).all()
    hulls = temp_session.query(Hull).all()
    engines = temp_session.query(Engine).all()
    ships = temp_session.query(Ship).all()

    for ship in ships:
        choices = ["weapon", "hull", "engine"]
        component_to_change = random.choice(choices)

        # Randomly change the weapon, hull, or engine of the ship
        if component_to_change == "weapon":
            random_weapon = random.choice(weapons)
            ship.weapon = random_weapon.weapon

        elif component_to_change == "hull":
            random_hull = random.choice(hulls)
            ship.hull = random_hull.hull

        elif component_to_change == "engine":
            random_engine = random.choice(engines)
            ship.engine = random_engine.engine

        if "weapon" in choices:
            weapon_object = (
                temp_session.query(Weapon).filter(Weapon.weapon == ship.weapon).first()
            )
            Weapon.change_random_attribute(weapon_object)

        if "hull" in choices:
            hull_object = (
                temp_session.query(Hull).filter(Hull.hull == ship.hull).first()
            )
            Hull.change_random_attribute(hull_object)

        if "engine" in choices:
            engine_object = (
                temp_session.query(Engine).filter(Engine.engine == ship.engine).first()
            )
            Engine.change_random_attribute(engine_object)

        temp_session.merge(ship)

    temp_session.commit()

    yield temp_session

    temp_session.close()


def pytest_generate_tests(metafunc):
    if "ship_id" in metafunc.fixturenames and "component_name" in metafunc.fixturenames:
        engine = create_engine("sqlite:///data/database.db")
        Session = sessionmaker(bind=engine)
        session = Session()

        ships = session.query(Ship).all()

        params = []
        for ship in ships:
            for component in ["weapon", "hull", "engine"]:
                params.append((ship.ship, component))

        session.close()

        metafunc.parametrize("ship_id, component_name", params)
