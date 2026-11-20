import csv
import json
import sys
import tempfile
import unittest
from pathlib import Path


sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from prepare_public_release import redact_file


class PublicReleaseTest(unittest.TestCase):
    def test_json_escaped_newline_stays_valid_after_redaction(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "response.json"
            path.write_text(json.dumps({"text": "first line\nhello@example.com 010-1234-5678"}))
            counts = redact_file(path)
            text = json.loads(path.read_text())["text"]
            self.assertEqual(counts, (1, 1))
            self.assertEqual(text, "first line\n[email removed] [phone removed]")

    def test_csv_cells_stay_readable_after_redaction(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "comments.csv"
            with path.open("w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["id", "text"])
                writer.writerow(["c1", "contact me at hello@example.com, thanks"])
            self.assertEqual(redact_file(path), (1, 0))
            with path.open(newline="") as file:
                rows = list(csv.reader(file))
            self.assertEqual(rows[1], ["c1", "contact me at [email removed], thanks"])


if __name__ == "__main__":
    unittest.main()
