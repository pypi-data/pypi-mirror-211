"""Get Entries from Disease Atlas"""

import pandas as pd
from needl import api_handler as ah
from needl.objects.gene import Gene, gene_creator, genes_creator
from needl.objects.run import Run, run_creator, runs_creator
from needl.objects.tissue import tissues_creator, Tissue
from needl.objects.variant import Variant, variant_creator, variants_creator
from needl.objects.organism import Organism, organism_creator, organisms_creator
from needl.objects.candidateset import CandidateSet, candidateset_creator, candidatesets_creator
from needl.objects.dataset import DataSet, dataset_creator, datasets_creator

url_base = "https://api.epistasis-disease-atlas.com/"


def get_variant(internal_id: int = None, variant_id: str = None) -> Variant:
    """
    Get a variant based on its internal ID or variant ID, also known as rsID.

    :param internal_id: internal ID of variant in database
    :param variant_id: rsID of variant
    :return: retrieved variant as Variant object
    """
    if internal_id is not None:
        url = f"{url_base}get_variant?id={internal_id}"
    elif variant_id is not None:
        url = f"{url_base}get_variant?rsid={variant_id}"
    else:
        raise Exception("Please enter either an internal ID or a variant ID.")
    resp = ah.call_api(url=url)
    result = ah.check_response(resp=resp, return_type="json")
    variant = variant_creator(info_dict=result)
    return variant

def get_variants(internal_ids: list = None, variant_ids: list = None) -> list:
    """
    Get variants based on their internal IDs or variant IDs, also known as rsIDs.

    :param internal_ids: list of internal IDs of variants in database
    :param variant_ids: list of rsIDs of variants
    :return: retrieved variants as list of Variant objects
    """
    url = f"{url_base}get_variants"
    if internal_ids is not None:
        json = {"ids": internal_ids}
    elif variant_ids is not None:
        json = {"rsids": variant_ids}
    else:
        raise Exception("Please enter either internal IDs or variant IDs.")
    resp = ah.call_api(url=url, json=json)
    result = ah.check_response(resp=resp, return_type="json")
    variants = variants_creator(info_dict=result)
    return variants

def get_gene(internal_id: int = None, name: str = None, entrez: str = None, ensembl: str = None) -> Gene:
    """
    Get a gene based on its internal ID, name, entrez or ensembl ID.

    :param internal_id: internal ID of gene in database
    :param name: gene symbol
    :param entrez: entrez ID of gene
    :param ensembl: ensembl ID of gene
    :return: retrieved gene as Gene object
    """
    if internal_id is not None:
        url = f"{url_base}get_gene?id={internal_id}"
    elif name is not None:
        url = f"{url_base}get_gene?name={name}"
    elif entrez is not None:
        url = f"{url_base}get_gene?entrez={entrez}"
    elif ensembl is not None:
        url = f"{url_base}get_gene?ensembl={ensembl}"
    else:
        raise Exception("Please enter either an internal ID, a gene name, an entrez ID or an ensemble ID.")
    resp = ah.call_api(url=url)
    result = ah.check_response(resp=resp, return_type="json")
    gene = gene_creator(info_dict=result)
    return gene


def get_genes(internal_ids: list = None, names: list = None, entrez_ids: list = None, ensembl_ids: list = None) -> list:
    """
    Get a genes based on their internal IDs, names or gene IDs.

    :param internal_ids: list of internal IDs of genes in database
    :param names: list of gene symbols
    :param entrez_ids: list of entrez IDs of genes
    :param ensembl_ids: list of ensembl IDs of genes
    :return: list with retrieved genes as Gene object
    """
    url = f"{url_base}get_genes"
    if internal_ids is not None:
        json = {"ids": internal_ids}
    elif names is not None:
        json = {"names": names}
    elif entrez_ids is not None:
        json = {"entrez": entrez_ids}
    elif ensembl_ids is not None:
        json = {"ensembl": ensembl_ids}
    else:
        raise Exception("Please enter either a gene IDs, names, entrez IDs or ensembl IDs.")
    resp = ah.call_api(url=url, json=json)
    result = ah.check_response(resp=resp, return_type="json")
    genes = genes_creator(info_dict=result)
    return genes


def match_genes(query: str) -> list:
    """
    Search for substring in gene symbols, entrez IDS or ensembl IDs.

    :param query: substring that should match
    :return: list of genes matched by substring
    """
    url = f"{url_base}match_genes?query={query}"
    resp = ah.call_api(url=url)
    result = ah.check_response(resp=resp, return_type="json")
    genes = genes_creator(info_dict=result)
    return genes


