#!/usr/bin/env python3
"""GitHub-native cross-repository inventory.

Reads registry/PROJECT_REGISTRY.json and records repository metadata plus root
contents. Public repositories can be scanned with no token. Private repositories
require NEXENT_GITHUB_TOKEN stored as a GitHub Actions secret.
"""
import json, os, urllib.request
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
registry=json.loads((ROOT/"registry/PROJECT_REGISTRY.json").read_text())
token=os.environ.get("NEXENT_GITHUB_TOKEN") or os.environ.get("GITHUB_TOKEN")
out={"schema_version":"1.0","repositories":[]}

def get(url):
    req=urllib.request.Request(url,headers={"Accept":"application/vnd.github+json"})
    if token:
        req.add_header("Authorization",f"Bearer {token}")
    with urllib.request.urlopen(req,timeout=30) as r:
        return json.load(r)

for item in registry["repositories"]:
    owner,repo=item["repo"].split("/",1)
    record=dict(item)
    url=f"https://api.github.com/repos/{owner}/{repo}"
    try:
        meta=get(url)
        record.update({"default_branch":meta["default_branch"],"visibility":meta["visibility"],
                       "size_kb":meta["size"],"sha":meta["pushed_at"]})
        record["root_files"]=get(f"{url}/contents?ref={meta['default_branch']}")
        record["scan_status"]="SCANNED"
    except Exception as exc:
        record["scan_status"]="BLOCKED"
        record["error"]=str(exc)
    out["repositories"].append(record)

Path("evidence").mkdir(exist_ok=True)
Path("evidence/github-inventory.json").write_text(json.dumps(out,ensure_ascii=False,indent=2))
print(json.dumps({"repositories":len(out["repositories"]),"output":"evidence/github-inventory.json"},ensure_ascii=False))
