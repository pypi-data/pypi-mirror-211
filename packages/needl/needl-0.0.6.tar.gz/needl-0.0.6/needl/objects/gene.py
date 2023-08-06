from .ontology import gos_creator, pathways_creator
import pandas as pd

class Gene:

    def __init__(self, internal_id, name, entrez_id, ensembl_id, cytoband,
                 description, organism, wikipathways, geneontology):
        self.internal_id = internal_id
        self.name = name
        self.entrez_id = entrez_id
        self.ensembl_id = ensembl_id
        self.cytoband = cytoband
        self.description = description
        self.organism = organism
        self.wikipathways = wikipathways
        self.geneontology = geneontology

    def get_internal_id(self):
        return self.internal_id

    def get_name(self):
        return self.name

    def get_entrez_id(self):
        return self.entrez_id

    def get_ensembl_id(self):
        return self.ensembl_id

    def get_cytoband(self):
        return self.cytoband

    def get_description(self):
        return self.description

    def get_organism(self):
        return self.organism

    def get_wikipathways(self):
        return self.wikipathways

    def get_geneontology(self):
        return self.geneontology

    def to_dataframe(self):
        df = pd.DataFrame(columns=["ID", "Name", "EntrezID", "EnsemblID", "Cytoband", "Description", "Organism",
                                   "Wikipathways", "GeneOntology"])
        df.loc[0] = [self.internal_id, self.name, self.entrez_id, self.ensembl_id, self.cytoband, self.description,
                     self.organism, self.wikipathways, self.geneontology]
        return df


def gene_creator(info_dict: dict):
    if not type(info_dict) is dict:
        return Gene(internal_id=info_dict, name=None, entrez_id=None,
                    ensembl_id=None, cytoband=None, description=None,
                    organism=None, wikipathways=None, geneontology=None)
    organism = info_dict["Organism"] if "Organism" in info_dict else None
    gos = gos_creator(info_dict=info_dict["GeneOntology"]) if "GeneOntology" in info_dict else None
    pathways = pathways_creator(info_dict=info_dict["Wikipathways"]) if "Wikipathways" in info_dict else None
    cytoband = info_dict["Cytoband"] if "Cytoband" in info_dict else None
    description = info_dict["Description"] if "Description" in info_dict else None
    return Gene(internal_id=info_dict["ID"], name=info_dict["Name"], entrez_id=info_dict["EntrezID"],
                ensembl_id=info_dict["EnsemblID"], cytoband=cytoband, description=description,
                organism=organism, wikipathways=pathways, geneontology=gos)


def genes_creator(info_dict: dict):
    genes = list()
    for gene_info in info_dict:
        genes.append(gene_creator(info_dict=gene_info))
    return genes