def get_variants_affecting_gene(gene_id: str = None, gene: Gene = None) -> list:
    """
    A Gene is directly influenced by Variants that occur within the genomic boundaries of the Gene or through
    indirect effects like for example changes in the upstream area. Get all variants affecting a gene using
    an internal gene id or a gene object.

    :param gene_id: internal ID of gene in database
    :param gene: Gene object
    :return: list of variants affecting input gene
    """
    if gene_id is not None:
        url = f"{url_base}get_variants_affecting_gene?id={gene_id}"
    elif gene is not None:
        url = f"{url_base}get_variants_affecting_gene?id={gene.get_internal_id()}"
    else:
        raise Exception("Please enter either an internal gene ID or a gene object.")
    resp = ah.call_api(url=url)
    result = ah.check_response(resp=resp, return_type="json")
    variants = variants_creator(info_dict=result)
    return variants


def get_variants_affecting_genes(gene_ids: list = None, genes: list = None) -> list:
    """
    A Gene is directly influenced by Variants that occur within the genomic boundaries of the Gene or through
    indirect effects like for example changes in the upstream area. Get all variants affecting a list of genes using
    a list of internal gene ids or a list of gene objects.

    :param gene_ids: list of internal IDs of genes in database
    :param genes: list of Gene objects
    :return: list of variants affecting input genes
    """
    url = f"{url_base}get_variants_affecting_genes"
    if gene_ids is not None:
        json = {"ids": gene_ids}
    elif genes is not None:
        json = {"ids": [gene.get_internal_id() for gene in genes]}
    else:
        raise Exception("Please enter either internal gene IDs or gene objects.")
    resp = ah.call_api(url=url, json=json)
    result = ah.check_response(resp=resp, return_type="json")
    variants = variants_creator(info_dict=result)
    return variants

def get_organism(internal_id: int = None, organism_name: str = None) -> Organism:
    """
    Get an Organism entry by internal ID or name

    :param internal_id: internal ID of organism
    :param organism_name: name of the organism
    :return: organism as Organism object
    """
    if internal_id is not None:
        url = f"{url_base}get_organism?id={internal_id}"
    elif organism_name is not None:
        url = f"{url_base}get_organism?name={organism_name}"
    else:
        raise Exception("Please enter either an internal ID or an organism name.")
    resp = ah.call_api(url=url)
    result = ah.check_response(resp=resp, return_type="json")
    organism = organism_creator(info_dict=result)
    return organism


def list_organisms() -> list:
    """
    List all organisms present in this database.

    :return: list of organisms of type Organism
    """
    url = f"{url_base}list_organisms"
    resp = ah.call_api(url=url)
    result = ah.check_response(resp=resp, return_type="json")
    organisms = organisms_creator(info_dict=result)
    return organisms


def get_dataset(internal_id: int = None, dataset_name: str = None) -> list:
    """
    Get a Dataset entry by internal ID or name.

    :param dataset_name: dataset name
    :param internal_id: dataset internal ID
    :return: list of matched datasets as DataSet object
    """
    if dataset_name is not None:
        url = f"{url_base}get_dataset?name={dataset_name}"
    elif internal_id is not None:
        url = f"{url_base}get_dataset?id={internal_id}"
    else:
        raise Exception("Please enter either a dataset name or a dataset ID.")
    resp = ah.call_api(url=url)
    result = ah.check_response(resp=resp, return_type="json")
    datasets = datasets_creator(info_dict=result)
    return datasets[0]


def list_datasets() -> list:
    """
    Lists all Datasets available in the Epistasis Disease Atlas.

    :return: list of datasets as DataSet object
    """
    url = f"{url_base}list_datasets"
    resp = ah.call_api(url=url)
    result = ah.check_response(resp=resp, return_type="json")
    datasets = datasets_creator(info_dict=result)
    return datasets


def get_runs(dataset_id: int = None, dataset: DataSet = None) -> list:
    """
    Lists all Runs performed on a single Dataset for evaluation of CandidateSets of Genes being in epistais.

    :param dataset_id: internal dataset ID
    :param dataset: dataset as DataSet object
    :return: all runs listed in form of a dataframe
    """
    if dataset_id is not None:
        url = f"{url_base}get_runs?dataset={dataset_id}"
    elif dataset is not None:
        url = f"{url_base}get_runs?dataset={dataset.get_internal_id()}"
    else:
        raise Exception("Please enter either an internal dataset ID or a dataset object.")
    resp = ah.call_api(url=url)
    result = ah.check_response(resp=resp, return_type="json")
    runs = runs_creator(info_dict=result["Runs"])
    return runs


