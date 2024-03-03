from helpers import *
import re

with open("data/qa_data_enriched.json", encoding="utf-8") as f_in:
    for line in f_in:
        data = from_json(line)
        qa_pairs = data["qa_pairs"]
        openai_answers = data["openai_answers"]
        if len(qa_pairs) > 1:
            openai_answers = re.split(r"[\n\t]+", openai_answers)
        else:
            openai_answers = [openai_answers]
        if len(openai_answers) != len(qa_pairs) and openai_answers[0].startswith("The document"):
            openai_answers = ["" for _ in range(len(qa_pairs))]
        for i in range(len(qa_pairs)):
            print(f"{qa_pairs[i]['question']}\t{qa_pairs[i]['answer']}\t{openai_answers[i]}\n")
        print("-" * 80)
