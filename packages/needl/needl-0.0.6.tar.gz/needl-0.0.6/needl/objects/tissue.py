import pandas as pd

class Tissue:

    def __init__(self, internal_id: int, name : str, organism: str ):
        self.internal_id = internal_id
        self.name = name
        self.organism = organism

    def get_internal_id(self):
        return self.internal_id

    def get_name(self):
        return self.name

    def get_organism(self):
        return self.organism

    def to_dataframe(self):
        df = pd.DataFrame(columns=["ID", "Name", "Organism"])
        df.loc[0] = [self.internal_id, self.name, self.organism]
        return df

def tissue_creator(info_dict: dict) -> Tissue:
    return Tissue(internal_id=info_dict["ID"], name=info_dict["Name"], organism=info_dict["Organism"])

def tissues_creator(info_dict: dict):
    tissues = list()
    for tissue_info in info_dict:
        tissues.append(tissue_creator(info_dict=tissue_info))
    return tissues
