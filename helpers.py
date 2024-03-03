import glob
import hashlib
import html
import json
import re
from typing import List


def from_json(json_string: str):
    return json.loads(json_string)


def to_json(data, indent=None):
    return json.dumps(data, ensure_ascii=False, indent=indent)


def from_json_file(file_path):
    with open(file_path, encoding="utf-8") as f_in:
        return from_json(f_in.read())


def glob_files(glob_format: str) -> List[str]:
    return list(sorted(glob.glob(glob_format)))


def md5(input_string: str) -> str:
    return hashlib.md5(input_string.encode()).hexdigest()


def safe_clean_text(text: str):
    text = html.unescape(text)
    text = text.encode(encoding="utf-8", errors="ignore").decode(encoding="utf-8")
    text = text.replace(u'\xa0', ' ')
    text = text.replace(u'\xc2\xa0', ' ')
    text = text.replace(u'\xe2\x80\x8A', ' ')
    text = text.replace("\u200D", " ")
    text = re.sub(r"(\w)\s*,\s*(\w)", "\\1, \\2", text)
    text = re.sub(r"(\w)\s+([.,)])", "\\1\\2", text)
    text = re.sub(r"(\w{2,})\.(\w{2,})", "\\1. \\2", text)
    text = re.sub(r"\. \. \.", " ", text)
    text = re.sub(r"\[\d+]", " ", text)
    text = re.sub(r"[`’‘]", "'", text)
    text = re.sub(r"…", ". ", text)
    text = text.replace("…", ". ")
    text = re.sub(r"[\t ]+", " ", text).strip()
    text = re.sub(r"[ ]+\n", "\n", text)
    text = re.sub(r"\n[ ]+", "\n", text)
    text = re.sub(r"[ ]+,", ",", text)
    return text
