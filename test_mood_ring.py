import os
from tempfile import TemporaryDirectory
import unittest

from mood_ring_utils import extract_video_id, load_comments_csv_rows


class MoodRingTests(unittest.TestCase):
    def test_extracts_short_url_video_id(self):
        self.assertEqual(
            extract_video_id("https://youtu.be/ERCMXc8x7mc?t=12"),
            "ERCMXc8x7mc",
        )

    def test_rejects_invalid_video_id(self):
        with self.assertRaises(ValueError):
            extract_video_id("not valid!")

    def test_loads_xquik_tweet_text_export(self):
        with TemporaryDirectory() as directory:
            csv_path = os.path.join(directory, "xquik-comments.csv")
            with open(csv_path, "w", encoding="utf-8") as file:
                file.write("Tweet Text,Author Username,likes\nGreat launch,alice,5\n,,2\n")

            rows = load_comments_csv_rows(csv_path)

        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0]["text"], "Great launch")
        self.assertEqual(rows[0]["author"], "alice")


if __name__ == "__main__":
    unittest.main()
