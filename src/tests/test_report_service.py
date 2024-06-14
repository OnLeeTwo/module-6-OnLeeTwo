import pytest
from services.report import generate_animal_reports


mock_animals = {
    "A-1234": {
        "enclosure_id": "EN-HSH324",
        "name": "Simba",
        "species": "Panthera leo",
        "familia": "Felidae",
        "age": 5,
        "gender": "Male",
    },
    "A-5678": {
        "enclosure_id": "EN-HSH324",
        "name": "Nala",
        "species": "Panthera leo",
        "familia": "Felidae",
        "age": 4,
        "gender": "Female",
    },
    "A-9101": {
        "enclosure_id": "EN-HSH325",
        "name": "Mufasa",
        "species": "Panthera leo",
        "familia": "Felidae",
        "age": 8,
        "gender": "Male",
    },
    "A-1121": {
        "enclosure_id": "EN-HSH326",
        "name": "Dumbo",
        "species": "Loxodonta africana",
        "familia": "Elephantidae",
        "age": 7,
        "gender": "Female",
    },
    "A-3141": {
        "enclosure_id": "EN-HSH327",
        "name": "Pingu",
        "species": "Aptenodytes forsteri",
        "familia": "Spheniscidae",
        "age": 3,
        "gender": "Male",
    },
}

mock_enclosures = {
    "EN-HSH324": {
        "name": "Savannah",
        "type": "Outdoor",
        "animals": ["A-1234", "A-5678"],
    },
    "EN-HSH325": {"name": "Jungle", "type": "Outdoor", "animals": ["A-9101"]},
    "EN-HSH326": {"name": "Forest", "type": "Outdoor", "animals": ["A-1121"]},
    "EN-HSH327": {"name": "Arctic", "type": "Outdoor", "animals": ["A-3141"]},
}


# Unit tests
def test_generate_animal_reports():
    reports = generate_animal_reports(mock_animals, mock_enclosures)

    assert len(reports) == 3

    for report in reports:
        if report["species"] == "Panthera leo":
            assert report["gender_distribution"] == {"Male": 2, "Female": 1}
            assert report["enclosure_distribution"] == {"Savannah": 2, "Jungle": 1}
        elif report["species"] == "Loxodonta africana":
            assert report["gender_distribution"] == {"Male": 0, "Female": 1}
            assert report["enclosure_distribution"] == {"Forest": 1}
        elif report["species"] == "Aptenodytes forsteri":
            assert report["gender_distribution"] == {"Male": 1, "Female": 0}
            assert report["enclosure_distribution"] == {"Arctic": 1}
