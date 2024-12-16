import pytest
from tables import Ship, Weapon, Hull, Engine
from sqlalchemy.orm import Session


def test_ship(
    ship_id: str,
    component_name: str,
    original_db_session: Session,
    temp_db_session: Session,
):
    original_row = original_db_session.query(Ship).filter(Ship.ship == ship_id).first()
    temporary_row = temp_db_session.query(Ship).filter(Ship.ship == ship_id).first()

    original_component = getattr(original_row, component_name)
    temporary_component = getattr(temporary_row, component_name)

    if original_component != temporary_component:
        pytest.fail(
            f"{ship_id}, {original_component}\n"
            + f"\texpected: {original_component}, was: {temporary_component}"
        )

    components_model_map = {
        "weapon": Weapon,
        "hull": Hull,
        "engine": Engine,
    }

    component_model = components_model_map[component_name]
    primary_key = list(component_model.__table__.primary_key.columns.keys())[0]

    original_component_row = (
        original_db_session.query(component_model)
        .filter_by(**{primary_key: original_component})
        .first()
    )

    temporary_component_row = (
        temp_db_session.query(component_model)
        .filter_by(**{primary_key: temporary_component})
        .first()
    )

    failed_messages = []

    for column in component_model.__table__.columns:
        attribute_name = column.name
        original_value = getattr(original_component_row, attribute_name)
        temporary_value = getattr(temporary_component_row, attribute_name)

        if original_value != temporary_value:
            failed_messages.append(
                f"{attribute_name}: expected {original_value}, was {temporary_value}"
            )

    if failed_messages:
        pytest.fail(
            f"{ship_id}, {original_component}\n\t" + "\n\t".join(failed_messages)
        )
