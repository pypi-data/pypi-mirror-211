class GeneOntology:

    def __init__(self, go_key, name, description, category):
        self.go_key = go_key
        self.name = name
        self.description = description
        self.category = category

    def get_go_key(self):
        return self.go_key

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description

    def get_category(self):
        return self.category


def go_creator(info_dict: dict):
    return GeneOntology(go_key=info_dict["GOKey"], name=info_dict["GOSymbol"],
                        description=info_dict["Description"], category=info_dict["Category"])


def gos_creator(info_dict: dict):
    gos = list()
    for go_info in info_dict:
        gos.append(go_creator(info_dict=go_info))
    return gos


class WikiPathways:

    def __init__(self, pathways_id, name, description):
        self.pathways_id = pathways_id
        self.name = name
        self.description = description

    def get_pathways_id(self):
        return self.pathways_id

    def get_name(self):
        return self.name

    def get_description(self):
        return self.description


def pathway_creator(info_dict: dict):
    return WikiPathways(pathways_id=info_dict["Wikipathways_key"], name=info_dict["Name"], description=info_dict["Description"])


def pathways_creator(info_dict: dict):
    pathways = list()
    for pathway_info in info_dict:
        pathways.append(pathway_creator(info_dict=pathway_info))
    return pathways





