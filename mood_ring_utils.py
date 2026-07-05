import csv
import re

YOUTUBE_ID_RE = re.compile(r"^[0-9A-Za-z_-]{11}$")
TEXT_COLUMN_ALIASES = (
    "text",
    "comment",
    "comments",
    "review",
    "tweet_text",
    "tweet text",
    "full_text",
    "full text",
    "content",
)
LIKES_COLUMN_ALIASES = ("likes", "like_count", "like count", "favorite_count")
AUTHOR_COLUMN_ALIASES = ("author", "author_name", "author username", "username")
DATE_COLUMN_ALIASES = ("date", "published_at", "published at", "created_at")


def normalize_column(column):
    return str(column).strip().lower().replace("_", " ")


def first_matching_column(columns, aliases):
    normalized_aliases = {normalize_column(alias) for alias in aliases}
    for column in columns:
        if normalize_column(column) in normalized_aliases:
            return column
    return None


def extract_video_id(url_or_id):
    value = str(url_or_id).strip()
    if YOUTUBE_ID_RE.fullmatch(value):
        return value

    regex = r"(?:v=|youtu\.be/|/shorts/)([0-9A-Za-z_-]{11})"
    match = re.search(regex, value)
    if match:
        return match.group(1)
    raise ValueError("Enter a valid YouTube URL or 11-character video ID.")


def parse_like_count(value):
    if value is None or str(value).strip() == "":
        return 0
    try:
        return int(value)
    except (TypeError, ValueError):
        try:
            return int(float(str(value).strip()))
        except (TypeError, ValueError):
            return 0


def load_comments_csv_rows(path):
    with open(path, newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        rows_by_column = list(reader)
        columns = list(reader.fieldnames or [])

    text_column = first_matching_column(columns, TEXT_COLUMN_ALIASES)
    if text_column is None:
        supported = ", ".join(TEXT_COLUMN_ALIASES)
        raise ValueError(f"CSV must include one text column: {supported}")

    likes_column = first_matching_column(columns, LIKES_COLUMN_ALIASES)
    author_column = first_matching_column(columns, AUTHOR_COLUMN_ALIASES)
    date_column = first_matching_column(columns, DATE_COLUMN_ALIASES)

    rows = []
    for row in rows_by_column:
        text = str(row.get(text_column, "")).strip()
        if not text:
            continue

        likes = row.get(likes_column, 0) if likes_column else 0
        rows.append({
            'text': text,
            'likes': parse_like_count(likes),
            'author': row.get(author_column, "") if author_column else "",
            'date': row.get(date_column, "") if date_column else "",
        })

    return rows
