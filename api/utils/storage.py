import os
def save_originals(project_id, files):
    base = f"/tmp/{project_id}/Imports"; os.makedirs(base, exist_ok=True)
    paths = []
    for f in files:
        p = os.path.join(base, f.filename)
        with open(p, "wb") as out: out.write(f.file.read())
        f.file.seek(0)
        paths.append(p)
    return paths

def save_dedup_artifacts(project_id, merge_log, duplicates_csv):
    base = f"/tmp/{project_id}/Dedup"; os.makedirs(base, exist_ok=True)
    ml = os.path.join(base, "Dedup_MergeLog.csv")
    dp = os.path.join(base, "Duplicates.csv")
    open(ml,"w",encoding="utf-8").write(merge_log)
    open(dp,"w",encoding="utf-8").write(duplicates_csv)
    return {"merge_log_path": ml, "duplicates_csv_path": dp}
