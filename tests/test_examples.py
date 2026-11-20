import sys
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "실습"))

from examples import housing_quality, population_profile, sentiment_summary, spotify_summary


class LectureExamplesTest(unittest.TestCase):
    def test_spotify_summary_uses_real_dataset(self):
        result = spotify_summary(ROOT / "실습" / "Spotify.csv")
        self.assertEqual(result["rows"], 114000)
        self.assertEqual(result["columns"], 21)
        self.assertEqual(result["top_genres"][0]["genre"], "kids")
        self.assertEqual(result["top_genres"][0]["count"], 1000)

    def test_housing_quality_counts_missing_values(self):
        result = housing_quality(ROOT / "실습" / "housing.csv")
        self.assertEqual(result["rows"], 20640)
        self.assertEqual(result["missing"]["total_bedrooms"], 207)

    def test_population_profile_uses_available_age_bands(self):
        result = population_profile(ROOT / "실습" / "population.csv")
        self.assertEqual(result["national_total"], 51169148)
        self.assertEqual(len(result["regions"]), 17)
        self.assertIn("70세 이상", result["age_bands_available"])
        self.assertNotIn("65세 이상", result["age_bands_available"])

    def test_sentiment_summary_classifies_source_text(self):
        result = sentiment_summary(ROOT / "실습" / "감성분석.csv")
        self.assertEqual(result["rows"], 3534)
        self.assertEqual(result["counts"], {"positive": 1718, "negative": 902, "neutral": 914})
        self.assertEqual(round(sum(result["percentages"].values()), 1), 100.0)


if __name__ == "__main__":
    unittest.main()
