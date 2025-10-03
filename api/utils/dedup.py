def run(project_id: str, threshold: float):
    summary = {"total_before": 0, "removed": 0, "total_after": 0}
    merge_log = "group_id,kept,duplicates,rule\n"
    duplicates_csv = "work_id,title,doi,pmid,reason\n"
    return summary, merge_log, duplicates_csv
