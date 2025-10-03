from typing import List
from fastapi import UploadFile
import rispy, bibtexparser, httpx

def strict_parse(files: List[UploadFile]):
    records = []
    for f in files:
        name = f.filename.lower()
        content = f.file.read()
        if name.endswith(".ris"):
            entries = rispy.loads(content.decode("utf-8"))
            for e in entries:
                records.append({
                    "source": "import",
                    "source_id": e.get("primary_title") or e.get("title"),
                    "doi": e.get("doi"),
                    "pmid": e.get("pmid"),
                    "title": e.get("title"),
                    "abstract": e.get("abstract"),
                    "authors": ", ".join(e.get("authors",[])),
                    "year": e.get("year"),
                    "venue": e.get("journal_name") or e.get("secondary_title"),
                    "url": e.get("url")
                })
        elif name.endswith(".bib") or name.endswith(".bibtex"):
            bibdb = bibtexparser.loads(content.decode("utf-8"))
            for e in bibdb.entries:
                records.append({
                    "source": "import",
                    "source_id": e.get("ID"),
                    "doi": e.get("doi"),
                    "pmid": e.get("pmid"),
                    "title": e.get("title"),
                    "abstract": e.get("abstract"),
                    "authors": e.get("author"),
                    "year": e.get("year"),
                    "venue": e.get("journal") or e.get("booktitle"),
                    "url": e.get("url")
                })
        elif name.endswith(".xml") or name.endswith(".csv"):
            raise ValueError(f"Parser not implemented for {f.filename} in MVP")
        else:
            raise ValueError(f"Unsupported file type: {f.filename}")
        f.file.seek(0)
    return records

async def enrich_metadata(records):
    out = []
    async with httpx.AsyncClient(timeout=20) as client:
        for r in records:
            if not r.get("doi") and r.get("title"):
                try:
                    q = r["title"]
                    x = await client.get("https://api.crossref.org/works", params={"query.bibliographic": q, "rows": 1})
                    if x.status_code == 200:
                        items = x.json().get("message",{}).get("items",[])
                        if items:
                            r["doi"] = items[0].get("DOI") or r.get("doi")
                except:
                    pass
            out.append(r)
    return out

def persist_records(project_id, records):
    # Helper returns counts; the Lovable app stores rows in its own DB.
    return {"imported": len(records), "dedup_removed": 0, "unique_added": len(records)}