def get_run(internal_id: int) -> Run:
    """
    A Run defines the evaluation of a specific CandidateSet of Genes on a Dataset to estimate
    the chances of them being in epistatis. Get run details based on an internal run ID.

    :param internal_id: internal run ID
    :return: details of the given run in dataframe format
    """
    url = f"{url_base}get_run?id={internal_id}"
    resp = ah.call_api(url=url)
    result = ah.check_response(resp=resp, return_type="json")
    run = run_creator(info_dict=result)
    return run


def get_candidate_set(internal_id: int, run_id: int = None, scoretype_id: int = None) -> CandidateSet:
    """
    A CandidateSet is a set of Variants being evaluated of being in epistatis given a specific Dataset in a Run.
    Get the candidate set based on an internal ID.

    :param internal_id: internal ID of candidate set
    :param run_id: internal ID of run
    :param scoretype_id: internal ID of scoretype
    :return: candidate set as CandidateSet object
    """
    url = f"{url_base}get_candidate_set?id={internal_id}"
    if run_id is not None:
        url += f"&run={run_id}"
    if scoretype_id is not None:
        url += f"&scoretype={scoretype_id}"
    resp = ah.call_api(url=url)
    result = ah.check_response(resp=resp, return_type="json")
    candidate_set = candidateset_creator(info_dict=result)
    return candidate_set


def get_candidate_sets(run_id: int = None, dataset_id: int = None, scoretype_id: int = None) -> list:
    """
    CandidateSets are linked to the Runs they are used in or to Datasets they were evaluated on for epistasis.
    Get candidate sets fom a internal run ID, internal dataset ID or a scoretype ID.

    :param run_id: internal run ID
    :param dataset_id:
    :param scoretype_id:
    :return: list with candidate sets as CandidateSet object
    """
    if run_id is not None:
        url = f"{url_base}get_candidate_sets?run={run_id}"
    elif dataset_id is not None:
        url = f"{url_base}get_candidate_sets?dataset={dataset_id}"
    else:
        raise Exception("Please enter either a run ID or a dataset ID.")
    if scoretype_id is not None:
        url += f"&scoretype={scoretype_id}"
    resp = ah.call_api(url=url)
    result = ah.check_response(resp=resp, return_type="json")
    dataset = dataset_creator(info_dict=result["Dataset"]) if "Dataset" in result else None
    candidate_sets = candidatesets_creator(info_dict=result["CandidateSets"], dataset=dataset)
    return candidate_sets

def get_tissue(internal_id: int = None, tissue_name: str = None) -> Tissue:
    """
    Get a Tissue entry by internal ID or name.

    :param internal_id: tissue internal ID
    :param tissue_name: tissue name
    :return: list of matched tissues as Tissue object
    """
    tissues = list_tissues()
    for tissue in tissues:
        if tissue_name is not None and tissue_name == tissue.get_name():
            return tissue
        elif internal_id is not None and internal_id == tissue.get_internal_id():
            return tissue
    return None

def list_tissues() -> dict:
    """
    List all tissues with available gene expression values from GTEx.

    :return: dataframe with all listed tissues
    """
    url = f"{url_base}list_tissues"
    resp = ah.call_api(url=url)
    result = ah.check_response(resp=resp, return_type="json")
    tissues = tissues_creator(info_dict=result)
    return tissues


def get_dataset_tissues(dataset_id: int) -> pd.DataFrame:
    """
    Retrieve Tissues linked to disease of specific Dataset.

    :param dataset_id: internal ID of dataset
    :return: dataframe with all linked tissues
    """
    url = f"{url_base}get_dataset_tissues?id={dataset_id}"
    resp = ah.call_api(url=url)
    result = ah.check_response(resp=resp, return_type="json")
    tissues = tissues_creator(info_dict=result)
    return tissues


def get_gene_expression(internal_gene_ids: list = None, internal_tissue_id: str = None) -> pd.DataFrame:
    """
    Retrieve Gene expression values given a specific Tissue.

    :param internal_gene_ids: list with internal gene IDs
    :param internal_tissue_id: internal ID of tissue
    :return: dataframe with all linked tissues
    """
    url = f"{url_base}get_tissue_gene_expression"
    if internal_gene_ids is not None:
        json = {"genes": internal_gene_ids}
    elif internal_tissue_id is not None:
        json = {"tissue": internal_tissue_id}
    else:
        raise Exception("Please enter either a list of internal gene IDs or an internal tissue ID.")
    resp = ah.call_api(url=url, json=json)
    result = ah.check_response(resp=resp, return_type="json")
    return pd.json_normalize(result)


