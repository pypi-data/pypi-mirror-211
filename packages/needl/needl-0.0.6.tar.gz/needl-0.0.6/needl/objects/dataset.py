import pandas as pd


class DataSet:

    def __init__(self, internal_id, name, disease_samples, healthy_samples, abbreviation, notes, organism, origin, replicate, ancestry):
        self.internal_id = internal_id
        self.name = name
        self.disease_samples = disease_samples
        self.healthy_samples = healthy_samples
        self.abbreviation = abbreviation
        self.notes = notes
        self.organism = organism
        self.origin = origin
        self.replicate = replicate
        self.ancestry = ancestry

    def get_internal_id(self):
        return self.internal_id

    def get_name(self):
        return self.name

    def get_disease_samples(self):
        return self.disease_samples

    def get_healthy_samples(self):
        return self.healthy_samples

    def get_abbreviation(self):
        return self.abbreviation

    def get_notes(self):
        return self.notes

    def get_organism(self):
        return self.organism

    def get_origin(self):
        return self.origin

    def get_replicate(self):
        return self.replicate

    def get_ancestry(self):
        return self.ancestry

    def to_dataframe(self):
        df = pd.DataFrame(columns=["ID", "Name", "DiseaseSamples", "HealthySamples", "Abbreviation", "Notes",
                                   "Organism", "Origin", "IsReplicate", "Ancestry"])
        df.loc[0] = [self.internal_id, self.name, self.disease_samples, self.healthy_samples, self.abbreviation,
                     self.notes, self.organism, self.origin, self.replicate, self.ancestry]
        return df


def dataset_creator(info_dict: dict) -> DataSet:
    return DataSet(internal_id=info_dict["ID"], name=info_dict["Name"], disease_samples=info_dict["DiseaseSamples"],
                   healthy_samples=info_dict["HealthySamples"], abbreviation=info_dict["Abbreviation"],
                   notes=info_dict["Notes"], organism=info_dict["Organism"], origin=info_dict["Origin"],
                   replicate=info_dict["IsReplicate"], ancestry=info_dict["Ancestry"])


def datasets_creator(info_dict: dict) -> list:
    datasets = list()
    for dataset_info in info_dict:
        datasets.append(dataset_creator(info_dict=dataset_info))
    return datasets


