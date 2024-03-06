import glob  # Module for file path expansion
import hashlib  # Module for hashing functions
import json  # Module for JSON serialization and deserialization
import math  # Module providing mathematical functions
import re  # Module for regular expressions
from typing import Any, Dict, List  # Type hints for variables and functions

import numpy as np  # NumPy, a library for numerical computing


def create_instance_key(data: Dict[str, Any]) -> str:
    """
    Create a unique key for the instance based on its pre-text, table, and post-text.

    Args:
        data (Dict[str, Any]): A dictionary containing pre-text, table, and post-text.

    Returns:
        str: A unique key for the instance.
    """
    return md5("\t".join([data["pre_text"], data["table"], data["post_text"]]))


def create_message_body(data: Dict[str, Any]) -> str:
    """
    Create a message body based on the document and QA pairs.

    Args:
        data (Dict[str, Any]): A dictionary containing pre-text, table, post-text, and QA pairs.

    Returns:
        str: The message body.
    """
    # Clean pre-text, table, and post-text
    pre_text = re.sub(r"[\n\t\s]+", " ", data["pre_text"])
    table = re.sub(r"[\n\t\s]+", " ", data["table"])
    post_text = re.sub(r"[\n\t\s]+", " ", data["post_text"])

    # Extract QA pairs and determine information based on the number of pairs
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

    # Prepare the message body with document, questions, and instructions
    question_text = "\n".join([qa_pair["question"] for qa_pair in qa_pairs])
    return (f"Here is a document and {question_info} regarding the document. "
            f"Please respond with the numerical {answer_info} {delimiter_info}.\n\n"
            f"Please be sure to respond only with {numerical_info} and do not reply with words.\n\n"
            f"DOCUMENT: {pre_text}\n{table}\n{post_text}"
            f"{question_header}\n\n{question_text}")


def is_yes_or_no_answer(text_input: str) -> float:
    """
    Check if the text input represents a yes or no answer.

    Args:
        text_input (str): The input text to be checked.

    Returns:
        bool: True if the input represents a yes or no answer, False otherwise.
    """
    # Check if the text input is None
    if text_input is None:
        return False

    # Use regular expression to match "yes" or "no" (case insensitive)
    if re.match(r"^\s*(?:yes|no)\s*$", text_input, re.IGNORECASE):
        return True

    return False


def yes_or_no_answer_to_float(text_input: str) -> float:
    """
    Convert a yes or no answer represented as a string to a float value.

    Args:
        text_input (str): The input text representing a yes or no answer.

    Returns:
        float: The float value corresponding to the yes or no answer (1 for "yes", 0 for "no", NaN otherwise).
    """
    # Convert "yes" to 1, "no" to 0, and other values to NaN
    if text_input.lower() == 'yes':
        return 1
    elif text_input.lower() == 'no':
        return 0
    return math.nan


def parse_numerical_values(text_input: str) -> List[float]:
    """
    Parse numerical values from a given text input and return them as a list of floats.

    Args:
        text_input (str): The input text containing numerical values.

    Returns:
        List[float]: A list of floats representing the numerical values parsed from the input text.
    """
    # If the input text is None, return a list containing NaN
    if text_input is None:
        return [math.nan]
    try:
        # If the text starts with "The", return NaN
        if text_input.startswith("The"):
            return [math.nan]
        # If the text contains an expression of the form "=number", extract the number
        if re.search(r"=[\-\d.]+$", text_input):
            text_input = text_input.split("=")[-1]
        # Use regular expression to find numerical values in the text and convert them to floats
        return [float(x) for x in re.findall(r'\b[\-\d.]+\b', str(text_input))]
    except ValueError:
        # If there's an error during conversion, return NaN
        return [math.nan]


def from_json(json_string: str):
    """
    Parse a JSON string and convert it into a Python object.

    Args:
        json_string (str): The JSON string to parse.

    Returns:
        Any: The Python object representing the parsed JSON.
    """
    # Use json.loads() to parse the JSON string and convert it into a Python object
    return json.loads(json_string)


def to_json(data, indent=None):
    """
    Serialize a Python object into a JSON-formatted string.

    Args:
        data: The Python object to serialize.
        indent (int, optional): The number of spaces to use for indentation. Defaults to None.

    Returns:
        str: The JSON-formatted string representing the serialized data.
    """
    # Use json.dumps() to serialize the Python object into a JSON-formatted string
    # Set ensure_ascii=False to allow non-ASCII characters in the output
    # Set indent to control the indentation level of the output (None for compact representation)
    return json.dumps(data, ensure_ascii=False, indent=indent)


def from_json_file(file_path):
    """
    Deserialize JSON data from a file.

    Args:
        file_path (str): The path to the JSON file.

    Returns:
        dict: A Python dictionary containing the deserialized JSON data.
    """
    # Open the JSON file for reading
    with open(file_path, encoding="utf-8") as f_in:
        json_string = f_in.read()
        # Deserialize the JSON data using the from_json function
        return from_json(json_string)


def glob_files(glob_format: str) -> List[str]:
    """
       Glob files based on a specified format.

       Args:
           glob_format (str): The format for globbing files.

       Returns:
           List[str]: A sorted list of file paths matching the glob format.
       """
    # Use glob to match files based on the provided format
    matched_files = glob.glob(glob_format)
    # Sort the matched file paths
    sorted_files = sorted(matched_files)
    # Return the sorted list of file paths
    return list(sorted_files)


def md5(input_string: str) -> str:
    """
    Calculate the MD5 hash of an input string.

    Args:
        input_string (str): The input string to calculate the MD5 hash for.

    Returns:
        str: The MD5 hash of the input string.
    """
    # Encode the input string as bytes and calculate the MD5 hash
    md5_hash = hashlib.md5(input_string.encode()).hexdigest()
    # Return the MD5 hash as a hexadecimal string
    return md5_hash


def essentially_equals(x: float, y: float) -> bool:
    """
    Check if two floating-point numbers are essentially equal.

    Args:
        x (float): The first floating-point number.
        y (float): The second floating-point number.

    Returns:
        bool: True if the two numbers are essentially equal, False otherwise.
    """
    # Check if x is NaN
    if np.isnan(x):
        # If x is NaN, check if y is also NaN
        if np.isnan(y):
            return False
        else:
            return True
    else:
        # If x is not NaN, check if y is NaN
        if np.isnan(y):
            return False
        else:
            # Calculate the absolute difference between x and y
            delta = abs(x - y)
            # Check if the absolute difference is less than 0.5 or less than 1% of the maximum of x and y
            if delta < 0.5 or abs(delta / max(x, y)) < 0.01:
                return True
            else:
                return False
