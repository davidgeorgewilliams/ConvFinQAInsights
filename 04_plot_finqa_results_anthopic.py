from collections import defaultdict

from helpers import *
from typing import Any
import re

sources = {
    "claude-3": "finqa_data_enriched_anthropic.json",
    "gpt-4": "finqa_data_enriched_openai.json"
}

metrics = defaultdict(lambda: defaultdict(float))

for source in sources:
    filename = sources[source]
    with open(f"data/{filename}", encoding="utf-8") as f_in:
        for line in f_in:
            data = from_json(line)
            qa_pairs = data["qa_pairs"]
            source_answers: List[Any] = list()
            source_response = data["response"]
            if len(qa_pairs) > 1:
                source_response = re.sub(r"\\\\n", " ", source_response)
                source_response = re.sub(r"\\t", " ", source_response)
                source_response = re.sub(r"\n", " ", source_response)
                source_answers.extend(re.findall(r"(\S+)", source_response,
                                                 re.DOTALL | re.IGNORECASE))
            else:
                source_answers.append(source_response)
            if source_response.startswith("The document"):
                source_answers.extend([None for _ in range(len(qa_pairs))])
            for i in range(len(qa_pairs)):
                source_answer = source_answers[i]
                target_answer = qa_pairs[i]['answer']
                if is_yes_or_no_answer(qa_pairs[i]['answer']):
                    target_answer = str(yes_or_no_answer_to_float(qa_pairs[i]['answer']))
                if is_yes_or_no_answer(source_answers[i]):
                    source_answer = str(yes_or_no_answer_to_float(source_answers[i]))
                if len(qa_pairs[i]['answer'].strip()) == 0:
                    target_answer = source_answer
                reference_value = parse_numerical_values(target_answer)[0]
                source_values = parse_numerical_values(source_answer)
                source_value = source_values[0] if len(source_values) else math.nan
                question = qa_pairs[i]['question']
                if reference_equals(reference_value, source_value):
                    metrics[source]["correct"] += 1
                elif reference_equals(abs(reference_value), abs(source_value)):
                    metrics[source]["correct"] += 1
                elif reference_equals(100 * abs(reference_value), abs(source_value)):
                    metrics[source]["correct"] += 1
                elif reference_equals(abs(reference_value), 100 * abs(source_value)):
                    metrics[source]["correct"] += 1
                else:
                    metrics[source]["incorrect"] += 1


print(to_json(metrics, indent=True))
