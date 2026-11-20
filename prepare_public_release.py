"""강의 폴더를 공개 저장소용으로 복사하고 YouTube 연락처를 가린다."""

from __future__ import annotations

import argparse
import csv
import json
import re
import shutil
import unicodedata
from pathlib import Path


ROOT = Path(__file__).resolve().parent
EMAIL = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
PHONE = re.compile(r"(?<!\d)01[016789][- ]?\d{3,4}[- ]?\d{4}(?!\d)")


def redact_file(path: Path) -> tuple[int, int]:
    """구조를 파싱한 뒤 셀이나 문자열 값 안의 연락처만 가린다."""
    emails = phones = 0

    def redact(value):
        nonlocal emails, phones
        if isinstance(value, str):
            value, found_emails = EMAIL.subn("[email removed]", value)
            value, found_phones = PHONE.subn("[phone removed]", value)
            emails += found_emails
            phones += found_phones
        elif isinstance(value, list):
            value = [redact(item) for item in value]
        elif isinstance(value, dict):
            value = {key: redact(item) for key, item in value.items()}
        return value

    if path.suffix == ".json":
        data = redact(json.loads(path.read_text(encoding="utf-8-sig")))
        if emails or phones:
            path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    elif path.suffix == ".csv":
        has_bom = path.read_bytes().startswith(b"\xef\xbb\xbf")
        with path.open(encoding="utf-8-sig", newline="") as file:
            rows = [[redact(cell) for cell in row] for row in csv.reader(file)]
        if emails or phones:
            with path.open("w", encoding="utf-8-sig" if has_bom else "utf-8", newline="") as file:
                csv.writer(file).writerows(rows)
    else:
        raise ValueError(f"지원하지 않는 파일 형식: {path}")
    return emails, phones


def prepare(destination: Path) -> dict[str, int]:
    destination = destination.resolve()
    if destination == ROOT or ROOT in destination.parents:
        raise ValueError("공개 사본은 강의 폴더 바깥에 만들어야 합니다.")
    shutil.copytree(
        ROOT,
        destination,
        dirs_exist_ok=True,
        ignore=shutil.ignore_patterns(".git", ".DS_Store", "__pycache__", "*.pyc"),
    )
    counts = {"files": 0, "emails": 0, "phones": 0}
    for path in destination.rglob("*"):
        normalized = unicodedata.normalize("NFC", str(path.relative_to(destination)))
        if not path.is_file() or "/유튜브/" not in "/" + normalized or path.suffix not in {".csv", ".json"}:
            continue
        emails, phones = redact_file(path)
        if emails or phones:
            counts["files"] += 1
            counts["emails"] += emails
            counts["phones"] += phones
        if redact_file(path) != (0, 0):
            raise ValueError(f"연락처가 남았습니다: {path}")
    return counts


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()
    print(prepare(args.destination))
