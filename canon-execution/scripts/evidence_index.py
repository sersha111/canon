#!/usr/bin/env python3
"""Index explicitly selected exported histories; optionally preserve exact private copies."""
import argparse, hashlib, json, os, shutil, tempfile
from pathlib import Path

def digest_file(path):
    digest=hashlib.sha256();size=0
    with path.open("rb") as f:
        while True:
            block=f.read(1024*1024)
            if not block: break
            digest.update(block);size+=len(block)
    return digest.hexdigest(),size

def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("manifest",type=Path);ap.add_argument("destination",type=Path)
    ap.add_argument("--copy",action="store_true",help="Copy authorized sources privately; no secret redaction is implied")
    a=ap.parse_args();entries=json.loads(a.manifest.read_text())
    if not isinstance(entries,list):raise ValueError("Manifest must be a list")
    out=a.destination.absolute()
    if out.exists():raise ValueError("Destination must be new; preserve prior exports")
    prepared=[];unique={}
    for entry in entries:
        for key in ("harness","session_id","path","coverage"):
            if not isinstance(entry.get(key),str) or not entry[key]:raise ValueError("Missing required metadata: "+key)
        p=Path(entry["path"]).expanduser().resolve()
        if not p.is_file():raise ValueError("An explicit source file is unavailable")
        digest,size=digest_file(p)
        unique.setdefault(digest,p)
        prepared.append({**entry,"path":str(p),"sha256":digest,"bytes":size,
                         "parent_id":entry.get("parent_id"),"metadata_provenance":"caller declared",
                         "instruction_versions":entry.get("instruction_versions",[]),
                         "archive":("objects/"+digest) if a.copy else None})
    out.parent.mkdir(parents=True,exist_ok=True)
    staging=Path(tempfile.mkdtemp(prefix=".canon-export-",dir=out.parent))
    try:
        if a.copy:
            (staging/"objects").mkdir(mode=0o700)
            for digest,source in unique.items():
                p=staging/"objects"/digest
                fd=os.open(str(p),os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
                with os.fdopen(fd,"wb") as f, source.open("rb") as src:shutil.copyfileobj(src,f,1024*1024)
                if digest_file(p)[0]!=digest:raise ValueError("Source changed or archive readback mismatched")
        record={"version":1,"entries":prepared,"unique_files":len(unique),
                "limitations":["Exact-byte deduplication only","Metadata is declared, not proof of instruction loading",
                               "No decryption or automatic extraction from live databases",
                               "Private raw copies may contain secrets; not safe for publication"]}
        p=staging/"index.json";p.write_text(json.dumps(record,indent=2)+"\n");p.chmod(0o600)
        os.rename(staging,out)
    except Exception:
        shutil.rmtree(staging);raise
    print(json.dumps({"index":str(out/"index.json"),"entries":len(prepared),"unique_files":len(unique),"copied":a.copy}))
if __name__=="__main__":
    try:main()
    except (ValueError,OSError,KeyError,json.JSONDecodeError) as e:raise SystemExit(str(e))
