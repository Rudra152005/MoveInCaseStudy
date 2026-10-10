"""
playstore_pulse.py
==================
MoveInSync Play Store Ratings - Weekly Pulse Report
Forward Deployed Engineer tool | Runs every Monday or on demand

Usage:
    pip install google-play-scraper pandas tabulate
    python playstore_pulse.py

Output: prints the 6-line standard answer + theme breakdown table.
Optionally writes a CSV and a JSON snapshot for trending.

Author: FDE candidate | Data: public Play Store via google-play-scraper
"""

import json
import os
import datetime
import collections
from pathlib import Path

# -- Dependency check ---------------------------------------------------------
try:
    from google_play_scraper import app as gps_app, reviews, Sort
    import pandas as pd
    from tabulate import tabulate
except ImportError:
    print(
        "Missing dependencies. Run:\n"
        "  pip install google-play-scraper pandas tabulate\n"
        "then re-run this script."
    )
    raise

# -- Config --------------------------------------------------------------------
APP_ID          = "com.moveinsync.ets"          # MoveInSync employee app
COUNTRY         = "in"                           # India - primary market
LANG            = "en"
MAX_REVIEWS     = 500                            # pull up to 500 per run
ROLLING_DAYS    = 30                             # for rolling average
SNAPSHOT_DIR    = Path("pulse_snapshots")        # where JSON snapshots are saved
SNAPSHOT_DIR.mkdir(exist_ok=True)

# Theme keyword mapping (expand as needed)
THEME_KEYWORDS = {
    "No Show / penalty":        ["no show", "noshow", "penalty", "penalised", "penalized",
                                  "check in", "checkin", "marked absent", "deducted"],
    "Booking / date bug":       ["booking", "booked", "date", "wrong date", "not booked",
                                  "trip not found", "shuttle", "cancel"],
    "Tracking / GPS / ETA":     ["tracking", "gps", "location", "eta", "pickup time",
                                  "live location", "navigation", "route", "map"],
    "Notifications":            ["notification", "notify", "alert", "reminder", "push"],
    "OTP / login / safety":     ["otp", "login", "password", "seat belt", "seatbelt",
                                  "verification", "cannot board", "boarding"],
    "UI / redesign":            ["ui", "interface", "design", "button", "layout",
                                  "confusing", "ugly", "update changed", "redesign"],
    "Crash / performance":      ["crash", "crashes", "slow", "freeze", "hang",
                                  "loading", "not opening", "black screen", "stuck"],
    "Support / ops":            ["driver", "support", "complaint", "helpline", "ops",
                                  "transport desk", "customer care", "no response"],
}

# -- Helpers -------------------------------------------------------------------

def fetch_app_meta() -> dict:
    """Fetch top-level app metadata (rating, install count, etc.)."""
    return gps_app(APP_ID, lang=LANG, country=COUNTRY)


def fetch_reviews_df(count: int = MAX_REVIEWS) -> pd.DataFrame:
    """Pull the most recent reviews and return as a DataFrame."""
    result, _ = reviews(
        APP_ID,
        lang=LANG,
        country=COUNTRY,
        sort=Sort.NEWEST,
        count=count,
    )
    df = pd.DataFrame(result)
    df["at"] = pd.to_datetime(df["at"])
    return df


def tag_themes(text: str) -> list[str]:
    """Return list of matching theme labels for a review text."""
    text_lower = (text or "").lower()
    matched = [
        theme
        for theme, keywords in THEME_KEYWORDS.items()
        if any(kw in text_lower for kw in keywords)
    ]
    return matched if matched else ["Other"]


def classify_reviews(df: pd.DataFrame) -> pd.DataFrame:
    """Add a 'themes' column to the dataframe."""
    df = df.copy()
    df["themes"] = df["content"].apply(tag_themes)
    return df


def rolling_stats(df: pd.DataFrame, days: int = ROLLING_DAYS) -> dict:
    """Compute stats for the last N days."""
    cutoff = pd.Timestamp.now(tz="UTC") - pd.Timedelta(days=days)
    # Ensure 'at' is timezone-aware for comparison
    if df["at"].dt.tz is None:
        df = df.copy()
        df["at"] = df["at"].dt.tz_localize("UTC")
    recent = df[df["at"] >= cutoff]
    if recent.empty:
        return {"count": 0, "avg": None, "one_star_pct": None}
    avg = recent["score"].mean()
    one_star_pct = (recent["score"] == 1).sum() / len(recent) * 100
    return {"count": len(recent), "avg": round(avg, 2), "one_star_pct": round(one_star_pct, 1)}


def version_breakdown(df: pd.DataFrame) -> pd.DataFrame:
    """Average rating per app version (most recent versions first)."""
    df = df.copy()
    vb = (
        df.groupby("reviewCreatedVersion", dropna=False)["score"]
        .agg(count="count", avg_rating="mean")
        .reset_index()
        .rename(columns={"reviewCreatedVersion": "version"})
        .sort_values("count", ascending=False)
        .head(8)
    )
    vb["avg_rating"] = vb["avg_rating"].round(2)
    return vb


def top_themes(df: pd.DataFrame, top_n: int = 5) -> list[tuple]:
    """Count theme occurrences (a review can have multiple themes)."""
    counter: collections.Counter = collections.Counter()
    for themes in df["themes"]:
        for t in themes:
            counter[t] += 1
    return counter.most_common(top_n)


