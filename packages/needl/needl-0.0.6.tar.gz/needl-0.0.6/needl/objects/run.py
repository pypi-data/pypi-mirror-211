import pandas as pd

from needl.objects.dataset import dataset_creator


class Run:

    def __init__(self, internal_id, dataset, seeding_routine, model, kmin, kmax, local_search_rounds, maf_filter,
                mma_filter, community_detection, percentage_biological_qc, integrate_new_connections, notes):
        self.internal_id = internal_id
        self.dataset = dataset
        self.seeding_routine = seeding_routine
        self.model = model
        self.kmin = kmin
        self.kmax = kmax
        self.local_search_rounds = local_search_rounds
        self.maf_filter = maf_filter
        self.mma_filter = mma_filter
        self.community_detection = community_detection
        self.percentage_biological_qc = percentage_biological_qc
        self.integrate_new_connections = integrate_new_connections
        self.notes = notes

    def get_internal_id(self):
        return self.internal_id

    def get_dataset(self):
        return self.dataset

    def get_seeding_routine(self):
        return self.seeding_routine

    def get_model(self):
        return self.model

    def get_kmin(self):
        return self.kmin

    def get_kmax(self):
        return self.kmax

    def get_local_search_rounds(self):
        return self.local_search_rounds

    def get_maf_filter(self):
        return self.maf_filter

    def get_mma_filter(self):
        return self.mma_filter

    def get_community_detection(self):
        return self.community_detection

    def get_percentage_biological_qc(self):
        return self.percentage_biological_qc

    def get_integrate_new_connections(self):
        return self.integrate_new_connections

    def get_notes(self):
        return self.notes

    def to_dataframe(self):
        df = pd.DataFrame(columns=["ID", "Dataset", "SeedingRoutine", "Model", "Kmin", "Kmax", "LocalSearchRounds",
                                   "MAFFilter", "MMAFilter", "CommunityDetection", "PercentageBiologicalQC",
                                   "IntegrateNewConnections", "Notes"])
        df.loc[0] = [self.internal_id, self.dataset, self.seeding_routine, self.model, self.kmin, self.kmax,
                     self.local_search_rounds, self.maf_filter, self.mma_filter, self.community_detection,
                     self.percentage_biological_qc, self.integrate_new_connections, self.notes]
        return df

def run_creator(info_dict: dict) -> Run:
    dataset = dataset_creator(info_dict["Dataset"]) if "Dataset" in info_dict else None
    return Run(internal_id=info_dict["ID"], dataset=dataset, seeding_routine=info_dict["SeedingRoutine"],
               model=info_dict["Model"], kmin=info_dict["KMin"], kmax=info_dict["KMax"],
               local_search_rounds=info_dict["LocalSearchRounds"], maf_filter=info_dict["MAFFilter"],
               mma_filter=info_dict["MMAFilter"], community_detection=info_dict["CommunityDetection"],
               percentage_biological_qc=info_dict["PercentageBiologicalQC"],
               integrate_new_connections=info_dict["IntegrateNewConnections"], notes=info_dict["Notes"])

def runs_creator(info_dict: dict) -> list:
    runs = []
    for run in info_dict:
        runs.append(run_creator(run))
    return runs