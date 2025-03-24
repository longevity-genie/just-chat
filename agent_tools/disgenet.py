import sqlite3
from pathlib import Path
import polars as pl
from thefuzz import fuzz
from agent_tools.links import link_rsID, link_gene, link_PubMed

PATH_TO_DISGENET_DB = Path("data", "genetics", "disgenet_2020.sqlite")
PATH_TO_DISGENET_NAMES = Path("data", "genetics", "disease_names.csv")


def _aggregate_last_field(rows):
    """Function-helper to aggregate the last field of the rows."""
    current = list(rows[0])
    current[-1] = str(current[-1])
    res:list = []
    for row in rows[1:]:
        row = list(row)
        if current[:-1] != row[:-1]:
            res.append(current)
            current = row
            current[-1] = str(current[-1])
        else:
            current[-1] += ", " + str(row[-1]).strip()

    res.append(current)

    return res


def _get_similar_names(name):
    """Function-helper to get similar names from the database."""
    name = " " + name.strip() + " "

    def levenshtein_dist(struct: dict) -> int:
        return fuzz.partial_ratio(struct["name"], name)

    frame = pl.read_csv(PATH_TO_DISGENET_NAMES)
    frame = frame.select(
        [pl.struct(["name"]).apply(levenshtein_dist).alias("dist"), "name"])
    frame = frame.sort(by="dist", descending=True).select(["name"])
    names = frame.head(10).get_column("name").to_list()
    return "\n".join(names)


def rsid_lookup(rsid:str) -> str:
    """Function to lookup a rsid in the disgenet database. Provide an rsid that the user asked about in format 'rs123456789'."""
    with sqlite3.connect(PATH_TO_DISGENET_DB) as conn:
        cursor = conn.cursor()
        query:str = f"SELECT vdnet.pmid, varat.most_severe_consequence, vdnet.sentence, disat.diseaseName, disat.type, dclass.diseaseClassName " \
                    f"FROM variantAttributes AS varat " \
                    f"JOIN variantDiseaseNetwork AS vdnet ON varat.variantNID = vdnet.variantNID " \
                    f"JOIN diseaseAttributes AS disat ON vdnet.diseaseNID = disat.diseaseNID " \
                    f"LEFT JOIN disease2class AS d2c ON disat.diseaseNID = d2c.diseaseNID " \
                    f"LEFT JOIN diseaseClass AS dclass ON d2c.diseaseClassNID = dclass.diseaseClassNID " \
                    f"WHERE varat.variantId = '{rsid}' ORDER BY disat.diseaseName"
        cursor.execute(query)
        rows = cursor.fetchall()
        if rows is None or len(rows) == 0:
            return ""

        text = f"Diseases asociate with {rsid}:\n"
        text += "Pub Med ID; most severe consequence; description; disease name; type; disease class\n"

        rows = _aggregate_last_field(rows)

        if len(rows) > 100:
            rows = rows[:100]

        for row in rows:
            text += link_PubMed(str(row[0])) + "; " + "; ".join([str(i) for i in row[1:]]) + "\n"
        text += "\n"

        return text


def gene_lookup(gene: str) -> str:
    """Function to lookup a gene in the disgenet database. Provide a gene that the user asked about in format 'ENSG00000123456'."""
    with sqlite3.connect(PATH_TO_DISGENET_DB) as conn:
        cursor = conn.cursor()
        query: str = f"SELECT gendis.pmid, gendis.sentence, disat.diseaseName, disat.type, dclass.diseaseClassName " \
                    f"FROM geneAttributes AS genat " \
                    f"JOIN geneDiseaseNetwork AS gendis ON genat.geneNID = gendis.geneNID " \
                    f"JOIN diseaseAttributes AS disat ON gendis.diseaseNID = disat.diseaseNID " \
                    f"LEFT JOIN disease2class AS d2c ON disat.diseaseNID = d2c.diseaseNID " \
                    f"LEFT JOIN diseaseClass AS dclass ON d2c.diseaseClassNID = dclass.diseaseClassNID " \
                    f"WHERE genat.geneName = '{gene}' ORDER BY disat.diseaseName"
        cursor.execute(query)
        rows = cursor.fetchall()

        if rows is None or len(rows) == 0:
            return ""

        text = f"Diseases asociate with {gene}:\n"
        text += "Pub Med ID; description; disease name; type; disease class\n"

        rows = _aggregate_last_field(rows)

        if len(rows) > 100:
            rows = rows[:100]

        for row in rows:
            text += link_PubMed(str(row[0]))+"; " + "; ".join([str(i) for i in row[1:]])+"\n"
        text += "\n"

        return text


def disease_lookup(disease: str) -> str:
    """Function to lookup a disease in the disgenet database. Provide a disease that the user asked about."""
    with sqlite3.connect(PATH_TO_DISGENET_DB) as conn:
        cursor = conn.cursor()
        query: str = f"SELECT genat.geneName, varat.variantId, varat.most_severe_consequence " \
                    f"FROM variantDiseaseNetwork as vardis, variantAttributes as varat, " \
                    f"diseaseAttributes as disat, variantGene as vargen, geneAttributes as genat " \
                    f"WHERE disat.diseaseName = '{disease}' AND " \
                    f"disat.diseaseNID = vardis.diseaseNID AND vardis.variantNID = varat.variantNID AND " \
                    f"vargen.variantNID = vardis.variantNID AND genat.geneNID = vargen.geneNID " \
                    f"ORDER BY genat.geneNID "
        cursor.execute(query)
        rows = cursor.fetchall()

        if rows is None or len(rows) == 0:
            disease_names = _get_similar_names(disease)
            return f"There are no such disease ({disease}) in database. " \
                    f"The database is case-sensitive, make sure you use strictly the same name as in the database. " \
                    f"Please use following disease names if they apply:\n{disease_names}"

        if len(rows) > 100:
            rows = rows[:100]

        text = f"Variants associate with disease '{disease}' grouped by gene:\n"
        gene = ""
        for row in rows:
            if gene != row[0]:
                text += link_gene(row[0])+":\n"
                gene = row[0]
            text += f"  " + link_rsID(row[1]) + ", " + row[2] + "\n"
        text += "\n"

        return text