def reply_stats(df: pd.DataFrame) -> dict:
    """Compute developer reply rate on 1-2 star reviews."""
    low_star = df[df["score"] <= 2]
    if low_star.empty:
        return {"total_low": 0, "replied": 0, "rate_pct": None}
    replied = low_star["replyContent"].notna().sum()
    rate = replied / len(low_star) * 100
    return {
        "total_low": len(low_star),
        "replied": int(replied),
        "rate_pct": round(rate, 1),
    }


def save_snapshot(meta: dict, stats: dict) -> None:
    """Persist a JSON snapshot for week-on-week trending."""
    today = datetime.date.today().isoformat()
    snapshot = {
        "date": today,
        "global_rating": meta.get("score"),
        "total_ratings": meta.get("ratings"),
        "rolling_30d_avg": stats.get("avg"),
        "rolling_30d_one_star_pct": stats.get("one_star_pct"),
    }
    path = SNAPSHOT_DIR / f"snapshot_{today}.json"
    with open(path, "w") as f:
        json.dump(snapshot, f, indent=2)
    print(f"\n[Snapshot saved -> {path}]")


def load_previous_snapshot() -> dict | None:
    """Load the most recent previous snapshot for delta reporting."""
    files = sorted(SNAPSHOT_DIR.glob("snapshot_*.json"))
    # skip today's file if already saved
    today = datetime.date.today().isoformat()
    prev_files = [f for f in files if today not in f.name]
    if not prev_files:
        return None
    with open(prev_files[-1]) as f:
        return json.load(f)


# -- Main report ---------------------------------------------------------------

def print_standard_answer(meta: dict, rolling: dict, prev: dict | None,
                           version_df: pd.DataFrame, themes: list[tuple],
                           reply: dict) -> None:
    """Print the 6-line standard answer used in recurring check-ins."""
    global_rating = meta.get("score", "N/A")
    total_ratings  = meta.get("ratings", "N/A")

    delta_global = ""
    if prev and prev.get("global_rating"):
        diff = round(global_rating - prev["global_rating"], 3)
        sign = "+" if diff >= 0 else ""
        delta_global = f"  ({sign}{diff} vs last week)"

    delta_30d = ""
    if prev and prev.get("rolling_30d_avg") and rolling.get("avg"):
        diff = round(rolling["avg"] - prev["rolling_30d_avg"], 2)
        sign = "+" if diff >= 0 else ""
        delta_30d = f"  ({sign}{diff} vs last week)"

    print("\n" + "=" * 68)
    print("  MOVEINSYNC PLAY STORE PULSE -- " + datetime.date.today().isoformat())
    print("=" * 68)

    # Line 1
    print(f"\n1. Global rating : {global_rating} *  ({total_ratings:,} total ratings){delta_global}")

    # Line 2
    if rolling["avg"]:
        print(f"2. Rolling 30-day: avg {rolling['avg']} *  |  "
              f"1-star share {rolling['one_star_pct']}%  "
              f"({rolling['count']} new ratings){delta_30d}")
    else:
        print("2. Rolling 30-day: insufficient data in fetched batch")

    # Line 3 - version breakdown
    print("\n3. Rating by version (recent):")
    print(tabulate(version_df, headers="keys", tablefmt="simple", showindex=False))

    # Line 4 - top themes
    print("\n4. Top complaint themes this period:")
    for rank, (theme, count) in enumerate(themes, 1):
        print(f"   {rank}. {theme}  ({count} mentions)")

    # Line 5 - reply rate
    if reply["rate_pct"] is not None:
        print(f"\n5. Developer reply rate on 1-2* reviews: "
              f"{reply['replied']}/{reply['total_low']}  ({reply['rate_pct']}%)")
    else:
        print("\n5. Developer reply rate: no low-star reviews in fetched batch")

    # Line 6 - one-sentence summary
    top_theme = themes[0][0] if themes else "unknown"
    trend = "stable"
    if prev and prev.get("rolling_30d_avg") and rolling.get("avg"):
        diff = rolling["avg"] - prev["rolling_30d_avg"]
        trend = "improving" if diff > 0.05 else ("declining" if diff < -0.05 else "stable")
    print(f"\n6. Summary: 30-day trend is {trend}; "
          f"top complaint this week is '{top_theme}' -- "
          f"check P0 action items if this theme persists.")

    print("\n" + "=" * 68)


def main() -> None:
    print("Fetching MoveInSync Play Store data ...")

    meta    = fetch_app_meta()
    df_raw  = fetch_reviews_df()
    df      = classify_reviews(df_raw)
    rolling = rolling_stats(df)
    ver_df  = version_breakdown(df)
    themes  = top_themes(df[df["score"] <= 3])      # focus on low-star themes
    reply   = reply_stats(df)
    prev    = load_previous_snapshot()

    save_snapshot(meta, rolling)
    print_standard_answer(meta, rolling, prev, ver_df, themes, reply)

    # Optional: export raw tagged reviews to CSV
    out_csv = f"reviews_{datetime.date.today().isoformat()}.csv"
    df[["at", "score", "reviewCreatedVersion", "content", "themes",
        "replyContent"]].to_csv(out_csv, index=False)
    print(f"[Raw reviews exported -> {out_csv}]\n")


if __name__ == "__main__":
    main()
