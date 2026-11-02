#!/usr/bin/env python3
"""Portable task state and cooperative execution support; not a tool sandbox."""
import argparse, contextlib, fcntl, hashlib, json, os, re, shutil, socket, tempfile
from pathlib import Path
from datetime import datetime, timezone

def now():
    return datetime.now(timezone.utc).isoformat()
def fingerprint(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p, data):
    if p.is_symlink():
        raise ValueError("Refusing a symlink state/output")
    p.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix=".canon-", dir=p.parent)
    try:
        with os.fdopen(fd, "w") as f:
            json.dump(data, f, indent=2); f.write("\n"); f.flush(); os.fsync(f.fileno())
        os.replace(tmp, p)
    finally:
        if os.path.exists(tmp): os.unlink(tmp)
@contextlib.contextmanager
def locked(path):
    path.parent.mkdir(parents=True, exist_ok=True)
    lp = path.with_name(path.name + ".lock")
    fd = os.open(str(lp), os.O_CREAT | os.O_RDWR | getattr(os, "O_NOFOLLOW", 0), 0o600)
    try:
        fcntl.flock(fd, fcntl.LOCK_EX)
        yield
    finally:
        os.close(fd)
def source_path(state, value):
    root = Path(state["root"]).resolve()
    p = Path(value)
    p = (root / p).resolve() if not p.is_absolute() else p.resolve()
    if not p.is_relative_to(root):
        raise ValueError("Path lies outside recorded task root")
    return p
def contract_hash(state):
    accepted = sorted((d["key"], d["value"]) for d in state["decisions"] if d["status"] == "accepted")
    return hashlib.sha256(json.dumps([sorted(state["sources"]), accepted]).encode()).hexdigest()
def private_source(p):
    if p.name == ".env" or (p.name.startswith(".env.") and not p.name.endswith(".example")) or p.suffix in (".pem", ".key", ".p12"):
        return True
    # Deliberately bounded detection, not a guarantee of secret-free content.
    data = p.read_bytes()
    return bool(re.search(rb"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----|https?://[^/\s:@]+:[^/\s@]+@", data))
