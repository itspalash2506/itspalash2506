"""
Step 5a: Pull public contribution data (no token) -> assets/contributions.json
Source: https://github.com/users/<USER>/contributions  (the same fragment
        GitHub's own profile page uses; no auth required).
"""
import json, re, datetime as dt
from pathlib import Path
import httpx
from lxml import html

USER = "itspalash2506"

def main():
    url = f"https://github.com/users/{USER}/contributions"
    r = httpx.get(url, headers={
        "User-Agent": "Mozilla/5.0 (github-profile-graph)",
        "X-Requested-With": "XMLHttpRequest",
    }, timeout=30, follow_redirects=True)
    r.raise_for_status()
    doc = html.fromstring(r.text)

    # exact counts live in <tool-tip for="cell-id"> "N contributions on ..." </tool-tip>
    counts = {}
    for tip in doc.xpath("//tool-tip"):
        fid = tip.get("for")
        if not fid:
            continue
        m = re.match(r"\s*(No|\d+)", tip.text_content())
        counts[fid] = 0 if (not m or m.group(1) == "No") else int(m.group(1))

    days = []
    for td in doc.xpath("//td[contains(@class,'ContributionCalendar-day')]"):
        date = td.get("data-date")
        if not date:
            continue
        level = int(td.get("data-level") or 0)
        count = counts.get(td.get("id"), [0, 1, 3, 6, 10][level])   # fallback via level
        days.append({"date": date, "count": count, "level": level})

    days.sort(key=lambda x: x["date"])
    if not days:
        raise SystemExit("No contribution cells found — GitHub markup may have changed.")

    total = sum(d["count"] for d in days)

    # longest streak (any run of active days)
    longest = cur = 0
    for d in days:
        cur = cur + 1 if d["count"] > 0 else 0
        longest = max(longest, cur)

    # current streak = trailing run of active days up to today
    current = 0
    today = dt.date.today()
    for d in reversed(days):
        if dt.date.fromisoformat(d["date"]) > today:
            continue
        if d["count"] > 0:
            current += 1
        else:
            break

    # most active weekday
    names = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    tally = [0] * 7
    for d in days:
        tally[dt.date.fromisoformat(d["date"]).weekday()] += d["count"]
    busiest = names[tally.index(max(tally))] if total else "—"

    out = {
        "user": USER, "total": total,
        "current_streak": current, "longest_streak": longest,
        "busiest_day": busiest,
        "generated": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "days": days,
    }
    Path("assets/contributions.json").write_text(json.dumps(out, indent=2))
    print(f"wrote assets/contributions.json  {len(days)} days, {total} contributions, "
          f"current {current}d, longest {longest}d, busiest {busiest}")

if __name__ == "__main__":
    main()