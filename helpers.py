import glob
import hashlib
import html
import json
import math
import re
from typing import Any, Dict, List

import numpy as np


def create_instance_key(data: Dict[str, Any]) -> str:
    return md5("\t".join([data["pre_text"], data["table"], data["post_text"]]))


def create_message_body(data: Dict[str, Any]) -> str:
    pre_text = re.sub(r"[\n\t\s]+", " ", data["pre_text"])
    table = re.sub(r"[\n\t\s]+", " ", data["table"])
    post_text = re.sub(r"[\n\t\s]+", " ", data["post_text"])
    qa_pairs = data["qa_pairs"]
    num_qa_pairs = len(qa_pairs)
    if num_qa_pairs == 1:
        question_info = "a question"
        question_header = "QUESTION:"
        answer_info = "answer"
        delimiter_info = ""
        numerical_info = "a numerical response"
    elif num_qa_pairs == 2:
        question_info = "two questions"
        question_header = "QUESTIONS:"
        answer_info = "answers"
        delimiter_info = "tab delimited"
        numerical_info = "numerical responses"
    else:
        raise ValueError(f"Unexpected number of qa_pairs")
    question_text = "\n".join([qa_pair["question"] for qa_pair in qa_pairs])
    return (f"Here is a document and {question_info} regarding the document. "
            f"Please respond with the numerical {answer_info} {delimiter_info}.\n\n"
            f"Please be sure to respond only with {numerical_info} and do not reply with words.\n\n"
            f"DOCUMENT: {pre_text}\n{table}\n{post_text}"
            f"{question_header}\n\n{question_text}")


def is_yes_or_no_answer(text_input: str) -> float:
    if text_input is None:
        return False
    if re.match(r"^\s*(?:yes|no)\s*$", text_input, re.IGNORECASE):
        return True
    return False


def yes_or_no_answer_to_float(text_input: str) -> float:
    if text_input.lower() == 'yes':
        return 1
    elif text_input.lower() == 'no':
        return 0
    return math.nan


def parse_numerical_values(text_input: str) -> List[float]:
    if text_input is None:
        return [math.nan]
    try:
        if text_input.startswith("The"):
            return [math.nan]
        if re.search(r"=[\-\d.]+$", text_input):
            text_input = text_input.split("=")[-1]
        return [float(x) for x in re.findall(r'\b[\-\d.]+\b', str(text_input))]
    except ValueError:
        return [math.nan]


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


def reference_equals(x: float, y: float) -> bool:
    if np.isnan(x):
        if np.isnan(y):
            return False
        else:
            return True
    else:
        if np.isnan(y):
            return False
        else:
            delta = abs(x - y)
            if delta < 0.5 or abs(delta / max(x, y)) < 0.01:
                return True
            else:
                return False
