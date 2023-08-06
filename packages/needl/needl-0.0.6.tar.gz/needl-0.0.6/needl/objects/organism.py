import pandas as pd


class Organism:

    def __init__(self, internal_id, name, description: str = None, database_name: str = None, database_url: str = None):
        self.internal_id = internal_id
        self.name = name
        self.description = description
        self.database_name = database_name
        self.database_url = database_url

    def get_internal_id(self):
        return self.internal_id

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def get_database_name(self):
        return self.database_name

    def get_database_url(self):
        return self.database_url

    def to_dataframe(self):
        df = pd.DataFrame(columns=["ID", "Name", "Description", "DatabaseName", "DatabaseURL"])
        df.loc[0] = [self.internal_id, self.name, self.description, self.database_name, self.database_url]
        return df


def organism_creator(info_dict: dict):
    description = info_dict["Description"] if "Description" in info_dict else None
    db_name = info_dict["DatabaseName"] if "DatabaseName" in info_dict else None
    db_url = info_dict["DatabaseURL"] if "DatabaseURL" in info_dict else None
    return Organism(internal_id=info_dict["ID"], name=info_dict["Name"], description=description,
                    database_name=db_name, database_url=db_url)


def organisms_creator(info_dict: dict):
    organisms = list()
    for organism_info in info_dict:
        organisms.append(organism_creator(info_dict=organism_info))
    return organisms
