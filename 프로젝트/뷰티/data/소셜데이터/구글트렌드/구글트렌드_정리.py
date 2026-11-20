"""사용자가 내보낸 Google Trends CSV의 이름과 통합본을 정리한다."""

import csv
import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TERMS = ["선크림", "피부장벽", "세럼", "립틴트", "두피케어", "스킨케어", "탈모샴푸", "비건화장품"]
PATTERN = re.compile(r"^(searched_with_(?:top|rising)-searches_(?:topics|queries)|time_series|by_region)_KR_(202[56])\d{4}-\d{4}_20261118-(\d{4})(?: \((\d+)\))?\.csv$")

# 원본 CSV에는 기준 검색어가 없다. 연관어 내용과 연속 내보내기 순서로 판별한 매핑이다.
MAP = {
    (2025, "top_queries"): {"2100": ["선크림", "피부장벽", "세럼", "두피케어"], "2101": ["스킨케어", "탈모샴푸"]},
    (2025, "rising_queries"): {"2100": ["선크림", "피부장벽", "세럼", "두피케어"], "2101": ["스킨케어", "탈모샴푸"]},
    (2025, "top_topics"): {"2100": ["선크림", "피부장벽", "세럼", "립틴트", "두피케어"], "2101": ["스킨케어", "탈모샴푸"]},
    (2025, "rising_topics"): {"2100": ["선크림", "피부장벽", "세럼", "립틴트"], "2101": ["두피케어", "스킨케어", "탈모샴푸"]},
    (2026, "top_queries"): {"2102": ["선크림", "피부장벽", "세럼", "립틴트", "두피케어"], "2103": ["스킨케어", "탈모샴푸", "비건화장품"]},
    (2026, "rising_queries"): {"2102": ["선크림", "피부장벽", "세럼", "립틴트", "두피케어"], "2103": ["스킨케어", "탈모샴푸", "비건화장품"]},
    (2026, "top_topics"): {"2102": ["선크림", "피부장벽", "세럼", "립틴트", "두피케어"], "2103": ["스킨케어", "탈모샴푸", "비건화장품"]},
    (2026, "rising_topics"): {"2102": ["선크림", "피부장벽", "세럼", "립틴트"], "2103": ["두피케어", "스킨케어", "탈모샴푸", "비건화장품"]},
}

def classify(name):
    match = PATTERN.match(name)
    if not match:
        raise ValueError(f"Unexpected source file: {name}")
    prefix, year_string, time, suffix_string = match.groups()
    year, suffix = int(year_string), int(suffix_string or 0)
    if prefix in ("time_series", "by_region"):
        return year, prefix, "", time, suffix
    metric = ("top" if "top-searches" in prefix else "rising") + "_" + ("topics" if prefix.endswith("topics") else "queries")
    term = MAP[(year, metric)][time][suffix]
    return year, metric, term, time, suffix

def rows(path):
    with path.open(encoding="utf-8-sig", newline="") as stream:
        reader = csv.DictReader(stream)
        return reader.fieldnames, list(reader)

files = sorted(p for p in ROOT.glob("*.csv") if PATTERN.match(p.name))
if not files and (ROOT / "관리/구글트렌드_파일명변경목록.csv").exists():
    print("Google Trends files have already been organized.")
    sys.exit(0)
assert len(files) == 62, f"Expected 62 Google exports, found {len(files)}"
renames = []
for source in files:
    year, metric, term, time, suffix = classify(source.name)
    if metric == "time_series":
        new_name = f"구글트렌드_검색관심도_주간_8개검색어_{year}조회_원본.csv"
    elif metric == "by_region":
        new_name = f"구글트렌드_지역별관심도_8개검색어_{year}조회_원본.csv"
    else:
        kind, subject = metric.split("_")
        new_name = f"구글트렌드_연관{'검색어' if subject == 'queries' else '주제'}_{'상위' if kind == 'top' else '급상승'}_{term}_{year}조회_원본.csv"
    category = {
        "time_series": "검색관심도",
        "by_region": "지역별관심도",
    }.get(metric, "연관검색어" if metric.endswith("queries") else "연관주제")
    target = ROOT / category / "원본" / new_name
    assert not target.exists(), f"Target already exists: {target}"
    header, data = rows(source)
    renames.append((source, target, year, metric, term, header, data, hashlib.sha256(source.read_bytes()).hexdigest()))
assert len({item[1] for item in renames}) == 62, "Renamed file names collide"

for source, target, *_ in renames:
    target.parent.mkdir(parents=True, exist_ok=True)
    source.rename(target)

def write(name, header, data):
    output = ROOT / name
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("w", encoding="utf-8-sig", newline="") as stream:
        writer = csv.writer(stream)
        writer.writerow(header)
        writer.writerows(data)

weekly = []
regional = []
related_queries = []
related_topics = []
manifest = []
for source, target, year, metric, term, header, data, checksum in renames:
    assert hashlib.sha256(target.read_bytes()).hexdigest() == checksum
    manifest.append([source.name, target.name, year, metric, term, len(data), checksum,
                     "내용·내보내기 순서로 기준어 추정" if term else "열 이름으로 8개 검색어 확인"])
    if metric == "time_series":
        assert header == ["Time", *TERMS]
        weekly.extend([[year, record["Time"], *[record[t] for t in TERMS], target.name] for record in data])
    elif metric == "by_region":
        assert header == ["Region", *TERMS]
        regional.extend([[year, record["Region"], *[record[t] for t in TERMS], target.name] for record in data])
    else:
        word_type = "query" if metric.endswith("queries") else "topic"
        assert header == [word_type, "search interest", "increase percent"]
        output = related_queries if word_type == "query" else related_topics
        output.extend([[year, term, "상위" if metric.startswith("top") else "급상승", rank,
                        record[word_type], record["search interest"], record["increase percent"], target.name]
                       for rank, record in enumerate(data, start=1)])

weekly.sort(key=lambda record: (record[0], record[1]))
regional.sort(key=lambda record: (record[0], record[1]))
related_queries.sort(key=lambda record: (record[0], record[1], record[2], record[3]))
related_topics.sort(key=lambda record: (record[0], record[1], record[2], record[3]))
write("검색관심도/구글트렌드_검색관심도.csv",
      ["조회구분연도", "주간시작일", *TERMS], [row[:-1] for row in weekly])
write("지역별관심도/구글트렌드_지역별관심도_2025-2026_조회별정규화.csv",
      ["조회구분연도", "지역", *TERMS, "원본파일"], regional)
write("연관검색어/구글트렌드_연관검색어_2025-2026_통합.csv",
      ["조회구분연도", "기준검색어_추정", "구분", "원본순위", "연관검색어", "상대관심도", "증가율", "원본파일"], related_queries)
write("연관주제/구글트렌드_연관주제_2025-2026_통합.csv",
      ["조회구분연도", "기준검색어_추정", "구분", "원본순위", "연관주제", "상대관심도", "증가율", "원본파일"], related_topics)
write("관리/구글트렌드_파일명변경목록.csv",
      ["기존파일명", "변경파일명", "조회구분연도", "자료유형", "기준검색어", "행수", "원본SHA256", "기준검색어확인방법"], manifest)
for _, target, _, metric, *_ in renames:
    if metric == "time_series":
        target.unlink()
weekly_raw = ROOT / "검색관심도/원본"
if weekly_raw.exists() and not any(weekly_raw.iterdir()):
    weekly_raw.rmdir()
print("renamed", len(renames), "weekly", len(weekly), "regional", len(regional),
      "related_queries", len(related_queries), "related_topics", len(related_topics))
