import regex as re

def link_rsID(rsid:str) -> str:
    return f"https://www.ncbi.nlm.nih.gov/snp/?term={rsid}"

def link_PubMed(pubmed_id:str) -> str:
    return f"https://pubmed.ncbi.nlm.nih.gov/{pubmed_id}"

def link_gene(gene:str) -> str:
    return f"https://www.ncbi.nlm.nih.gov/gene/?term={gene}"

def replace_rsid(text:str) -> str:
    rsid_pattern = r'rs\d+'
    updated_text = re.sub(rsid_pattern, lambda x: link_rsID(x.group()), text)
    return updated_text


def replace_pmid(text:str) -> str:
    pubmed_pattern = r'PMID:? (\d+)'
    def replace_pubmed(match):
        return "PMID: " + link_PubMed(match.group(1))

    updated_text = re.sub(pubmed_pattern, replace_pubmed, text)
    return updated_text