import math
import numpy as np
from helpers import *
from typing import Any
import re

correct_answers = 0
incorrect_answers = 0

with open("data/finqa_data_enriched_openai.json", encoding="utf-8") as f_in:
    for line in f_in:
        data = from_json(line)
        data2 = from_json(line)
        qa_pairs = data["qa_pairs"]
        openai_answers: List[Any] = list()
        if len(qa_pairs) > 1:
            openai_answers = re.split(r"\s+", data["openai_answers"])
        else:
            openai_answers = [data["openai_answers"]]
        if openai_answers[0].startswith("The document"):
            openai_answers = ["" for _ in range(len(qa_pairs))]
        for i in range(len(qa_pairs)):
            if is_yes_or_no_answer(qa_pairs[i]['answer']):
                qa_pairs[i]['answer'] = str(yes_or_no_answer_to_float(qa_pairs[i]['answer']))
            if is_yes_or_no_answer(openai_answers[i]):
                openai_answers[i] = str(yes_or_no_answer_to_float(openai_answers[i]))
            if len(qa_pairs[i]['answer'].strip()) == 0:
                qa_pairs[i]['answer'] = openai_answers[i]
            reference_value = parse_numerical_values(qa_pairs[i]['answer'])[0]
            gpt4_values = parse_numerical_values(openai_answers[i])
            gpt4_value = gpt4_values[0] if len(gpt4_values) else math.nan
            question = qa_pairs[i]['question']
            if reference_equals(reference_value, gpt4_value):
                correct_answers += 1
            elif reference_equals(abs(reference_value), abs(gpt4_value)):
                correct_answers += 1
            elif reference_equals(100 * abs(reference_value), abs(gpt4_value)):
                correct_answers += 1
            elif reference_equals(abs(reference_value), 100 * abs(gpt4_value)):
                correct_answers += 1
            else:
                incorrect_answers += 1
            print(f"Question:{question}")
            print(f"Reference Value:{reference_value}")
            print(f"GPT-4 Response: {gpt4_value}")
            print(f"Running Accuracy: {correct_answers / (correct_answers + incorrect_answers)}")
        print("-" * 100)
