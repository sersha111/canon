#!/usr/bin/env python3
"""Run a reviewed explicit check manifest with bounded output and process-group cleanup."""
import argparse, hashlib, json, os, selectors, signal, subprocess, time
from pathlib import Path
def execute(check,root):
    start=time.monotonic();deadline=start+check.get("timeout_seconds",60)
    limit=check.get("max_output_bytes",8*1024*1024)
    sizes={"stdout":0,"stderr":0};hashes={k:hashlib.sha256() for k in sizes}
    record={"name":check["name"],"passed":False}
    proc=None;selector=selectors.DefaultSelector()
    try:
        proc=subprocess.Popen(check["argv"],cwd=(root/check.get("cwd",".")).resolve(),
                              stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
        for key,stream in (("stdout",proc.stdout),("stderr",proc.stderr)):
            os.set_blocking(stream.fileno(),False);selector.register(stream,selectors.EVENT_READ,key)
        while selector.get_map() or proc.poll() is None:
            remaining=deadline-time.monotonic()
            if remaining<=0:
                record["failure"]="timeout";break
            for selected,_ in selector.select(min(remaining,0.1)):
                data=os.read(selected.fileobj.fileno(),65536)
                if data:
                    sizes[selected.data]+=len(data);hashes[selected.data].update(data)
                else:
                    selector.unregister(selected.fileobj);selected.fileobj.close()
            if sum(sizes.values())>limit:
                record["failure"]="output-limit";break
        if "failure" not in record:
            record.update(exit=proc.wait(),passed=proc.returncode==0)
        record["output_complete"]="failure" not in record
    except OSError as e:
        record.update(failure=type(e).__name__,output_complete=False)
    finally:
        # Commands in this gate must not leave persistent services behind.
        if proc is not None:
            try:os.killpg(proc.pid,signal.SIGKILL)
            except ProcessLookupError:pass
            proc.wait()
            for stream in (proc.stdout,proc.stderr):
                if stream and not stream.closed:stream.close()
        selector.close()
    record.update(elapsed_seconds=round(time.monotonic()-start,4))
    for key in sizes:
        record[key+"_bytes_observed"]=sizes[key]
        record[key+"_observed_sha256"]=hashes[key].hexdigest()
    return record
def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument("manifest",type=Path);ap.add_argument("--root",type=Path,required=True)
    ap.add_argument("--report",type=Path,required=True);a=ap.parse_args()
    root=a.root.resolve()
    if not root.is_dir():raise ValueError("Root must be an existing directory")
    if a.report.is_symlink():raise ValueError("Report cannot be a symlink")
    config=json.loads(a.manifest.read_text());checks=config.get("checks",[])
    if not checks:raise ValueError("No checks configured; zero checks is not a passing gate")
    names=set()
    for c in checks:
        if not c.get("name") or c["name"] in names:raise ValueError("Checks need unique names")
        names.add(c["name"])
        if c.get("effects") not in ("read-only","temporary-only","build-output"):
            raise ValueError("Check effects must be explicitly reviewed; deployment is not a verification check")
        if not isinstance(c.get("argv"),list) or not c["argv"] or not all(isinstance(v,str) for v in c["argv"]):
            raise ValueError("Commands must be nonempty argument arrays, not shell text")
        for key,default in (("timeout_seconds",60),("max_output_bytes",8*1024*1024)):
            if not isinstance(c.get(key,default),(int,float)) or c.get(key,default)<=0:
                raise ValueError("Limits must be positive")
        cwd=(root/c.get("cwd",".")).resolve()
        if not cwd.is_relative_to(root) or not cwd.is_dir():raise ValueError("Check cwd must stay in the declared root")
    results=[execute(c,root) for c in checks]
    report={"root":str(root),"manifest_sha256":hashlib.sha256(a.manifest.read_bytes()).hexdigest(),
            "passed":all(c["passed"] for c in results),"checks":results,
            "limits":"Effects are reviewed declarations, not a sandbox. Raw output is not retained. Deliberately detached sessions are outside process-group cleanup."}
    a.report.parent.mkdir(parents=True,exist_ok=True)
    a.report.write_text(json.dumps(report,indent=2)+"\n");a.report.chmod(0o600)
    print(json.dumps(report,indent=2))
    if not report["passed"]:raise SystemExit(1)
if __name__=="__main__":
    try:main()
    except (ValueError,OSError,KeyError,json.JSONDecodeError) as e:raise SystemExit(str(e))
