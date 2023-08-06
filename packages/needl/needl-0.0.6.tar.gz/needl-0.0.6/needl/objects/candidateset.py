from .dataset import DataSet
from .variant import variants_creator
from .score import scores_creator
import pandas as pd

class CandidateSet:

    def __init__(self, internal_id, dataset, snps: list, scores: list = None, ranks: str = None):
        self.internal_id = internal_id
        self.dataset = dataset
        self.snps = snps
        self.scores = scores
        self.ranks = ranks

    def get_internal_id(self):
        return self.internal_id

    def get_dataset(self):
        return self.dataset

    def get_snps(self):
        return self.snps

    def get_scores(self):
        return self.scores

    def get_ranks(self):
        return self.ranks

    def to_dataframe(self):
        df = pd.DataFrame(columns=["ID", "SNPs", "Scores", "Ranks"])
        df.loc[0] = [self.internal_id, self.snps, self.scores, self.ranks]
        return df


def candidateset_creator(info_dict: dict, dataset: DataSet = None) -> CandidateSet:
    if info_dict is None:
        return None
    variants = variants_creator(info_dict=info_dict["SNPs"]) if "SNPs" in info_dict else None
    scores = scores_creator(info_dict=info_dict["Scores"]) if "Scores" in info_dict else None
    ranks = scores_creator(info_dict=info_dict["Ranks"]) if "Ranks" in info_dict else None
    return CandidateSet(internal_id=info_dict["ID"], dataset=dataset,
                        snps=variants, scores=scores, ranks=ranks)


def candidatesets_creator(info_dict: dict, dataset: DataSet = None) -> list:
    candidate_sets = list()
    for candidate_set_info in info_dict:
        candidate_sets.append(candidateset_creator(info_dict=candidate_set_info, dataset=dataset))
    return candidate_sets