def list_evidences() -> pd.DataFrame:
    """
    Lists all Variant-Variant interaction Evidence types provided by Epistasis Disease Atlas

    :return: dataframe with all listed evidence types
    """
    url = f"{url_base}list_evidences"
    resp = ah.call_api(url=url)
    result = ah.check_response(resp=resp, return_type="json")
    return pd.json_normalize(result)


def get_gene_network(dataset_id :int, internal_ids: list = None, variant_ids: list = None,
                     candidate_set_id: int = None) -> dict:
    """
    Construct gene network based on affecting Variants.

    :param dataset_id: internal ID of dataset
    :param internal_ids: list of internal variant IDs
    :param variant_ids: list of rsIDs of variants
    :param candidate_set_id: internal ID of candidate set
    :return: dict with {"Edges":list(list), "Nodes":list}
    """
    url = f"{url_base}get_gene_network"
    json = dict()
    json["dataset"] = dataset_id
    if internal_ids is not None:
        json["snps"] = internal_ids
    elif variant_ids is not None:
        json["rsids"] = variant_ids
    else:
        raise Exception("Please enter either a variant rsIDs or internal IDs.")
    if candidate_set_id is not None:
        json["candidate_set"] = candidate_set_id
    resp = ah.call_api(url=url, json=json)
    result = ah.check_response(resp=resp, return_type="json")
    # transform nodes
    nodes = dict()
    for node in result["Nodes"]:
        gene = gene_creator(info_dict=node)
        nodes[gene.get_internal_id()] = gene
    result["Nodes"] = nodes
    # transform edge list
    edges = list()
    for edge in result["Edges"]:
        edges.append([str(edge["Gene1"]), str(edge["Gene2"])])
    result["Edges"] = edges
    return result


def get_variant_network_from_ids(dataset_id: int, run_id: int, evidence_ids: list,
                                 internal_ids: list = None, variant_ids: list = None) -> dict:
    """
    Given a list of variants (rsIDs or SNPIDs), this endpoint returns a network of variants and their interactions.

    :param dataset_id: internal ID of dataset
    :param run_id: internal run ID
    :param evidence_ids: list of internal evidence IDs
    :param internal_ids: list of internal variant IDs
    :param variant_ids: list of rsIDs of variants
    :return: dict with {"Edges":list(list), "Nodes":list, "Evidences":list, "Run":dict}
    """
    url = f"{url_base}get_snp_network_from_ids"
    json = dict()
    if internal_ids is not None:
        json["ids"] = internal_ids
    elif variant_ids is not None:
        json["rsids"] = variant_ids
    else:
        raise Exception("Please enter either a variant rsIDs or internal IDs.")
    json["run"] = run_id
    json["dataset"] = dataset_id
    json["evidences"] = evidence_ids
    resp = ah.call_api(url=url, json=json)
    result = ah.check_response(resp=resp, return_type="json")
    # transform nodes
    nodes = dict()
    for node in result["Nodes"]:
        gene = variant_creator(info_dict=node)
        nodes[gene.get_internal_id()] = gene
    result["Nodes"] = nodes
    # transform edge list
    edges = list()
    for edge in result["Edges"]:
        edges.append([str(edge["SNP1"]), str(edge["SNP2"])])
    result["Edges"] = edges
    return result

def get_variant_network_from_candidate_set(dataset_id: int, candidate_set_id: int, run_id: int, evidence_ids: list) -> dict:
    """
    Given a candidate set, this endpoint returns a network of variants and their interactions.

    :param dataset_id: internal dataset ID
    :param candidate_set_id: internal candidate set ID
    :param run_id: internal run ID
    :param evidence_ids: list of internal evidence IDs
    :return: dict with {"Edges":list(list), "Nodes":list, "Evidences":list, "Run":dict}
    """
    url = f"{url_base}get_snp_network_from_candidate_set"
    json = dict()
    json["dataset"] = dataset_id
    json["run"] = run_id
    json["candidate_set"] = candidate_set_id
    json["evidences"] = evidence_ids
    resp = ah.call_api(url=url, json=json)
    result = ah.check_response(resp=resp, return_type="json")
    # transform nodes
    nodes = dict()
    for node in result["Nodes"]:
        gene = variant_creator(info_dict=node)
        nodes[gene.get_internal_id()] = gene
    result["Nodes"] = nodes
    # transform edge list
    edges = list()
    for edge in result["Edges"]:
        edges.append([str(edge["SNP1"]), str(edge["SNP2"])])
    result["Edges"] = edges
    return result