def main():
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    p = sub.add_parser("init"); p.add_argument("path", type=Path)
    p.add_argument("--root", required=True, type=Path); p.add_argument("--intent", required=True)
    p.add_argument("--mode", choices=["analysis","implementation"], required=True)
    p.add_argument("--source", action="append", default=[]); p.add_argument("--item", action="append", default=[])
    p.add_argument("--instruction", type=Path, action="append", default=[])
    p = sub.add_parser("decision"); p.add_argument("path", type=Path)
    p.add_argument("--key", required=True); p.add_argument("--value", required=True); p.add_argument("--evidence", required=True)
    p = sub.add_parser("item"); p.add_argument("path", type=Path); p.add_argument("item")
    p.add_argument("--status", choices=["pending","blocked","done"], required=True)
    p.add_argument("--output", type=Path); p.add_argument("--source", action="append", default=[])
    p.add_argument("--check"); p.add_argument("--note", default="")
    p = sub.add_parser("sources"); p.add_argument("path", type=Path)
    p.add_argument("--source", action="append", required=True); p.add_argument("--evidence", required=True)
    p = sub.add_parser("status"); p.add_argument("path", type=Path)
    p = sub.add_parser("attempt"); p.add_argument("path", type=Path)
    p.add_argument("--operation", required=True); p.add_argument("--input", required=True)
    p.add_argument("--error", required=True); p.add_argument("--recovery")
    p = sub.add_parser("checkpoint"); p.add_argument("path", type=Path)
    p.add_argument("--file", action="append", default=[]); p.add_argument("--deleted", action="append", default=[]); p.add_argument("--base", required=True)
    p = sub.add_parser("guard"); p.add_argument("path", type=Path)
    p.add_argument("--target", required=True); p.add_argument("--action", choices=["read","write"], required=True)
    for command in ("claim","release"):
        p = sub.add_parser(command); p.add_argument("path", type=Path)
        p.add_argument("--resource", required=True); p.add_argument("--owner", required=True)
    args = parser.parse_args(); path = args.path.absolute()
    if args.command in ("claim","release"):
        path.mkdir(parents=True, exist_ok=True)
        key = hashlib.sha256(args.resource.encode()).hexdigest()
        claim = path / (key + ".json")
        with locked(claim):
            if args.command == "claim":
                if claim.exists():
                    raise ValueError("Resource already claimed; coordinate with its owner")
                save(claim, {"resource":args.resource,"owner":args.owner,"host":socket.gethostname(),"created":now()})
            else:
                if not claim.exists() or json.loads(claim.read_text())["owner"] != args.owner:
                    raise ValueError("Cannot release another owner's or absent claim")
                claim.unlink()
        print(json.dumps({"resource":args.resource,"action":args.command})); return
    with locked(path):
        if args.command == "init":
            if path.exists(): raise ValueError("Task already exists")
            root = args.root.resolve()
            if not root.is_dir(): raise ValueError("Task root must exist")
            instructions = [{"path":str(p.resolve()),"sha256":fingerprint(p),"provenance":"caller declares loaded"} for p in args.instruction]
            state = {"version":1,"host":socket.gethostname(),"root":str(root),"intent":args.intent,
                     "mode":args.mode,"created":now(),"sources":args.source,"instructions":instructions,
                     "decisions":[],"items":{i:{"status":"pending"} for i in args.item},"attempts":[],"checkpoints":[]}
            save(path,state); print(json.dumps({"created":str(path)})); return
        if path.is_symlink(): raise ValueError("Refusing symlink state")
        state = json.loads(path.read_text())
        if state["host"] != socket.gethostname():
            raise ValueError("Task belongs to another host; explicitly re-establish the task contract")
        result = {}; exit_code = 0
        if args.command == "decision":
            for entry in state["decisions"]:
                if entry["key"] == args.key and entry["status"] == "accepted":
                    entry["status"] = "superseded"
            state["decisions"].append({"key":args.key,"value":args.value,"evidence":args.evidence,"status":"accepted","time":now()})
        elif args.command == "sources":
            state.setdefault("source_history",[]).append({"superseded":state["sources"],"evidence":args.evidence,"time":now()})
            state["sources"] = args.source
        elif args.command == "item":
            if args.item not in state["items"]: raise ValueError("Item was not in the declared inventory")
            refs = {}
            for ref in args.source:
                key, sep, value = ref.partition("=")
                if not sep or not value.strip(): raise ValueError("Use source-id=supporting-location")
                if key in refs: raise ValueError("Duplicate source reference")
                refs[key] = value
            entry = {"status":args.status,"sources":refs,"check":args.check,"note":args.note,"time":now()}
            if args.status == "done":
                if set(state["sources"]) - set(refs): raise ValueError("Required source coverage is missing")
                if not args.output or not args.check: raise ValueError("Done requires an output and substantive check evidence")
                out = source_path(state,str(args.output))
                if not out.is_file(): raise ValueError("Output does not exist")
                entry.update(output=str(out),sha256=fingerprint(out),contract_sha256=contract_hash(state))
            state["items"][args.item] = entry
        elif args.command == "status":
            items = {}
            for name, entry in state["items"].items():
                status = entry["status"]
                if status == "done":
                    p = Path(entry["output"])
                    if not p.is_file() or fingerprint(p) != entry["sha256"] or entry.get("contract_sha256") != contract_hash(state): status = "stale"
                items[name] = status
            print(json.dumps({"intent":state["intent"],"items":items,
                              "accepted_decisions":[d for d in state["decisions"] if d["status"]=="accepted"]},indent=2)); return
        elif args.command == "attempt":
            signature = hashlib.sha256(json.dumps([args.operation,args.input,args.error]).encode()).hexdigest()
            previous = state["attempts"][-1] if state["attempts"] else {}
            repeated = previous.get("signature")==signature
            count = previous.get("count",0)+1 if repeated else 1
            event = {"signature":signature,"operation":args.operation,"input":args.input,"error":args.error,
                     "count":count,"recovery":args.recovery,"time":now()}
            state["attempts"].append(event)
            result = {"identical_failures":count,"stop_unchanged_approach":count>=2}
            exit_code = 3 if count>=2 else 0
        elif args.command == "guard":
            target = source_path(state,args.target)
            if args.action == "write" and state["mode"] != "implementation":
                raise ValueError("Analysis task does not authorize writes")
            result = {"scope_check":"passed","target":str(target),"action":args.action,
                      "limit":"Does not establish external-action authorization or isolate tool execution"}
        elif args.command == "checkpoint":
            if not args.file and not args.deleted: raise ValueError("Select files or deleted paths")
            deleted = [source_path(state,item) for item in args.deleted]
            if any(p.exists() for p in deleted): raise ValueError("Deleted paths must actually be absent")
            selected = []
            for item in args.file:
                raw = Path(item)
                raw = raw if raw.is_absolute() else Path(state["root"])/raw
                # A byte-only checkpoint must not silently convert links into files.
                for component in [raw, *raw.parents]:
                    if component == Path(state["root"]): break
                    if component.is_symlink(): raise ValueError("Symlink checkpoint requires link-aware project recovery tooling")
                p = source_path(state,item)
                if not p.is_file(): raise ValueError("Checkpoint source must be an explicit existing file")
                if private_source(p): raise ValueError("Potential secret source refused; use protected project recovery tooling")
                selected.append(p)
            directory = path.parent / (path.stem+"-checkpoints")
            directory.mkdir(mode=0o700,exist_ok=True)
            dest = Path(tempfile.mkdtemp(prefix="source-",dir=directory))
            entries = []
            for p in selected:
                rel = p.relative_to(Path(state["root"]))
                out = dest/"files"/rel; out.parent.mkdir(parents=True,exist_ok=True)
                data = p.read_bytes()
                fd = os.open(str(out),os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600)
                with os.fdopen(fd,"wb") as f:f.write(data)
                digest=hashlib.sha256(data).hexdigest()
                if fingerprint(out)!=digest:raise ValueError("Checkpoint readback failed")
                entries.append({"source":str(p),"relative":str(rel),"sha256":digest,"source_mode":p.stat().st_mode & 0o777})
            checkpoint={"directory":str(dest),"root":state["root"],"host":state["host"],
                        "base":args.base,"files":entries,"deleted":[str(p.relative_to(Path(state["root"]))) for p in deleted],"created":now(),
                        "limit":"Selected complete file bytes; caller must distinguish owned and preexisting changes"}
            save(dest/"manifest.json",checkpoint);state["checkpoints"].append(checkpoint);result=checkpoint
        save(path,state)
        print(json.dumps(result or {"updated":str(path)},indent=2))
        if exit_code:raise SystemExit(exit_code)
if __name__ == "__main__":
    try:main()
    except (ValueError,OSError,KeyError,json.JSONDecodeError) as e:
        raise SystemExit(str(e))
