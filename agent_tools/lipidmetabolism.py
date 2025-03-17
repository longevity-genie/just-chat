import sqlite3
from pathlib import Path

from agent_tools.links import link_rsID, link_gene, replace_pmid, replace_rsid

def rsid_lookup(rsid:str) -> str:
    """This function is used to lookup lipid metabolism data for a given rsid. Provide rsid that user asked to find information about this rsid"""
    path:Path = Path(Path(__file__).parent, "data", "genetics","lipid_metabolism.sqlite")
    print(path)
    with sqlite3.connect(path) as conn:
        cursor = conn.cursor()
        query:str = f"SELECT rsid, gene, rsid_conclusion, population, p_value FROM rsids WHERE rsid = '{rsid}'"
        cursor.execute(query)
        row = cursor.fetchone()

        if row is None:
            return "lipid metabolism: No results found."

        result: str = "lipid metabolism:\n"
        result += "rsid; gene; conclusion; population; pvalue\n"
        row = [str(i).replace(";", ",") for i in row]
        result += link_rsID(row[0]) + "; " + link_gene(row[1]) + "; " + replace_pmid(replace_rsid(row[2])) + "; " + "; ".join(row[3:])+"\n\n"

        query = f"SELECT populations, p_value FROM studies WHERE snp = '{rsid}'"
        cursor.execute(query)
        rows = cursor.fetchall()
        result += "lipid metabolism studies:\n"
        result += "description; pvalue\n"
        for row in rows:
            row = [str(i).replace(";", ",") for i in row]
            result += "; ".join(row)+"\n"
        result += "\n"


        query = f"SELECT genotype, weight, genotype_specific_conclusion FROM weight WHERE rsid = '{rsid}'"
        cursor.execute(query)
        rows = cursor.fetchall()
        result += "lipid metabolism weights:\n"
        result += "genotype; weight; genotype_specific_conclusion\n"
        for row in rows:
            row = [str(i).replace(";", ",") for i in row]
            result += "; ".join(row[:2]) + "; " + replace_pmid(replace_rsid(row[2])) + "\n"
        result += "\n"
        cursor.close()

    return result


def gene_lookup(gene: str) -> str:
    """This function is used to lookup lipid metabolism data for a given gene. Provide gene name that user asked to find information about this gene"""
    path:Path = Path(Path(__file__).parent, "data", "genetics","lipid_metabolism.sqlite")
    with sqlite3.connect(path) as conn:
        cursor = conn.cursor()
        query: str = f"SELECT rsid, gene, rsid_conclusion, population, p_value FROM rsids WHERE gene = '{gene}'"
        cursor.execute(query)
        rows = cursor.fetchall()

        if rows is None or len(rows) == 0:
            return "lipid metabolism: No results found."

        result: str = "lipid metabolism:\n"
        result += "rsid; gene; conclusion; population; pvalue\n"
        for row in rows:
            row = [str(i).replace(";", ",") for i in row]
            result += link_rsID(row[0]) + "; " + link_gene(row[1]) + "; " + replace_pmid(replace_rsid(row[2])) + "; " + "; ".join(row[3:])+"\n"
        result += "\n"

        rsids = set([row[0] for row in rows])

        result += "lipid metabolism studies:\n"
        result += "rsid; description; pvalue\n"
        for rsid in rsids:
            query = f"SELECT snp, populations, p_value FROM studies WHERE snp = '{rsid}'"
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows:
                row = [str(i).replace(";", ",") for i in row]
                result += link_rsID(row[0]) + "; " + "; ".join(row[1:]) + "\n"
        result += "\n"

        result += "lipid metabolism weights:\n"
        result += "rsid; genotype_specific_conclusion; genotype; weight\n"
        for rsid in rsids:
            query = f"SELECT rsid, genotype_specific_conclusion, genotype, weight FROM weight WHERE rsid = '{rsid}'"
            cursor.execute(query)
            rows = cursor.fetchall()
            for row in rows:
                row = [str(i).replace(";", ",") for i in row]
                result += link_rsID(row[0]) + "; " + replace_pmid(replace_rsid(row[1])) + "; " + "; ".join(row[2:]) + "\n"
        result += "\n"
        cursor.close()

    return result
