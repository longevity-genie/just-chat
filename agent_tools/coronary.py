import sqlite3
from pathlib import Path
from agent_tools.links import link_rsID, link_gene, replace_rsid, replace_pmid


PATH_TO_CORONARY_DB = Path("data", "genetics", "coronary.sqlite")

def _field_lookup(field:str, val:str):
    """Function-helper to lookup a field in the coronary disease database."""
    with sqlite3.connect(PATH_TO_CORONARY_DB) as conn:
        cursor = conn.cursor()
        query:str = f"SELECT rsID, Gene, Conclusion, GWAS_study_design, P_value, Risk_allele, Genotype, Weight, " \
                    f"Population FROM coronary_disease WHERE {field} = '{val}'"
        cursor.execute(query)
        rows = cursor.fetchall()

        if rows is None or len(rows) == 0:
            return "coronary disease: No results found."

        result = "coronary disease:\n"
        result += "rsid; Gene; Conclusion; GWAS study design; Pvalue; Risk allele; Genotype; Weight; " \
                    f" Population\n"
        for row in rows:
            row = [str(i).replace(";", ",") for i in row]
            result += link_rsID(row[0])+ "; " + link_gene(row[1]) + "; " + replace_pmid(replace_rsid(row[2])) +\
                        "; " + replace_pmid(row[3]) + "; " + replace_pmid(row[4]) + "; " + "; ".join(row[5:]) + "\n"
        result += "\n"
        cursor.close()

    return result


def rsid_lookup(rsid:str) -> str:
    """Function to lookup a rsid in the coronary disease database. Provide an rsid that the user asked about in format 'rs123456789'."""
    return _field_lookup("rsID", rsid)


def gene_lookup(gene: str) -> str:
    """Function to lookup a gene in the coronary disease database. Provide a gene that the user asked about in format 'ENSG00000123456'."""
    return _field_lookup("Gene", gene)