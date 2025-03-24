import sqlite3
from pathlib import Path

from agent_tools.links import link_rsID, link_gene


PATH_TO_LONGEVITYMAP_DB = Path("data", "genetics", "longevitymap.sqlite")


def rsid_lookup(rsid:str) -> str:
    """Function to lookup a rsid in the longevity map database. Provide an rsid that the user asked about in format 'rs123456789'."""
    with sqlite3.connect(PATH_TO_LONGEVITYMAP_DB) as conn:
        cursor = conn.cursor()
        query:str = f"SELECT identifier, study_design, conclusions, association, population.name as population, gene_id " \
                    f"FROM variant, population WHERE population.id = population_id AND identifier = '{rsid}'"
        cursor.execute(query)
        rows = cursor.fetchall()

        if rows is None or len(rows) == 0:
            return "longevity map: No results found."

        gene_ids = set([r[5] for r in rows])

        result: str = "longevity map:\n"
        result += "identifier; study design; conclusions; association; population\n"
        for row in rows:
            row = [str(i).replace(";", ",") for i in row[:5]]
            result += link_rsID(row[0]) + "; " + "; ".join(row[1:])+"\n"
        result += "\n"

        result += "longevity map genes:\n"
        result += "symbol; gene name; alias; description\n"
        for gene_id in gene_ids:
            query = f"SELECT symbol, name, symbol, alias, description FROM gene WHERE id = '{gene_id}'"
            cursor.execute(query)
            row = cursor.fetchone()

            row = [str(i).replace(";", ",") for i in row]
            result += link_gene(row[0]) + "; " + "; ".join(row[1:])+"\n"
        result += "\n"

        query = f"SELECT rsid, allele, state, zygosity, weight, categories.description, categories.recommendation, categories.name as category FROM allele_weights, categories " \
                f"WHERE categories.id = category_id AND rsid = '{rsid}'"
        cursor.execute(query)
        rows = cursor.fetchall()

        if rows is not None and len(rows) > 0:
            category = rows[0][5:]
            result += f"rdID's pathway is {category[2]}, its description: {category[:-1]}\n longevity map weights:\n"

        result += "rsid; allele; state; zygosity; weight\n"
        for row in rows:
            row = [str(i).replace(";", ",") for i in row[:-3]]
            result += link_rsID(row[0]) + "; " + "; ".join(row[1:]) + "\n"
        result += "\n"
        cursor.close()

    return result


def gene_lookup(gene: str) -> str:
    """Function to lookup a gene in the longevity map database. Provide a gene that the user asked about in format 'ENSG00000123456'."""
    with sqlite3.connect(PATH_TO_LONGEVITYMAP_DB) as conn:
        cursor = conn.cursor()
        query: str = f"SELECT identifier, study_design, conclusions, association, population.name as population, gene_id " \
                        f"FROM variant, population, gene WHERE population.id = population_id AND gene.id = gene_id AND gene.symbol = '{gene}'"
        cursor.execute(query)
        rows = cursor.fetchall()

        if rows is None or len(rows) == 0:
            return "longevity map: No results found."

        gene_ids = set([r[5] for r in rows])
        rsids = set([r[0] for r in rows])

        result: str = "longevity map:\n"
        result += "rsid; study design; conclusions; association; population\n"
        for row in rows:
            row = [str(i).replace(";", ",") for i in row[:5]]
            result += link_rsID(row[0]) + "; " + "; ".join(row[1:]) + "\n"
        result += "\n"

        result += "longevity map genes:\n"
        result += "symbol; gene name; alias; description\n"
        for gene_id in gene_ids:
            query = f"SELECT symbol, name, symbol, alias, description FROM gene WHERE id = '{gene_id}'"
            cursor.execute(query)
            row = cursor.fetchone()

            row = [str(i).replace(";", ",") for i in row]
            result += link_gene(row[0]) + "; " + "; ".join(row[1:]) + "\n"
        result += "\n"

        result += "longevity map weights:\n"
        result += "rsid; allele; state; zygosity; weight; category\n"
        for rsid in rsids:
            query = f"SELECT rsid, allele, state, zygosity, weight, categories.name as category FROM allele_weights, categories " \
                    f"WHERE categories.id = category_id AND rsid = '{rsid}'"
            cursor.execute(query)
            rows = cursor.fetchall()

            for row in rows:
                row = [str(i).replace(";", ",") for i in row]
                result += link_rsID(row[0]) + "; " +  "; ".join(row[1:]) + "\n"
        result += "\n"
        cursor.close()

    return result


def pathway_lookup(pathway:str) -> str:
    """Function to lookup a pathway in the longevity map database. 
    Provide a pathway that the user asked about.
    The pathway should be one of the following: 
            other
            lipids
            insulin
            antioxidant
            mitochondria
            sirtuin
            mtor
            tumor-suppressor
            renin-angiotensin
            heat-shock
            inflammation
            genome_maintenance
    """
    with sqlite3.connect(PATH_TO_LONGEVITYMAP_DB) as conn:
        cursor = conn.cursor()
        query:str = f"SELECT name, description, recommendation FROM categories " \
                    f"WHERE name = '{pathway}'"
        cursor.execute(query)
        rows = cursor.fetchall()

        if rows is None or len(rows) == 0:
            return "pathway: No results found."

        result = ""
        result += "name; description; recommendation\n"
        for row in rows:
            row = [str(i).replace(";", ",") for i in row]
            result += "; ".join(row)+"\n"
        result += "\n"

        query: str = f"SELECT rsid, gene.symbol, allele, state, zygosity, weight, priority " \
                        f"FROM allele_weights " \
                        f"JOIN variant ON allele_weights.rsid = variant.identifier " \
                        f"JOIN gene ON variant.gene_id = gene.id " \
                        f"WHERE allele_weights.category_id IN (SELECT id FROM categories WHERE name = '{pathway}');"

        cursor.execute(query)
        rows = cursor.fetchall()
        rsids = set([r[0] for r in rows])

        positive_rsid = 0
        negative_rsid = 0

        for row in rows:
            if row[5] > 0:
                positive_rsid += 1
            else:
                negative_rsid += 1

        result: str = f"Amount of rsIDs in the pathways: {len(rsids)}, pro-longevity: {positive_rsid},"
        f" anti-longevity: {negative_rsid}), the list of rsids: {rsids}. rsID table:\n"
        result += "rsid; gene; allele; state; zygosity; weight, priority\n"
        for row in rows:
            row = [str(i).replace(";", ",") for i in row]
            result += link_rsID(row[0]) + "; " + link_gene(row[1]) + "; " + "; ".join(row[2:]) + "\n"
        result += "\n"

        cursor.close()

    return result