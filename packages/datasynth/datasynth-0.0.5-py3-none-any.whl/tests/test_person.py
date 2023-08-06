from datasynth.models.person import Person

import pandas as pd
import pytest


def test_person():
    pers_gen = Person(
        attributes=["first_name", "last_name", "city", "state", "postcode", "ssn"]
    )
    people = pers_gen.generate_people(number=10)
    people_df = pd.DataFrame(people)
    assert people_df.shape[0] == 10
    assert people_df.columns.values.tolist() == [
        "first_name",
        "last_name",
        "city",
        "state",
        "postcode",
        "ssn",
    ]


def test_wrong_attribute():
    pers_gen = Person(attributes=["first_na"])
    with pytest.raises(
        Exception,
        match="Attribute - first_na - does not have a Faker provider. Attribute name must be a Faker provider method. See default list here: https://faker.readthedocs.io/en/master/providers.html",
    ):
        people = pers_gen.generate_people(number=10)
