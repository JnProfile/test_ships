import random
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import declarative_base

Base = declarative_base()


class RandomAttributeInterface:
    @classmethod
    def change_random_attribute(cls, instance):
        attributes = [
            column.name
            for column in cls.__table__.columns
            if column.name != cls.__mapper__.primary_key[0].name
        ]

        random_attribute = random.choice(attributes)
        random_value = random.randint(1, 20)

        setattr(instance, random_attribute, random_value)

        return random_attribute, random_value


class Weapon(Base, RandomAttributeInterface):
    __tablename__ = "weapons"
    weapon = Column(String, primary_key=True)
    reload_speed = Column(Integer)
    rotational_speed = Column(Integer)
    diameter = Column(Integer)
    power_volley = Column(Integer)
    count = Column(Integer)


class Hull(Base, RandomAttributeInterface):
    __tablename__ = "hulls"
    hull = Column(String, primary_key=True)
    armor = Column(Integer)
    type = Column(Integer)
    capacity = Column(Integer)


class Engine(Base, RandomAttributeInterface):
    __tablename__ = "engines"
    engine = Column(String, primary_key=True)
    power = Column(Integer)
    type = Column(Integer)


class Ship(Base, RandomAttributeInterface):
    __tablename__ = "ships"
    ship = Column(String, primary_key=True)
    weapon = Column(String, ForeignKey("weapons.weapon"))
    hull = Column(String, ForeignKey("hulls.hull"))
    engine = Column(String, ForeignKey("engines.engine"))
