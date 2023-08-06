from .gene import genes_creator
import pandas as pd

class Variant:

    def __init__(self, internal_id, rsid, description: str = None, genes: list = None, chromosome: str = None,
                 position : int = None, cytoband :str = None):
        self.internal_id = internal_id
        self.rsid = rsid
        self.description = description
        self.genes = genes
        self.chromosome = chromosome
        self.position = position
        self.cytoband = cytoband

    def get_internal_id(self):
        return self.internal_id

    def get_rsid(self):
        return self.rsid

    def get_description(self):
        return self.description

    def get_genes(self):
        return self.genes

    def get_chromosome(self):
        return self.chromosome

    def get_position(self):
        return self.position

    def get_cytoband(self):
        return self.cytoband

    def to_dataframe(self):
        df = pd.DataFrame(columns=["ID", "RSID", "Description", "Genes", "Chromosome", "Position", "Cytoband"])
        df.loc[0] = [self.internal_id, self.rsid, self.description, self.genes, self.chromosome, self.position, self.cytoband]
        return df


def variant_creator(info_dict: dict):
    if not type(info_dict) is dict:
        return Variant(internal_id=info_dict, rsid=None, description=None,
                       genes=None, chromosome=None, position=None, cytoband=None)
    rsid = info_dict["RSID"] if "RSID" in info_dict else None
    description = info_dict["Description"] if "Description" in info_dict else None
    genes = genes_creator(info_dict=info_dict["Genes"]) if "Genes" in info_dict else None
    chromosome = info_dict["Chromosome"] if "Chromosome" in info_dict else None
    position = info_dict["Position"] if "Position" in info_dict else None
    cytoband = info_dict["Cytoband"] if "Cytoband" in info_dict else None
    return Variant(internal_id=info_dict["ID"], rsid=rsid, description=description, genes=genes,
                   chromosome=chromosome, position=position, cytoband=cytoband)


def variants_creator(info_dict: dict):
    variants = list()
    for variants_info in info_dict:
        variants.append(variant_creator(info_dict=variants_info))
    return variants
