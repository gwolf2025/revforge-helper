import os, csv, json, zipfile, time
from .prisma import counts, figure_png

def build_bundle(project_id: str, include_individual_files: bool=True):
    ts = time.strftime("%Y%m%d")
    root = f"/tmp/{project_id}_export_{ts}"
    os.makedirs(root, exist_ok=True)

    csv_path = os.path.join(root, "Results.csv")
    with open(csv_path, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id","title","abstract","authors","year","venue","doi","pmid","decision","reason"])
        # The Lovable app can upload a CSV later; MVP leaves content empty.

    ris_path = os.path.join(root, "Results.ris"); open(ris_path,"w",encoding="utf-8").close()
    bib_path = os.path.join(root, "Results.bib"); open(bib_path,"w",encoding="utf-8").close()
    enxml_path = os.path.join(root, "Results.xml"); open(enxml_path,"w",encoding="utf-8").close()

    counts_csv = os.path.join(root, "PRISMA_counts.csv")
    c = counts(project_id)
    with open(counts_csv, "w", newline="", encoding="utf-8") as f:
        w = csv.writer(f); w.writerow(["Stage","Count"])
        for k,v in c.items(): w.writerow([k,v])
    svg_path = os.path.join(root, "PRISMA.svg")
    png_path = os.path.join(root, "PRISMA.png")
    figure_png(project_id, svg_path, png_path, c)

    prov_path = os.path.join(root, "provenance.json")
    with open(prov_path, "w", encoding="utf-8") as f:
        json.dump({"project_id": project_id, "export_date": ts}, f, indent=2)

    dups_csv = os.path.join(root, "Duplicates.csv"); open(dups_csv,"w",encoding="utf-8").close()
    mlog_csv = os.path.join(root, "Dedup_MergeLog.csv"); open(mlog_csv,"w",encoding="utf-8").close()

    zip_path = f"/tmp/{project_id}_Export_{ts}.zip"
    with zipfile.ZipFile(zip_path, "w", zipfile.ZIP_DEFLATED) as z:
        for fp in [csv_path, ris_path, bib_path, enxml_path, counts_csv, svg_path, png_path, prov_path, dups_csv, mlog_csv]:
            z.write(fp, arcname=os.path.basename(fp))

    files = [csv_path, ris_path, bib_path, enxml_path, counts_csv, svg_path, png_path, prov_path, dups_csv, mlog_csv]
    return zip_path, files
