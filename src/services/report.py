def generate_animal_reports(animals_data, enclosures_data):
    new_reports = []

    species_set = set(animal["species"] for animal in animals_data.values())

    for species in species_set:
        gender_distribution = {"Male": 0, "Female": 0}
        enclosure_distribution = {}

        for animal_id, animal in animals_data.items():
            if animal["species"] == species:
                gender = animal["gender"]
                if gender in gender_distribution:
                    gender_distribution[gender] += 1

                enclosure_id = animal["enclosure_id"]
                enclosure_name = enclosures_data[enclosure_id]["name"]
                if enclosure_name in enclosure_distribution:
                    enclosure_distribution[enclosure_name] += 1
                else:
                    enclosure_distribution[enclosure_name] = 1

        new_reports.append(
            {
                "species": species,
                "gender_distribution": gender_distribution,
                "enclosure_distribution": enclosure_distribution,
            }
        )

    return new_reports
