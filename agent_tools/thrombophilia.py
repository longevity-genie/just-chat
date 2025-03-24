import sqlite3
from pathlib import Path

from agent_tools.links import link_rsID, link_gene, link_PubMed, replace_pmid, replace_rsid


PATH_TO_THROMBOPHILIA_DB = Path("data", "genetics", "thrombophilia.sqlite")


def parse_PMID(text:str):
    """Function-helper to parse a PMID from a text."""
    parts = text.split(";")
    pmids = []
    for part in parts:
        if part.strip() != "":
            step1 = part.split("]")[0].strip()
            step2 = step1.split(" ")[1]
            pmids.append("'"+step2+"'")

    return set(pmids)


def rsid_lookup(rsid:str) -> str:
    """Function to lookup a rsid in the thrombophilia database. Provide an rsid that the user asked about in format 'rs123456789'."""
    with sqlite3.connect(PATH_TO_THROMBOPHILIA_DB) as conn:
        cursor = conn.cursor()
        query:str = f"SELECT rsid, gene, rsid_conclusion, population FROM rsids WHERE rsid = '{rsid}'"
        cursor.execute(query)
        row = cursor.fetchone()

        if row is None:
            return "thrombophilia: No results found."

        result: str = "thrombophilia:\n"
        result += "rsid; gene; conclusion; population\n"
        row = [str(i).replace(";", ",") for i in row]
        result += link_rsID(row[0]) + "; " + link_gene(row[1]) + "; " + replace_pmid(replace_rsid(row[2])) + "; " + row[3]+"\n\n"

        query = f"SELECT p_value, genotype, weight, genotype_specific_conclusion FROM weight WHERE rsid = '{rsid}'"
        cursor.execute(query)
        rows = cursor.fetchall()
        result += "thrombophilia weights:\n"
        result += "PMID with p-pvalue; genotype; weight; genotype_specific_conclusion\n"
        pmids:set = set()
        for row in rows:
            pmids = pmids.union(parse_PMID(row[0]))
            row = [str(i).replace(";", ",") for i in row]
            result += replace_pmid(row[0]) + "; " + "; ".join(row[1:]) + "\n"
        result += "\n"

        text_pmids = ", ".join(pmids)
        query = f"SELECT pubmed_id, populations, p_value FROM studies WHERE pubmed_id IN ({text_pmids}) "
        cursor.execute(query)
        rows = cursor.fetchall()
        result += "thrombophilia studies:\n"
        result += "PMID; description; pvalue\n"
        for row in rows:
            row = [str(i).replace(";", ",") for i in row]
            result += link_PubMed(row[0]) + "; " + "; ".join(row[1:])+"\n"
        result += "\n"
        cursor.close()

    return result


def gene_lookup(gene: str) -> str:
    """Function to lookup a gene in the thrombophilia database. Provide a gene that the user asked about in format 'ENSG00000123456'."""
    with sqlite3.connect(PATH_TO_THROMBOPHILIA_DB) as conn:
        cursor = conn.cursor()
        query: str = f"SELECT rsid, gene, rsid_conclusion, population FROM rsids WHERE gene = '{gene}'"
        cursor.execute(query)
        rows = cursor.fetchall()

        if rows is None or len(rows) == 0:
            return "thrombophilia: No results found."

        rsids = set([row[0] for row in rows])

        result: str = "thrombophilia:\n"
        result += "rsid; gene; conclusion; population\n"
        for row in rows:
            row = [str(i).replace(";", ",") for i in row]
            result += link_rsID(row[0]) + "; " + link_gene(row[1]) + "; " + replace_pmid(replace_rsid(row[2])) + "; " + row[3] + "\n"
        result += "\n"

        pmids: set = set()
        result += "thrombophilia weights:\n"
        result += "PMID with p-pvalue; genotype; weight; genotype_specific_conclusion\n"
        for rsid in rsids:
            query = f"SELECT p_value, genotype_specific_conclusion, genotype, weight FROM weight WHERE rsid = '{rsid}'"
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows:
                pmids = pmids.union(parse_PMID(row[0]))
                row = [str(i).replace(";", ",") for i in row]
                result += replace_pmid(row[0]) + "; " + replace_pmid(row[1]) + "; " + "; ".join(row[2:]) + "\n"
        result += "\n"

        text_pmids = ", ".join(pmids)
        query = f"SELECT pubmed_id, populations, p_value FROM studies WHERE pubmed_id IN ({text_pmids}) "
        cursor.execute(query)
        rows = cursor.fetchall()
        result += "thrombophilia studies:\n"
        result += "PMID; description; pvalue\n"
        for row in rows:
            row = [str(i).replace(";", ",") for i in row]
            result += link_PubMed(row[0]) + "; " + "; ".join(row[1:]) + "\n"
        result += "\n"
        cursor.close()

    return result