def get_neighbors(dataset_id: int, run_id: int, evidence_ids: list, internal_ids: list = None, variant_ids: list = None) -> dict:
    """
    Given a list of variants (rsIDs or SNPIDs), this endpoint returns a network of variants and their interactions.

    :param dataset_id: internal ID of dataset
    :param run_id: internal run ID
    :param evidence_ids: internal evidence IDs
    :param internal_ids: internal variant IDs
    :param variant_ids: rsIDs of variants
    :return: neighbors
    """
    url = f"{url_base}get_neighbors"
    if internal_ids is not None:
        json = {"snps": internal_ids}
    elif variant_ids is not None:
        json = {"rsids": variant_ids}
    else:
        raise Exception("Please enter either a variant rsIDs or internal IDs.")
    json["dataset"] = dataset_id
    json["run"] = run_id
    json["evidences"] = evidence_ids
    resp = ah.call_api(url=url, json=json)
    result = ah.check_response(resp=resp, return_type="json")
    # transfer snps
    snps = dict()
    for snp in result["SNPs"]:
        snp = variant_creator(info_dict=snp)
        snps[snp.get_internal_id()] = snp
    result["SNPs"] = snps
    # transfer snp interactions
    snp_interactions = list()
    for snp_interaction in result["SNPInteractions"]:
        snp_interactions.append([snp_interaction["SNP1"], snp_interaction["SNP2"]])
    result["SNPInteractions"] = snp_interactions
    return result


def list_variant_score_types():
    """
    Lists all types of VariantScores calculated for single Variant entries.

    :return: dataframe with all listed score types
    """
    url = f"{url_base}list_variant_scores"
    resp = ah.call_api(url=url)
    result = ah.check_response(resp=resp, return_type="json")
    return pd.json_normalize(result)

def list_network_score_types():
    """
    Lists all types of NetworkScores calculated for Variant Networks.

    :return: dataframe with all listed score types
    """
    url = f"{url_base}list_network_scores"
    resp = ah.call_api(url=url)
    result = ah.check_response(resp=resp, return_type="json")
    return pd.json_normalize(result)


def request_scores(run_id: int, dataset_id: int, evidence_id: int,  internal_ids: list = None, variant_ids: list = None,
                   force_compute: bool = False) -> str:
    """
    A CandidateSet is a set of Variants that can be evaluated of being in epistatis given a specific Dataset in a Run.
    Request CandidateSet evaluation based on another Run.

    :param run_id: internal run ID
    :param dataset_id: internal dataset ID
    :param evidence_id: internal evidence ID
    :param internal_ids: list of internal variant IDs
    :param variant_ids: list of rsIDs
    :param force_compute: if True, the scores will be calculated even if they are already present in the database
    :return: a resultID which can be used to get scores once they are calculated
    """
    url = f"{url_base}request_variant_scores"
    if internal_ids is not None:
        json = {"snps": internal_ids}
    elif variant_ids is not None:
        json = {"rsids": variant_ids}
    else:
        raise Exception("Please enter either a variant rsIDs or internal IDs.")
    json["run"] = run_id
    json["dataset"] = dataset_id
    json["evidence"] = evidence_id
    json["force_compute"] = force_compute
    resp = ah.call_api(url=url, json=json)
    result = ah.check_response(resp=resp, return_type="json")
    return result["ResultID"]


def check_request_status(request_id: str) -> dict:
    """
    Gives a status update on calculated scores for the CandidateSet and individual Variants.

    :param request_id: the resultID gained but calling request_scores
    :return: dict looking like {"Done":bool, "Error":bool, "Message":str, "Progress":int, "Precomputed":bool}
    """
    url = f"{url_base}get_variant_scores?resultID={request_id}"
    resp = ah.call_api(url=url)
    result = ah.check_response(resp=resp, return_type="json")
    return result["Status"]


def get_scores(request_id: str):
    """
    Returns calculated scores for the CandidateSet and individual Variants.

    :param request_id: the resultID gained but calling request_scores
    :return: results as dict with CandidateSet and SNPs
    """
    url = f"{url_base}get_variant_scores?resultID={request_id}"
    resp = ah.call_api(url=url)
    result = ah.check_response(resp=resp, return_type="json")
    return result["Results"]

def results_to_dataframe(elements: list):
    datasets_df_list = [element.to_dataframe() for element in elements]
    return pd.concat(datasets_df_list, ignore_index=True)
