#!/usr/bin/env python3
"""House status: read-only GitHub REST report via `gh api`. 589/kin."""
import json, subprocess, sys, datetime, time
from zoneinfo import ZoneInfo

OWNERS = ["TREEOFLIFE-APOSTLES", "JESUSBURNING"]
ACCOUNT = "MultiDimensionalDevilsKingdomsRoute666"
INCLUDE_PRIVATE = "--include-private" in sys.argv
PT = ZoneInfo("America/Los_Angeles")

def api(path, paginate=False):
    cmd = ["gh", "api", "-H", "Accept: application/vnd.github+json", path]
    if paginate:
        cmd.insert(2, "--paginate"); cmd += ["--jq", ".[] | tojson"]
    for attempt in range(3):
        r = subprocess.run(cmd, capture_output=True, text=True)
        if not r.returncode:
            break
        time.sleep(2 * (attempt + 1))
    else:
        return None
    if paginate:
        return [json.loads(l) for l in r.stdout.splitlines() if l.strip()]
    return json.loads(r.stdout or "null")

def pt(ts):
    if not ts: return "-"
    return datetime.datetime.fromisoformat(ts.replace("Z", "+00:00")).astimezone(PT).strftime("%Y-%m-%d %H:%M PT")

def pages(full, has):
    if not has: return "-"
    d = api(f"repos/{full}/pages")
    if not d: return "configured?"
    b = api(f"repos/{full}/pages/builds/latest") or {}
    return f"{d.get('status') or b.get('status','?')} ({d.get('html_url','')})"

def rows(repos):
    out = []
    for r in sorted(repos, key=lambda x: x.get("pushed_at") or "", reverse=True):
        f = r["full_name"]
        prs = api(f"repos/{f}/pulls?state=open&per_page=100", True)
        npr = len(prs) if prs is not None else "?"
        nis = r.get("open_issues_count", 0) - (npr if isinstance(npr, int) else 0)
        out.append(f"| [{f}]({r['html_url']}) | {pt(r.get('pushed_at'))} | {npr} | {nis} | "
                   f"{pages(f, r.get('has_pages'))} |")
    return out

def main(path):
    now = datetime.datetime.now(PT).strftime("%Y-%m-%d %H:%M PT")
    lines = [f"# House status", f"_Generated {now} by house_status.py (read-only)._", ""]
    total = 0
    hdr = ["| Repo | Last push | Open PRs | Open issues | Pages |", "|---|---|---|---|---|"]
    for o in OWNERS:
        repos = api(f"orgs/{o}/repos?per_page=100&type=all", True)
        if repos is None:
            repos = api(f"users/{o}/repos?per_page=100", True) or []
        hidden = sum(1 for r in repos if r.get("private"))
        if not INCLUDE_PRIVATE:
            repos = [r for r in repos if not r.get("private")]
        total += len(repos)
        note = f", {hidden} private not listed" if hidden and not INCLUDE_PRIVATE else ""
        lines += [f"## {o} ({len(repos)} repos{note})", ""] + hdr + rows(repos) + [""]
    forks = [r for r in (api(f"users/{ACCOUNT}/repos?per_page=100&type=owner", True) or []) if r.get("fork")]
    total += len(forks)
    lines += [f"## {ACCOUNT} forks ({len(forks)})", ""] + hdr + rows(forks) + ["", f"**Total repos: {total}**", ""]
    open(path, "w").write("\n".join(lines))
    print(f"wrote {path}: {total} repos")

if __name__ == "__main__":
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    main(args[0] if args else "reports/house-status.md")
