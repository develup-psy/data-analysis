"""강의 CSV의 수치와 분석 기준을 재현하는 작은 실행 예제."""

from __future__ import annotations

import argparse
import csv
import json
import statistics
import unicodedata
from collections import Counter, defaultdict
from pathlib import Path


DATA_DIR = Path(__file__).resolve().parent


def data_path(path: Path) -> Path:
    """macOS의 분해형 한글 파일명과 일반 한글 파일명을 함께 찾는다."""
    path = Path(path)
    if path.exists():
        return path
    target = unicodedata.normalize("NFC", path.name)
    for candidate in path.parent.iterdir():
        if unicodedata.normalize("NFC", candidate.name) == target:
            return candidate
    raise FileNotFoundError(path)


def read_rows(path: Path, encoding: str = "utf-8-sig") -> list[dict[str, str]]:
    with data_path(path).open(encoding=encoding, newline="") as file:
        return list(csv.DictReader(file))


def spotify_summary(path: Path = DATA_DIR / "Spotify.csv") -> dict:
    rows = read_rows(path)
    grouped = defaultdict(list)
    for row in rows:
        if row["danceability"]:
            grouped[row["track_genre"]].append(float(row["danceability"]))
    top = sorted(
        (
            {
                "genre": genre,
                "count": len(values),
                "mean_danceability": round(statistics.mean(values), 4),
                "median_danceability": round(statistics.median(values), 4),
            }
            for genre, values in grouped.items()
        ),
        key=lambda item: (-item["mean_danceability"], item["genre"]),
    )[:10]
    return {"rows": len(rows), "columns": len(rows[0]), "top_genres": top}


def housing_quality(path: Path = DATA_DIR / "housing.csv") -> dict:
    rows = read_rows(path)
    columns = list(rows[0])
    missing = {column: sum(not row[column].strip() for row in rows) for column in columns}
    missing = {column: count for column, count in missing.items() if count}
    return {"rows": len(rows), "columns": len(columns), "missing": missing}


def population_profile(path: Path = DATA_DIR / "population.csv") -> dict:
    rows = read_rows(path, encoding="cp949")
    national = next(row for row in rows if row["지역"] == "전국")
    regions = [row for row in rows if row["지역"] != "전국"]
    top = sorted(
        ({"region": row["지역"], "population": int(row["전체_총인구수"].strip())} for row in regions),
        key=lambda item: -item["population"],
    )[:5]
    return {
        "national_total": int(national["전체_총인구수"].strip()),
        "regions": [row["지역"] for row in regions],
        "top_regions": top,
        "age_bands_available": ["60세 이상", "70세 이상"],
        "encoding": "cp949",
    }


def sentiment_summary(path: Path = DATA_DIR / "감성분석.csv") -> dict:
    from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

    rows = read_rows(path)
    analyzer = SentimentIntensityAnalyzer()
    counts = Counter({"positive": 0, "negative": 0, "neutral": 0})
    for row in rows:
        compound = analyzer.polarity_scores(row["text"])["compound"]
        label = "positive" if compound >= 0.05 else "negative" if compound <= -0.05 else "neutral"
        counts[label] += 1
    total = len(rows)
    return {
        "rows": total,
        "method": "VADER, 원문 text의 compound 점수",
        "thresholds": {"positive": ">= 0.05", "negative": "<= -0.05", "neutral": "그 사이"},
        "counts": dict(counts),
        "percentages": {label: round(count / total * 100, 2) for label, count in counts.items()},
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("topic", choices=["spotify", "housing", "population", "sentiment"])
    args = parser.parse_args()
    functions = {
        "spotify": spotify_summary,
        "housing": housing_quality,
        "population": population_profile,
        "sentiment": sentiment_summary,
    }
    print(json.dumps(functions[args.topic](), ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
