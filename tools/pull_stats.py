"""
Upgrade 1: Pull GitHub stats -> assets/stats.json
Anonymous locally; uses GITHUB_TOKEN automatically when present (GitHub Actions).
"""
import os, json, datetime as dt
from pathlib import Path
import httpx

USER = "itspalash2506"

def client():
    h = {"User-Agent": "profile-stats", "Accept": "application/vnd.github+json"}
    tok = os.environ.get("GITHUB_TOKEN")
    if tok:
        h["Authorization"] = f"Bearer {tok}"
    return httpx.Client(headers=h, timeout=30, follow_redirects=True)

def main():
    c = client()

    user = c.get(f"https://api.github.com/users/{USER}").json()

    # all repos (paginate)
    repos, page = [], 1
    while True:
        batch = c.get(f"https://api.github.com/users/{USER}/repos",
                      params={"per_page": 100, "page": page, "type": "owner"}).json()
        if not isinstance(batch, list) or not batch:
            break
        repos += batch
        if len(batch) < 100:
            break
        page += 1

    own = [r for r in repos if not r.get("fork")]
    stars = sum(r.get("stargazers_count", 0) for r in own)
    forks = sum(r.get("forks_count", 0) for r in own)

    # language bytes across own repos
    lang_bytes = {}
    for r in own:
        try:
            langs = c.get(r["languages_url"]).json()
            for k, v in langs.items():
                lang_bytes[k] = lang_bytes.get(k, 0) + v
        except Exception:
            pass
    total_b = sum(lang_bytes.values()) or 1
    ranked = sorted(lang_bytes.items(), key=lambda kv: kv[1], reverse=True)
    top = ranked[:5]
    top_pct = [(k, round(v / total_b * 100, 1)) for k, v in top]
    other = round(100 - sum(p for _, p in top_pct), 1)
    if other > 0.1 and len(ranked) > 5:
        top_pct.append(("Other", other))

    # total contributions from the graph pull, if present
    contrib = 0
    cj = Path("assets/contributions.json")
    if cj.exists():
        contrib = json.loads(cj.read_text()).get("total", 0)

    followers = user.get("followers", 0)
    repo_count = user.get("public_repos", len(own))

    # simple honest rank from a weighted score
    score = stars * 4 + followers * 3 + repo_count + contrib * 0.4 + forks * 2
    rank = ("A+" if score >= 200 else "A" if score >= 120 else "B+" if score >= 70
            else "B" if score >= 35 else "C+" if score >= 15 else "C")
    rank_pct = min(0.97, 0.25 + score / 260)   # ring fill 0..1

    out = {
        "user": USER,
        "name": user.get("name") or USER,
        "followers": followers,
        "public_repos": repo_count,
        "stars": stars,
        "forks": forks,
        "contributions": contrib,
        "rank": rank,
        "rank_pct": round(rank_pct, 3),
        "languages": top_pct,
        "generated": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
    }
    Path("assets/stats.json").write_text(json.dumps(out, indent=2))
    print(f"wrote assets/stats.json  repos={repo_count} stars={stars} followers={followers} "
          f"contrib={contrib} rank={rank}")
    print("languages:", top_pct)

if __name__ == "__main__":
    main()